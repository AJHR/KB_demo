"""Generador de dataset SINTETICO explicitamente etiquetado (data/raw_sintetico).

Proposito: replicar los ESQUEMAS del pipeline real de costos del SEN para que
las fases de baselines / autoresearch sean demostrables mientras el backfill
real (GitHub Actions; la red del sandbox esta bloqueada) no haya poblado
data/raw. Se descarta automaticamente cuando llegan datos reales: la tabla
maestra construida desde aca lleva `origen_datos="sintetico"`.

NO contiene datos reales del CEN / Open-Meteo / mercados. Toda serie sale de
un modelo generativo con numpy seed=42 (ver data/raw_sintetico/SINTETICO.md).
La unica entrada REAL que consume es data/raw/calendario (feriados), que se
copia a data/raw_sintetico/calendario y se extiende con un 2019 sintetico
(el calendario real arranca en 2020).

Fuentes generadas (mismo particionado que comun.ruta_particion):
  data/raw_sintetico/{fuente}/{YYYY}/{fuente}_{YYYY-MM}.parquet

  cen_demanda      [fecha, hora, demanda_mwh]
  cen_cmg_real     [barra, fecha, hora, cmg_usd_mwh, regimen]
  cen_generacion   [fecha, hora, tecnologia, generacion_mwh]
  cen_embalses     [fecha, embalse, cota_msnm, afluente_m3s]
  combustibles     [fecha(str ISO), serie, valor, origen='sintetico']
  clima_observado  [fecha, punto, latitud, longitud, <7 vars diarias>]
  clima_pronostico [fecha, punto, lead='previous_day2', <6 vars>]  (desde 2021)

Coherencia interna (mismo "mundo" sintetico):
  - deficit_hidrico (indice 0-1, seco 2019-2021 / humedo 2023-2025) gobierna
    precipitacion de cuencas, generacion hidro, cotas de embalses y CMg.
  - la demanda usa la temperatura sintetica de demanda_santiago y los
    feriados REALES del calendario.
  - el CMg usa el brent sintetico, el deficit hidrico y la demanda neta de
    solar (duck curve creciente 2019->2026).
  - la generacion cuadra con demanda * (1.06 +- 0.02) por hora.

Uso:
  cd tools/etl && python3 generar_sintetico.py
Luego:
  python3 construir_tabla_maestra.py --dir-raw ../../data/raw_sintetico --origen sintetico
"""

from __future__ import annotations

import shutil
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from comun import (DIR_RAW, RAIZ_REPO, escribir_parquet_atomico, log,
                   registrar_manifiesto, ruta_particion)
from extractor_clima import PUNTOS  # nombres EXACTOS de los 11 puntos

SEED = 42
DIR_SINT = RAIZ_REPO / "data" / "raw_sintetico"

INICIO = date(2019, 1, 1)
FIN = date(2026, 6, 10)
INICIO_PRONOSTICO = date(2021, 1, 1)  # simula archivo limitado de la API real
QUIEBRE_REGIMEN = date(2024, 7, 15)

BARRAS = ["QUILLOTA__220", "CRUCERO__220", "CHARRUA__220",
          "POLPAICO__220", "ALTO_JAHUEL__220"]
TECNOLOGIAS = ["hidroembalse", "hidropasada", "solar", "eolica",
               "termica_carbon", "termica_gnl", "termica_diesel",
               "geotermia", "bess"]
EMBALSES = {
    #            cota base, amp anual, sens. interanual, afl base, afl deshielo, afl lluvia
    "LAGO_LAJA": dict(cota=1335.0, amp=7.0, k=14.0, afl=55.0, melt=45.0, rain=8.0),
    "COLBUN":    dict(cota=434.0,  amp=9.0, k=6.0,  afl=170.0, melt=110.0, rain=20.0),
    "RAPEL":     dict(cota=103.0,  amp=2.5, k=2.0,  afl=110.0, melt=40.0,  rain=22.0),
    "RALCO":     dict(cota=720.0,  amp=12.0, k=8.0, afl=140.0, melt=90.0,  rain=25.0),
    "INVERNADA": dict(cota=1270.0, amp=6.0, k=5.0,  afl=38.0,  melt=35.0,  rain=5.0),
}

# Perfil intradiario de demanda: doble pico (mediodia y 20-22h), valle 4-5h.
PERFIL_24H = np.array([0.88, 0.84, 0.81, 0.79, 0.78, 0.80, 0.85, 0.92,
                       0.99, 1.04, 1.07, 1.10, 1.12, 1.11, 1.09, 1.07,
                       1.06, 1.07, 1.10, 1.14, 1.18, 1.17, 1.08, 0.96])
PERFIL_24H = PERFIL_24H / PERFIL_24H.mean()

