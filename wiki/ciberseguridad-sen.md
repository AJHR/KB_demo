---
title: Ciberseguridad del SEN — estandar y protocolo de notificacion
sources:
  - sources/regulation-coordinador-normativa-tecnica/Estandar-Ciberseguridad-SEN-Octubre-2022.pdf
  - sources/regulation-coordinador-normativa-tecnica/Protocolo-de-Notificacion-de-Incidentes-de-Ciberseguridad.pdf
last_synthesized: 2026-05-18
---

# Ciberseguridad del SEN — obligaciones para Coordinados

> Marco obligatorio para todas las empresas Coordinadas del SEN (generadores, transmisoras, distribuidoras, dueños de SSCC y BESS). Basado en NERC-CIP. Fiscalizado por el CEN y la SEC.

## 1. Estandar de Ciberseguridad (CEN, oct 2022)

El **Estandar de Ciberseguridad para el Sector Electrico** (oct 2022, 100 pp.) es el documento maestro. Lo emite el CEN y rige a todas las empresas Coordinadas.

> "ESTANDAR DE CIBERSEGURIDAD PARA EL SECTOR ELECTRICO. Octubre 2022."
> — `sources/regulation-coordinador-normativa-tecnica/Estandar-Ciberseguridad-SEN-Octubre-2022.pdf` p.1

El estandar adopta el modelo **NERC-CIP** (North American Electric Reliability Corp - Critical Infrastructure Protection) adaptado para Chile. La tabla de contenidos identifica al menos 7 capitulos CIP (p.2-3):

| Capitulo | Tema |
|----------|------|
| **CIP-002** | Categorizacion de Ciber Sistemas SEN |
| **CIP-005** | Perimetro de Seguridad Electronica (referenciado en el protocolo) |
| **CIP-006** | Seguridad fisica (Sec. 7.5) |
| **CIP-007** | Gestion de la seguridad de sistemas (Sec. 7.6) |
| **CIP-008** | Reporte de Incidentes y Planes de Respuesta (Sec. 7.7) |
| **CIP-009/010/011** | Recuperacion, gestion de cambios, proteccion de informacion (en capitulos siguientes) |

### Niveles de impacto

El estandar define tres niveles para clasificar los Ciber Sistemas SEN:

- **Impacto Alto** (Sec. 6.1)
- **Impacto Medio** (Sec. 6.2)
- **Impacto Bajo** (implicito)

La asignacion depende del rol del sistema en la operacion del SEN (despacho, control, monitoreo critico, etc.). Sistemas que controlan instalaciones criticas son Impacto Alto.

### Aplicabilidad

> Cada capitulo CIP define su "Aplicabilidad Especifica y Excepciones" — es decir, no todo aplica por igual. Una distribuidora chica cumple un subset distinto al de una generadora con central de impacto alto.

### Cumplimiento y monitoreo

El CEN monitorea el cumplimiento (Sec. 4 del estandar). Las empresas Coordinadas tienen obligacion de reserva y confidencialidad sobre los detalles de sus sistemas (Sec. 5).

## 2. Protocolo de Notificacion de Ciberincidentes (CEN, dic 2021)

Cuando ocurre un incidente, este protocolo (7 pp.) define que reportar, cuando y como.

### Cadena de notificacion

> "Las empresas Coordinadas deberan comunicar al Coordinador Electrico Nacional CEN y este a la Superintendencia de Electricidad y Combustibles SEC, y a otras autoridades que defina la SEC, los incidentes y amenazas de ciberseguridad que afecten o intenten poner en riesgo la seguridad y confiabilidad del Sistema Electrico Nacional."
> — `sources/regulation-coordinador-normativa-tecnica/Protocolo-de-Notificacion-de-Incidentes-de-Ciberseguridad.pdf` p.3

Flujo:

```
Empresa Coordinada -> CEN -> SEC -> autoridades adicionales (segun caso)
```

### Que constituye un incidente reportable

> "**Incidentes de Ciberseguridad Reportables (ICR)**: Corresponden a aquellos Incidentes de Ciberseguridad que han comprometido o interrumpido:
>
> - Un Ciber Sistema SEN que desempena una o mas funciones asociadas a mantener la seguridad y confiabilidad del SEN..., sean de impacto alto, medio o bajo.
> - Un **Perimetro de Seguridad Electronica (PSE)** de un Ciber Sistema SEN de Impacto Alto o Medio.
> - Un **Sistema de Monitoreo**..." (truncado en la extraccion)
> — Protocolo p.3

### Estructura del protocolo

| Seccion | Tema |
|---------|------|
| 1 | Comunicacion de incidentes (cadena CEN -> SEC) |
| 2 | Aplicabilidad (a quien y a que incidentes) |
| 3 | Periodicidad de reportes |
| 4 | Notificacion de incidentes (formato y plazos) |
| 5 | Informe de cierre del incidente |
| 6 | Envio de la informacion (canal seguro) |

### Implicancia operacional para un generador

Si tu central tiene un ICR (sea por intrusion, ransomware, manipulacion de PLC, etc.), tienes que:

1. **Notificar al CEN** dentro del plazo del protocolo (Sec. 3-4).
2. Mantener al CEN y SEC **informados de la evolucion** y de las acciones de deteccion/respuesta/recuperacion.
3. Emitir un **Informe de Cierre** al final (Sec. 5).
4. Toda la comunicacion va por **canal seguro** (Sec. 6).

Esto implica tener **proceso interno operativo** (no solo IT) para detectar y reportar — un equipo SOC + runbooks coordinados con el CEN.

## 3. Relacion con NERC-CIP

El estandar chileno declara explicitamente que esta "basado en el estandar NERC-CIP". Para una empresa multinacional con operaciones en USA/Canada, hay solapamiento conceptual fuerte: misma estructura de CIP-002 a CIP-011, mismo concepto de Ciber Sistemas e Impacto, mismo flujo de reporte. Pero **la implementacion chilena es propia** — los detalles de cada CIP y los plazos no son identicos a NERC.

## 4. Lagunas conocidas

- No tenemos en el KB la **resolucion CNE que aprobo formalmente el estandar** (el documento se atribuye al CEN pero generalmente la CNE lo refrenda via resolucion exenta). Buscarla en `sources/regulation-cne-normas-tecnicas/`.
- Faltan posibles **actualizaciones posteriores a octubre 2022** (el sector tipicamente revisa el estandar cada 2-3 anos).
- No esta capturada la **Politica de Ciberseguridad** general de la CNE / Ministerio de Energia.

## 5. Para profundizar

- Servicios complementarios y obligaciones de Coordinados → `wiki/servicios-complementarios-y-transferencias.md`
- Vision general del rol del CEN → `wiki/mercado-mayorista-chile.md`
