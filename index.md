# Index — Knowledge Base

Catalogo navegable de este repositorio. Para reglas y schema ver [`CLAUDE.md`](./CLAUDE.md). Para historial de cambios ver [`log.md`](./log.md).

## Zonas

### `sources/` — Referencia inmutable

PDFs de regulacion electrica chilena (CNE, Coordinador, Minenergia) descargados via scraping respetuoso. Cada subcarpeta lleva su `RESUMEN.md`.

| Carpeta | Tema | Archivos |
|---------|------|---------:|
| [`regulation-cne-sector-electrico`](./sources/regulation-cne-sector-electrico/RESUMEN.md) | LGE, decretos historicos, normativa base | 80 |
| [`regulation-cne-obras-nuevas-urgentes`](./sources/regulation-cne-obras-nuevas-urgentes/RESUMEN.md) | Decretos 6T/14T, costo de falla, precios estabilizados | 48 |
| [`regulation-cne-precios-nudo`](./sources/regulation-cne-precios-nudo/RESUMEN.md) | **Informes y decretos de precios de nudo** (semestrales, Art. 163 LGSE) | 46 |
| [`regulation-cne-normas-tecnicas`](./sources/regulation-cne-normas-tecnicas/RESUMEN.md) | ResEx ERNC, decretos por sistema mediano | 40 |
| [`regulation-coordinador-reportes-estadisticas`](./sources/regulation-coordinador-reportes-estadisticas/RESUMEN.md) | Guias de usuario CEN (IT, Gescal, Licitaciones, RENOVA) | 40 |
| [`regulation-minenergia-marco-regulatorio`](./sources/regulation-minenergia-marco-regulatorio/RESUMEN.md) | Decretos exentos, instructivos, IIR (informes impacto regulatorio) | 30 |
| [`regulation-cne-reglamentos-mercado`](./sources/regulation-cne-reglamentos-mercado/RESUMEN.md) | NT Coordinacion y Operacion, NTCO-PMGD 2026, DS 144, DS 48, Panel de Expertos, sistemas de medidas | 11 |
| [`regulation-coordinador-mercados-servicios`](./sources/regulation-coordinador-mercados-servicios/RESUMEN.md) | Servicios complementarios, transferencias economicas | 9 |
| [`regulation-coordinador-desarrollo-transmision`](./sources/regulation-coordinador-desarrollo-transmision/RESUMEN.md) | Jornadas tecnicas 2026: BESS, control de tension, monitoreo | 8 |
| [`regulation-coordinador-operacion-sen`](./sources/regulation-coordinador-operacion-sen/RESUMEN.md) | ⚠️ Solo 1 archivo — URL del Coordinador sigue sin entregar | 1 |

**Carpetas pendientes** (URLs no alcanzan a poblarlas — pueden necesitar Playwright o cambio manual):
- `regulation-coordinador-normativa-tecnica` (PTN, ciberseguridad, grid forming)
- `regulation-coordinador-operacion-sen` (Procedimientos DO, programa de operacion)

**Total actual: 313 archivos, 253 unicos, ~527 MB.**

### `work/` — Documentos vivos

_(vacio — agregar minutas, diagnosticos, etc. cuando arranque trabajo del proyecto)_

### `wiki/` — Sintesis

Paginas escritas para entender el mercado desde la posicion de un generador. Ver [`wiki/RESUMEN.md`](./wiki/RESUMEN.md).

| Pagina | Tema | Ultima sintesis |
|--------|------|-----------------|
| [`wiki/mercado-mayorista-chile.md`](./wiki/mercado-mayorista-chile.md) | Estructura institucional + despacho + transferencias + potencia firme | 2026-05-15 |
| [`wiki/servicios-complementarios-y-transferencias.md`](./wiki/servicios-complementarios-y-transferencias.md) | Como se cobra por mantener el sistema operando (SSCC, transferencias mensuales, fallas) | 2026-05-15 |
| [`wiki/conexion-y-transmision.md`](./wiki/conexion-y-transmision.md) | Conectar una central nueva, segmentos de transmision, BESS, costo de falla | 2026-05-15 |
| [`wiki/marco-pmgd-y-distribuida.md`](./wiki/marco-pmgd-y-distribuida.md) | PMGD <=9 MW, NTCO-PMGD 2026 con BESS, sistemas medianos, estabilizacion tarifaria | 2026-05-15 |

### `tools/` — Mantenimiento

| Script | Proposito |
|--------|-----------|
| [`tools/lint-kb.sh`](./tools/lint-kb.sh) | Verificar invariantes del KB (ver CLAUDE.md) |

### `data/vector/` — Vector store (busqueda semantica)

Indice vectorial sobre `sources/regulation-*/*.pdf`. Ver [`data/vector/README.md`](./data/vector/README.md).

- `manifest.json` — inventario de PDFs indexados (versionado)
- `lancedb/` — base binaria (gitignored, se regenera local)
- Modelo: `paraphrase-multilingual-MiniLM-L12-v2` (gratis, multilingue, dim=384)
- Chunking: 800 tokens, overlap 150

Generar: `bash run_vector.sh`. Consultar: `python generador-demo-electrico/scripts/query_kb.py "tu pregunta"`.

### Subproyectos

| Subproyecto | Proposito |
|-------------|-----------|
| [`generador-demo-electrico/`](./generador-demo-electrico/README.md) | Pipeline de scraping respetuoso. Estado actual: corrida de regulacion completada (commit `093393b`), ingestio operacional CEN/CNE/Energia Abierta pendiente (requiere red sin allowlist restringida). |

## Glossario rapido para no-electricistas

| Sigla | Significado |
|-------|-------------|
| **CEN** | Coordinador Electrico Nacional (operador del sistema, ex CDEC) |
| **CNE** | Comision Nacional de Energia (regulador) |
| **SEN** | Sistema Electrico Nacional |
| **LGSE / DFL 4** | Ley General de Servicios Electricos (DFL 4/2006, texto refundido del DFL 1/1982) |
| **NT** | Norma Tecnica (el "como" operativo, lo emite la CNE) |
| **NTSyCS** | NT de Seguridad y Calidad de Servicio |
| **NTCO** | NT de Coordinacion y Operacion |
| **PMGD** | Pequeno Medio de Generacion Distribuida (<= 9 MW en distribucion) |
| **SSCC** | Servicios Complementarios |
| **CMg** | Costo Marginal (precio horario por barra del mercado spot) |
| **PPA** | Power Purchase Agreement (contrato bilateral de suministro) |
| **PNCP** | Precios de Nudo de Corto Plazo (fijados semestralmente por CNE para regulados) |
| **BESS** | Battery Energy Storage System |
| **PES** | Pruebas de Puesta en Servicio |
| **SCR** | Solicitud de Conexion a la Red |
| **IT** | Informe Tecnico (de la CNE, e.g. precios de nudo, costo de falla) |
