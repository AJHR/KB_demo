# CLAUDE.md — Gobernanza del Knowledge Base

Este archivo es la fuente de verdad para agentes AI (Claude Code) que operan sobre este repositorio. Lo leen primero, antes de tocar nada mas.

> Patron de inspiracion: Karpathy KB (raw sources / wiki synthesis / schema governance).

## Estructura del repositorio

Tres zonas con responsabilidades distintas, mas una zona de herramientas:

| Zona | Mutabilidad | Que contiene | Quien escribe |
|------|-------------|--------------|---------------|
| `sources/` | INMUTABLE | Material de referencia importado de afuera: exports de Confluence, estandares, propuestas de terceros, PDFs. No se edita despues de ingerir. | Humano (ingestion) |
| `work/` | VIVO | Documentos del proyecto que evolucionan: minutas, diagnosticos, stakeholders, decisiones. Editable. | Humano + agente |
| `wiki/` | SINTESIS | Paginas generadas por LLM que sintetizan a traves de `sources/` + `work/`. Cada pagina cita sus fuentes via frontmatter. | Agente (con supervision) |
| `tools/` | UTIL | Scripts de mantenimiento (lint, exports, migraciones). | Humano |

Y tres archivos meta en la raiz:

| Archivo | Audiencia | Proposito |
|---------|-----------|-----------|
| `CLAUDE.md` | Agentes AI | Gobernanza: reglas, schema, como comportarse, templates (este archivo) |
| `index.md` | Humanos | Catalogo clickeable: "que hay en este repo?" |
| `log.md` | Ambos | Registro cronologico append-only de cambios al KB |

## Reglas de navegacion para agentes

Cuando entres a este repo, sigue este orden:

1. Lee `CLAUDE.md` (este archivo) primero.
2. Para visin de alto nivel del tema X, lee `wiki/{tema}.md` y sigue sus `sources:`.
3. Para profundidad por carpeta, lee `RESUMEN.md` de la carpeta correspondiente ANTES de abrir archivos individuales.
4. `sources/` es read-only. No edites, no renombres, no reformatees. Si necesitas el contenido en otro formato, genera el `.md` companion y dejalo al lado.
5. `work/` se puede editar libremente. Mantenelo limpio, mueve drafts viejos a una subcarpeta `archive/` si crecen mucho.
6. Si tocas algo, actualiza el `RESUMEN.md` de la carpeta y agrega entrada a `log.md`.

## Convenciones de nombres

- Carpetas: ingles, kebab-case. Ejemplo: `payment-redesign-2025/`, no `Payment Redesign 2025/`.
- `RESUMEN.md`: uno por carpeta de contenido, en MAYUSCULA, contenido en espanol.
- Archivos en `sources/`: NO renombrar. Preservar nombres originales de exportacion para que el origen siga siendo trazable.
- Archivos en `work/` y `wiki/`: kebab-case.
- Meta-archivos en raiz (`CLAUDE.md`, `index.md`, `log.md`): MAYUSCULA inicial / convencion de cada uno.

## Template de RESUMEN.md

Cada carpeta de contenido (en `sources/`, `work/`, `wiki/`) lleva un `RESUMEN.md` con esta estructura:

```markdown
# [Nombre de la carpeta]

## Que contiene
[1-2 oraciones: proposito y origen del contenido]

## Archivos clave
| Archivo | Descripcion | Notas |
|---------|-------------|-------|
| archivo.md | Que contiene | Tamano, formato, advertencias |

## Advertencias
- [Archivos grandes >500KB que requieren lectura por chunks]
- [Formatos raw (HTML, PDF) que necesitan exportacion a markdown]
- [Contenido stale o con links rotos]
```

## Frontmatter de wiki pages

Cada pagina en `wiki/` (excepto `RESUMEN.md`) lleva frontmatter YAML obligatorio:

```yaml
---
title: Nombre de la pagina
sources:
  - sources/ruta/al/archivo.md
  - work/ruta/al/otro.md
last_synthesized: YYYY-MM-DD
---
```

- `sources:` lista las rutas (post-rename, finales) de los archivos que la sintesis cita.
- `last_synthesized:` fecha ISO de la ultima vez que se regenero/revis la pagina.
- `tools/lint-kb.sh` marca como stale las paginas cuyas `sources:` se modificaron despues de `last_synthesized`.

## Flujo de ingestion — Cuando entra contenido nuevo

### Paso 1: Formato

- Si el archivo es markdown, listo, usar directo.
- Si es raw (PDF, HTML, XLSX, PPTX), exportar a markdown y guardar ambos lado a lado. El raw es para humanos; el `.md` es para agentes.

### Paso 2: Zona

- Referencia externa que no vamos a editar: va a `sources/`.
- Documento nuestro que va a evolucionar: va a `work/`.

### Paso 3: Post-ingestion

1. Actualizar `RESUMEN.md` de la carpeta destino (o crearlo si la carpeta es nueva).
2. Actualizar `index.md` si es una carpeta nueva.
3. Registrar en `log.md`: fecha, que se agrego, origen.
4. Pedir a Claude: "actualiza `wiki/` con lo nuevo".
5. Commit con mensaje descriptivo.

## Flujo de wiki — Como sintetizar

1. Identifica el tema (cross-fuente, no un resumen de una sola carpeta).
2. Lee `sources:` candidatas, prioriza las mas recientes/autoritativas.
3. Escribe `wiki/{tema}.md` con frontmatter completo.
4. Cita inline (no solo en frontmatter) los hechos no obvios: "Segun `sources/x/y.md`, ...".
5. Actualiza `last_synthesized` cada vez que regeneres.
6. Si una fuente cambia, marca la pagina como stale (regenera o ajusta).

## Reglas de integridad de datos

- `sources/` es inmutable. Si necesitas corregir algo, anotalo en el `RESUMEN.md` de la carpeta o en una pagina de `wiki/`, no edites el original.
- No borrar archivos sin registrar en `log.md`.
- No mover archivos sin actualizar las rutas en `wiki/*.sources` ni los links de `index.md`.
- Una sola sintesis puede citar multiples fuentes; una fuente puede ser citada por multiples sintesis. Trazabilidad bidireccional via `lint-kb.sh`.

## Personas clave del proyecto

> _Llenar cuando entre contenido. Esta seccion es un placeholder._

| Rol | Nombre | Contacto | Notas |
|-----|--------|----------|-------|
| - | - | - | - |

## Checks de `tools/lint-kb.sh`

El linter verifica:

1. `RESUMEN.md` existe en cada subcarpeta directa de `sources/`, `work/`, `wiki/`.
2. Nombres de carpetas son kebab-case (sin espacios, sin mayusculas).
3. Wiki pages: `sources:` modificados despues de `last_synthesized` (stale).
4. Archivos mayores a 500KB (problematicos para agentes; sugiere chunking o export).
5. Archivos raw (PDF/HTML/XLSX/PPTX) sin companion `.md`.
6. Links relativos en `index.md` apuntan a archivos existentes.
7. Archivos en `sources/` no modificados despues de su fecha de import (inmutabilidad).

Correr: `bash tools/lint-kb.sh`. Exit code != 0 = hay problemas.