FERIADOS_2019 = {
    "2019-01-01": "Año Nuevo", "2019-04-19": "Viernes Santo",
    "2019-04-20": "Sábado Santo", "2019-05-01": "Día del Trabajo",
    "2019-05-21": "Glorias Navales", "2019-06-29": "San Pedro y San Pablo",
    "2019-07-16": "Virgen del Carmen", "2019-08-15": "Asunción de la Virgen",
    "2019-09-18": "Independencia Nacional", "2019-09-19": "Glorias del Ejército",
    "2019-09-20": "Fiestas Patrias (adicional)",
    "2019-10-12": "Encuentro de Dos Mundos",
    "2019-10-31": "Iglesias Evangélicas", "2019-11-01": "Todos los Santos",
    "2019-12-08": "Inmaculada Concepción", "2019-12-25": "Navidad",
}
IRRENUNCIABLES_2019 = {"2019-01-01", "2019-05-01", "2019-09-18",
                       "2019-09-19", "2019-12-25"}


# ----------------------------------------------------------------------------
# utilitarios numericos
# ----------------------------------------------------------------------------

def _ar1(rng: np.random.Generator, n: int, rho: float, sd: float) -> np.ndarray:
    """Proceso AR(1) estacionario de media 0."""
    e = rng.normal(0.0, sd * np.sqrt(1 - rho ** 2), n)
    x = np.empty(n)
    x[0] = rng.normal(0.0, sd)
    for i in range(1, n):
        x[i] = rho * x[i - 1] + e[i]
    return x


def _suavizar(x: np.ndarray, ventana: int) -> np.ndarray:
    k = np.ones(ventana) / ventana
    pad = np.r_[np.full(ventana, x[0]), x, np.full(ventana, x[-1])]
    return np.convolve(pad, k, mode="same")[ventana:-ventana]


# ----------------------------------------------------------------------------
# drivers globales del "mundo" sintetico
# ----------------------------------------------------------------------------

def construir_ejes():
    fechas = pd.date_range(INICIO, FIN, freq="D")
    doy = fechas.dayofyear.to_numpy().astype(float)
    yf = fechas.year.to_numpy() + (doy - 1) / 365.25       # año fraccional
    t01 = (yf - 2019.0) / (2026.45 - 2019.0)                # progreso 0..1
    return fechas, doy, yf, t01


def generar_deficit_hidrico(rng, yf):
    """Indice 0 (muy humedo) .. 1 (muy seco). Seco 2019-2021, humedo 2023-2025."""
    anclas_x = [2018.5, 2019.5, 2020.5, 2021.5, 2022.5, 2023.5, 2024.5, 2025.5, 2026.6]
    anclas_y = [0.70,   0.74,   0.80,   0.85,   0.55,   0.30,   0.25,   0.32,   0.45]
    base = np.interp(yf, anclas_x, anclas_y)
    ruido = _suavizar(_ar1(rng, len(yf), 0.97, 0.05), 45)
    return np.clip(base + ruido, 0.05, 0.95)


def cargar_feriados(fechas) -> tuple[np.ndarray, np.ndarray]:
    """es_finde y es_feriado por dia. Feriados 2020+ del calendario REAL;
    2019 de la lista sintetica FERIADOS_2019."""
    feriados = set(FERIADOS_2019)
    for ruta in sorted((DIR_RAW / "calendario").glob("*/*.parquet")):
        cal = pd.read_parquet(ruta, columns=["fecha", "es_feriado"])
        cal["fecha"] = pd.to_datetime(cal["fecha"]).dt.strftime("%Y-%m-%d")
        feriados |= set(cal.loc[cal.es_feriado.astype(bool), "fecha"])
    iso = fechas.strftime("%Y-%m-%d")
    es_feriado = np.array([f in feriados for f in iso])
    es_finde = fechas.dayofweek.to_numpy() >= 5
    return es_finde, es_feriado


def generar_calendario_2019() -> pd.DataFrame:
    """Extiende el calendario real (2020+) con un 2019 sintetico, mismo schema."""
    fechas = pd.date_range("2019-01-01", "2019-12-31", freq="D")
    iso = fechas.strftime("%Y-%m-%d")
    dow = fechas.dayofweek.to_numpy()
    es_feriado = np.array([f in FERIADOS_2019 for f in iso])
    es_finde = dow >= 5
    libre = es_finde | es_feriado
    vispera = np.r_[es_feriado[1:], False]
    # sandwich: habil entre dos dias libres
    sandwich = np.zeros(len(fechas), bool)
    sandwich[1:-1] = (~libre[1:-1]) & libre[:-2] & libre[2:]
    dst = (fechas < "2019-04-07") | (fechas >= "2019-09-08")
    cambio = np.isin(iso, ["2019-04-07", "2019-09-08"])
    return pd.DataFrame({
        "fecha": iso,
        "dia_semana": dow.astype("int64"),
        "mes": fechas.month.to_numpy().astype("int64"),
        "dia_mes": fechas.day.to_numpy().astype("int64"),
        "es_finde": es_finde,
        "es_feriado": es_feriado,
        "nombre_feriado": pd.array([FERIADOS_2019.get(f) for f in iso],
                                   dtype="string"),
        "es_vispera_feriado": vispera,
        "es_sandwich": sandwich,
        "semana_18sept": np.isin(iso, [f"2019-09-{d}" for d in
                                       ("15", "16", "17", "18", "19", "20", "21")]),
        "vacaciones_verano": fechas.month.to_numpy() <= 2,
        "vacaciones_invierno": (iso >= "2019-07-08") & (iso <= "2019-07-28"),
        "es_eleccion": np.zeros(len(fechas), bool),
        "es_vispera_eleccion": np.zeros(len(fechas), bool),
        "es_irrenunciable": np.isin(iso, sorted(IRRENUNCIABLES_2019)),
        "es_dst": np.asarray(dst),
        "cambio_hora": cambio,
    })


