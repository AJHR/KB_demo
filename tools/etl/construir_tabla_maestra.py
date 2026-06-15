"""Construccion de la tabla maestra diaria (capa data/processed).

Una fila por dia objetivo T. Convencion anti-fuga (decision D-006):
TODAS las features de la fila T se computan exclusivamente con informacion
disponible publicamente antes de las 20:00 hora Chile del dia T-1. Los lags
se aplican AQUI (no en evaluacion.py ni en los modelos), y cada columna queda
declarada en data/processed/metadatos_features.json con su justificacion;
models/evaluacion.py::verificar_antifuga rechaza features no declaradas.

Lags por fuente (justificacion en sources/costos_sen/catalogo_fuentes.md):

  calendario          lag 0  (determinista, conocido con anos de anticipacion)
  clima_pronostico    lag 0  (pronostico para T emitido en T-2: previous_day2)
  clima_observado     lag 5  (rezago de consolidacion ERA5: 2-5 dias)
  combustibles        lag 1  (cierres ~17:00 ET = 18-19h Chile del dia T-1,
                              antes del corte 20:00; series EIA: lag 7)
  cen_generacion      lag 2  (dato de T-2, disponible manana de T)
  cen_embalses        lag 2  (cota publicada diaria; conservador)
  cen_cmg_real        lag 3  (CMg preliminar se publica con dias de rezago)
  cen_cmg_programado  EXCLUIDO de features (cumple_regla_2000=false) hasta
                      confirmar empiricamente la hora de publicacion del PO
                      (riesgo nº1 del catalogo). El mecanismo anti-fuga lo
                      bloquea en evaluacion.py.

Objetivo (columna `cmg_medio_diario`, decision D-013):
  Media del CMg real horario en USD/MWh sobre todas las barras de referencia
  del dia T. Es el LABEL del dia T: se conoce ex-post y solo se usa para
  entrenar/evaluar, nunca como feature sin lag.

  Nota: el objetivo original (demanda*CMg proxy, D-004) requeria cen_demanda,
  cuyo endpoint SIP resulto inhallable (11 rutas 404 en 2 hosts sin acceso
  a documentacion autenticada). Se pivoto al CMg diario directo (D-013):
  elimina la dependencia y precisa lo que el modelo predice (precio de
  mercado spot por barra de referencia).

Uso:
  python3 construir_tabla_maestra.py [--dir-raw data/raw] [--salida data/processed]
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

import pandas as pd

from comun import DIR_PROCESSED, DIR_RAW, log

LAG_CLIMA_OBS = 5
LAG_COMBUSTIBLES = 1
LAG_CEN = 2
LAG_CMG = 3


def _leer_fuente(dir_raw: Path, fuente: str) -> pd.DataFrame | None:
    rutas = sorted((dir_raw / fuente).glob("*/*.parquet"))
    if not rutas:
        log.warning("tabla maestra: fuente %s sin datos en %s", fuente, dir_raw)
        return None
    df = pd.concat([pd.read_parquet(r) for r in rutas], ignore_index=True)
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
    return df


def _pivot_diario(df: pd.DataFrame, col_grupo: str, col_valor: str,
                  prefijo: str, agg: str = "sum") -> pd.DataFrame:
    d = (df.groupby(["fecha", col_grupo])[col_valor].agg(agg).unstack()
           .add_prefix(prefijo))
    d.columns = [c.lower().replace(" ", "_").replace("-", "_") for c in d.columns]
    return d.reset_index()


def _a_calendario(df_diario: pd.DataFrame) -> pd.DataFrame:
    """Reindexa un agregado diario a calendario continuo ANTES de aplicar
    shift. Sin esto, shift(k) es posicional: con un hueco de fechas trae el
    dato de k+1 dias atras (hallazgo H6 de la auditoria — el error era
    conservador, nunca fuga, pero es incorrecto con datos reales del CEN
    que si tienen huecos)."""
    d = df_diario.set_index("fecha")
    d.index = pd.to_datetime(d.index)
    d = d.asfreq("D")
    d = d.reset_index()
    d["fecha"] = d["fecha"].dt.date
    return d


def construir(dir_raw: Path | None = None, dir_salida: Path | None = None,
              origen_datos: str = "real") -> Path:
    dir_raw = dir_raw or DIR_RAW
    dir_salida = dir_salida or DIR_PROCESSED
    dir_salida.mkdir(parents=True, exist_ok=True)
    meta: dict[str, dict] = {}

    def declarar(cols, fuente, lag, disponible, cumple=True, nota=""):
        for c in cols:
            meta[c] = {"fuente": fuente, "lag_dias": lag,
                       "disponible_a_las": disponible,
                       "cumple_regla_2000": cumple, "nota": nota}

    # ---- objetivo (CMg real diario, D-013) ------------------------------
    cmg = _leer_fuente(dir_raw, "cen_cmg_real")
    if cmg is None:
        raise SystemExit(
            "falta cen_cmg_real: sin objetivo no hay tabla maestra. "
            "Ejecutar el backfill (o generar_sintetico.py).")
    cmg_d_obj = (cmg.groupby("fecha", as_index=False)
                    .agg(cmg_medio_diario=("cmg_usd_mwh", "mean"),
                         cmg_max_diario=("cmg_usd_mwh", "max")))
    base = cmg_d_obj.sort_values("fecha").copy()
    idx = pd.DataFrame({"fecha": pd.date_range(base.fecha.min(), base.fecha.max(),
                                               freq="D").date})
    base = idx.merge(base, on="fecha", how="left")

    # ---- calendario (lag 0, determinista) -------------------------------
    cal = _leer_fuente(dir_raw, "calendario")
    if cal is not None:
        cols = ["dia_semana", "mes", "es_finde", "es_feriado", "es_irrenunciable",
                "es_vispera_feriado", "es_sandwich", "semana_18sept",
                "vacaciones_verano", "vacaciones_invierno", "es_eleccion",
                "es_vispera_eleccion", "es_dst"]
        cols = [c for c in cols if c in cal.columns]
        base = base.merge(cal[["fecha"] + cols], on="fecha", how="left")
        declarar(cols, "calendario", 0, "siempre",
                 nota="determinista, conocido con anticipacion")

    # ---- lags y rolling del objetivo (features autoregresivas) ----------
    # CMg real: rezago minimo 3 dias (proceso de transferencias; CMg con
    # menos de 3 dias de rezago no esta publicado a las 20:00 de T-1).
    for lag in (1, 2, 3, 7, 14, 21, 28):
        base[f"cmg_lag{lag}"] = base.cmg_medio_diario.shift(lag)
    base["cmg_ma7"] = base.cmg_medio_diario.shift(LAG_CMG).rolling(7).mean()
    base["cmg_ma28"] = base.cmg_medio_diario.shift(LAG_CMG).rolling(28).mean()
    for lag in (3, 7, 14, 21, 28):
        declarar([f"cmg_lag{lag}"], "cen_cmg_real", lag,
                 "rezago publicacion CMg preliminar")
    declarar(["cmg_ma7", "cmg_ma28"], "cen_cmg_real", LAG_CMG,
             "rezago publicacion CMg preliminar",
             nota="rolling sobre shift(3): solo usa CMg de <= T-3")
    # lag1 y lag2: CMg con rezago insuficiente -> NO conformes.
    # Existen solo para el baseline teorico de persistencia (saltar_antifuga).
    declarar(["cmg_lag1", "cmg_lag2"], "cen_cmg_real", 1,
             "ex-post (CMg < 3 dias de rezago: no publicado)", cumple=False,
             nota="solo baseline teorico (saltar_antifuga)")

    # ---- generacion (lag 2) ----------------------------------------------
    gen = _leer_fuente(dir_raw, "cen_generacion")
    if gen is not None:
        gen_d = _a_calendario(
            _pivot_diario(gen, "tecnologia", "generacion_mwh", "gen_"))
        cols_gen = [c for c in gen_d.columns if c != "fecha"]
        total = gen_d[cols_gen].sum(axis=1)
        for c in cols_gen:
            gen_d[c.replace("gen_", "share_")] = gen_d[c] / total
        cols_todas = [c for c in gen_d.columns if c != "fecha"]
        gen_d[cols_todas] = gen_d[cols_todas].shift(LAG_CEN)
        base = base.merge(gen_d, on="fecha", how="left")
        declarar(cols_todas, "cen_generacion", LAG_CEN, "manana de T (dato de T-2)")

    # ---- embalses (lag 2) ------------------------------------------------
    emb = _leer_fuente(dir_raw, "cen_embalses")
    if emb is not None:
        emb_d = _a_calendario(
            _pivot_diario(emb, "embalse", "cota_msnm", "cota_", agg="mean"))
        cols_e = [c for c in emb_d.columns if c != "fecha"]
        emb_d[cols_e] = emb_d[cols_e].shift(LAG_CEN)
        base = base.merge(emb_d, on="fecha", how="left")
        declarar(cols_e, "cen_embalses", LAG_CEN, "manana de T (dato de T-2)")

    # ---- combustibles (lag 1 futuros; lag 7 spot EIA) --------------------
    comb = _leer_fuente(dir_raw, "combustibles")
    if comb is not None:
        comb_d = _pivot_diario(comb, "serie", "valor", "fx_", agg="last")
        comb_d = comb_d.set_index("fecha").asfreq("D").ffill().reset_index()
        comb_d["fecha"] = pd.to_datetime(comb_d["fecha"]).dt.date
        cols_c = [c for c in comb_d.columns if c != "fecha"]
        spot = [c for c in cols_c if "spot" in c]
        fut = [c for c in cols_c if c not in spot]
        comb_d[fut] = comb_d[fut].shift(LAG_COMBUSTIBLES)
        comb_d[spot] = comb_d[spot].shift(7)
        base = base.merge(comb_d, on="fecha", how="left")
        declarar(fut, "combustibles", LAG_COMBUSTIBLES,
                 "cierre 18-19h Chile de T-1 (< 20:00)")
        declarar(spot, "combustibles_eia", 7, "rezago publicacion EIA")

    # ---- clima pronostico para T (lag 0, emitido T-2) --------------------
    pron = _leer_fuente(dir_raw, "clima_pronostico")
    if pron is not None:
        vars_p = [c for c in pron.columns
                  if c not in ("fecha", "punto", "lead")]
        anchas = []
        for v in vars_p:
            w = pron.pivot_table(index="fecha", columns="punto", values=v)
            w.columns = [f"pron_{v}_{p}" for p in w.columns]
            anchas.append(w)
        pron_w = pd.concat(anchas, axis=1).reset_index()
        base = base.merge(pron_w, on="fecha", how="left")
        declarar([c for c in pron_w.columns if c != "fecha"],
                 "clima_pronostico", 0,
                 "corrida 12z de T-2/T-1 (previous_day2)",
                 nota="pronostico emitido antes del corte, no clima observado")

    # ---- clima observado (lag 5) -----------------------------------------
    obs = _leer_fuente(dir_raw, "clima_observado")
    if obs is not None:
        hidro = obs[obs.punto.str.startswith("hidro")]
        pr = (hidro.groupby("fecha", as_index=False)
                   .agg(precip_hidro=("precipitation_sum", "mean"),
                        temp_hidro=("temperature_2m_mean", "mean")))
        pr = pr.set_index("fecha").asfreq("D").reset_index()
        pr["fecha"] = pd.to_datetime(pr["fecha"]).dt.date
        pr["precip_hidro_30d"] = pr.precip_hidro.rolling(30, min_periods=10).sum()
        pr["precip_hidro_90d"] = pr.precip_hidro.rolling(90, min_periods=30).sum()
        cols_o = ["precip_hidro_30d", "precip_hidro_90d", "temp_hidro"]
        pr[cols_o] = pr[cols_o].shift(LAG_CLIMA_OBS)
        base = base.merge(pr[["fecha"] + cols_o], on="fecha", how="left")
        declarar(cols_o, "clima_observado", LAG_CLIMA_OBS,
                 "consolidacion ERA5 (2-5 dias)")

    # ---- CMg programado: capturado pero BLOQUEADO como feature -----------
    declarar(["cmg_programado_d1"], "cen_cmg_programado", 0,
             "SIN CONFIRMAR (hora publicacion PO)", cumple=False,
             nota="columna AUN NO MATERIALIZADA (pre-registro). riesgo nº1 del catalogo: no usar hasta verificar "
                  "empiricamente que el PO de D+1 se publica antes de las "
                  "20:00; evaluacion.py lo rechaza automaticamente")

    # ---- salida -----------------------------------------------------------
    base["origen_datos"] = origen_datos
    ruta_tabla = dir_salida / "tabla_maestra.parquet"
    base.to_parquet(ruta_tabla, index=False)
    meta["_meta"] = {"generado": datetime.utcnow().isoformat() + "Z",
                     "origen_datos": origen_datos,
                     "filas": len(base),
                     "rango": [str(base.fecha.min()), str(base.fecha.max())]}
    (dir_salida / "metadatos_features.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False))
    log.info("tabla maestra: %d filas (%s..%s), %d columnas, origen=%s",
             len(base), base.fecha.min(), base.fecha.max(),
             base.shape[1], origen_datos)
    return ruta_tabla


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dir-raw", type=Path, default=None)
    p.add_argument("--salida", type=Path, default=None)
    p.add_argument("--origen", default="real", choices=["real", "sintetico"])
    a = p.parse_args()
    construir(a.dir_raw, a.salida, a.origen)
