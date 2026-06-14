"""Tests OFFLINE del pipeline CEN — sin red, sin user_key, sin fixtures externos.

La red del sandbox esta bloqueada y el codigo correra recien en GitHub
Actions, asi que aca se prueba todo lo testeable sin tocar los endpoints:
parsers (fixtures JSON inline con los nombres de campo mas probables de la
API SIP), filtrado de barras, logica de paginacion (con una sesion fake),
y los validadores (con parquets temporales generados al vuelo).

Correr:
    python3 tests_offline.py
Imprime 'TODOS LOS TESTS OFFLINE OK' si todo pasa; aborta con AssertionError
(y exit code != 0) si algo falla.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import date
from pathlib import Path

# Ejecutable desde cualquier cwd + sin pausas de rate limit en los tests.
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ["CEN_API_PAUSA_SEG"] = "0"

import pandas as pd  # noqa: E402

import cen_api  # noqa: E402
import extractor_cen_cmg_programado as cmg_prog  # noqa: E402
import extractor_cen_cmg_real as cmg_real  # noqa: E402
import extractor_cen_demanda as demanda  # noqa: E402
import extractor_cen_embalses as embalses  # noqa: E402
import extractor_cen_generacion as generacion  # noqa: E402
import extractor_cen_po as cen_po  # noqa: E402
import validadores  # noqa: E402


# ---------------------------------------------------------------------------
# Infraestructura: sesion HTTP fake para probar get_paginado sin red
# ---------------------------------------------------------------------------

class _RespuestaFake:
    def __init__(self, datos):
        self._datos = datos

    def raise_for_status(self):
        pass

    def json(self):
        return self._datos

    @property
    def text(self):
        return json.dumps(self._datos)


class _SesionFake:
    """session.get falsa: `responder(url, params) -> objeto JSON`."""

    def __init__(self, responder):
        self._responder = responder
        self.llamadas = []

    def get(self, url, params=None, timeout=None):
        params = dict(params or {})
        self.llamadas.append((url, params))
        return _RespuestaFake(self._responder(url, params))


# ---------------------------------------------------------------------------
# Tests de cen_api: extraccion de filas, paginacion, filtro de barras
# ---------------------------------------------------------------------------

def test_extraer_filas_variantes():
    filas, sig = cen_api.extraer_filas({"data": [{"a": 1}], "next": "http://x/p2"})
    assert filas == [{"a": 1}] and sig == "http://x/p2"
    filas, sig = cen_api.extraer_filas({"results": [{"b": 2}]})
    assert filas == [{"b": 2}] and sig is None
    filas, sig = cen_api.extraer_filas({"items": []})
    assert filas == [] and sig is None
    filas, sig = cen_api.extraer_filas([{"c": 3}])  # lista cruda
    assert filas == [{"c": 3}] and sig is None
    filas, sig = cen_api.extraer_filas({"mensaje": "sin lista"})
    assert filas == [] and sig is None


def test_get_paginado_lista_cruda():
    s = _SesionFake(lambda url, params: [{"x": 1}, {"x": 2}])
    filas = cen_api.get_paginado(s, "http://api/x", {"user_key": "k"})
    assert filas == [{"x": 1}, {"x": 2}]
    assert len(s.llamadas) == 1


def test_get_paginado_next_url():
    def responder(url, params):
        if url.endswith("/p2"):
            # la URL next no trae user_key: get_paginado debe reinyectarlo
            assert params.get("user_key") == "k", params
            return {"results": [{"x": 2}], "next": None}
        return {"results": [{"x": 1}], "next": "http://api/x/p2"}

    s = _SesionFake(responder)
    filas = cen_api.get_paginado(s, "http://api/x", {"user_key": "k"})
    assert filas == [{"x": 1}, {"x": 2}], filas
    assert len(s.llamadas) == 2


def test_get_paginado_por_page():
    paginas = {1: [{"x": 1}, {"x": 2}], 2: [{"x": 3}, {"x": 4}], 3: []}

    def responder(url, params):
        return {"data": paginas[params.get("page", 1)], "total": 4}

    s = _SesionFake(responder)
    filas = cen_api.get_paginado(s, "http://api/x", {"user_key": "k"})
    assert filas == [{"x": 1}, {"x": 2}, {"x": 3}, {"x": 4}], filas
    # con total=4 declarado no hace falta pedir la pagina 3 (vacia)
    assert len(s.llamadas) == 2, s.llamadas


def test_get_paginado_servidor_ignora_page():
    # dict con clave de paginacion pero que repite siempre la misma pagina:
    # no debe duplicar filas ni iterar hasta el tope de 500
    s = _SesionFake(lambda url, params: {"data": [{"x": 1}], "page": 1})
    filas = cen_api.get_paginado(s, "http://api/x", {"user_key": "k"})
    assert filas == [{"x": 1}], filas
    assert len(s.llamadas) == 2, s.llamadas  # pagina 1 + sondeo de pagina 2


def test_get_paginado_sin_indicios_de_paginacion():
    # dict sin claves de paginacion -> se asume respuesta completa (1 request)
    s = _SesionFake(lambda url, params: {"data": [{"x": 1}]})
    filas = cen_api.get_paginado(s, "http://api/x", {"user_key": "k"})
    assert filas == [{"x": 1}]
    assert len(s.llamadas) == 1


def test_filtrar_barras_con_y_sin_acentos():
    df = pd.DataFrame({"barra": [
        "BA S/E CHARRÚA 220KV",        # con acento -> debe matchear CHARRUA
        "ba s/e quillota 220kv",       # minusculas
        "BA S/E ALTO JAHUEL 220KV",
        "Alto-Jahuel 220",             # separador alternativo
        "Crucero 220",
        "BA S/E POLPAICO 220KV",
        "BA S/E PUERTO MONTT 110KV",   # NO es barra de referencia
        "BA S/E QUILLOTA 110KV",       # tension equivocada
    ]})
    res = cen_api.filtrar_barras(df, "barra")
    assert len(res) == 6, res["barra"].tolist()
    assert not res["barra"].str.contains("PUERTO MONTT").any()
    # columna inexistente: devuelve vacio sin morir
    vacio = cen_api.filtrar_barras(df, "no_existe")
    assert vacio.empty


def test_buscar_columna_laxa():
    df = pd.DataFrame(columns=["FechaHora", "Cmg_USD_MWh", "BARRA_INFO"])
    assert cen_api.buscar_columna(df, ["fecha_hora"]) == "FechaHora"
    assert cen_api.buscar_columna(df, ["cmg_usd_mwh_", "cmg_usd_mwh"]) == "Cmg_USD_MWh"
    assert cen_api.buscar_columna(df, ["barra_info"]) == "BARRA_INFO"
    assert cen_api.buscar_columna(df, ["inexistente"]) is None


def test_user_key_falta():
    viejo = os.environ.pop("COORDINADOR_USER_KEY", None)
    try:
        try:
            cen_api.user_key()
            raise AssertionError("user_key() debio lanzar RuntimeError")
        except RuntimeError as e:
            assert "portal.api.coordinador.cl" in str(e)
            assert "COORDINADOR_USER_KEY" in str(e)
        os.environ["COORDINADOR_USER_KEY"] = "abc123"
        assert cen_api.user_key() == "abc123"
    finally:
        if viejo is None:
            os.environ.pop("COORDINADOR_USER_KEY", None)
        else:
            os.environ["COORDINADOR_USER_KEY"] = viejo


# ---------------------------------------------------------------------------
# Tests de parsers (fixtures inline con nombres de campo probables de la SIP)
# ---------------------------------------------------------------------------

FIXTURE_CMG_REAL = {
    "data": [
        {"barra_info": "BA S/E QUILLOTA 220KV",
         "fecha_hora": "2024-07-14 01:00:00", "cmg_usd_mwh_": 62.45},
        {"barra_info": "BA S/E CRUCERO 220KV",
         "fecha_hora": "2024-07-15 02:00:00", "cmg_usd_mwh_": 58.1},
        {"barra_info": "BA S/E ALTO JAHUEL 220KV",
         "fecha_hora": "2024-07-15 03:00:00", "cmg_usd_mwh_": "61.7"},
        {"barra_info": "BA S/E PUERTO MONTT 110KV",  # debe filtrarse
         "fecha_hora": "2024-07-15 03:00:00", "cmg_usd_mwh_": 70.0},
    ],
    "next": None,
}


def test_parser_cmg_real():
    df = cmg_real.parsear_respuesta(FIXTURE_CMG_REAL)
    assert list(df.columns) == ["barra", "fecha", "hora", "cmg_usd_mwh"]
    assert len(df) == 3, df  # PUERTO MONTT filtrado
    assert pd.api.types.is_float_dtype(df["cmg_usd_mwh"]), df.dtypes
    assert pd.api.types.is_integer_dtype(df["hora"]), df.dtypes
    assert df["cmg_usd_mwh"].round(2).tolist() == [62.45, 58.1, 61.7]
    assert df["hora"].tolist() == [1, 2, 3]
    assert df["fecha"].tolist() == ["2024-07-14", "2024-07-15", "2024-07-15"]
    # parser tolera respuesta vacia
    vacio = cmg_real.parsear_respuesta({"data": []})
    assert vacio.empty and list(vacio.columns) == list(df.columns)


FIXTURE_CMG_ONLINE_15MIN = {
    "data": [
        # 4 intervalos de 15 min de la misma barra/hora -> deben colapsar a 1
        {"barra": "BA S/E QUILLOTA 220KV",
         "fecha_hora": "2024-01-10 05:00:00", "cmg_usd_mwh_": 60.0},
        {"barra": "BA S/E QUILLOTA 220KV",
         "fecha_hora": "2024-01-10 05:15:00", "cmg_usd_mwh_": 62.0},
        {"barra": "BA S/E QUILLOTA 220KV",
         "fecha_hora": "2024-01-10 05:30:00", "cmg_usd_mwh_": 64.0},
        {"barra": "BA S/E QUILLOTA 220KV",
         "fecha_hora": "2024-01-10 05:45:00", "cmg_usd_mwh_": 66.0},
        # otra hora de la misma barra -> fila aparte
        {"barra": "BA S/E QUILLOTA 220KV",
         "fecha_hora": "2024-01-10 06:00:00", "cmg_usd_mwh_": 70.0},
    ],
    "next": None,
}


def test_cmg_real_online_agrega_a_horario():
    """El CMg online es de 15 min; parsear_respuesta lo agrega a horario
    (media de los 4 intervalos por barra/fecha/hora)."""
    df = cmg_real.parsear_respuesta(FIXTURE_CMG_ONLINE_15MIN)
    assert list(df.columns) == ["barra", "fecha", "hora", "cmg_usd_mwh"]
    assert len(df) == 2  # hora 5 (4 intervalos) + hora 6 (1 intervalo)
    assert df["hora"].tolist() == [5, 6]
    # hora 5 = media(60,62,64,66) = 63.0 ; hora 6 = 70.0
    assert df["cmg_usd_mwh"].round(2).tolist() == [63.0, 70.0]


FIXTURE_CMG_PROG = {
    "data": [
        {"nmb_barra_info": "BA S/E POLPAICO 220KV", "fecha": "2026-06-11",
         "hora": 14, "cmg": 71.2, "fecha_publicacion": "2026-06-10T16:30:00"},
        {"nmb_barra_info": "BA S/E CHARRUA 220KV", "fecha": "2026-06-11",
         "hora": 14, "cmg": 65.0, "fecha_publicacion": "2026-06-10T16:30:00"},
        {"nmb_barra_info": "BA S/E PID PRUEBA 066KV", "fecha": "2026-06-11",
         "hora": 14, "cmg": 99.9, "fecha_publicacion": "2026-06-10T16:30:00"},
    ]
}


def test_parser_cmg_programado():
    df = cmg_prog.parsear_respuesta(FIXTURE_CMG_PROG)
    assert list(df.columns[:4]) == ["barra", "fecha", "hora", "cmg_usd_mwh"]
    assert len(df) == 2, df  # la barra de prueba 066KV se filtra
    # metadato de publicacion preservado (clave para el analisis anti-fuga)
    assert "fecha_publicacion" in df.columns, df.columns
    assert (df["fecha_publicacion"] == "2026-06-10T16:30:00").all()
    assert df["hora"].tolist() == [14, 14]
    assert pd.api.types.is_float_dtype(df["cmg_usd_mwh"])


# lista cruda (sin envoltorio): tambien debe parsear
FIXTURE_DEMANDA = [
    {"fecha": "2026-03-01", "hora": 1, "demanda": 9870.4, "id": 1},
    {"fecha": "2026-03-01", "hora": 2, "demanda": 9554.1, "id": 2},
    {"fecha": "2026-03-01", "hora": 3, "demanda": "9301.8", "id": 3},
]


def test_parser_demanda():
    df = demanda.parsear_respuesta(FIXTURE_DEMANDA)
    assert list(df.columns) == ["fecha", "hora", "demanda_mwh"]
    assert len(df) == 3
    assert pd.api.types.is_float_dtype(df["demanda_mwh"]), df.dtypes
    assert pd.api.types.is_integer_dtype(df["hora"]), df.dtypes
    assert df["demanda_mwh"].round(1).tolist() == [9870.4, 9554.1, 9301.8]
    assert df["fecha"].unique().tolist() == ["2026-03-01"]
    assert demanda.parsear_respuesta({"data": []}).empty


FIXTURE_GENERACION = {
    "results": [
        {"fecha": "2026-03-01", "hora": 1, "tipo_central": "Solar",
         "generacion_real_mwh": 10.0, "central": "PFV Uno"},
        {"fecha": "2026-03-01", "hora": 1, "tipo_central": "Solar",
         "generacion_real_mwh": 5.5, "central": "PFV Dos"},
        {"fecha": "2026-03-01", "hora": 1, "tipo_central": "Termica",
         "generacion_real_mwh": 100.0, "central": "CT Uno"},
        {"fecha": "2026-03-01", "hora": 2, "tipo_central": "Solar",
         "generacion_real_mwh": 12.0, "central": "PFV Uno"},
    ]
}


def test_parser_generacion_agrega_por_tecnologia():
    df = generacion.parsear_respuesta(FIXTURE_GENERACION)
    assert list(df.columns) == ["fecha", "hora", "tecnologia", "generacion_mwh"]
    assert len(df) == 3, df  # (h1,Solar) (h1,Termica) (h2,Solar)
    solar_h1 = df[(df.hora == 1) & (df.tecnologia == "Solar")]
    assert solar_h1["generacion_mwh"].iloc[0] == 15.5  # 10.0 + 5.5 agregadas
    assert "central" not in df.columns  # el detalle por central no se persiste
    assert pd.api.types.is_float_dtype(df["generacion_mwh"])
    assert pd.api.types.is_integer_dtype(df["hora"])


FIXTURE_EMBALSES = {
    "items": [
        {"fecha": "2026-03-01", "nombre_embalse": "EMBALSE COLBUN",
         "cota": 423.5, "afluente": 120.3},
        {"fecha": "2026-03-01", "nombre_embalse": "LAGO LAJA",
         "cota": 1305.1},  # sin afluente -> NA
        {"fecha": "2026-03-01", "nombre_embalse": "EMBALSE RAPEL",
         "cota": "104.9", "afluente": 80.0},
    ]
}


def test_parser_embalses():
    df = embalses.parsear_respuesta(FIXTURE_EMBALSES)
    assert list(df.columns) == ["fecha", "embalse", "cota_msnm", "afluente_m3s"]
    assert len(df) == 3
    assert pd.api.types.is_float_dtype(df["cota_msnm"]), df.dtypes
    assert df["cota_msnm"].round(1).tolist() == [423.5, 1305.1, 104.9]
    assert pd.isna(df["afluente_m3s"].iloc[1])  # LAGO LAJA sin afluente
    assert df["afluente_m3s"].iloc[0] == 120.3
    assert embalses.parsear_respuesta({"data": []}).empty


# ---------------------------------------------------------------------------
# Tests de extractor_cen_po (solo las partes puras, sin red)
# ---------------------------------------------------------------------------

def test_cen_po_fecha_de_url():
    f = cen_po._fecha_de_url
    assert f("https://x.cl/PO-2025-06-07.zip") == date(2025, 6, 7)
    assert f("https://x.cl/Programa20250607.zip") == date(2025, 6, 7)
    assert f("https://x.cl/PO_07-06-2025_def.zip") == date(2025, 6, 7)
    assert f("https://x.cl/sin_fecha.zip") is None
    assert f("https://x.cl/PO-2025-13-45.zip") is None  # fecha invalida


def test_cen_po_candidatos():
    assert cen_po._es_candidato("Resultados/COSTOSVARIABLES.csv")
    assert cen_po._es_candidato("resumen_PO.xlsx")
    assert cen_po._es_candidato("salida/Costo_Objetivo.csv")
    assert not cen_po._es_candidato("COSTOSVARIABLES.dat")  # extension no candidata
    assert not cen_po._es_candidato("topologia/barras.csv")


# ---------------------------------------------------------------------------
# Tests de validadores
# ---------------------------------------------------------------------------

def test_validar_outliers_con_outlier_plantado():
    n = 60
    valores = [50.0 + (i % 7) * 0.5 for i in range(n)] + [500.0]  # outlier al final
    df = pd.DataFrame({"fecha": [f"2026-01-{(i % 28) + 1:02d}" for i in range(n + 1)],
                       "valor": valores})
    sospechosas = validadores.validar_outliers(df, "valor", k=4.0)
    assert len(sospechosas) == 1, sospechosas
    assert sospechosas["valor"].iloc[0] == 500.0
    assert "_desviacion_robusta" in sospechosas.columns
    # sin outliers -> vacio
    limpio = validadores.validar_outliers(df.iloc[:n], "valor", k=4.0)
    assert limpio.empty, limpio


def test_validar_completitud_con_parquets_temporales():
    with tempfile.TemporaryDirectory() as tmp:
        dir_raw = Path(tmp)
        carpeta = dir_raw / "fuente_x" / "2025"
        carpeta.mkdir(parents=True)
        # 1..10 ene + 15..20 ene -> hueco 11..14 (4 dias)
        fechas = ([date(2025, 1, d).isoformat() for d in range(1, 11)]
                  + [date(2025, 1, d).isoformat() for d in range(15, 21)])
        pd.DataFrame({"fecha": fechas, "valor": range(len(fechas))}).to_parquet(
            carpeta / "fuente_x_2025-01.parquet", index=False)
        res = validadores.validar_completitud(dir_raw)
        assert len(res) == 1, res
        fila = res.iloc[0]
        assert fila["fuente"] == "fuente_x"
        assert fila["dias_presentes"] == 16 and fila["dias_esperados"] == 20
        assert fila["pct_completitud"] == 80.0
        assert fila["n_huecos"] == 1
        assert "2025-01-11..2025-01-14" in fila["huecos"], fila["huecos"]
    # directorio inexistente -> DataFrame vacio con columnas
    res = validadores.validar_completitud(Path(tmp) / "no_existe")
    assert res.empty and list(res.columns) == validadores.COLUMNAS_COMPLETITUD


def test_validar_consistencia_cruzada():
    with tempfile.TemporaryDirectory() as tmp:
        dir_raw = Path(tmp)
        d_dem = dir_raw / "cen_demanda" / "2025"
        d_gen = dir_raw / "cen_generacion" / "2025"
        d_dem.mkdir(parents=True)
        d_gen.mkdir(parents=True)
        # dia 1: gen 210 vs dem 200 (5%, ok); dia 2: gen 320 vs dem 200 (60%)
        pd.DataFrame({
            "fecha": ["2025-01-01"] * 2 + ["2025-01-02"] * 2,
            "hora": [1, 2, 1, 2],
            "demanda_mwh": [100.0, 100.0, 100.0, 100.0],
        }).to_parquet(d_dem / "cen_demanda_2025-01.parquet", index=False)
        pd.DataFrame({
            "fecha": ["2025-01-01"] * 2 + ["2025-01-02"] * 2,
            "hora": [1, 2, 1, 2],
            "tecnologia": ["solar", "termica", "solar", "termica"],
            "generacion_mwh": [105.0, 105.0, 160.0, 160.0],
        }).to_parquet(d_gen / "cen_generacion_2025-01.parquet", index=False)
        violaciones = validadores.validar_consistencia_cruzada(dir_raw)
        assert len(violaciones) == 1, violaciones
        assert "2025-01-02" in violaciones[0]
        # sin cen_generacion -> no evaluable -> []
        import shutil
        shutil.rmtree(dir_raw / "cen_generacion")
        assert validadores.validar_consistencia_cruzada(dir_raw) == []


def test_generar_reporte_sin_datos():
    with tempfile.TemporaryDirectory() as tmp:
        dir_raw = Path(tmp) / "raw_vacio"
        salida = Path(tmp) / "calidad_datos.md"
        ruta = validadores.generar_reporte(dir_raw, salida)
        texto = ruta.read_text(encoding="utf-8")
        assert texto.startswith("---"), texto[:80]  # frontmatter YAML
        assert "last_synthesized:" in texto
        assert "data/processed/tabla_maestra.parquet" in texto
        assert "esperando primer backfill" in texto


def test_generar_reporte_con_datos():
    with tempfile.TemporaryDirectory() as tmp:
        dir_raw = Path(tmp)
        carpeta = dir_raw / "cen_demanda" / "2025"
        carpeta.mkdir(parents=True)
        pd.DataFrame({
            "fecha": ["2025-01-01"] * 24,
            "hora": list(range(24)),
            "demanda_mwh": [9000.0] * 23 + [90000.0],  # outlier plantado
        }).to_parquet(carpeta / "cen_demanda_2025-01.parquet", index=False)
        salida = Path(tmp) / "calidad_datos.md"
        texto = validadores.generar_reporte(dir_raw, salida).read_text(encoding="utf-8")
        assert "Completitud por fuente" in texto
        assert "cen_demanda" in texto
        assert "1 filas sospechosas" in texto, texto


def main() -> None:
    pruebas = sorted((nombre, fn) for nombre, fn in globals().items()
                     if nombre.startswith("test_") and callable(fn))
    for nombre, fn in pruebas:
        fn()
        print(f"  ok {nombre}")
    print(f"\n{len(pruebas)} tests pasaron.")
    print("TODOS LOS TESTS OFFLINE OK")


if __name__ == "__main__":
    main()