# ----------------------------------------------------------------------------
# clima sintetico (11 puntos de extractor_clima.PUNTOS)
# ----------------------------------------------------------------------------

ZONA_PRECIP = {  # prob_base, prob_invierno, escala_mm
    "norte":   (0.004, 0.01, 1.5),
    "centro":  (0.03, 0.25, 9.0),
    "c_sur":   (0.05, 0.32, 11.0),
    "sur":     (0.10, 0.38, 12.0),
    "austral": (0.32, 0.30, 8.0),
}
ZONA_PUNTO = {
    "solar_maria_elena": "norte", "solar_diego_almagro": "norte",
    "eolica_taltal": "norte", "demanda_antofagasta": "norte",
    "demanda_santiago": "centro", "hidro_rapel": "centro",
    "hidro_maule": "c_sur",
    "hidro_biobio_laja": "sur", "demanda_concepcion": "sur",
    "eolica_renaico": "sur",
    "eolica_chiloe": "austral",
}


def generar_clima(rng, fechas, doy, deficit):
    n = len(fechas)
    estacion = np.cos(2 * np.pi * (doy - 15) / 365.25)        # 1 = pleno verano
    invierno = np.maximum(0.0, np.cos(2 * np.pi * (doy - 196) / 365.25)) ** 1.5
    humedad = 1.0 - deficit                                    # 1 = año humedo

    # eventos de lluvia compartidos (frentes): u comun + monto comun
    u_frente = rng.random(n)
    monto_frente = rng.gamma(0.9, 1.0, n)

    clima: dict[str, dict[str, np.ndarray]] = {}
    for punto, (lat, lon) in PUNTOS.items():
        alat = abs(lat)
        zona = ZONA_PUNTO[punto]

        # temperatura: norte calido/estable, sur frio/estacional
        t_base = 21.5 - 0.62 * (alat - 20.0)
        t_amp = 3.0 + 0.30 * (alat - 20.0)
        tmean = (t_base + t_amp * estacion + _ar1(rng, n, 0.70, 1.5))
        tmax = tmean + 5.5 + 1.2 * estacion + np.abs(rng.normal(0, 1.0, n))
        tmin = tmean - 5.2 - np.abs(rng.normal(0, 1.0, n))

        # precipitacion: concentrada may-ago, escalada por humedad del año
        p_base, p_inv, escala = ZONA_PRECIP[zona]
        prob = np.clip((p_base + p_inv * invierno) * (0.65 + 0.7 * humedad), 0, 0.95)
        llueve = u_frente < prob
        monto = (monto_frente * escala * (0.6 + 0.8 * humedad)
                 * (0.7 + 0.6 * rng.random(n)))
        precip = np.where(llueve, monto, 0.0)

        # radiacion (MJ/m2 dia): alta y estable en zona solar, estacional al sur
        if punto.startswith("solar") or zona == "norte":
            rad = 24.0 + 6.0 * estacion + rng.normal(0, 1.0, n)
        elif zona in ("centro", "c_sur"):
            rad = 17.5 + 9.0 * estacion + rng.normal(0, 1.6, n)
        else:
            rad = 13.0 + 9.0 * estacion + rng.normal(0, 1.8, n)
        rad = np.clip(rad * (1 - 0.45 * llueve), 0.8, 36.0)

        # viento: mas alto y persistente en puntos eolicos
        v_base = 9.0 if punto.startswith("eolica") else 5.5
        viento = np.clip(v_base + 3.0 * _ar1(rng, n, 0.75, 1.0)
                         + 0.8 * estacion, 1.0, None)
        rachas = viento * (1.45 + 0.15 * rng.random(n))

        clima[punto] = dict(lat=lat, lon=lon, tmean=tmean, tmax=tmax, tmin=tmin,
                            rad=rad, precip=precip, viento=viento, rachas=rachas)
    return clima


def df_clima_observado(fechas, clima) -> pd.DataFrame:
    fechas_d = fechas.date
    partes = []
    for punto, c in clima.items():
        partes.append(pd.DataFrame({
            "fecha": fechas_d, "punto": punto,
            "latitud": c["lat"], "longitud": c["lon"],
            "temperature_2m_max": c["tmax"],
            "temperature_2m_min": c["tmin"],
            "temperature_2m_mean": c["tmean"],
            "shortwave_radiation_sum": c["rad"],
            "precipitation_sum": c["precip"],
            "wind_speed_10m_max": c["viento"],
            "wind_gusts_10m_max": c["rachas"],
        }))
    return pd.concat(partes, ignore_index=True)


