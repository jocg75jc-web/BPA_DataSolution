# BPA DataCentric — Framework E2E de Información Operacional
### Visión Ejecutiva para Dirección · Versión 1.1 · Junio 2026

---

## Tabla de Contenidos

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [El problema que resuelve](#2-el-problema-que-resuelve)
3. [Visión del framework](#3-visión-del-framework)
4. [Arquitectura por capas](#4-arquitectura-por-capas)
5. [La Wiki de Indicadores — De catálogo a motor generador de KPIs](#5-la-wiki-de-indicadores--de-catálogo-a-motor-generador-de-kpis)
6. [La Historia de Usuario como entrada del proceso](#6-la-historia-de-usuario-como-entrada-del-proceso)
7. [Capa 1 — Adquisición de datos](#7-capa-1--adquisición-de-datos)
8. [Capa 2 — Procesamiento y almacenamiento](#8-capa-2--procesamiento-y-almacenamiento)
9. [Capa 3 — Observabilidad y monitoreo](#9-capa-3--observabilidad-y-monitoreo)
10. [Capa 4 — Presentación en dashboard](#10-capa-4--presentación-en-dashboard)
11. [Capa 5 — Gobierno de datos](#11-capa-5--gobierno-de-datos)
12. [Casos de uso reales: los procesos piloto](#12-casos-de-uso-reales-los-procesos-piloto)
13. [Modelo de madurez de reutilización](#13-modelo-de-madurez-de-reutilización)
14. [Ciclo de vida de un nuevo proceso](#14-ciclo-de-vida-de-un-nuevo-proceso)
15. [Stack tecnológico y modelo de despliegue](#15-stack-tecnológico-y-modelo-de-despliegue)
16. [Métricas de éxito del framework](#16-métricas-de-éxito-del-framework)
17. [Hoja de ruta](#17-hoja-de-ruta)
18. [Glosario rápido](#18-glosario-rápido)

---

## 1. Resumen ejecutivo

**BPA DataCentric** es una plataforma de datos operacionales que permite a la organización convertir información dispersa en fuentes heterogéneas (bases de datos, APIs, archivos) en **indicadores accionables visibles en dashboard**, de forma automatizada, trazable, gobernada y escalable.

El framework cubre el ciclo completo de información:

```
Solicitud de negocio (Historia de Usuario)
        ↓
Adquisición automática de datos
        ↓
Procesamiento y publicación en nube
        ↓
Monitoreo operativo + salud del dato (observabilidad)
        ↓
Dashboard de KPIs para consumo directivo y operativo
        ↓
Medición de adopción y valor entregado (cierre del ciclo)
```

**Propuesta de valor central:**
> Un equipo de negocio puede solicitar un nuevo indicador operacional. En menos de 2 días hábiles, ese indicador está disponible en un dashboard actualizado automáticamente, gobernado y con calidad de dato verificada, sin necesidad de desarrollar código desde cero cuando el origen y los KPIs ya están soportados.

**Qué cambió en la versión 1.1:** esta revisión incorpora tres ejes que elevan el framework de *pipeline de extracción + visualización* a *plataforma de datos*: (1) **gobierno de datos** como capa de primera clase, (2) **observabilidad del dato y del consumo** —no solo de la ejecución—, y (3) **generación de KPIs por configuración** a partir de una Wiki de Indicadores ejecutable. Además, racionaliza el patrón multi-stack hacia un **stack canónico de producción** y reconoce explícitamente el modelo de despliegue actual y su evolución hacia un orquestador portable.

---

## 2. El problema que resuelve

### Antes del framework

| Problema | Impacto |
|---|---|
| Cada proceso de datos se construía de forma independiente, sin estándar | Alto costo de mantenimiento y duplicidad de lógica |
| No había visibilidad de si los procesos se ejecutaban correctamente | Fallos silenciosos, datos desactualizados sin aviso |
| Agregar un nuevo proceso requería desarrollo desde cero | Tiempo de entrega largo, alto riesgo de error |
| Las áreas de negocio no tenían forma de consumir KPIs actualizados en tiempo real | Decisiones basadas en información manual y desactualizada |
| Los indicadores se calculaban en hojas de cálculo o reportes estáticos | Sin trazabilidad, sin historial, sin alertas |
| No había forma de saber quién consumía qué dato ni de dónde venía cada KPI | Sin linaje, sin control de acceso, sin gobierno |

### Después del framework

| Capacidad | Beneficio |
|---|---|
| Motor unificado de extracción configurable | Un nuevo proceso = una nueva entrada en configuración, no código nuevo |
| Monitor de ejecuciones con logs en tiempo real | Visibilidad total del estado de cada proceso, con historial |
| Validación de salud del dato post-publicación | Se detecta un output incompleto o anómalo antes de que rompa el dashboard |
| Publicación automática en Azure Blob Storage | Los datos están disponibles para cualquier consumidor autorizado |
| Dashboards con actualización automática | KPIs frescos, disponibles para operación y dirección |
| Plantilla estándar de solicitud (Historia de Usuario) | Solicitudes completas desde el primer intento, sin idas y vueltas |
| Wiki de Indicadores ejecutable | Los KPIs estándar se calculan por configuración, no se reprograman |
| Capa de gobierno (linaje, acceso, versionado) | Cada KPI es trazable a su origen y su acceso está controlado |

---

## 3. Visión del framework

### Principio rector

> **"De la necesidad de negocio al indicador visible, en el menor tiempo posible, con la mayor confiabilidad y gobierno posibles — y con evidencia de que se usa."**

El framework está diseñado sobre cinco premisas no negociables:

1. **Configuración primero, código por excepción**: agregar un proceso no debe requerir desarrollar un extractor nuevo si el origen ya está soportado, ni reprogramar un KPI si ya existe en la Wiki de Indicadores. El código se reserva para lo genuinamente nuevo (un origen no soportado, un KPI no catalogado).
2. **Observabilidad de extremo a extremo**: todo proceso tiene logs, historial y estado visible desde el primer día — y además se observa la **salud del dato** producido y la **disponibilidad del consumo** (el dashboard), no solo si el job corrió.
3. **Continuidad operativa**: los procesos programados no se interrumpen ante cambios, actualizaciones o incidentes transitorios.
4. **Presentación como ciudadana de primera clase**: todo proceso que extrae datos debe tener una capa de visualización definida desde su solicitud.
5. **Gobierno y valor desde el diseño**: cada dato tiene linaje conocido, acceso controlado y un contrato versionado; y cada KPI entregado tiene un consumidor real cuya adopción se mide.

### El flujo en una imagen

```
┌─────────────────────────────────────────────────────────────────────┐
│                      BPA DataCentric Framework                       │
│                                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────────┐  │
│  │  ORIGEN  │    │  MOTOR   │    │  NUBE    │    │  DASHBOARD   │  │
│  │          │    │UNIFICADO │    │          │    │ (canónico +  │  │
│  │ Base de  │───▶│          │───▶│  Azure   │───▶│  generado)   │  │
│  │  datos   │    │ Config   │    │   Blob   │    │              │  │
│  │  APIs    │    │ Extraer  │    │ Storage  │    │  KPIs Wiki   │  │
│  │ Archivos │    │ Validar  │    │          │    │              │  │
│  └──────────┘    │ Publicar │    └──────────┘    └──────────────┘  │
│                  └──────────┘                                        │
│                       │                                              │
│         ┌─────────────┴─────────────┐                               │
│         ▼                           ▼                               │
│  ┌─────────────────┐        ┌─────────────────┐                    │
│  │ PROCESS MONITOR │        │   GOBIERNO DE   │                    │
│  │ (Observabilidad)│        │     DATOS       │                    │
│  │ Ejecución·Dato  │        │ Linaje·Acceso   │                    │
│  │ ·Consumo·Alertas│        │ Contratos·Catál.│                    │
│  └─────────────────┘        └─────────────────┘                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Arquitectura por capas

El framework está estructurado en **cuatro capas funcionales** más **dos capas transversales** (observabilidad y gobierno):

```
┌────────────────────────────────────────────────────────────┐
│  CAPA 4 — PRESENTACIÓN                                      │
│  Dashboard canónico (generado por composición)             │
│  KPIs · Tendencias · SLA · Alertas visuales                │
├────────────────────────────────────────────────────────────┤
│  CAPA 3 — ALMACENAMIENTO / PUBLICACIÓN                      │
│  Azure Blob Storage · Archivos CSV / JSON                  │
│  Contratos de datos · Frescura garantizada                 │
├────────────────────────────────────────────────────────────┤
│  CAPA 2 — MOTOR UNIFICADO DE EXTRACCIÓN                     │
│  ExecutionEngine · ExtractorRegistry · ConfigLoader        │
│  ParameterValidator · RuntimeEnvValidator                  │
├────────────────────────────────────────────────────────────┤
│  CAPA 1 — FUENTES DE DATOS                                  │
│  PostgreSQL · SQL Server · APIs · Archivos                 │
│  Proceso A · Proceso B · (futuras fuentes)                 │
├────────────────────────────────────────────────────────────┤
│  TRANSVERSAL A — OBSERVABILIDAD                             │
│  ProcessMonitor · Salud de ejecución / dato / consumo      │
│  Logs · Estado · Historial · Drift · Alertas               │
├────────────────────────────────────────────────────────────┤
│  TRANSVERSAL B — GOBIERNO DE DATOS                          │
│  Linaje · Control de acceso · Versionado de contratos      │
│  Catálogo · Retención                                      │
└────────────────────────────────────────────────────────────┘
```

Cada capa tiene responsabilidades bien definidas y puede evolucionar de forma independiente. Agregar un nuevo origen de datos solo afecta la Capa 1. Agregar un nuevo tipo de visualización solo afecta la Capa 4. Las capas transversales aplican a **todos** los procesos sin excepción.

---

## 5. La Wiki de Indicadores — De catálogo a motor generador de KPIs

### Por qué construir una wiki de indicadores

Uno de los problemas más comunes al construir dashboards es que el equipo técnico puede extraer y procesar datos correctamente, pero no siempre sabe qué indicadores son relevantes para el área de negocio. Y el área de negocio puede saber qué necesita medir, pero no cómo formularlo en términos técnicamente precisos.

Para cerrar este gap de forma sistemática, el framework BPA DataCentric incluye una **wiki de indicadores operacionales de industria** como componente activo del proceso de análisis y diseño de dashboards. La wiki no es documentación de referencia pasiva: es una herramienta de trabajo que el equipo consulta activamente cada vez que analiza un nuevo dataset — y, en su estado objetivo, es el **motor que genera el cálculo del KPI por configuración**.

### Qué es la Wiki de Indicadores

Es un repositorio estructurado de definiciones estándar de indicadores, organizado por categorías, que cubre tanto indicadores propios del negocio como indicadores ampliamente utilizados en la industria.

**Cobertura actual: 41 indicadores en 7 categorías**

| Categoría | Indicadores propios | Indicadores de industria | Total |
|---|---|---|---|
| KPIs — Rendimiento y desempeño | 2 | 12 | 14 |
| SLAs — Nivel de servicio | 2 | 2 | 4 |
| MCIs — Indicadores críticos de misión | 2 | 0 | 2 |
| Volumetría | 2 | 3 | 5 |
| Observabilidad técnica | 2 | 3 | 5 |
| Impacto de negocio | 2 | 2 | 4 |
| Calidad de datos (ISO 8000 / DAMA) | 2 | 5 | 7 |
| **Total** | **14** | **27** | **41** |

Cada indicador en la wiki documenta: nombre, definición precisa, fórmula de cálculo, unidad de medida, umbrales sugeridos (alerta / objetivo / crítico), fuentes de datos típicas y estándar de referencia cuando aplica.

### Estándares de industria cubiertos

Los indicadores cubiertos pertenecen a dominios de alta relevancia para operaciones de servicio:

- **Contact Center** — FCR (First Contact Resolution), AHT (Average Handle Time), ASA (Average Speed of Answer), Tasa de Abandono, NPS, CSAT, CES (referencia: COPC / ICMI).
- **ITSM / Ticketing** — MTTR (Mean Time To Resolve), Backlog de Tickets, Tasa de Reapertura, SLA Compliance Rate (referencia: ITIL v4).
- **Calidad de Datos** — Completitud, Precisión, Oportunidad (Timeliness), Consistencia, Unicidad, No Conformidades, Eficiencia de Reprocesos (referencia: ISO 8000 / DAMA DMBOK).
- **Observabilidad técnica** — Latencia de extracción, Tasa de errores, MTTD (Mean Time To Detect), Throughput de procesamiento.
- **Impacto de negocio** — ROI de automatización, Costo por transacción, Customer Lifetime Value.

### El salto conceptual: de catálogo de referencia a motor ejecutable

La wiki es el activo más diferenciador del framework, pero hoy se usa principalmente como **referencia de consulta**. Su potencial real es ser el **núcleo generativo** que materializa la promesa de "configuración primero". El framework define tres niveles de madurez para la wiki:

| Nivel | Estado de la wiki | Qué significa en la práctica |
|---|---|---|
| **N1 — Catálogo** | Definiciones + fórmulas en texto | El equipo consulta la wiki y **programa a mano** el cálculo en `dataProcessor` |
| **N2 — Catálogo ejecutable** | Cada indicador es una función parametrizable con `inputs` (campos requeridos) y `output` (cálculo) | El cálculo del KPI **se invoca por configuración**; el `dataProcessor` deja de escribirse a mano para KPIs catalogados |
| **N3 — Motor de recomendación** | La wiki conoce el contrato de datos y propone KPIs | Dado el contrato de un proceso nuevo, la wiki **sugiere automáticamente** qué KPIs son calculables con los campos disponibles |

**Estado objetivo:** llevar la wiki a **N2 como mínimo** para todos los indicadores de industria, de modo que un proceso cuyo contrato de datos exponga los campos requeridos obtenga sus KPIs **sin escribir código de cálculo**. El N3 automatiza el paso 3 del análisis de contenido (hoy manual).

### Especificación de un indicador ejecutable (N2)

Cada indicador catalogado expone una firma estándar que el motor puede invocar:

```
INDICADOR: SLA Compliance Rate (ITIL v4)
  inputs:
    - fecha_apertura   : datetime  (requerido)
    - fecha_cierre     : datetime  (requerido)
    - sla_objetivo_hrs : number    (requerido, default 24)
  output:
    - valor   : porcentaje de casos cerrados dentro del SLA objetivo
    - unidad  : "%"
  umbrales:
    - objetivo : >= 97
    - alerta   : 90–97
    - critico  : < 90
  referencia: ITIL v4 — Service Level Management
```

Un proceso cuyo contrato de datos exponga `fecha_apertura` y `fecha_cierre` obtiene este KPI **mapeando campos**, no reprogramando la fórmula. Esto garantiza además que el mismo indicador se calcule idéntico en todos los procesos.

### Cómo se usa la wiki en el proceso de análisis de contenido

Cuando llega un nuevo dataset al framework, el equipo realiza un **análisis de contenido estructurado** antes de definir los KPIs del dashboard. La wiki es el catálogo de referencia — y, en N3, el motor de recomendación — en ese proceso:

```
ANÁLISIS DE CONTENIDO DEL DATASET
          ↓
1. Inventario de campos disponibles
   (fechas, categorías, métricas, identificadores)
          ↓
2. Clasificación por dominio operacional
   (¿contact center? ¿operaciones? ¿ITSM? ¿calidad de datos?)
          ↓
3. Cruce con la Wiki de Indicadores
   — [N1/N2] manual: ¿qué KPIs pueden calcularse con estos campos?
   — [N3] automático: la wiki propone los KPIs calculables
          ↓
4. Propuesta de KPIs sugeridos y justificados con evidencia
          ↓
5. Validación con el área solicitante
          ↓
6. Definición final en la Historia de Usuario (Nivel 2 — Presentación)
```

Este flujo garantiza que los KPIs del dashboard no son una elección arbitraria, sino una **selección fundamentada en estándares de industria** y validada contra los datos disponibles. El área de negocio recibe propuestas informadas, no preguntas abiertas sobre qué quieren ver.

### Beneficios concretos de este enfoque

| Beneficio | Sin wiki | Con wiki (N1) | Con wiki ejecutable (N2/N3) |
|---|---|---|---|
| Tiempo para proponer KPIs | Investigación desde cero | Catálogo consultable | Propuesta automática por contrato |
| Cálculo del KPI | Código a medida por proceso | Código guiado por la definición | Invocación por configuración |
| Consistencia de definiciones | Cada proceso calcula distinto | Fórmulas unificadas en texto | Fórmula única ejecutada idéntica |
| Alineación con estándares | Conocimiento individual | Referencia explícita (ISO/ITIL/COPC/DAMA) | Referencia embebida en el cálculo |
| Calidad de datos | Omitida o parcial | Categoría dedicada | Validada en el contrato de entrada |

---

## 6. La Historia de Usuario como entrada del proceso

### Por qué la Historia de Usuario es el punto de entrada

En el framework BPA DataCentric, **ningún proceso se construye sin una Historia de Usuario aprobada**. Este requisito no es burocrático: es el mecanismo que garantiza que la información extraída tenga un consumidor real, un objetivo medible y una capa de presentación definida.

Una solicitud incompleta genera procesos "huérfanos": datos que se extraen y almacenan pero que nadie consume, y que nadie sabe si están correctos.

### Anatomía de la Historia de Usuario en este framework

La Historia de Usuario en BPA DataCentric tiene **tres niveles complementarios**: extracción, presentación y —nuevo en v1.1— adopción/resultado.

#### Nivel 1 — El proceso de extracción

```
Como [rol solicitante]
quiero [proceso de extracción / generación / descarga de datos]
para [objetivo de negocio medible con criterio de éxito claro].

Criterio de aceptación:
- Los datos se actualizan cada [frecuencia] con un retraso máximo de [SLA].
- El archivo/JSON resultante refleja [ventana de datos esperada].
- El proceso notifica si falla en los primeros [N] minutos.
```

#### Nivel 2 — La capa de presentación (obligatorio)

```
Como [rol consumidor: gerente / analista / operador]
quiero [visualizar indicadores y tendencias del proceso en dashboard]
para [tomar decisiones / detectar desvíos / presentar resultados]
con una latencia máxima de [N horas/minutos desde la última ejecución].

KPIs mínimos requeridos:
- Volumen: total de registros procesados por corrida.
- Confiabilidad: tasa de éxito/fallo del proceso en el período.
- Cumplimiento SLA: % de ejecuciones dentro del tiempo objetivo.
- [KPIs específicos de negocio, seleccionados desde la Wiki de Indicadores].

SLA de visualización:
- Los datos del dashboard deben tener una antigüedad máxima de [N horas].
- El dashboard debe estar disponible en [URL/puerto] con tiempo de carga < [N segundos].
```

#### Nivel 3 — Adopción y resultado (evaluado a 30 días)

```
Como responsable del valor entregado,
quiero verificar que el indicador se usa y habilita decisiones,
para mantener, ajustar o retirar el proceso según su valor real.

Criterios de adopción:
- Decisión habilitada: [qué decisión / acción concreta apoya este KPI].
- Consumo: [N] consultas/usuarios distintos en los primeros 30 días.
- Evidencia de uso: el dashboard registra accesos (no es un dato huérfano).
- Veredicto a 30 días: MANTENER · AJUSTAR · RETIRAR.
```

### Por qué cada nivel es obligatorio

**Sin el Nivel 2** definido desde el inicio:
- El proceso produce datos que nadie visualiza de forma sistemática.
- No hay forma de saber si el SLA se cumple desde el punto de vista del consumidor.
- Los KPIs se descubren a posteriori, generando retrabajo en el dashboard.

**Sin el Nivel 3** definido desde el inicio:
- El framework previene crear procesos huérfanos, pero no detecta los que **mueren de uso**.
- No existe métrica de valor entregado, solo de ejecución técnica.
- Los recursos se consumen indefinidamente en procesos que ya nadie consulta.

**Con los tres niveles definidos**, el equipo técnico sabe exactamente qué construir, el consumidor tiene un SLA explícito, y la dirección obtiene evidencia de adopción que permite decidir el ciclo de vida del proceso.

### Ejemplo completo: Historia de Usuario bien formulada

```
HISTORIA DE USUARIO — HU-[AÑO]-[NNN]
Proceso: Indicadores operacionales — [Nombre del sistema / área]

Nivel 1 (Extracción):
Como responsable de [área u operación],
quiero un proceso automático que descargue [tipo de registros]
del sistema [fuente] cada [N] horas,
para disponer de datos actualizados para análisis operacional.

Criterio de aceptación técnico:
- Archivos CSV disponibles en almacenamiento con antigüedad < [N] horas.
- Volumen esperado: ~[N] registros principales + [N] complementarios por corrida.
- Proceso notifica fallo si no completa en [N] minutos.
- Lock de concurrencia activo para evitar solapamiento.

Nivel 2 (Presentación):
Como [gerente / analista] del área de [nombre del área],
quiero un dashboard que muestre los indicadores clave de [dominio operacional],
para identificar [tendencias / desvíos / cumplimiento] en tiempo casi real.

KPIs requeridos (seleccionados desde la Wiki de Indicadores):
- [KPI de volumen] — total de registros procesados en el período.
- [KPI de rendimiento] — tasa de resolución / cumplimiento en primer intento.
- [KPI de SLA] — porcentaje de casos atendidos dentro del tiempo acordado.
- [KPI de calidad] — tasa de error / no conformidad operacional.
- [KPI de tendencia] — evolución mensual del indicador principal.

SLA de visualización:
- Dashboard actualizado cada vez que el proceso de extracción completa.
- Disponible en el stack canónico de producción.
- Tiempo de carga < [N] segundos en red interna.

Nivel 3 (Adopción — revisión a 30 días):
- Decisión que habilita: [ej. reasignar carga entre grupos de operación].
- Meta de consumo: ≥ [N] usuarios distintos / [N] consultas en 30 días.
- Veredicto previsto de revisión: MANTENER / AJUSTAR / RETIRAR.
```

---

## 7. Capa 1 — Adquisición de datos

### Qué hace esta capa

Conecta con las fuentes de datos de la organización y extrae la información según las reglas definidas en la configuración del proceso. Esta capa es responsable de:

- Establecer conexión con la fuente (BD, API, archivo).
- Ejecutar la consulta o lógica de extracción.
- Validar el resultado (volumen mínimo, frescura, completitud).
- Generar el archivo de salida en el formato acordado.
- Registrar evidencia de la extracción (log, timestamp, tamaño) **y su linaje** (qué query/tabla origen produjo el archivo).

### Fuentes soportadas actualmente

| Fuente | Tipo | Protocolo | Estado |
|---|---|---|---|
| Proceso A — Analytics conversacional (PostgreSQL) | Base de datos relacional | psycopg3 | ✅ Activo |
| Proceso B — Operaciones de atención (PostgreSQL) | Base de datos relacional | psycopg3 | ✅ Activo |
| (futuras fuentes) | SQL Server / MySQL / API REST | por configuración | 🔲 Pendiente |

### Cómo se agrega una nueva fuente

1. Crear un extractor (`BaseExtractor`) con la lógica de conexión y extracción.
2. Registrarlo en el `ExtractorRegistry`.
3. Definir el proceso en `processes.json` con sus parámetros.
4. No se modifica ningún otro componente del framework.

### Garantías operativas de esta capa

- **Anti-solapamiento**: lock de concurrencia por proceso. No pueden ejecutarse dos instancias simultáneas del mismo proceso.
- **Validación de frescura**: después de extraer, se verifica que el archivo resultante tenga un tamaño y timestamp esperados.
- **Rutas absolutas**: todos los paths son explícitos para evitar dependencias del directorio de trabajo.
- **Salida prematura detectada**: si el proceso termina con código 0 pero sin el marcador de éxito esperado, se clasifica como fallo.
- **Registro de linaje**: cada extracción registra el origen exacto (query/tabla/endpoint) que la generó, alimentando la Capa 5 — Gobierno.

---

## 8. Capa 2 — Procesamiento y almacenamiento

### Qué hace esta capa

Una vez que el extractor genera el archivo de salida, esta capa se encarga de:

- Validar el archivo generado (tamaño, estructura, completitud).
- **Verificar el contrato de datos** (schema y campos clave presentes) antes de publicar.
- Mover o copiar el archivo al destino de almacenamiento en nube.
- Registrar la evidencia de publicación (timestamp remoto, tamaño en Blob).
- Generar artefactos de pre-agregación cuando el volumen lo requiere.

### Almacenamiento actual

**Azure Blob Storage** es el destino primario:

| Proceso | Contenedor | Archivos |
|---|---|---|
| Proceso A | `[contenedor] / [directorio]` | N archivos CSV (vistas SQL del sistema origen) |
| Proceso B | `[contenedor] / [directorio]` | N archivos CSV (registros principales + complementarios) |
| Proceso B (pre-agregado) | `[contenedor] / [directorio]` | `[proceso]_summary.json` (KPIs calculados) |

### Pre-agregación para dashboards de alto volumen

Cuando el volumen de datos es alto (ej. millones de transacciones en procesos de operaciones), el framework genera un **JSON pre-agregado** (`[proceso]_summary.json`) que concentra los KPIs calculados. Los dashboards consumen este JSON en lugar del CSV crudo, logrando:

- Tiempo de carga del dashboard < 1 segundo (vs. parsear archivos CSV de cientos de MB).
- Cálculos consistentes en el dashboard (no hay divergencia por lógica duplicada).
- Un único punto de actualización: regenerar el JSON cada vez que el CSV se actualiza.

> **Nota de diseño:** el JSON pre-agregado debe cumplir el mismo **contrato de datos versionado** que el resto de artefactos. Un summary con campos faltantes (p. ej. sin `operationalSummary`) es un fallo de contrato y debe detectarse en la validación de salud del dato (Capa 3), **no** descubrirse cuando el dashboard se rompe.

### Contrato de datos

Cada proceso define un **contrato de datos** explícito: los campos que garantiza producir, su tipo, y los criterios de calidad mínimos. Este contrato es el puente entre la capa de extracción y la capa de presentación, y está **versionado** en la Capa 5 (ver gobierno de contratos).

---

## 9. Capa 3 — Observabilidad y monitoreo

### Qué hace esta capa

El **ProcessMonitor** es la interfaz de control de toda la plataforma. La observabilidad del framework abarca **tres niveles**, no solo la ejecución del job:

```
Nivel 1 — SALUD DE EJECUCIÓN   →  ¿corrió el proceso? ✅
Nivel 2 — SALUD DEL DATO       →  ¿el output cumple el contrato? ¿hay drift?
Nivel 3 — SALUD DEL CONSUMO    →  ¿el dashboard carga con datos frescos?
```

El framework parte de una observabilidad de ejecución madura y la extiende hacia la **salud del dato** y la **salud del consumo**, porque la mayoría de los incidentes reales (un summary incompleto, un CSV faltante) producen un `exit 0` engañoso: el proceso "corrió bien" pero el dashboard queda inservible.

### Nivel 1 — Salud de ejecución

Permite a operadores y administradores:

- Ver el estado en tiempo real de todos los procesos registrados.
- Ejecutar procesos manualmente con un clic.
- Ver logs de ejecución en tiempo real (WebSocket).
- Consultar el historial de ejecuciones con estado y duración.
- Analizar tendencias de éxito/fallo por proceso y período.
- Ver la próxima ejecución programada de cada proceso.
- Arrancar y monitorear el dashboard de presentación.

### Nivel 2 — Salud del dato (Data Health)

Complementa "¿corrió?" con "¿el dato es correcto?":

| Verificación | Qué detecta |
|---|---|
| **Validación de contrato post-publicación** | El artefacto publicado tiene el schema esperado y todos los campos clave presentes (no solo tamaño/timestamp). |
| **Detección de drift** | El volumen o un KPI se desvía más de X% respecto de la media histórica → alerta de anomalía. |
| **Frescura por consumidor** | La antigüedad del dato publicado respecto del SLA de visualización declarado en la HU. |

### Nivel 3 — Salud del consumo (synthetic check)

Un **chequeo sintético** carga periódicamente el dashboard y verifica que:

- Responde HTTP 200 en el tiempo de carga objetivo.
- Renderiza los KPIs con datos cuya antigüedad cumple el SLA.
- No cae en estados de error de datos ("datos parciales", "no fue posible leer el archivo").

> Este chequeo habría atrapado el incidente de "datos parciales" **antes** que el usuario final, cerrando la brecha entre "el proceso corrió" y "el indicador es visible".

### Componentes técnicos

| Componente | Tecnología | Puerto | Función |
|---|---|---|---|
| Backend API | Flask + Socket.IO | 5052 | Motor de monitoreo, REST + WebSocket |
| Frontend | React + MUI | 5173 | Dashboard de control |

### Secciones del monitor

| Sección | Descripción |
|---|---|
| **Procesos** | Vista de todas las fuentes registradas con botón de ejecución manual |
| **Historial** | Registro histórico de todas las ejecuciones con estado y duración |
| **Próximas ejecuciones** | Calendario de próximas corridas según cron configurado |
| **Logs en vivo** | Stream en tiempo real de los logs de la ejecución activa |
| **Salud del dato** | Resultado de validación de contrato y detección de drift por proceso |
| **Salud del consumo** | Estado de los chequeos sintéticos de dashboard |
| **Analytics** | Gráficos de tendencias de éxito/fallo y duración por proceso |
| **Dashboards** | Control de arranque del dashboard de presentación |

### Scheduler y automatización

Los procesos se ejecutan automáticamente mediante el **scheduler del entorno** (hoy Windows Task Scheduler):

| Proceso | Frecuencia | Estado |
|---|---|---|
| Proceso A | Cada 2 horas | ✅ Activo |
| Proceso B | Cada 4 horas | ✅ Activo |

El ProcessMonitor también puede lanzar ejecuciones ad-hoc desde su interfaz sin intervención en el scheduler. La evolución del scheduler hacia un orquestador portable se describe en la sección 15.

---

## 10. Capa 4 — Presentación en dashboard

### Filosofía de presentación

La capa de presentación no es un extra: es la **razón de ser** de todo el pipeline anterior. Un proceso de datos sin una capa de presentación accionable es un proceso incompleto.

En BPA DataCentric, **cada proceso tiene al menos un dashboard** que materializa los KPIs definidos en la Historia de Usuario.

### De "tres stacks por proceso" a "un stack canónico generado"

Durante la fase piloto, el framework construyó cada dashboard en **tres tecnologías** (React+MUI, React+Tailwind, SvelteKit+ECharts) con un objetivo legítimo: **evaluar stacks** comparando experiencia de usuario, rendimiento y mantenibilidad. Esa evaluación ya cumplió su propósito.

Mantener tres implementaciones por proceso de forma permanente, sin embargo, **multiplica el costo de la capa más crítica** y contradice la meta de "2 días por proceso" y "reuso > 80%": con 2 procesos son 6 dashboards; con 20 procesos serían 60. Por eso el framework separa explícitamente dos fases:

| Fase | Propósito | Estado |
|---|---|---|
| **Evaluación de stack** | Comparar tecnologías con implementaciones reales | ✅ Completada con los pilotos |
| **Producción** | **Un único stack canónico** + **dashboard generado por composición** a partir del contrato de datos y los KPIs de la Wiki | 🔲 En adopción |

**Decisión de diseño v1.1:**
- Se designa **un stack canónico de producción** (selección entre los tres evaluados según rendimiento, mantenibilidad y bundle).
- Las otras dos implementaciones se **congelan como referencia** (no se mantienen por proceso nuevo).
- Los procesos nuevos obtienen su dashboard mediante un **generador por composición**: dado el contrato de datos y los KPIs de la wiki, se ensambla el dashboard sin reescribir lógica a mano.

### El dashboard generado por composición

```
Contrato de datos del proceso
        +
KPIs seleccionados desde la Wiki (N2 — ejecutables)
        ↓
GENERADOR DE DASHBOARD (stack canónico)
        ↓
Dashboard de producción ensamblado
(tarjetas de KPI · tendencias · tablas · alertas)
```

El concepto ganador es **un dashboard compuesto por configuración**, no múltiples dashboards mantenidos a mano. Esto convierte la capa de presentación en la beneficiaria directa de la Wiki ejecutable (sección 5).

### Servicios compartidos del stack canónico

Para garantizar consistencia, el stack canónico comparte un conjunto único de servicios:

| Servicio | Función |
|---|---|
| `blobService` | Lectura desde Azure Blob Storage con fallback local y manejo de CORS |
| `dataProcessor` | Transformación de CSV/JSON crudo → métricas; usa los KPIs ejecutables de la Wiki |
| `useProcessData` / store | Hook/store de datos con auto-refresh y estado de carga |
| `[proceso]-core/types` | Tipos compartidos (contrato de datos versionado) |

### KPIs implementados por proceso

#### Proceso A — Analytics de conversaciones del asistente virtual

| KPI | Descripción | Target |
|---|---|---|
| Total Conversaciones | Volumen total en el período | — |
| Usuarios Únicos | Personas distintas que interactuaron | — |
| Promedio Diario | Conversaciones por día | — |
| Tiempo Prom. Manejo | Duración media de conversación (min) | — |
| % B2C / % B2B | Distribución por segmento de cliente | — |
| Conv. / Usuario | Intensidad de uso por persona | — |

#### Proceso B — Operaciones de atención

| KPI | Descripción | Target |
|---|---|---|
| Tasa Primer Intento | % de órdenes resueltas sin reintento | > 80% |
| Sobresfuerzo por Reintento | % de órdenes que requirieron más de 1 intento | < 20% |
| SLA Cumplimiento 24h | % de casos atendidos en ≤ 24 horas | > 97% |
| Tasa de Error Operacional | % de transacciones con error | < 10% |
| Distribución por Grupo | Carga por grupo de operación | — |
| Tendencia Mensual | Evolución de reintentos por mes y grupo | — |
| Top Errores | Errores más frecuentes por categoría | — |

### Actualización de dashboards

Los dashboards consumen datos de forma automática:

```
Scheduler (cada 2h / 4h)
    → Extracción CSV
    → Validación de contrato + publicación en Azure Blob
    → Regeneración JSON pre-agregado (+ upload a Blob)
    → Chequeo sintético de dashboard (salud del consumo)
    → Dashboard recarga automáticamente en próxima visita
```

---

## 11. Capa 5 — Gobierno de datos

### Por qué el gobierno es una capa de primera clase

Un framework que aspira a ser organizacional no puede tratar el gobierno como un añadido. Sin gobierno, un dashboard es un número sin trazabilidad: nadie sabe de dónde sale, quién puede verlo, ni qué pasa cuando su definición cambia. La Capa 5 hace explícito lo que antes era implícito.

### Componentes del gobierno

| Componente | Qué resuelve | Estado |
|---|---|---|
| **Linaje (lineage)** | De qué query/tabla/endpoint origen proviene cada KPI del dashboard, atravesando extracción → Blob → pre-agregado → dashboard | 🔲 A formalizar |
| **Control de acceso** | Quién puede consumir cada dato; reemplazo de tokens de URL embebidos (SAS) por un modelo de autorización por identidad | 🔲 A formalizar |
| **Versionado de contratos** | Qué versión del contrato produce cada proceso y cómo se gestionan los cambios incompatibles (breaking changes) | 🔲 A formalizar |
| **Catálogo de datos** | Inventario maestro consultable de procesos, contratos, KPIs y consumidores | 🔲 A formalizar |
| **Retención** | Cuánto tiempo se conserva cada artefacto y bajo qué política se purga | 🔲 A formalizar |

### Linaje: trazabilidad de extremo a extremo

Cada KPI visible debe poder rastrearse hasta su origen:

```
KPI en dashboard
   ↑ se calcula desde
Campo del contrato de datos (versión X)
   ↑ proviene de
Artefacto publicado en Blob (timestamp, tamaño)
   ↑ generado por
Query / tabla / endpoint origen (registrado en Capa 1)
```

Este encadenamiento responde, ante cualquier KPI: *"¿de dónde sale este número y cuándo se actualizó por última vez?"* — pregunta hoy difícil de contestar de forma sistemática.

### Control de acceso: del SAS embebido al acceso por identidad

El modelo actual de publicación apoya el acceso mediante **tokens SAS en la URL**, lo que implica que cualquiera con la URL accede al dato y que la rotación del token es un punto único de riesgo. El estado objetivo del gobierno es:

- **Acceso por identidad** (managed identity / RBAC) en lugar de tokens embebidos en clientes.
- **Principio de menor privilegio**: cada consumidor accede solo a los datos de su dominio.
- **Rotación gestionada** de credenciales sin tocar el código de los dashboards.

### Versionado de contratos: gestionar el cambio sin romper consumidores

Cuando el contrato de un proceso cambia (un campo se renombra, se agrega o se elimina), el framework debe distinguir:

| Tipo de cambio | Compatibilidad | Acción |
|---|---|---|
| Aditivo (campo nuevo opcional) | Compatible | Incrementar versión menor; consumidores no se afectan |
| Renombrado / eliminación / cambio de tipo | **Breaking** | Incrementar versión mayor; notificar consumidores; periodo de transición |

El contrato versionado es el mismo `types` compartido que consume el dashboard, de modo que un cambio incompatible es **visible y gestionado**, no una sorpresa en producción.

### Catálogo y retención

- **Catálogo:** inventario único donde cada proceso declara su origen, contrato, KPIs y consumidores — la fuente de verdad para auditar qué existe y quién lo usa.
- **Retención:** política explícita de cuánto se conservan CSVs crudos, pre-agregados e históricos, alineada con las necesidades de negocio y el costo de almacenamiento.

---

## 12. Casos de uso reales: los procesos piloto

Los dos procesos piloto del framework son sus **sujetos de prueba activos**. Su propósito no es solo operativo: cada uno valida un conjunto de patrones que luego quedan disponibles para reutilización en cualquier fuente nueva.

### Proceso A — Analytics de conversaciones del asistente virtual

| Aspecto | Detalle |
|---|---|
| **Qué extrae** | Vistas SQL de analytics de conversaciones e interacciones del asistente virtual |
| **Origen** | Base de datos relacional (PostgreSQL) en producción |
| **Frecuencia** | Cada 2 horas |
| **Archivos generados** | 6 archivos CSV (clasificación, historial, usuarios, segmentos, etc.) |
| **Destino** | Azure Blob Storage |
| **Dashboard** | Implementación de referencia en 3 stacks (evaluación) → stack canónico (producción) |
| **Patrón validado** | Extracción multi-query, credenciales por archivo, rutas absolutas |

### Proceso B — Operaciones de atención

| Aspecto | Detalle |
|---|---|
| **Qué extrae** | Transacciones de operaciones de atención + registros complementarios |
| **Origen** | Base de datos relacional (PostgreSQL) en producción, múltiples modelos de datos |
| **Frecuencia** | Cada 4 horas |
| **Archivos generados** | 2 CSVs (registros principales + complementarios) + 1 JSON pre-agregado |
| **Destino** | Azure Blob Storage |
| **Dashboard** | Implementación de referencia en 3 stacks (evaluación) → stack canónico (producción) |
| **Patrón validado** | Extracción de alto volumen, pre-agregación JSON, SLA de atención, segmentación por grupo operacional |

### Patrones validados por ambos procesos

Los siguientes patrones están probados en producción y disponibles para reutilización en cualquier nuevo proceso:

| Patrón | Dónde se usa |
|---|---|
| Lock anti-solapamiento con detección de PID huérfano | Proceso A + Proceso B |
| Validación de frescura y tamaño post-extracción | Proceso A + Proceso B |
| Validación de contrato de datos post-publicación | Proceso A + Proceso B |
| Bridge de ejecución estable (fallback transparente) | Proceso A + Proceso B |
| Proxy Vite para CORS con Azure Blob | Dashboards |
| Servicios de datos compartidos del stack canónico | Dashboards |
| JSON pre-agregado para dashboards de alto volumen | Proceso B |
| Hook de auto-refresh con estado de carga | Dashboards |
| Fallback local ante artefacto incompleto en Blob | Proceso B (dashboards ONNET) |

---

## 13. Modelo de madurez de reutilización

La promesa "configuración primero" no es binaria: depende de cuánto del proceso nuevo ya está soportado. El framework hace explícito un **modelo de madurez** que indica, para cada proceso, cuánto código real requiere — y orienta el esfuerzo hacia mover procesos a los niveles superiores.

| Nivel | Situación del proceso nuevo | Qué requiere | Esfuerzo |
|---|---|---|---|
| **Nivel 0** | Origen **no** soportado | Implementar `BaseExtractor` (código) + dataProcessor + KPIs | Alto |
| **Nivel 1** | Origen soportado, KPIs **no** catalogados | Solo dataProcessor + KPIs a medida (código ligero) | Medio |
| **Nivel 2** | Origen soportado, KPIs **en la Wiki (N2 ejecutable)** | **Solo configuración**: mapeo de campos a KPIs del catálogo | Mínimo |

**Meta del framework:** maximizar la proporción de procesos que se incorporan en **Nivel 2**. Cada origen que se promueve a "soportado" y cada KPI que se eleva a "ejecutable en la Wiki" empuja a los procesos futuros hacia el nivel de menor esfuerzo. Así, "configuración primero" deja de ser un eslogan y se vuelve una métrica medible (ver sección 16: *% de procesos incorporados en Nivel 2*).

---

## 14. Ciclo de vida de un nuevo proceso

Cuando un área de negocio necesita un nuevo indicador operacional, el ciclo en BPA DataCentric es el siguiente:

```
FASE 1 — SOLICITUD (Día 0)
├── Área completa la plantilla de Historia de Usuario (HU Nivel 1 + 2 + 3)
├── Se define: origen, frecuencia, SLA, KPIs del dashboard, metas de adopción
└── Se asigna responsable técnico y responsable funcional

FASE 2 — CONFIGURACIÓN (Día 1, ~2-4 horas)
├── Se determina el nivel de madurez del proceso (0 / 1 / 2)
│   ├── Nivel 2 → solo entrada en processes.json + mapeo de KPIs de la Wiki
│   ├── Nivel 1 → + dataProcessor a medida
│   └── Nivel 0 → + BaseExtractor para el nuevo origen
├── Se define y versiona el contrato de datos (types / JSON schema)
├── Se registra el linaje del proceso (origen → artefacto)
└── Se valida configuración con validate_config.py

FASE 3 — PRUEBA DE EXTRACCIÓN (Día 1, ~2-4 horas)
├── Ejecución manual desde ProcessMonitor
├── Verificación de archivo generado (tamaño, estructura, frescura)
├── Validación de contrato de datos (campos y tipos esperados)
└── Verificación de publicación en Blob + registro de linaje

FASE 4 — DASHBOARD (Día 2, ~2-6 horas)
├── Generación del dashboard por composición (stack canónico)
├── KPIs ensamblados desde la HU Nivel 2 / Wiki ejecutable
├── Chequeo sintético de salud del consumo
└── Validación visual con el solicitante

FASE 5 — CIERRE (Día 2, ~1 hora)
├── Registro del proceso en scheduler
├── Alta en el catálogo de datos (Capa 5)
├── Documentación de la HU aprobada
└── Gate E2E: evidencia de extracción + contrato válido + visualización correcta

FASE 6 — REVISIÓN DE ADOPCIÓN (Día +30)
├── Evaluación de HU Nivel 3 (consumo y decisiones habilitadas)
└── Veredicto: MANTENER / AJUSTAR / RETIRAR
```

**Tiempo total estimado: 2 días hábiles** para un proceso de **Nivel 1 o 2** (origen ya soportado). El Nivel 2 tiende al extremo inferior del rango gracias a la generación por composición y los KPIs ejecutables.

---

## 15. Stack tecnológico y modelo de despliegue

### Backend / Motor

| Componente | Tecnología | Versión |
|---|---|---|
| Motor de extracción | Python | 3.12 |
| API de monitoreo | Flask + Flask-SocketIO | 3.x |
| Conectores BD | psycopg3, pyodbc (futuro) | — |
| Almacenamiento nube | Azure SDK (azure-storage-blob) | 12.x |
| Scheduler (actual) | Windows Task Scheduler | — |

### Frontend / Dashboards

| Componente | Tecnología | Rol |
|---|---|---|
| Monitor de procesos | React 19 + MUI v9 | Interfaz de control |
| Stack canónico de producción | (seleccionado entre los evaluados) | Dashboard generado por composición |
| Implementaciones de referencia | React+MUI+Recharts · React+Tailwind+Chart.js · SvelteKit+ECharts | Congeladas (evaluación de stack) |
| Build / Dev server | Vite 5 | 5.x |
| Tipos compartidos | TypeScript 5 | 5.x |

### Modelo de despliegue: estado actual y visión

El framework reconoce explícitamente su modelo de despliegue actual y su evolución, para no confundir un puente con la arquitectura objetivo:

| Dimensión | Estado actual | Visión target |
|---|---|---|
| **Ejecución** | Single-node operacional (una máquina) | Despliegue portable y contenerizado |
| **Orquestación** | Windows Task Scheduler (atado al SO) | Orquestador de jobs portable (Airflow / Prefect / Dagster o equivalente Azure) |
| **Disponibilidad** | Recuperación manual (restart inmediato) | Alta disponibilidad real con reintentos y failover |
| **Entornos** | Entorno único | Separación dev / staging / prod |
| **Contenerización** | Base Docker definida | Docker Compose / orquestación 🔲 (requiere WSL2 + Docker Desktop) |

> **Por qué importa:** Windows Task Scheduler es un **puente válido** para la fase actual, pero impone un techo (atado al SO, sin HA, single-node). El concepto del framework admite explícitamente que la orquestación evolucionará hacia una plataforma portable; no es necesario migrar ya, pero la arquitectura no debe asumir el scheduler local como permanente.

### Infraestructura

| Componente | Tecnología | Estado |
|---|---|---|
| Almacenamiento primario | Azure Blob Storage | ✅ Activo |
| Contenerización | Docker (base definida) | 🔲 Pendiente WSL2/Docker install |
| Orquestación | Docker Compose → orquestador de jobs | 🔲 Pendiente |
| Acceso a datos | SAS token (actual) → identidad/RBAC (objetivo) | 🔲 A formalizar (Capa 5) |

---

## 16. Métricas de éxito del framework

### Métricas operativas (proceso)

| Métrica | Objetivo | Estado actual |
|---|---|---|
| Tasa de éxito de ejecuciones Proceso A | > 95% | ✅ Validado |
| Tasa de éxito de ejecuciones Proceso B | > 95% | ✅ Validado |
| Latencia máxima de datos en Blob | < 30 min post-ejecución | ✅ Validado |
| Detección de lock huérfano | Automática, sin intervención | ✅ Implementado |
| Falsos éxitos (exit 0 sin completar) | 0% | ✅ Prevenidos |

### Métricas de salud del dato (nuevas en v1.1)

| Métrica | Objetivo | Estado |
|---|---|---|
| Validación de contrato post-publicación | 100% de artefactos validados | 🔲 A implementar |
| Incidentes de contrato detectados antes del consumidor | 100% | 🔲 A implementar |
| Detección de drift de volumen / KPI | Alerta si desvío > umbral vs. histórico | 🔲 A implementar |
| Cobertura de chequeo sintético de dashboards | 100% de dashboards productivos | 🔲 A implementar |

### Métricas de framework (plataforma)

| Métrica | Objetivo | Estado actual |
|---|---|---|
| Tiempo de alta de nuevo proceso (origen soportado) | < 2 días hábiles | ✅ Validado con 2 procesos piloto |
| **% de procesos incorporados en Nivel 2 (solo config)** | Creciente trimestre a trimestre | 🔲 A medir |
| Reuso de componentes por nuevo proceso | > 80% | ✅ Servicios compartidos del stack canónico |
| Trazabilidad de ejecuciones | 100% | ✅ Logs + historial en monitor |
| **Cobertura de linaje (KPI → origen)** | 100% de KPIs productivos | 🔲 A formalizar (Capa 5) |
| Disponibilidad del monitor | > 99% en horario laboral | ✅ Restart inmediato disponible |

### Métricas de presentación (dashboard)

| Métrica | Objetivo | Estado actual |
|---|---|---|
| Tiempo de carga del dashboard | < 3 segundos | ✅ JSON pre-agregado |
| Antigüedad máxima de datos visualizados | ≤ frecuencia del proceso + 30 min | ✅ Validado |
| Consistencia de KPIs | Cálculo idéntico vía Wiki ejecutable | 🔲 En adopción (N2) |

### Métricas de adopción / valor (nuevas en v1.1)

| Métrica | Objetivo | Estado |
|---|---|---|
| Procesos con HU Nivel 3 definida | 100% de procesos nuevos | 🔲 A implementar |
| Adopción a 30 días (usuarios/consultas distintos) | Según meta declarada en la HU | 🔲 A medir |
| Procesos huérfanos retirados | Revisión y veredicto a 30 días | 🔲 A medir |

---

## 17. Hoja de ruta

### Completado ✅

- Motor unificado de extracción con configuración declarativa.
- Extractores de los 2 procesos piloto en producción.
- ProcessMonitor con API REST + WebSocket + analytics.
- Dashboards operativos en 3 stacks (fase de evaluación) por proceso piloto.
- Pre-agregación JSON para proceso de alto volumen (millones de registros → dashboard < 1s).
- Control de dashboards desde el monitor (arranque con un clic).
- Fallback local ante artefacto incompleto en Blob (resiliencia del dashboard).
- Documentación operativa completa.

### Próximos pasos 🔲

| Item | Prioridad | Descripción |
|---|---|---|
| Wiki ejecutable (N2) | **Muy alta** | Convertir los indicadores de industria en funciones parametrizables invocables por configuración |
| Stack canónico + dashboard generado | **Muy alta** | Designar el stack de producción, congelar los otros dos y generar dashboards por composición |
| Salud del dato (Data Health) | Alta | Validación de contrato post-publicación + detección de drift |
| Chequeo sintético de dashboards | Alta | Health-check E2E que verifique que el dashboard renderiza con datos frescos |
| Hook post-extracción | Alta | Regenerar el JSON pre-agregado automáticamente tras cada extracción del proceso de alto volumen |
| Upload JSON a Blob | Alta | Publicar el pre-agregado en Azure Blob para acceso desde cualquier cliente |
| Capa 5 — Gobierno (linaje + contratos) | Alta | Linaje KPI→origen y versionado de contratos de datos |
| Capa 5 — Acceso por identidad | Alta | Reemplazar SAS embebido por managed identity / RBAC |
| HU Nivel 3 — Adopción | Media | Plantilla y proceso de revisión de valor a 30 días |
| Orquestador portable | Media | Evaluar migración de Task Scheduler a orquestador de jobs |
| Docker / contenerización | Media | Despliegue del motor y monitor en contenedor (requiere WSL2 + Docker Desktop) |
| Soporte SQL Server | Media | Nuevo extractor para fuentes SQL Server |
| Webhook de alertas | Media | Notificación a Teams/Slack ante fallo de proceso o de salud del dato |
| Catálogo de datos | Media | Inventario maestro de procesos, contratos, KPIs y consumidores |
| Wiki N3 — Motor de recomendación | Baja | Sugerencia automática de KPIs calculables a partir del contrato de datos |
| Dashboard de calidad de datos | Baja | Métricas de completitud, unicidad y consistencia por proceso |

---

## 18. Glosario rápido

| Término | Definición |
|---|---|
| **Framework E2E** | Sistema que cubre el ciclo completo desde la adquisición de datos hasta su presentación visual y la medición de su adopción |
| **Motor unificado** | Componente central (`ExecutionEngine`) que orquesta la ejecución de cualquier proceso de extracción |
| **Extractor** | Módulo Python que implementa la lógica de conexión y extracción para una fuente específica |
| **Proceso** | Unidad de configuración que define una extracción: origen, parámetros, destino, schedule |
| **processes.json** | Archivo de configuración canónico donde se registran todos los procesos del framework |
| **Azure Blob Storage** | Servicio de almacenamiento en nube donde se publican los archivos generados |
| **ProcessMonitor** | Interfaz web de observabilidad y control del framework (backend Flask + frontend React) |
| **JSON pre-agregado** | Artefacto de datos calculados (`*_summary.json`) que concentra los KPIs para consumo eficiente en dashboard |
| **Historia de Usuario** | Plantilla estándar de solicitud de nuevo proceso, con tres niveles: extracción, presentación y adopción |
| **Contrato de datos** | Definición formal y **versionada** de los campos, tipos y garantías que produce un proceso |
| **Wiki de Indicadores** | Catálogo de indicadores de industria; en su estado objetivo, **motor ejecutable** que calcula KPIs por configuración |
| **Wiki ejecutable (N2)** | Indicador expresado como función parametrizable (`inputs`/`output`) invocable sin reprogramar la fórmula |
| **Modelo de madurez de reutilización** | Clasificación (Nivel 0/1/2) que indica cuánto código real requiere incorporar un proceso nuevo |
| **Salud del dato (Data Health)** | Observabilidad de que el artefacto cumple su contrato y no presenta drift, más allá de que el job corrió |
| **Chequeo sintético** | Health-check que carga el dashboard y verifica que renderiza con datos frescos (salud del consumo) |
| **Drift** | Desviación significativa de un KPI o del volumen respecto de su media histórica |
| **Gobierno de datos** | Capa transversal de linaje, control de acceso, versionado de contratos, catálogo y retención |
| **Linaje (lineage)** | Trazabilidad de un KPI hasta su query/tabla/endpoint origen, atravesando todas las capas |
| **Stack canónico** | Tecnología única designada para los dashboards de producción tras la fase de evaluación |
| **Dashboard generado por composición** | Dashboard ensamblado a partir del contrato de datos y los KPIs de la Wiki, sin reescribir lógica a mano |
| **Gate E2E** | Criterio de aceptación que valida el flujo completo: extracción → contrato válido → Blob → dashboard visible |
| **SLA de visualización** | Tiempo máximo aceptable entre la generación del dato y su disponibilidad en dashboard |
| **Lock anti-solapamiento** | Mecanismo que impide que dos instancias del mismo proceso corran simultáneamente |
| **Bridge** | Script de ejecución alternativo que garantiza estabilidad ante fallos en la ruta principal |
| **Single-node operacional** | Modelo de despliegue actual en una sola máquina; puente hacia un orquestador portable |

---

*Documento generado: 2026-06-02 · Actualizado a v1.1: 2026-06-04 · BPA DataCentric*
*Para actualización o consultas técnicas contactar al responsable del framework.*
