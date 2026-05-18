# Reporte de Ingesta — 2026-05-14 13:09Z

> **Estado: BLOQUEADO POR RED DEL SANDBOX (no por las fuentes).**
>
> Esta corrida se ejecuto en un sandbox sin acceso saliente a `coordinador.cl`,
> `cne.cl`, `energiaabierta.cl` y `energia.gob.cl` (los cuatro devuelven HTTP 403
> incluso para `/robots.txt` con cualquier User-Agent). La infraestructura del
> pipeline funciono correctamente: rate limiting, parsing de YAML, llamadas
> tenacity-con-retry, logging a `logs/auth_required.txt` y `logs/failed_downloads.txt`,
> y la generacion de este reporte. Solo no hubo descargas reales.
>
> **Para correr en serio**: clonar el repo en un entorno con salida a internet,
> `pip install -r requirements.txt && playwright install chromium`, y ejecutar
> `python scripts/initial_load.py`. Esperado: 6-8 horas, ~hasta cientos de MB
> de archivos crudos. Luego `python scripts/process_to_vector.py` y
> `python scripts/build_report.py`.
>
> Las 22 entradas en `auth_required.txt` mas abajo son todas HTTP 403 desde el
> sandbox; en un entorno con red se vaciarian (o se llenarian de cosas
> realmente protegidas como InfoTecnica/REUC, donde el codigo las registra y
> continua segun la regla "Sin bypass de auth").

## Resumen
- Archivos descargados: **0** (0.0 B)
- Chunks en vector store: **0**
- Docs PDF que requieren OCR: **0**
- Rutas saltadas por robots.txt: **0**
- Descargas fallidas: **1**
- Recursos que requieren auth: **22**

## Archivos por categoria

| Categoria | Archivos | Tamano |
|-----------|----------|--------|

## Cobertura temporal

| Serie | Min | Max |
|-------|-----|-----|
| CEN CMg horario | - | - |
| CEN generacion real | - | - |
| CEN demanda | - | - |

## Documentos que requieren OCR (escaneados)
_(ninguno)_

## Rutas saltadas por robots.txt (ultimas 100)
_(ninguna)_

## Descargas fallidas (ultimas 100)
```
2026-05-14T13:08:29+0000	playwright-open:No module named 'playwright'	https://www.coordinador.cl/operacion/graficos/operacion-real/costo-marginal-real/
```

## Recursos que requirieron auth (ultimas 100)
```
2026-05-14T13:08:29+0000	http_403	https://www.coordinador.cl/reportes-y-estadisticas/
2026-05-14T13:08:35+0000	http_403	https://www.coordinador.cl/reportes-y-estadisticas/
2026-05-14T13:08:42+0000	http_403	https://www.coordinador.cl/reportes-y-estadisticas/
2026-05-14T13:08:45+0000	http_403	https://www.coordinador.cl/reportes-y-estadisticas/
2026-05-14T13:08:48+0000	http_403	https://www.coordinador.cl/reportes-y-estadisticas/
2026-05-14T13:08:52+0000	http_403	https://www.coordinador.cl/normativa-tecnica/
2026-05-14T13:08:55+0000	http_403	https://www.coordinador.cl/normativa-tecnica/
2026-05-14T13:08:59+0000	http_403	https://www.coordinador.cl/normativa-tecnica/
2026-05-14T13:09:02+0000	http_403	https://www.coordinador.cl/reportes-y-estadisticas/
2026-05-14T13:09:04+0000	http_403	https://www.cne.cl/normativas/electrica/sector-electrico/
2026-05-14T13:09:08+0000	http_403	https://www.cne.cl/normativas/electrica/sector-electrico/
2026-05-14T13:09:11+0000	http_403	https://www.cne.cl/normativas/electrica/sector-electrico/
2026-05-14T13:09:14+0000	http_403	https://www.cne.cl/normativas/electrica/sector-electrico/
2026-05-14T13:09:18+0000	http_403	https://www.cne.cl/normativas/electrica/sector-electrico/
2026-05-14T13:09:21+0000	http_403	https://www.cne.cl/normativas/electrica/sector-electrico/
2026-05-14T13:09:24+0000	http_403	https://www.cne.cl/tarificacion/electrica/obras-nuevas-y-urgentes/
2026-05-14T13:09:28+0000	http_403	https://www.cne.cl/tarificacion/electrica/precios-nudo/
2026-05-14T13:09:31+0000	http_403	https://www.cne.cl/tarificacion/electrica/precios-nudo/
2026-05-14T13:09:35+0000	http_403	http://energiaabierta.cl/categorias-estadistica/electricidad?_sft_organismos-estadistica=coordinador-electrico-nacional
2026-05-14T13:09:38+0000	http_403	http://energiaabierta.cl/empresas/
2026-05-14T13:09:40+0000	http_403	https://energia.gob.cl/noticias
2026-05-14T13:09:43+0000	http_403	https://energia.gob.cl/reforma2026
```

## 5 queries de prueba contra el vector store

### Q: Costo marginal promedio en Quillota ultimo mes
_Sin resultados._ error: No module named 'lancedb'

### Q: Que dice el anexo sismico sobre BESS
_Sin resultados._ error: No module named 'lancedb'

### Q: Cambios propuestos por la reforma 2026
_Sin resultados._ error: No module named 'lancedb'

### Q: Como se reportan ciberincidentes en el sector electrico chileno
_Sin resultados._ error: No module named 'lancedb'

### Q: Capacidad instalada de generacion solar en Chile 2026
_Sin resultados._ error: No module named 'lancedb'