def df_clima_pronostico(rng, fechas, clima) -> pd.DataFrame:
    """Pronostico previous_day2 = observado + error gaussiano. Desde 2021."""
    mask = fechas.date >= INICIO_PRONOSTICO
    fechas_d = fechas.date[mask]
    n = int(mask.sum())
    partes = []
    for punto, c in clima.items():
        precip = c["precip"][mask].copy()
        seco = precip <= 0.1
        falso_pos = seco & (rng.random(n) < 0.07)       # pronostica lluvia que no cae
        falso_neg = (~seco) & (rng.random(n) < 0.08)    # no ve la lluvia real
        precip = precip * (1 + rng.normal(0, 0.25, n))
        precip[falso_pos] = rng.exponential(1.5, int(falso_pos.sum()))
        precip[falso_neg] = 0.0
        partes.append(pd.DataFrame({
            "fecha": fechas_d, "punto": punto, "lead": "previous_day2",
            "temp_media": c["tmean"][mask] + rng.normal(0, 1.2, n),
            "radiacion_media": np.clip(
                c["rad"][mask] * (1 + rng.normal(0, 0.08, n)), 0, None),
            "viento100m_medio": np.clip(
                c["viento"][mask] * 1.30 * 0.78 * (1 + rng.normal(0, 0.15, n)), 0, None),
            "precipitacion_total": np.clip(precip, 0, None),
            "temp_max": c["tmax"][mask] + rng.normal(0, 1.5, n),
            "viento100m_max": np.clip(
                c["rachas"][mask] * 1.25 * (1 + rng.normal(0, 0.15, n)), 0, None),
        }))
    return pd.concat(partes, ignore_index=True)


# ----------------------------------------------------------------------------
# combustibles (solo dias habiles)
# ----------------------------------------------------------------------------

def _serie_ou(rng, yf_b, anclas, sigma, lo, hi, kappa=0.02):
    """Camino log-OU que revierte a un nivel medio interpolado entre anclas."""
    media = np.log(np.interp(yf_b, list(anclas.keys()), list(anclas.values())))
    x = np.empty(len(yf_b))
    x[0] = media[0]
    eps = rng.normal(0, sigma, len(yf_b))
    for i in range(1, len(yf_b)):
        x[i] = x[i - 1] + kappa * (media[i] - x[i - 1]) + eps[i]
    return np.clip(np.exp(x), lo, hi)


def generar_combustibles(rng, fechas):
    bd = pd.bdate_range(INICIO, FIN)
    doy_b = bd.dayofyear.to_numpy().astype(float)
    yf_b = bd.year.to_numpy() + (doy_b - 1) / 365.25
    nb = len(bd)

    brent = _serie_ou(rng, yf_b, {2018.5: 62, 2019.5: 64, 2020.3: 52, 2021.0: 56,
                                  2021.8: 76, 2022.4: 118, 2022.9: 95, 2023.5: 82,
                                  2024.5: 80, 2025.5: 72, 2026.6: 68},
                      0.012, 50, 120)
    henry = _serie_ou(rng, yf_b, {2018.5: 2.9, 2020.3: 2.1, 2021.0: 3.0,
                                  2022.5: 8.6, 2023.2: 2.7, 2024.5: 2.4,
                                  2025.5: 3.1, 2026.6: 3.4},
                      0.025, 2.0, 9.0)
    diesel = np.clip(brent / 42.0 * 1.32 + 0.18 + rng.normal(0, 0.04, nb), 1.2, 4.5)
    carbon = _serie_ou(rng, yf_b, {2018.5: 72, 2020.4: 62, 2021.5: 130,
                                   2022.6: 380, 2023.2: 135, 2024.5: 105,
                                   2025.5: 100, 2026.6: 95},
                       0.020, 60, 400)
    usdclp = _serie_ou(rng, yf_b, {2018.5: 705, 2019.8: 745, 2020.2: 840,
                                   2021.2: 725, 2022.5: 935, 2023.2: 805,
                                   2024.5: 935, 2025.5: 945, 2026.6: 955},
                       0.004, 700, 1000, kappa=0.015)

    iso = bd.strftime("%Y-%m-%d")
    partes = []
    for nombre, vals in [("brent_usd_bbl", brent), ("henry_hub_usd_mmbtu", henry),
                         ("diesel_ho_usd_gal", diesel), ("usd_clp", usdclp)]:
        partes.append(pd.DataFrame({"fecha": iso, "serie": nombre, "valor": vals}))
    # carbon API2: 15% de dias faltantes aleatorios (iliquidez del indice)
    presente = rng.random(nb) >= 0.15
    partes.append(pd.DataFrame({"fecha": iso[presente], "serie": "carbon_api2_usd_t",
                                "valor": carbon[presente]}))
    df = pd.concat(partes, ignore_index=True)
    df["origen"] = "sintetico"

    # brent diario (ffill) para alimentar la formula de CMg
    s = pd.Series(brent, index=bd).reindex(fechas).ffill().bfill()
    return df, s.to_numpy()


# ----------------------------------------------------------------------------
# demanda, generacion y CMg (horario)
# ----------------------------------------------------------------------------

