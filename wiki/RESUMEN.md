# wiki/

## Que contiene
Paginas de sintesis cross-fuente sobre el mercado electrico chileno, escritas para que un gerente de generadora pueda navegar el marco regulatorio rapido. Cada pagina cita inline los PDFs reales descargados a `sources/regulation-*/`.

## Archivos clave
| Archivo | Descripcion | Cobertura |
|---------|-------------|-----------|
| [mercado-mayorista-chile.md](./mercado-mayorista-chile.md) | Vision general: como esta organizado el mercado, quien decide que, como te despachan y te pagan | LGSE/DS 327, NT Coordinacion y Operacion, Anexo Sistemas de Medidas, Panel de Expertos |
| [servicios-complementarios-y-transferencias.md](./servicios-complementarios-y-transferencias.md) | SSCC, transferencias mensuales, potencia firme, informes de falla | NT Cap.3, DS 125, decreto transferencias potencia |
| [conexion-y-transmision.md](./conexion-y-transmision.md) | Como conectar una central nueva, regimen de transmision (troncal/zonal/distribucion), expansion, BESS | DS 144 (subtransmision), DS 48 (troncal), Jornada Tecnica Transmision 2026, BESS, costo de falla |
| [marco-pmgd-y-distribuida.md](./marco-pmgd-y-distribuida.md) | Regimen PMGD (<= 9 MW) y la NTCO-PMGD 2026 con almacenamiento | NTCO-PMGD-2026, DS 229 sistemas medianos, estabilizacion tarifaria |
| [ciberseguridad-sen.md](./ciberseguridad-sen.md) | Obligaciones de Coordinados: CIP-002 a CIP-011, niveles de impacto, protocolo de notificacion | Estandar Ciberseguridad CEN oct-2022, Protocolo Ciberincidentes dic-2021 |

## Como agregar una pagina
1. Identifica un tema cross-fuente.
2. Crea `wiki/{tema-en-kebab-case}.md` con frontmatter `title`, `sources:` y `last_synthesized:` (ver CLAUDE.md).
3. Cita inline los hechos no obvios: "Segun `sources/.../x.pdf`, ...".
4. Registra en `log.md` y este `RESUMEN.md`.
5. Si una fuente cambia, regenera y actualiza `last_synthesized`.

## Advertencias
- Las paginas son derivadas. La fuente de verdad sigue siendo `sources/`.
- `tools/lint-kb.sh` marca paginas stale (fuentes modificadas despues de `last_synthesized`).
- Lagunas conocidas estan listadas al final de cada pagina (seccion "Lagunas conocidas"). Cubrirlas requiere reintentar scraping con URLs corregidas — ver issue tracker en `log.md`.
