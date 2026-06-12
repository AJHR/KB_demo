# sources/costos_sen

## Que contiene
Catálogo de fuentes de datos públicas para el modelo predictivo del costo total de operación diario del SEN (horizonte D+1), producido por 7 agentes de investigación en paralelo (2026-06-12). Es la referencia de la fase 1 de la misión de predicción de costos; los extractores de `tools/etl/` se construyen contra este catálogo.

## Archivos clave
| Archivo | Descripcion | Notas |
|---------|-------------|-------|
| catalogo_fuentes.md | Tabla maestra consolidada: 22 fuentes con endpoint, auth, formato, granularidad, historia, hora de publicación y estado de verificación | Incluye el hallazgo central sobre la variable objetivo y los 6 riesgos principales |
| anexos/coordinador.md | Detalle CEN: definiciones de costo de operación, PO, API SIP, ecosistema de terceros | La fuente más crítica del proyecto |
| anexos/cne.md | CNE Energía Abierta (API Junar + capa desarrolladores) | |
| anexos/combustibles.md | EIA/FRED/stooq/yfinance, JKM/API2, USD/CLP | Define secrets opcionales |
| anexos/hidrologia.md | Embalses CEN, DGA, energía afluente | |
| anexos/clima.md | Open-Meteo: 5 APIs, anti-fuga de corridas, 11 puntos geográficos | |
| anexos/calendario.md | Validación local de `holidays` + gaps (elecciones) | Única fuente verificada en vivo desde el sandbox |
| anexos/noticias.md | Veredicto: descartada del MVP, con evidencia | |

## Advertencias
- Estado "pendiente — red del sandbox bloqueada": las URLs provienen de documentación oficial y código de terceros, no de descargas en vivo. La primera corrida de `backfill.yml` en GitHub Actions es la verificación real.
- La hora de publicación del Programa de Operación D+1 es el riesgo nº1 (regla anti-fuga de las 20:00) y está sin confirmar.