def generar_demanda(rng, fechas, doy, yf, clima, es_finde, es_feriado):
    n = len(fechas)
    crecimiento = 1.025 ** (yf - 2022.7)                      # 2.5%/año
    estacional = 1 + 0.035 * np.cos(2 * np.pi * (doy - 196) / 365.25)  # max invierno
    t_stgo = clima["demanda_santiago"]["tmean"]
    calefaccion = 0.0050 * np.maximum(0.0, 16.5 - t_stgo) ** 1.15
    aire_acond = 0.0085 * np.maximum(0.0, t_stgo - 21.5) ** 1.15
    factor_cal = np.minimum(np.where(es_finde, 0.92, 1.0),
                            np.where(es_feriado, 0.88, 1.0))
    ruido = np.exp(_ar1(rng, n, 0.65, 0.013))
    nivel = crecimiento * estacional * (1 + calefaccion + aire_acond) * factor_cal * ruido
    nivel *= 8800.0 / nivel.mean()                            # nivel medio ~8.800 MWh/h
    dem = nivel[:, None] * PERFIL_24H[None, :] * (1 + rng.normal(0, 0.006, (n, 24)))
    return dem


def generar_spikes(rng, fechas):
    """~8 eventos de escasez por año, x2-x4 durante 4-12 horas."""
    n = len(fechas)
    mult = np.ones((n, 24))
    activo = np.zeros((n, 24), bool)
    anios = fechas.year.to_numpy()
    for anio in np.unique(anios):
        idx = np.flatnonzero(anios == anio)
        for _ in range(rng.poisson(8)):
            d = int(rng.choice(idx))
            h0 = int(rng.integers(7, 20))
            dur = int(rng.integers(4, 13))
            factor = rng.uniform(2.0, 4.0)
            h1 = min(h0 + dur, 24)
            mult[d, h0:h1] = factor
            activo[d, h0:h1] = True
            if h0 + dur > 24 and d + 1 < n:                   # cola al dia siguiente
                resto = h0 + dur - 24
                mult[d + 1, :resto] = factor
                activo[d + 1, :resto] = True
    return mult, activo


def generar_generacion(rng, fechas, doy, t01, deficit, clima, dem, spike_activo):
    """Despacho sintetico que cuadra: suma por hora = demanda*(1.06±0.02)."""
    n = len(fechas)
    perdidas = 1.06 + np.clip(rng.normal(0, 0.008, n), -0.02, 0.02)
    total = dem * perdidas[:, None]
    e_dia = total.sum(axis=1)

    # --- solar: perfil diurno x capacidad creciente (share 8% -> 25%) -------
    w_dia = 5.6 + 1.4 * np.cos(2 * np.pi * (doy - 15) / 365.25)   # semiancho luz
    horas = np.arange(24, dtype=float)
    ang = (horas[None, :] - 13.0) / (2 * w_dia[:, None])
    forma = np.where(np.abs(horas[None, :] - 13.0) < w_dia[:, None],
                     np.maximum(0.0, np.cos(np.pi * ang)) ** 1.3, 0.0)
    forma_norm = forma / np.maximum(forma.max(axis=1, keepdims=True), 1e-9)
    forma_e = forma / np.maximum(forma.sum(axis=1, keepdims=True), 1e-9)
    rad_sol = 0.5 * (clima["solar_maria_elena"]["rad"]
                     + clima["solar_diego_almagro"]["rad"])
    rad_rel = np.clip(rad_sol / rad_sol.mean(), 0.55, 1.45)
    share_sol = np.clip((0.08 + 0.17 * t01) * rad_rel
                        * (1 + rng.normal(0, 0.05, n)), 0.02, 0.40)
    solar = (share_sol * e_dia)[:, None] * forma_e

    # --- eolica: ruido con persistencia ------------------------------------
    share_eol = 0.055 + 0.075 * t01
    f_eol = 0.18 + 0.72 / (1 + np.exp(-_ar1(rng, n, 0.72, 0.9)))
    f_eol /= f_eol.mean()
    ruido_h = 1 + 0.10 * _ar1(rng, n * 24, 0.90, 1.0).reshape(n, 24)
    forma_eol = np.clip(ruido_h, 0.3, None)
    forma_eol /= forma_eol.sum(axis=1, keepdims=True)
    eolica = (share_eol * f_eol * e_dia)[:, None] * forma_eol

    # --- hidro: anticorrelada con deficit; embalse sigue el peak neto ------
    dist = np.minimum(np.abs(doy - 335), 365.25 - np.abs(doy - 335))
    deshielo = np.exp(-0.5 * (dist / 45.0) ** 2)              # oct-ene
    share_hid = np.clip(0.36 - 0.22 * deficit + 0.04 * deshielo
                        + _suavizar(_ar1(rng, n, 0.9, 0.02), 20), 0.10, 0.45)
    e_hid = share_hid * e_dia
    pasada = (0.44 * e_hid)[:, None] * np.full((1, 24), 1 / 24.0)
    peso = np.maximum(dem - solar, 1.0) ** 1.4
    peso /= peso.sum(axis=1, keepdims=True)
    embalse = (0.56 * e_hid)[:, None] * peso

    # --- geotermia constante; bess chico desde 2023 -------------------------
    geo = 55.0 * (1 + rng.normal(0, 0.02, (n, 24)))
    cap_bess = np.clip((t01 - (2023.0 - 2019.0) / 7.45) * 7.45 / 3.45, 0, 1) * 260.0
    forma_bess = np.zeros(24)
    forma_bess[19:24] = [0.15, 0.30, 0.30, 0.20, 0.05]
    bess = cap_bess[:, None] * forma_bess[None, :] * (1 + rng.normal(0, 0.1, (n, 24)))
    bess = np.clip(bess, 0, None)

    # --- curtailment: si sobra renovable, recorta solar (luego eolica) ------
    resid = total - (solar + eolica + pasada + embalse + geo + bess)
    exceso = np.maximum(-resid, 0.0)
    rec = np.minimum(solar, exceso)
    solar -= rec
    exceso -= rec
    rec = np.minimum(eolica, exceso)
    eolica -= rec
    exceso -= rec
    rec = np.minimum(pasada, exceso)
    pasada -= rec
    resid = np.maximum(total - (solar + eolica + pasada + embalse + geo + bess), 0.0)

    # --- termicas cierran el balance: carbon -> gnl -> diesel ---------------
    cap_carbon = np.maximum(
        (3300.0 - 2300.0 * t01) * (1 + _suavizar(_ar1(rng, n, 0.9, 0.03), 30)), 800.0)
    # GNL holgado fuera de spikes: el diesel solo entra cuando un evento de
    # escasez recorta la disponibilidad de GNL (o en peaks extremos).
    cap_gnl = 6000.0 * (1 + _suavizar(_ar1(rng, n, 0.9, 0.04), 30))
    cap_gnl_h = cap_gnl[:, None] * np.where(spike_activo, 0.45, 1.0)
    carbon = np.minimum(resid, cap_carbon[:, None])
    resto = resid - carbon
    gnl = np.minimum(resto, cap_gnl_h)
    diesel = resto - gnl                                       # solo peaks/escasez

    gen = {"hidroembalse": embalse, "hidropasada": pasada, "solar": solar,
           "eolica": eolica, "termica_carbon": carbon, "termica_gnl": gnl,
           "termica_diesel": diesel, "geotermia": geo, "bess": bess}
    balance = sum(gen.values()) - total
    log.info("generacion: desbalance maximo |gen-demanda*perdidas| = %.1f MWh "
             "(curtailment extremo)", float(np.abs(balance).max()))
    return gen, forma_norm, rad_rel


