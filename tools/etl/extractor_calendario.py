"""Extractor de calendario chileno (feriados + features de calendario).

Fuente: libreria `holidays` (offline, sin red). Unica fuente 100 % verificable
desde cualquier entorno. Disponibilidad: inmediata (conocida con anos de
anticipacion), cumple trivialmente la regla anti-fuga de las 20:00.

Riesgo documentado: feriados decretados con poca anticipacion (ej. duelo
nacional) no aparecen hasta actualizar la libreria; el pipeline nocturno
usa la version instalada esa noche.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from comun import (DIR_RAW, escribir_parquet_atomico, log, meses_entre,
                   particion_completa, registrar_manifiesto, ruta_particion)

FUENTE = "calendario"

# Semana santa, fiestas patrias y fin de ano concentran las mayores
# desviaciones de demanda; se marcan como periodos especiales.

# La libreria `holidays` NO incluye feriados electorales ni censos (verificado
# v0.98, ver catalogo de fuentes). Tabla manual; ampliar cuando se convoquen.
ELECCIONES = {
    date(2020, 10, 25), date(2021, 5, 15), date(2021, 5, 16),
    date(2021, 6, 13), date(2021, 7, 18), date(2021, 11, 21),
    date(2021, 12, 19), date(2022, 9, 4), date(2023, 5, 7),
    date(2023, 12, 17), date(2024, 10, 26), date(2024, 10, 27),
    date(2025, 11, 16), date(2025, 12, 14), date(2028, 10, 29),
    date(2029, 11, 18),
}

# Irrenunciables para el comercio (impacto distinto en demanda que un feriado
# normal). `holidays` no los distingue; lista por ley + dias de eleccion.
IRRENUNCIABLES_FIJOS = {(1, 1), (5, 1), (9, 18), (9, 19), (12, 25)}


def _es_dst(f: date) -> bool:
    """Horario de verano chileno derivado de la tz IANA (no hard-codeado:
    la regla cambio varias veces por decreto)."""
    from zoneinfo import ZoneInfo
    from datetime import datetime, timezone

    dt = datetime(f.year, f.month, f.day, 12, tzinfo=ZoneInfo("America/Santiago"))
    return dt.utcoffset() == timedelta(hours=-3)


def _feriados_chile(anos: list[int]):
    import holidays

    return holidays.country_holidays("CL", years=anos)


def _df_calendario(fecha_inicio: date, fecha_fin: date) -> pd.DataFrame:
    anos = list(range(fecha_inicio.year, fecha_fin.year + 2))
    fer = _feriados_chile(anos)
    fechas = pd.date_range(fecha_inicio, fecha_fin, freq="D")
    df = pd.DataFrame({"fecha": fechas.date})
    df["dia_semana"] = [f.weekday() for f in df.fecha]
    df["mes"] = [f.month for f in df.fecha]
    df["dia_mes"] = [f.day for f in df.fecha]
    df["es_finde"] = df.dia_semana >= 5
    df["es_feriado"] = [f in fer for f in df.fecha]
    df["nombre_feriado"] = [fer.get(f) for f in df.fecha]
    df["es_vispera_feriado"] = [(f + timedelta(days=1)) in fer for f in df.fecha]

    # dia laboral "sandwich": habil atrapado entre feriado y fin de semana
    es_no_laboral = (df.es_finde | df.es_feriado).to_numpy()
    sandwich = []
    for i in range(len(df)):
        if es_no_laboral[i]:
            sandwich.append(False)
            continue
        antes = es_no_laboral[i - 1] if i > 0 else False
        despues = es_no_laboral[i + 1] if i < len(df) - 1 else False
        sandwich.append(bool(antes and despues))
    df["es_sandwich"] = sandwich

    df["semana_18sept"] = [(f.month == 9 and 15 <= f.day <= 21) for f in df.fecha]
    df["vacaciones_verano"] = [(f.month in (1, 2)) for f in df.fecha]
    df["vacaciones_invierno"] = [(f.month == 7 and 5 <= f.day <= 25) for f in df.fecha]
    df["es_eleccion"] = [f in ELECCIONES for f in df.fecha]
    df["es_vispera_eleccion"] = [(f + timedelta(days=1)) in ELECCIONES
                                 for f in df.fecha]
    df["es_irrenunciable"] = [((f.month, f.day) in IRRENUNCIABLES_FIJOS
                               and f in fer) or f in ELECCIONES
                              for f in df.fecha]
    df["es_dst"] = [_es_dst(f) for f in df.fecha]
    cambios = df.es_dst.ne(df.es_dst.shift(fill_value=df.es_dst.iloc[0]))
    df["cambio_hora"] = cambios
    return df


def extract(fecha_inicio: date, fecha_fin: date, dir_datos: Path | None = None,
            forzar: bool = False) -> list[Path]:
    rutas = []
    for ini, fin in meses_entre(fecha_inicio, fecha_fin):
        destino = ruta_particion(FUENTE, ini, dir_datos)
        if not forzar and particion_completa(destino, fin):
            rutas.append(destino)
            continue
        df = _df_calendario(ini, fin)
        escribir_parquet_atomico(df, destino)
        rutas.append(destino)
        log.info("%s: particion %s (%d filas)", FUENTE, destino.name, len(df))
    registrar_manifiesto(FUENTE, rutas, dir_datos)
    return rutas


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inicio", type=date.fromisoformat, required=True)
    p.add_argument("--fin", type=date.fromisoformat, required=True)
    p.add_argument("--forzar", action="store_true")
    a = p.parse_args()
    extract(a.inicio, a.fin, forzar=a.forzar)