def generar_cmg(rng, fechas, t01, deficit, brent_d, dem, solar, forma_norm,
                rad_rel, spike_mult):
    """CMg horario por barra via orden de merito sintetico + duck curve."""
    n = len(fechas)
    anios = fechas.year.to_numpy()
    dn = dem - solar                                           # demanda neta
    dnn = np.empty_like(dn)
    for anio in np.unique(anios):
        m = anios == anio
        dnn[m] = dn[m] / np.quantile(dn[m], 0.95)

    cmg = (35.0 + 0.9 * (brent_d[:, None] / 10.0) + 25.0 * deficit[:, None]
           + 30.0 * np.maximum(0.0, dnn - 0.75) ** 2)
    # duck curve: hundimiento solar de mediodia, 5 USD (2019) -> 35 USD (2026);
    # amplificado en dias de alta radiacion (CMg ~0-5 en primavera)
    hundimiento = (5.0 + 30.0 * t01) * rad_rel ** 2.2
    cmg -= hundimiento[:, None] * forma_norm
    cmg *= spike_mult                                          # escasez x2-x4
    cmg *= np.exp(rng.normal(0, 0.10, (n, 24)))                # ruido lognormal
    cmg = np.maximum(cmg, 0.0)                                 # piso 0

    factor_crucero = 0.08 + 0.22 * t01                         # solar abarata el dia
    ajuste = {
        "QUILLOTA__220": 1.005, "POLPAICO__220": 1.015, "ALTO_JAHUEL__220": 0.995,
        "CRUCERO__220": 1.0, "CHARRUA__220": 1.0,
    }
    por_barra = {}
    for barra in BARRAS:
        idio = np.exp(rng.normal(0, 0.35, (n, 24)))            # idiosincratico
        b = cmg * (0.92 + 0.08 * idio) * ajuste[barra]         # factor comun 0.92
        if barra == "CRUCERO__220":
            b = b * (1 - factor_crucero[:, None] * forma_norm)
        elif barra == "CHARRUA__220":
            b = b * (1 - 0.15 * (1 - deficit)[:, None])        # barato en años humedos
        por_barra[barra] = np.maximum(b, 0.0)
    return por_barra


def generar_embalses(rng, fechas, doy, deficit, clima):
    n = len(fechas)
    deficit_s = _suavizar(deficit, 120)
    dist = np.minimum(np.abs(doy - 335), 365.25 - np.abs(doy - 335))
    deshielo = np.exp(-0.5 * (dist / 45.0) ** 2)
    ciclo = np.sin(2 * np.pi * (doy - 250) / 365.25)           # llena dic-ene
    precip_cuenca = np.mean([clima[p]["precip"] for p in
                             ("hidro_maule", "hidro_biobio_laja", "hidro_rapel")],
                            axis=0)
    precip_roll = _suavizar(precip_cuenca, 12)
    humedad = 1 - deficit

    fechas_d = fechas.date
    partes = []
    for nombre, p in EMBALSES.items():
        cota = (p["cota"] + p["amp"] * ciclo
                - p["k"] * (deficit_s - 0.45) * 2.0
                + _suavizar(_ar1(rng, n, 0.97, 0.3), 15))
        afl = (p["afl"] * (0.45 + 1.1 * humedad)
               + p["rain"] * precip_roll / 5.0
               + p["melt"] * deshielo) * np.exp(rng.normal(0, 0.12, n))
        partes.append(pd.DataFrame({
            "fecha": fechas_d, "embalse": nombre,
            "cota_msnm": cota, "afluente_m3s": np.clip(afl, 1.0, None),
        }))
    return pd.concat(partes, ignore_index=True)


# ----------------------------------------------------------------------------
# armado de dataframes largos y escritura particionada
# ----------------------------------------------------------------------------

def _largo_horario(fechas, matrices: dict[str, np.ndarray], col_clave: str | None,
                   col_valor: str) -> pd.DataFrame:
    """(n_dias,24) -> formato largo [fecha, hora, (clave), valor]."""
    n = len(fechas)
    fecha_rep = np.repeat(fechas.date, 24)
    hora_rep = np.tile(np.arange(24), n)
    partes = []
    for clave, m in matrices.items():
        d = pd.DataFrame({"fecha": fecha_rep, "hora": hora_rep,
                          col_valor: m.reshape(-1)})
        if col_clave:
            d.insert(0, col_clave, clave)
        partes.append(d)
    return pd.concat(partes, ignore_index=True)


def escribir_fuente(df: pd.DataFrame, fuente: str) -> list[Path]:
    fechas_dt = pd.to_datetime(df["fecha"])
    rutas = []
    for (anio, mes), parte in df.groupby([fechas_dt.dt.year, fechas_dt.dt.month]):
        destino = ruta_particion(fuente, date(int(anio), int(mes), 1), DIR_SINT)
        escribir_parquet_atomico(parte.reset_index(drop=True), destino)
        rutas.append(destino)
    registrar_manifiesto(fuente, sorted(rutas), DIR_SINT, origen="sintetico",
                         seed=SEED, generador="tools/etl/generar_sintetico.py")
    log.info("%s: %d particiones, %d filas", fuente, len(rutas), len(df))
    return rutas


def escribir_sintetico_md():
    texto = f"""# ADVERTENCIA: DATOS 100% SINTETICOS

**TODO el contenido de `data/raw_sintetico/` es GENERADO por
`tools/etl/generar_sintetico.py` (numpy seed={SEED}). NO son datos reales del
CEN, de Open-Meteo ni de ningun mercado.**

## Para que existe

El backfill real corre en GitHub Actions (la red del sandbox esta bloqueada) y
puede tardar en poblar `data/raw/`. Este dataset replica los ESQUEMAS exactos
del pipeline (los mismos que consumen `construir_tabla_maestra.py` y los
extractores `extractor_cen_*` / `extractor_clima*` / `extractor_combustibles`)
para que baselines y autoresearch sean demostrables de punta a punta.

**Se descarta automaticamente cuando llegan los datos reales**: la tabla
maestra construida desde aca queda marcada con `origen_datos="sintetico"`
(columna y `metadatos_features.json`), y basta reconstruir con
`--dir-raw data/raw --origen real`.

## Que NO se puede concluir de estos datos

Los resultados de baselines/modelos sobre este dataset **NO son metricas del
problema real**: la dificultad, los regimenes y el ruido son inventados. Solo
validan la MAQUINARIA (esquemas, lags anti-fuga, joins, splits, evaluacion).

## Logica generativa (resumen)

- **Mundo comun**: un indice `deficit_hidrico` (0=humedo, 1=seco; seco
  2019-2021, humedo 2023-2025) gobierna coherentemente precipitacion de
  cuencas, generacion hidro, cotas/afluentes de embalses y nivel de CMg.
- **`cen_demanda`**: nivel medio ~8.800 MWh/h, crecimiento 2,5%/año,
  estacionalidad con maximo en invierno, perfil intradiario de doble pico
  (mediodia y 20-22h), -8% fin de semana, -12% feriados (feriados REALES de
  `data/raw/calendario`; 2019 con lista sintetica), sensibilidad a la
  temperatura sintetica de Santiago, ruido AR(1).
- **`cen_cmg_real`**: orden de merito sintetico
  `35 + 0.9*(brent/10) + 25*deficit_hidrico + 30*max(0, dnn-0.75)^2`,
  hundimiento solar de mediodia creciente (duck curve, 5 USD en 2019 a 35 USD
  en 2026; CMg ~0-5 en primaveras de alta radiacion), ~8 spikes de escasez por
  año (x2-x4, 4-12 h), piso 0, ruido lognormal. 5 barras correlacionadas
  (factor comun 0.92): CRUCERO mas barata de dia (solar), CHARRUA mas barata
  en años humedos. `regimen` cambia 'antiguo'->'nuevo' el {QUIEBRE_REGIMEN}.
- **`cen_generacion`**: cuadra con `demanda*(1.06±0.02)` por hora. Solar con
  share creciente 8%->25%; eolica con persistencia; hidro anticorrelada con el
  deficit; termicas cierran el balance carbon->gnl->diesel (diesel casi solo
  en spikes); carbon decreciente (descarbonizacion); bess chico desde 2023.
- **`cen_embalses`**: cota = base + ciclo anual (deshielo oct-ene) + tendencia
  interanual ligada al deficit + ruido suave; afluente correlacionado con la
  precipitacion sintetica de cuenca + deshielo.
- **`combustibles`**: caminos log-OU con anclas historicas estilizadas (spike
  2022 en brent/henry hub/carbon), solo dias habiles, carbon API2 con ~15% de
  dias faltantes (iliquidez), `origen='sintetico'` en cada fila.
- **`clima_observado` / `clima_pronostico`**: 11 puntos de
  `extractor_clima.PUNTOS`; radiacion alta y estable en `solar_*`, lluvia
  may-ago en `hidro_*`/Concepcion escalada por el año hidrologico; el
  pronostico es el observado + error gaussiano (~8% radiacion, ~1.2 C temp,
  ~15% viento, falsos positivos/negativos de lluvia) y existe solo desde
  {INICIO_PRONOSTICO} (simula archivo limitado de la API real).
- **`calendario/`**: copia del calendario REAL de `data/raw/calendario`
  (2020-2026) extendida con un 2019 sintetico de mismo schema.

Rango: {INICIO} a {FIN}. Regenerar: `cd tools/etl && python3 generar_sintetico.py`.
"""
    DIR_SINT.mkdir(parents=True, exist_ok=True)
    (DIR_SINT / "SINTETICO.md").write_text(texto, encoding="utf-8")


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main():
    rng = np.random.default_rng(SEED)
    fechas, doy, yf, t01 = construir_ejes()
    n = len(fechas)
    log.info("generando mundo sintetico: %d dias (%s..%s), seed=%d",
             n, INICIO, FIN, SEED)

    escribir_sintetico_md()

    # calendario: copia del real + 2019 sintetico (mismo schema)
    shutil.copytree(DIR_RAW / "calendario", DIR_SINT / "calendario",
                    dirs_exist_ok=True)
    cal19 = generar_calendario_2019()
    f19 = pd.to_datetime(cal19["fecha"])
    for mes, parte in cal19.groupby(f19.dt.month):
        destino = ruta_particion("calendario", date(2019, int(mes), 1), DIR_SINT)
        escribir_parquet_atomico(parte.reset_index(drop=True), destino)
    log.info("calendario: copiado real 2020-2026 + 12 particiones sinteticas 2019")

    # drivers
    deficit = generar_deficit_hidrico(rng, yf)
    es_finde, es_feriado = cargar_feriados(fechas)
    clima = generar_clima(rng, fechas, doy, deficit)
    df_comb, brent_d = generar_combustibles(rng, fechas)
    dem = generar_demanda(rng, fechas, doy, yf, clima, es_finde, es_feriado)
    spike_mult, spike_activo = generar_spikes(rng, fechas)
    gen, forma_norm, rad_rel = generar_generacion(
        rng, fechas, doy, t01, deficit, clima, dem, spike_activo)
    cmg_barras = generar_cmg(rng, fechas, t01, deficit, brent_d, dem,
                             gen["solar"], forma_norm, rad_rel, spike_mult)
    df_emb = generar_embalses(rng, fechas, doy, deficit, clima)

    # sanity interno: costo diario proxy = sum_h demanda_h * CMg_h (prom barras)
    cmg_prom = np.mean([cmg_barras[b] for b in BARRAS], axis=0)
    costo_dia = (dem * cmg_prom).sum(axis=1)
    log.info("sanity costo_op_usd diario [MUSD]: p5=%.1f p50=%.1f p95=%.1f media=%.1f",
             *np.percentile(costo_dia / 1e6, [5, 50, 95]),
             costo_dia.mean() / 1e6)

    # dataframes largos + escritura
    escribir_fuente(_largo_horario(fechas, {"": dem}, None, "demanda_mwh"),
                    "cen_demanda")

    df_cmg = _largo_horario(fechas, cmg_barras, "barra", "cmg_usd_mwh")
    df_cmg["regimen"] = np.where(
        pd.to_datetime(df_cmg["fecha"]).dt.date < QUIEBRE_REGIMEN,
        "antiguo", "nuevo")
    escribir_fuente(df_cmg, "cen_cmg_real")

    escribir_fuente(_largo_horario(fechas, {t: gen[t] for t in TECNOLOGIAS},
                                   "tecnologia", "generacion_mwh"),
                    "cen_generacion")
    escribir_fuente(df_emb, "cen_embalses")
    escribir_fuente(df_comb, "combustibles")
    escribir_fuente(df_clima_observado(fechas, clima), "clima_observado")
    escribir_fuente(df_clima_pronostico(rng, fechas, clima), "clima_pronostico")

    log.info("listo: data/raw_sintetico poblado. Siguiente paso: "
             "python3 construir_tabla_maestra.py --dir-raw ../../data/raw_sintetico "
             "--origen sintetico")


if __name__ == "__main__":
    main()
