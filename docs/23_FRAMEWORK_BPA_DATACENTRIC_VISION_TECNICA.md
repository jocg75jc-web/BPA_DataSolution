# BPA DataCentric — Necesidades Agénticas, Arquitectura e Infraestructura
### Documento de Diseño · Versión 1.0 · Junio 2026

---

## Tabla de Contenidos

1. [Por qué agenticidad en este framework](#1-por-qué-agenticidad-en-este-framework)
2. [Mapa de gaps que los agentes resuelven](#2-mapa-de-gaps-que-los-agentes-resuelven)
3. [Los 6 agentes del sistema](#3-los-6-agentes-del-sistema)
   - [Agente 1 — HU Analyst](#agente-1--hu-analyst)
   - [Agente 2 — KPI Recommender (Wiki N3)](#agente-2--kpi-recommender-wiki-n3)
   - [Agente 3 — Dashboard Composer](#agente-3--dashboard-composer)
   - [Agente 4 — Data Health Monitor](#agente-4--data-health-monitor)
   - [Agente 5 — Lineage Tracker](#agente-5--lineage-tracker)
   - [Agente 6 — Onboarding Orchestrator](#agente-6--onboarding-orchestrator)
4. [Arquitectura del sistema multi-agente](#4-arquitectura-del-sistema-multi-agente)
5. [Capa MCP — Model Context Protocol servers](#5-capa-mcp--model-context-protocol-servers)
6. [Agent Workspace — Interfaz de Estado y Colaboración Humano-Agente](#6-agent-workspace--interfaz-de-estado-y-colaboración-humano-agente)
7. [Stack tecnológico](#7-stack-tecnológico)
8. [Infraestructura y modelo de despliegue](#8-infraestructura-y-modelo-de-despliegue)
9. [Integración con el framework existente](#9-integración-con-el-framework-existente)
10. [Roadmap de implementación](#10-roadmap-de-implementación)
11. [Métricas de éxito de la capa agéntica](#11-métricas-de-éxito-de-la-capa-agéntica)
12. [Glosario](#12-glosario)

---

## 1. Por qué agenticidad en este framework

El framework BPA DataCentric v1.1 define una arquitectura de datos operacionales cuyo estado objetivo requiere que varias capacidades **"sucedan automáticamente"** ante eventos del sistema. El problema es que esas capacidades son fundamentalmente de razonamiento, adaptación y generación — no de lógica determinista que se pueda programar con reglas fijas.

Los tres ejes que elevan el framework a plataforma de datos (Wiki ejecutable, observabilidad del dato, gobierno de datos) tienen en común que sus funciones centrales son:

| Función | Por qué no se resuelve con código determinista |
|---|---|
| Proponer KPIs a partir de un contrato de datos | Requiere entender semántica de campos, no solo comparar nombres |
| Completar una Historia de Usuario desde lenguaje natural | Requiere interpretación de intención, no parsing de reglas |
| Generar código de dashboard desde un contrato | Requiere razonamiento sobre composición de componentes |
| Explicar una anomalía en el dato | Requiere contextualizar un desvío, no solo detectarlo |
| Trazar linaje de forma automática desde logs | Requiere inferencia sobre relaciones implícitas |
| Orquestar el ciclo de vida completo de un proceso | Requiere coordinación adaptativa entre herramientas |

La **capa agéntica** no reemplaza el motor de extracción ni los dashboards existentes: se monta **encima** del framework como una inteligencia coordinadora que automatiza los pasos que hoy requieren trabajo manual del equipo técnico y funcional.

---

## 2. Mapa de gaps que los agentes resuelven

Cruzando el framework v1.1 con sus propias métricas y fases "A formalizar" / "A implementar", los gaps que la capa agéntica cubre son:

| Gap del framework v1.1 | Sección afectada | Agente que lo cubre |
|---|---|---|
| Wiki N3 — propuesta automática de KPIs calculables | §5 — Wiki Indicadores | KPI Recommender |
| Wiki N2 — cálculo de KPI por configuración sin reprogramar | §5 — Wiki Indicadores | KPI Recommender |
| HU incompleta o iterativa entre negocio y técnico | §6 — Historia de Usuario | HU Analyst |
| Dashboard generado por composición (no a mano) | §10 — Presentación | Dashboard Composer |
| Validación de contrato post-publicación | §9 — Observabilidad N2 | Data Health Monitor |
| Detección de drift de volumen / KPI | §9 — Observabilidad N2 | Data Health Monitor |
| Chequeo sintético de dashboard | §9 — Observabilidad N3 | Data Health Monitor |
| Linaje KPI → origen (hoy no existe) | §11 — Gobierno | Lineage Tracker |
| Detección de breaking changes en contratos | §11 — Gobierno | Lineage Tracker |
| Catálogo de datos actualizado automáticamente | §11 — Gobierno | Lineage Tracker |
| Ciclo de vida de nuevo proceso (manual y costoso) | §14 — Ciclo de vida | Onboarding Orchestrator |
| % procesos en Nivel 2 (solo config) — métrica clave | §13 — Madurez | Onboarding Orchestrator |
| Revisión de adopción a 30 días | §6 — HU Nivel 3 | Onboarding Orchestrator |

---

## 3. Los 6 agentes del sistema

### Agente 1 — HU Analyst

**Rol:** Convierte una descripción en lenguaje natural de una necesidad de negocio en una Historia de Usuario completa (Niveles 1 + 2 + 3), con KPIs propuestos desde la Wiki.

**Por qué es un agente y no un formulario:** el área de negocio raramente puede articular con precisión técnica qué necesita medir. El agente interpreta la intención, infiere el dominio operacional, consulta la wiki y propone una HU fundamentada — reduciendo de múltiples iteraciones a un único ciclo de revisión.

```
TRIGGER
  Usuario envía descripción en lenguaje natural
  + (opcional) muestra de campos del dataset o nombre del sistema origen

INPUT
  - texto libre: "necesito ver cómo van las operaciones de alta de fibra"
  - (opcional) contrato preliminar: lista de campos disponibles

PROCESO
  1. Clasificar dominio operacional (contact center / ITSM / operaciones / ...)
  2. Inferir fuente probable y frecuencia esperada
  3. Consultar wiki por dominio → indicadores candidatos
  4. Si hay campos disponibles: cruzar con KPI Recommender para filtrar calculables
  5. Redactar HU Nivel 1 (extracción), Nivel 2 (KPIs propuestos), Nivel 3 (adopción)
  6. Validar completitud de la HU contra el schema estándar

OUTPUT
  - HU completa en formato estándar (markdown / JSON estructurado)
  - Lista de KPIs propuestos con justificación y estándar de referencia
  - Lista de campos mínimos requeridos para calcular cada KPI
  - Nivel de confianza por cada KPI propuesto
```

**Herramientas (tools) del agente:**

| Tool | Qué hace |
|---|---|
| `wiki_search(query, domain)` | Búsqueda semántica en la Wiki de Indicadores por dominio y concepto |
| `kpi_field_matcher(kpi_id, available_fields)` | Verifica si los campos disponibles satisfacen los `inputs` del KPI |
| `hu_template_filler(nivel, data)` | Genera el texto de la HU en formato estándar |
| `hu_validator(hu_json)` | Valida que la HU tiene todos los campos obligatorios de los 3 niveles |
| `domain_classifier(text)` | Clasifica el dominio operacional del texto recibido |

**Valor medible:** reducción del ciclo de solicitud de 3-5 días (iteraciones manuales) a < 1 día (un ciclo de revisión sobre la HU propuesta).

---

### Agente 2 — KPI Recommender (Wiki N3)

**Rol:** Dado un contrato de datos, determina qué KPIs de la Wiki son calculables, los presenta al usuario para validación y refinamiento iterativo, y solo tras la confirmación humana genera el `dataProcessor` definitivo. Implementa los niveles N2 y N3 de la Wiki ejecutable **con human-in-the-loop obligatorio**.

**Por qué es un agente y no una función:** la correspondencia entre un campo real (p. ej. `fec_apertura_ticket`) y un input de KPI (`fecha_apertura: datetime`) requiere razonamiento semántico — no matching exacto de nombres. Además, la generación del `dataProcessor` es síntesis de código que varía según el contrato. Y sobre todo: **el experto de negocio es la única fuente de verdad sobre si un KPI calculable es también un KPI relevante** para su operación particular.

**Por qué el HITL es obligatorio aquí y no opcional:** el matching semántico puede producir mapeos técnicamente válidos pero semánticamente incorrectos. Un campo `duracion_proceso` puede mapearse a MTTR con 78% de confianza, pero solo el área sabe si ese campo mide lo mismo que el estándar ITIL. Sin validación humana, el `dataProcessor` puede generar un KPI que se llama MTTR pero que calcula otra cosa — error silencioso que llega al dashboard de dirección.

El agente opera en **tres fases secuenciales**, donde la segunda es conversacional:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 1 — RECOMENDACIÓN (automática, sin intervención humana)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRIGGER
  Nuevo contrato de datos registrado en el sistema
  O solicitud explícita durante análisis de contenido del dataset

INPUT
  - contrato_de_datos: { campos: [{nombre, tipo, descripcion_muestra}] }
  - dominio_operacional: (opcional, puede inferirse)
  - stack_canonico: (tecnología target para el dataProcessor)

PROCESO
  1. Clasificar dominio si no viene explícito
  2. Listar KPIs candidatos de la Wiki para ese dominio
  3. Por cada KPI: matching semántico entre sus inputs y los campos del contrato
  4. Clasificar por score de confianza:
     - EXACTO (≥ 90%): nombre y tipo coinciden directamente
     - SEMÁNTICO (60–89%): significado equivalente, nombre distinto
     - INFERIDO (< 60%): relación plausible pero incierta
  5. Identificar KPIs no calculables y qué campos faltan
  6. Preparar propuesta estructurada para presentar al usuario

OUTPUT INTERNO (entrada a Fase 2)
  - kpis_exactos: lista de KPIs de alta confianza con mapeo y fórmula
  - kpis_semanticos: lista con mapeo propuesto y justificación
  - kpis_inferidos: lista con advertencia explícita de incertidumbre
  - kpis_no_calculables: lista con campos faltantes por KPI

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 2 — VALIDACIÓN ITERATIVA (human-in-the-loop via chat)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

El agente presenta la propuesta en el Agent Workspace (ver §6)
y entra en un bucle de refinamiento con el usuario.

EJEMPLO DE SESIÓN CONVERSACIONAL
─────────────────────────────────────────────────────
Agente:
  Analicé el contrato del proceso. Encontré 8 KPIs calculables.
  Te presento los 5 más relevantes para el dominio "Operaciones de Atención":

  ✅ SLA Compliance Rate (ITIL v4) — confianza EXACTA
     Mapeo: fec_apertura_ticket → fecha_apertura | fec_cierre_ticket → fecha_cierre
     Fórmula: % casos cerrados en ≤ 24h | Umbral wiki: ≥ 97%

  ✅ Tasa de Error Operacional — confianza EXACTA
     Mapeo: estado_transaccion → estado | cod_error → codigo_error
     Fórmula: errores / total × 100 | Umbral wiki: < 10%

  ⚠️  MTTR (Mean Time To Resolve) — confianza SEMÁNTICA (78%)
     Mapeo propuesto: duracion_proceso → tiempo_resolucion
     Justificación: "duracion_proceso" parece equivalente a tiempo de resolución
     Umbral wiki: ≤ 24h — ¿es correcto para tu proceso?

  ⚠️  FCR (First Contact Resolution) — confianza INFERIDA (42%)
     Mapeo propuesto: intento_numero → intentos
     Confianza baja — necesito confirmar si este campo mide intentos de contacto

  ❌ AHT (Average Handle Time) — no calculable
     Falta el campo: duracion_manejo (tiempo de gestión por operador)

  También encontré 3 KPIs adicionales disponibles.
  ¿Quieres revisarlos, ajustar algo o continuar con esta selección?

─────────────────────────────────────────────────────
Usuario:
  El MTTR está bien pero el umbral es 48h, no 24h para este proceso.
  El FCR no aplica aquí, quítalo.
  ¿Puedes agregar Volumetría Mensual también?

─────────────────────────────────────────────────────
Agente:
  Entendido. Actualizando:
  ✅ MTTR confirmado — umbral ajustado a 48h (fuera del estándar wiki, documentado)
  ❌ FCR eliminado de la selección
  ✅ Volumetría Mensual — calculable con el campo fecha_transaccion (confianza EXACTA)

  KPIs confirmados para el dataProcessor (4 en total):
  1. SLA Compliance Rate — objetivo ≥ 97%
  2. Tasa de Error Operacional — objetivo < 10%
  3. MTTR — umbral personalizado: 48h
  4. Volumetría Mensual

  ¿Apruebas esta selección para proceder con la generación?

─────────────────────────────────────────────────────
Usuario: Aprobado.
─────────────────────────────────────────────────────

REGLAS DEL BUCLE DE REFINAMIENTO
  - El agente puede recibir: confirmaciones, eliminaciones, adiciones,
    ajustes de umbral, cambios de mapeo o preguntas sobre un KPI.
  - Cada respuesta del usuario actualiza el estado de la sesión.
  - El bucle termina cuando el usuario emite aprobación explícita.
  - Si el usuario pide un KPI no calculable con los campos disponibles,
    el agente lo explica e informa qué campo adicional sería necesario.
  - El agente no genera código hasta que la selección esté aprobada.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 3 — GENERACIÓN (automática, post-aprobación)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRIGGER: aprobación explícita del usuario en la sesión de chat

PROCESO
  1. Tomar los KPIs aprobados (con mapeos y umbrales definitivos)
  2. Instanciar fórmulas con los campos reales del contrato
  3. Generar el código del `dataProcessor` para cada KPI
  4. Validar que el código compila sin errores
  5. Persistir la selección aprobada en el catálogo (para trazabilidad)

OUTPUT FINAL
  - Lista de KPIs aprobados con:
    - mapeo definitivo campo_contrato → input_kpi
    - fórmula instanciada con campos reales
    - umbrales definitivos (wiki o personalizados, ambos documentados)
    - estándar de referencia
  - Código `dataProcessor` generado y validado
  - Registro de la sesión de validación (quién aprobó, cuándo, qué cambios)
```

**Herramientas (tools) del agente:**

| Tool | Qué hace |
|---|---|
| `wiki_kpi_list(domain, filters)` | Lista KPIs del catálogo filtrados por dominio / categoría |
| `wiki_kpi_get(kpi_id)` | Retorna la definición completa de un KPI (inputs, fórmula, umbrales) |
| `semantic_field_match(kpi_inputs, contract_fields)` | Matching semántico entre inputs requeridos y campos disponibles |
| `formula_instantiate(kpi_id, field_mapping)` | Instancia la fórmula del KPI con los nombres reales de campos |
| `dataprocessor_generate(kpis_aprobados, contract, stack)` | Genera el `dataProcessor` solo para KPIs con aprobación humana |
| `code_syntax_check(code, language)` | Valida que el código generado compila sin errores |
| `chat_session_state_update(session_id, kpi_changes)` | Actualiza el estado de la sesión iterativa con los cambios del usuario |
| `kpi_selection_persist(session_id, approved_kpis)` | Guarda la selección aprobada en el catálogo para trazabilidad |

**Impacto en el diseño general:** la necesidad del bucle conversacional de la Fase 2 implica que la capa agéntica requiere un **Agent Workspace** dedicado. Este componente no es exclusivo de AG-2: AG-1 (refinamiento de la HU), AG-3 (revisión del dashboard generado) y AG-6 (checkpoints del onboarding) comparten el mismo patrón de interacción HITL. Ver §6 — Agent Workspace.

**Valor medible:**
- % de KPIs aprobados sin modificación en la sesión (mide qué tan buena es la propuesta inicial)
- % de procesos donde el `dataProcessor` es generado sin código adicional post-aprobación (objetivo: > 70% en dominios conocidos)
- Reducción del tiempo de análisis de contenido + selección de KPIs: de 1 día a < 2 horas

---

### Agente 3 — Dashboard Composer

**Rol:** Genera el dashboard de producción completo (componentes, servicios, tipos TypeScript) a partir del contrato de datos y los KPIs seleccionados, usando el stack canónico del framework.

**Por qué es un agente y no un generador de plantillas:** la composición de un dashboard depende del tipo de cada KPI (tarjeta de valor único, serie temporal, distribución, ranking, SLA gauge) y de cómo los KPIs se relacionan entre sí visualmente. Un generador de plantillas fijo no puede razonar sobre esa composición.

```
TRIGGER
  HU aprobada (Nivel 2 con KPIs finalizados)
  + Contrato de datos validado

INPUT
  - hu_nivel2: { kpis: [...], sla_visualizacion, rol_consumidor }
  - contrato_de_datos: { campos, version }
  - kpis_instanciados: output del KPI Recommender
  - stack_canonico: { nombre, version, component_library }

PROCESO
  1. Clasificar cada KPI por tipo de visualización:
     (valor único / serie temporal / distribución / ranking / gauge SLA / tabla)
  2. Determinar layout del dashboard (jerarquía visual: resumen → detalle → tendencia)
  3. Por cada KPI: seleccionar componente visual de la biblioteca del stack
  4. Generar `types.ts` desde el contrato de datos
  5. Generar `dataProcessor.ts` (si no viene del KPI Recommender)
  6. Generar `blobService.ts` / hook de datos configurado para el proceso
  7. Generar los componentes del dashboard ensamblados
  8. Validar que el código compila y que los tipos son consistentes

OUTPUT
  - Árbol de archivos del dashboard listo para despliegue:
    - types.ts · dataProcessor.ts · blobService.ts
    - componentes de KPI
    - página principal ensamblada
  - Instrucciones de despliegue (puerto, URL, configuración Vite)
  - Checkliste de validación visual para el solicitante
```

**Herramientas (tools) del agente:**

| Tool | Qué hace |
|---|---|
| `component_library_query(kpi_type, stack)` | Retorna el componente visual adecuado para el tipo de KPI y stack |
| `layout_planner(kpi_list)` | Genera la estructura de layout del dashboard según los KPIs |
| `types_generator(contract, version)` | Genera los tipos TypeScript desde el contrato de datos |
| `blobservice_configurator(process_id, stack)` | Genera el servicio de datos con proxy Vite y fallback local |
| `code_assembler(components, layout)` | Ensambla los componentes en la página principal |
| `typescript_compiler_check(files)` | Verifica que el código TypeScript generado compila |
| `process_monitor_register(dashboard_config)` | Registra el dashboard en el ProcessMonitor para control de arranque |

**Valor medible:** tiempo de la Fase 4 (Dashboard) reducido de 4-8 horas a < 1 hora para procesos con KPIs del catálogo.

---

### Agente 4 — Data Health Monitor

**Rol:** Vigila continuamente la salud de los artefactos publicados (CSVs, JSONs pre-agregados) en tres dimensiones: cumplimiento de contrato, drift estadístico y disponibilidad del dashboard. Es el guardián entre "el proceso corrió" y "el dato es correcto y visible".

**Por qué es un agente y no un script de validación:** la explicación de una anomalía (¿por qué el volumen bajó un 40%?) y la decisión de si disparar una alerta requieren contextualización. Un script detecta; el agente interpreta, contextualiza y comunica con tono apropiado según severidad.

```
TRIGGER (múltiple)
  A. Post-publicación: cada vez que un artefacto se sube al Blob
  B. Scheduled: cada N minutos (chequeo sintético de dashboards)
  C. On-demand: disparado manualmente desde el ProcessMonitor

INPUT (trigger A — post-publicación)
  - artifact_metadata: { proceso_id, ruta_blob, timestamp, tamaño }
  - contrato_de_datos: versión vigente del proceso

INPUT (trigger B — chequeo sintético)
  - dashboard_registry: lista de URLs y SLAs de visualización declarados en las HUs

PROCESO (validación de contrato)
  1. Descargar el artefacto desde Blob
  2. Verificar schema: todos los campos del contrato presentes con los tipos correctos
  3. Verificar campos clave no nulos (campos declarados como required en el contrato)
  4. Verificar volumen: dentro del rango histórico ± umbral de drift
  5. Si hay JSON pre-agregado: verificar que todas las secciones del contrato existen
  6. Generar health_report con estado (OK / WARNING / CRITICAL) y detalle
  7. Si WARNING o CRITICAL: invocar alert_dispatcher + registrar en monitor

PROCESO (chequeo sintético)
  1. Por cada dashboard registrado: GET a la URL
  2. Verificar HTTP 200 en < SLA de tiempo de carga
  3. Verificar que la página contiene evidencia de datos (no estado de error)
  4. Verificar antigüedad del dato (timestamp del último artefacto vs. SLA de frescura)
  5. Registrar resultado en la sección "Salud del consumo" del monitor

OUTPUT
  - health_report por artefacto: { estado, contrato_ok, drift_detectado, detalle }
  - synthetic_check_report por dashboard: { estado, latencia, frescura, errores }
  - alertas enviadas a Teams/Slack/Monitor según severidad
  - texto explicativo generado por LLM: "El volumen bajó 38% respecto al promedio
    de los últimos 7 días. El proceso corrió correctamente (exit 0). La causa
    probable es una restricción en el origen — revisar logs de la query."
```

**Herramientas (tools) del agente:**

| Tool | Qué hace |
|---|---|
| `blob_artifact_fetch(process_id, artifact_type)` | Descarga el artefacto más reciente del Blob |
| `contract_schema_validate(artifact, contract)` | Valida schema y campos requeridos |
| `drift_detector(current_metrics, historical_baseline, threshold)` | Detecta desvíos estadísticos |
| `synthetic_http_check(url, timeout_ms)` | Chequeo HTTP de disponibilidad |
| `dashboard_freshness_check(url, max_age_hours)` | Verifica antigüedad del dato en el dashboard |
| `alert_dispatcher(severity, message, channel)` | Envía alerta a Teams/Slack/Monitor |
| `monitor_health_update(process_id, health_report)` | Actualiza el estado en el ProcessMonitor |
| `explanation_generator(anomaly_context)` | Genera texto explicativo del incidente |

**Valor medible:** 100% de incidentes de contrato detectados antes de que el usuario final los reporte.

---

### Agente 5 — Lineage Tracker

**Rol:** Construye y mantiene automáticamente el grafo de linaje del framework: desde cada query/tabla origen hasta cada KPI visible en el dashboard, atravesando extracción → artefacto → pre-agregado → dashboard. Implementa la Capa 5 de Gobierno sin trabajo manual.

**Por qué es un agente y no un log parser:** el linaje requiere inferir relaciones entre entidades que no siempre están explícitamente conectadas en los logs. Por ejemplo, un campo `fecha_apertura` en el `dataProcessor` y un campo `fec_apertura_ticket` en la query de PostgreSQL son el mismo dato — el agente debe inferir esa equivalencia.

```
TRIGGER
  A. Post-ejecución: cada vez que un proceso completa (exit 0)
  B. Post-cambio de contrato: cuando se versiona un contrato de datos
  C. Post-despliegue de dashboard: cuando se registra un nuevo dashboard

INPUT (trigger A)
  - execution_log: logs completos de la ejecución
  - process_config: entrada del proceso en processes.json
  - query_files: queries SQL usadas en la extracción

INPUT (trigger B)
  - old_contract: versión anterior del contrato
  - new_contract: versión nueva del contrato
  - consumers: dashboards y servicios que consumen este contrato

PROCESO (construcción de linaje)
  1. Parsear los logs y extraer: queries ejecutadas, tablas accedidas, artefactos generados
  2. Cruzar campos del artefacto generado con campos en las queries (inferencia semántica)
  3. Cruzar campos del artefacto con los `inputs` de los KPIs que lo consumen
  4. Cruzar KPIs con los componentes del dashboard que los muestran
  5. Actualizar el grafo de linaje en la base de datos:
     tabla_origen → campo_query → campo_csv → kpi_instanciado → componente_dashboard
  6. Actualizar el catálogo de datos (proceso, contrato, versión, consumidores)

PROCESO (detección de breaking changes)
  1. Comparar old_contract vs new_contract
  2. Clasificar cada cambio: aditivo (compatible) / renombrado / eliminación / tipo (breaking)
  3. Por cada breaking change: identificar todos los consumidores afectados en el grafo
  4. Generar impact_report con lista de consumidores afectados y acciones requeridas
  5. Notificar al responsable del proceso y a los responsables de los dashboards afectados

OUTPUT
  - Grafo de linaje actualizado
  - Catálogo de datos actualizado
  - impact_report por breaking change: { campo, tipo_cambio, consumidores_afectados }
  - Respuestas a queries de linaje: "¿De dónde viene este KPI?" → ruta completa
```

**Herramientas (tools) del agente:**

| Tool | Qué hace |
|---|---|
| `log_parser(execution_log)` | Extrae metadata estructurada de los logs de ejecución |
| `sql_field_extractor(query_file)` | Extrae los campos seleccionados de una query SQL |
| `semantic_field_linker(source_fields, target_fields)` | Infiere equivalencias semánticas entre campos |
| `lineage_graph_upsert(nodes, edges)` | Actualiza el grafo de linaje |
| `catalog_upsert(process_id, contract, artifacts, consumers)` | Actualiza el catálogo de datos |
| `breaking_change_analyzer(old_contract, new_contract)` | Clasifica cambios y detecta breaking changes |
| `consumer_impact_query(contract_id, changed_fields)` | Consulta el grafo para encontrar consumidores afectados |
| `notification_sender(recipients, impact_report)` | Notifica a responsables por breaking change |

**Valor medible:** 100% de cobertura de linaje KPI→origen para todos los procesos productivos.

---

### Agente 6 — Onboarding Orchestrator

**Rol:** Coordina la incorporación completa de un proceso nuevo al framework, desde la HU inicial hasta el Gate E2E y la revisión de adopción a 30 días. Es el director de orquesta que invoca a los demás agentes en el orden correcto y adapta el flujo según el nivel de madurez del proceso (0/1/2).

**Por qué es un agente y no un pipeline determinista:** el ciclo de vida tiene bifurcaciones (¿el origen ya está soportado?, ¿los KPIs están en la wiki?, ¿el dashboard compila?), estados de espera (validación con el solicitante), y decisiones adaptativas (¿reintentar la generación del dashboard?, ¿escalar a un humano?). Un pipeline fijo no puede manejar esa variabilidad.

```
TRIGGER
  Nueva HU enviada al sistema (vía interface del ProcessMonitor o formulario)

ESTADO INICIAL
  hu_raw: texto de la solicitud
  dataset_sample: (opcional) muestra de campos del origen

FASE 1 — ANÁLISIS (invoca HU Analyst)
  ├── Invocar HU Analyst con hu_raw + dataset_sample
  ├── Revisar HU propuesta con responsable funcional (loop de confirmación)
  └── → CHECKPOINT: HU aprobada (Nivel 1 + 2 + 3)

FASE 2 — DETERMINACIÓN DE NIVEL DE MADUREZ
  ├── ¿El origen del proceso ya tiene extractor registrado? → sí/no
  ├── ¿Los KPIs de la HU están en la wiki como ejecutables (N2)?  → sí/no
  └── → CLASIFICAR: Nivel 0 / 1 / 2

FASE 3 — CONFIGURACIÓN
  ├── Nivel 2: solo registrar en processes.json + invocar KPI Recommender
  ├── Nivel 1: + generar dataProcessor a medida (KPI Recommender + revisión)
  ├── Nivel 0: + escalar a desarrollador para BaseExtractor + dataProcessor
  ├── Invocar Lineage Tracker: registrar linaje preliminar del proceso
  └── → CHECKPOINT: configuración validada

FASE 4 — PRUEBA DE EXTRACCIÓN
  ├── Lanzar ejecución manual desde ProcessMonitor (via tool)
  ├── Invocar Data Health Monitor: validar artefacto generado
  └── → CHECKPOINT: artefacto cumple contrato

FASE 5 — DASHBOARD
  ├── Invocar Dashboard Composer con HU Nivel 2 + contrato validado
  ├── Revisar dashboard generado con solicitante (loop de confirmación)
  ├── Invocar Data Health Monitor: chequeo sintético del dashboard
  └── → CHECKPOINT: Gate E2E (extracción + contrato + visualización correcta)

FASE 6 — CIERRE
  ├── Registrar proceso en scheduler
  ├── Alta en catálogo (Lineage Tracker)
  ├── Programar revisión de adopción a 30 días
  └── → PROCESO ACTIVO

FASE 7 — ADOPCIÓN (a 30 días)
  ├── Evaluar métricas de consumo (accesos, usuarios distintos)
  ├── Comparar con metas declaradas en HU Nivel 3
  └── → VEREDICTO: MANTENER / AJUSTAR / RETIRAR
```

**Herramientas (tools) del agente:**

| Tool | Qué hace |
|---|---|
| `hu_analyst_invoke(input)` | Delega al Agente 1 |
| `kpi_recommender_invoke(contract)` | Delega al Agente 2 |
| `dashboard_composer_invoke(hu, contract, kpis)` | Delega al Agente 3 |
| `data_health_monitor_invoke(process_id, trigger)` | Delega al Agente 4 |
| `lineage_tracker_invoke(execution_context)` | Delega al Agente 5 |
| `maturity_level_assess(process_config)` | Determina nivel de madurez (0/1/2) |
| `process_execution_trigger(process_id)` | Lanza ejecución manual en el ProcessMonitor |
| `processes_json_register(process_def)` | Registra el proceso en processes.json |
| `scheduler_register(process_id, cron_expression)` | Registra la tarea programada |
| `human_confirmation_request(checkpoint, context)` | Pausa el flujo y espera aprobación humana |
| `adoption_metrics_query(process_id, since_date)` | Consulta métricas de consumo del dashboard |

**Valor medible:** tiempo total del ciclo de vida de onboarding (Fases 1-6) reducido de 2 días a < 4 horas para procesos de Nivel 2.

---

## 4. Arquitectura del sistema multi-agente

### Visión de alto nivel

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       BPA DataCentric — Agentic Layer                        │
│                                                                               │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                    ONBOARDING ORCHESTRATOR (AG-6)                     │  │
│   │              Coordinador del ciclo de vida completo                   │  │
│   │    ┌──────────┐  ┌──────────────┐  ┌───────────────────┐             │  │
│   │    │HU Analyst│  │KPI Recomm.   │  │Dashboard Composer │             │  │
│   │    │  (AG-1)  │─▶│  (AG-2)      │─▶│     (AG-3)        │             │  │
│   │    └──────────┘  └──────────────┘  └───────────────────┘             │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
│   ┌───────────────────────────┐   ┌──────────────────────────┐              │
│   │  DATA HEALTH MONITOR       │   │    LINEAGE TRACKER        │              │
│   │       (AG-4)               │   │        (AG-5)             │              │
│   │  Post-publicación ·        │   │  Post-ejecución ·         │              │
│   │  Scheduled · On-demand     │   │  Post-cambio-contrato     │              │
│   └───────────────────────────┘   └──────────────────────────┘              │
│                                                                               │
│   ══════════════════════ MCP Tool Layer ═══════════════════════════          │
│   ┌───────────┐ ┌───────────┐ ┌──────────────┐ ┌────────────────────┐      │
│   │wiki-server│ │blob-server│ │monitor-server│ │lineage-server      │      │
│   └───────────┘ └───────────┘ └──────────────┘ └────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
          │               │               │                │
          ▼               ▼               ▼                ▼
   Azure OpenAI    Azure AI Search  ProcessMonitor    Azure Cosmos DB
   (LLM backbone)  (Wiki vectorial)  (API existente)  (Lineage graph)
          │               │
          └───────────────┘
           Azure Blob Storage
           (artefactos de datos)
```

### Patrones de interacción

Los agentes interactúan en dos modos:

**Modo orquestado (síncrono):**
El Onboarding Orchestrator (AG-6) dirige el flujo de onboarding invocando a los demás agentes en secuencia. Los checkpoints con humano (confirmación de HU, validación de dashboard) pausan el flujo hasta recibir aprobación.

**Modo reactivo (event-driven):**
Los agentes 4 y 5 son independientes y se disparan por eventos:
- AG-4 (Data Health Monitor): evento `artifact_published` en Azure Service Bus
- AG-5 (Lineage Tracker): evento `process_execution_completed` en Azure Service Bus

```
EVENTOS DE SISTEMA
                     ┌─────────────────────────┐
                     │    Azure Service Bus      │
                     │  artifact_published       │──▶ AG-4 (Data Health)
                     │  execution_completed      │──▶ AG-5 (Lineage Tracker)
                     │  hu_submitted             │──▶ AG-6 (Orchestrator)
                     │  contract_changed         │──▶ AG-5 (Breaking change)
                     └─────────────────────────┘
```

### Human-in-the-loop

Los agentes son autónomos pero no totalmente sin supervisión. Los checkpoints del Onboarding Orchestrator requieren confirmación humana explícita antes de continuar:

```
CHECKPOINTS CON HUMANO
  ├── CHECKPOINT 1: HU propuesta → aprobación del área solicitante
  ├── CHECKPOINT 2: configuración del proceso → aprobación técnica
  ├── CHECKPOINT 3: dashboard generado → validación visual con solicitante
  └── CHECKPOINT 4: Gate E2E → aprobación final antes de poner en producción
```

Los agentes 4 y 5 (Data Health y Lineage) son completamente autónomos — actúan sin confirmación humana, excepto cuando escalan incidentes.

---

## 5. Capa MCP — Model Context Protocol servers

Los agentes acceden a las capacidades del framework a través de **servidores MCP** que exponen las herramientas del sistema como un conjunto de funciones invocables por los LLMs. Esto desacopla la implementación del framework de la lógica del agente.

### wiki-mcp-server

Expone la Wiki de Indicadores al sistema agéntico.

| Tool expuesta | Descripción |
|---|---|
| `wiki_search` | Búsqueda semántica por texto libre en el catálogo de KPIs |
| `wiki_kpi_get` | Recupera la definición completa de un KPI por ID |
| `wiki_kpi_list` | Lista KPIs por dominio, categoría o estándar |
| `wiki_field_match` | Matching semántico entre campos de un contrato e inputs de KPIs |
| `wiki_formula_instantiate` | Instancia una fórmula con campos reales del contrato |
| `wiki_kpi_add` / `wiki_kpi_update` | Gestión del catálogo (agregar/actualizar indicadores) |

**Tecnología:** Python/FastAPI + Azure AI Search (índice vectorial de la wiki) + storage JSON para las definiciones completas.

### blob-mcp-server

Expone las capacidades de Azure Blob Storage y los contratos de datos.

| Tool expuesta | Descripción |
|---|---|
| `blob_artifact_list` | Lista artefactos disponibles por proceso |
| `blob_artifact_fetch` | Descarga un artefacto específico (CSV / JSON) |
| `contract_get` | Recupera el contrato de datos de un proceso (versión específica o última) |
| `contract_validate` | Valida un artefacto contra su contrato |
| `contract_diff` | Compara dos versiones de un contrato y clasifica cambios |
| `freshness_check` | Verifica la antigüedad de un artefacto respecto del SLA |

**Tecnología:** Python + azure-storage-blob SDK + sistema de versionado de contratos (JSON en Blob o Git).

### monitor-mcp-server

Expone la API del ProcessMonitor a los agentes.

| Tool expuesta | Descripción |
|---|---|
| `process_list` | Lista todos los procesos registrados con estado |
| `process_execute` | Lanza ejecución manual de un proceso |
| `execution_history_get` | Recupera historial de ejecuciones de un proceso |
| `health_report_update` | Actualiza el estado de salud del dato en el monitor |
| `dashboard_register` | Registra un nuevo dashboard en el monitor |
| `dashboard_start` / `dashboard_stop` | Control de arranque de dashboards |
| `scheduler_register` | Registra una tarea programada |

**Tecnología:** Cliente HTTP de la API Flask existente del ProcessMonitor (puerto 5052).

### lineage-mcp-server

Expone el grafo de linaje y el catálogo de datos.

| Tool expuesta | Descripción |
|---|---|
| `lineage_upsert` | Agrega/actualiza nodos y aristas en el grafo |
| `lineage_query_kpi` | "¿De dónde viene este KPI?" → ruta completa |
| `lineage_query_field` | "¿Qué KPIs usan este campo?" → consumidores |
| `lineage_query_process` | Grafo completo de un proceso |
| `catalog_process_upsert` | Alta/actualización de proceso en el catálogo |
| `catalog_search` | Búsqueda en el catálogo de datos |
| `impact_analysis` | Consumidores afectados ante un cambio de contrato |

**Tecnología:** Python/FastAPI + Azure Cosmos DB (API Gremlin para el grafo).

---

## 6. Agent Workspace — Interfaz de Estado y Colaboración Humano-Agente

### El paradigma: máquina de estados visible + HITL contextual

La incorporación del human-in-the-loop en AG-2 (KPI Recommender) no es un caso aislado. Es la manifestación de un patrón que aparece en cuatro de los seis agentes:

| Agente | Momento del HITL | Tipo de interacción |
|---|---|---|
| **AG-1** HU Analyst | Refinamiento de la HU propuesta | Iterativo: "cambia el SLA de extracción a 2h, no 4h" |
| **AG-2** KPI Recommender | Validación de KPIs sugeridos, umbrales y mapeos | Iterativo: "quita FCR, ajusta MTTR a 48h, agrega Volumetría" |
| **AG-3** Dashboard Composer | Revisión del dashboard generado | Iterativo: "sube el gauge de SLA, cambia barras a líneas" |
| **AG-6** Onboarding Orchestrator | Checkpoints de las fases 1, 2, 3 y 4 | Confirmación + preguntas de contexto |

Un chat lineal puro resuelve la interacción, pero no resuelve la **visibilidad**: el usuario no sabe en qué fase está el proceso, qué hicieron los agentes solos, qué falló, ni cuándo es su turno. Una interfaz de sólo chat aplana una máquina de estados en una conversación — perdiendo estructura que el usuario necesita ver.

El concepto correcto es el **Agent Workspace**: una superficie de trabajo que refleja la naturaleza real del sistema backend (LangGraph es una máquina de estados con nodos e interrupciones). El usuario ve el progreso de cada fase en tiempo real; cuando un agente necesita su input, la interfaz presenta el **widget adecuado para ese tipo de decisión** — no siempre un chat genérico.

> **Fundamento técnico:** LangGraph emite eventos de cambio de estado (SSE/WebSocket) en cada transición de nodo. Cuando un nodo es de tipo `interrupt` (HITL), emite un evento `waiting_for_human` con el tipo de interacción requerida. El frontend suscribe a estos eventos y renderiza dinámicamente el widget correspondiente. Cuando el usuario responde, el input desbloquea (`resume`) la ejecución del grafo.

### Layout del Agent Workspace

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ProcessMonitor  │  Procesos  │  Historial  │  Agent Workspace  ●  [2]     │
├──────────────────────────────┬──────────────────────────────────────────────┤
│  PANEL IZQUIERDO             │  PANEL DERECHO                               │
│  Estado del proceso          │  Actividad del agente activo                 │
│  ─────────────────────────   │  ─────────────────────────────────────────   │
│                              │                                              │
│  Onboarding:                 │  [Estado: AGENTE TRABAJANDO]                 │
│  "Operaciones Fibra"         │                                              │
│                              │  AG-2 · KPI Recommender                     │
│  ✅ Fase 1 — Análisis HU     │  Escaneando wiki para dominio                │
│     AG-1 completado 09:14    │  "Operaciones de Atención"...                │
│                              │  › Candidatos encontrados: 8                 │
│  ⚡ Fase 2 — KPIs            │  › Verificando campos del contrato...        │
│     AG-2 activo              │  › SLA Compliance Rate → match EXACTO ✓     │
│     [════════░░░░] 60%       │  › MTTR → match SEMÁNTICO (78%) ...         │
│                              │                                              │
│  🔒 Fase 3 — Extracción      │                                              │
│  🔒 Fase 4 — Dashboard       │                                              │
│  🔒 Fase 5 — Cierre          │                                              │
│  🔒 Fase 6 — Revisión 30d    │                                              │
│                              │                                              │
│  ─────────────────────────   │                                              │
│  Duración estimada: ~3h      │                                              │
│  Nivel de madurez: 2         │                                              │
│  [Pausar sesión]             │                                              │
└──────────────────────────────┴──────────────────────────────────────────────┘
```

Cuando AG-2 completa su análisis y llega al nodo `interrupt` (HITL), el panel derecho **cambia automáticamente** al widget de validación de KPIs:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ProcessMonitor  │  Procesos  │  Historial  │  Agent Workspace  ●  [2]     │
├──────────────────────────────┬──────────────────────────────────────────────┤
│  PANEL IZQUIERDO             │  PANEL DERECHO                               │
│  Estado del proceso          │  [Estado: TU TURNO — VALIDACIÓN DE KPIs]    │
│  ─────────────────────────   │  ─────────────────────────────────────────   │
│                              │                                              │
│  ✅ Fase 1 — Análisis HU     │  AG-2 encontró 8 KPIs calculables.           │
│  ⏸  Fase 2 — KPIs            │  Revisa y ajusta la selección:               │
│     ESPERANDO TU INPUT  ●    │                                              │
│                              │  ┌─────────────────────────────────────┐    │
│  🔒 Fase 3 — Extracción      │  │☑ SLA Compliance Rate   EXACTA  ≥97% │    │
│  🔒 Fase 4 — Dashboard       │  │  fec_apertura → fecha_apertura      │    │
│  🔒 Fase 5 — Cierre          │  ├─────────────────────────────────────┤    │
│                              │  │☑ Tasa de Error         EXACTA <10%  │    │
│                              │  ├─────────────────────────────────────┤    │
│                              │  │☑ MTTR          SEMÁNTICA 78%  ≤24h  │    │
│                              │  │  duracion_proceso → t_resolucion    │    │
│                              │  │  [Umbral: 24h ▼]  ← editable        │    │
│                              │  ├─────────────────────────────────────┤    │
│                              │  │☐ FCR           INFERIDA  42%        │    │
│                              │  │  Confianza baja — desactivado       │    │
│                              │  ├─────────────────────────────────────┤    │
│                              │  │✕ AHT           NO CALCULABLE        │    │
│                              │  │  Falta campo: duracion_manejo       │    │
│                              │  └─────────────────────────────────────┘    │
│                              │                                              │
│                              │  ╔══════════════════════════════════════╗   │
│                              │  ║ Dime si quieres ajustar algo...      ║   │
│                              │  ╚══════════════════════════════════════╝   │
│                              │  "el MTTR va con 48h no 24h, quita el FCR" │
│                              │  ────────────────────────────────────────   │
│                              │  [Ajustar según mi comentario]              │
│                              │                          [Aprobar y seguir] │
└──────────────────────────────┴──────────────────────────────────────────────┘
```

### Los estados del proceso en el panel izquierdo

Cada fase del Onboarding Orchestrator tiene un estado visible en tiempo real:

| Icono | Estado | Significado |
|---|---|---|
| `✅` | Completado | La fase y sus agentes terminaron correctamente |
| `⚡` | En curso | Un agente está activo en esta fase (progress bar) |
| `⏸` + `●` | Esperando input | El flujo está pausado en un nodo HITL — acción requerida |
| `⚠️` | Alerta | La fase completó con advertencias (p. ej. drift detectado) |
| `❌` | Error | La fase falló — el workspace muestra qué salió mal y qué hacer |
| `🔒` | Pendiente | Fase no iniciada (bloqueada por fases anteriores) |

El número entre corchetes en la pestaña (`[2]`) indica cuántas sesiones tienen input pendiente del usuario — badge de notificación.

### Los cuatro widgets HITL

El panel derecho no siempre muestra lo mismo. Cuando LangGraph alcanza un nodo `interrupt`, emite el tipo de widget requerido. El frontend renderiza el widget correcto para cada decisión:

#### Widget 1 — Editor de HU (AG-1 · Fase 1)

Presenta la HU propuesta como un documento estructurado editable con tres niveles visibles. El usuario puede editar campos directamente **o** escribir en el input de chat para refinamientos en lenguaje natural ("añade que el SLA es 2h", "el rol consumidor es el gerente de fibra"). El agente aplica el cambio y actualiza el documento en pantalla.

```
┌─ HU Propuesta ──────────────────────────────────────────────────────┐
│  Proceso: Indicadores Operaciones Fibra                              │
│  ┌─ Nivel 1 — Extracción ─────────────────────────────────────────┐ │
│  │ Origen: PostgreSQL · Frecuencia: cada 4h · SLA: [2h  ▼]       │ │
│  └────────────────────────────────────────────────────────────────┘ │
│  ┌─ Nivel 2 — KPIs ───────────────────────────────────────────────┐ │
│  │ SLA Compliance · Tasa Error · MTTR · Volumetría Mensual        │ │
│  └────────────────────────────────────────────────────────────────┘ │
│  ┌─ Nivel 3 — Adopción ───────────────────────────────────────────┐ │
│  │ Meta 30 días: ≥ 15 consultas · Rol: Gerente de Operaciones     │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ╔══════════════════════════════════════════════════════════════╗   │
│  ║ Ajusta algo o confirma...                                    ║   │
│  ╚══════════════════════════════════════════════════════════════╝   │
│                                          [Aprobar HU y continuar]   │
└─────────────────────────────────────────────────────────────────────┘
```

#### Widget 2 — Validador de KPIs (AG-2 · Fase 2)

Tabla interactiva con checkboxes y umbrales editables inline. El input de chat permite refinamientos expresados en lenguaje natural. El agente razona sobre cada cambio pedido y actualiza la tabla. Detallado en el mockup de la sección anterior.

#### Widget 3 — Revisor de Dashboard (AG-3 · Fase 4)

Muestra un thumbnail o preview del dashboard generado con la lista de componentes ensamblados. El input de chat recibe instrucciones de ajuste visual ("mueve el gauge de SLA al primer bloque", "cambia el gráfico de tendencia a líneas con área"). El agente re-genera los componentes afectados sin tocar los que no se pidió cambiar.

```
┌─ Dashboard Generado ────────────────────────────────────────────────┐
│  Stack: SvelteKit · 4 KPIs · Proceso: Operaciones Fibra            │
│                                                                      │
│  Componentes ensamblados:                                           │
│  [1] Tarjeta — SLA Compliance Rate (gauge)                          │
│  [2] Tarjeta — Tasa de Error Operacional (valor + delta)            │
│  [3] Gráfico — MTTR evolución mensual (barras)  ← ajustable        │
│  [4] Tabla — Volumetría Mensual por grupo                           │
│                                                                      │
│  Vista previa: http://localhost:5181 (dev server activo)            │
│                                                                      │
│  ╔══════════════════════════════════════════════════════════════╗   │
│  ║ ¿Ajusto algo antes de aprobar?                               ║   │
│  ╚══════════════════════════════════════════════════════════════╝   │
│  "cambia el MTTR a gráfico de líneas y ponlo primero"              │
│                                          [Aprobar · Gate E2E ✓]     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Widget 4 — Confirmación de Checkpoint (AG-6 · Fases 1/3/5/6)

Para los checkpoints de transición entre fases, el widget más simple: resumen de lo que el agente completó automáticamente, campo de comentario opcional, y botón de confirmación. Sin iteración — solo validar que el usuario está al tanto antes de que el sistema avance.

```
┌─ Checkpoint 3 — Prueba de Extracción ──────────────────────────────┐
│  El proceso corrió correctamente. Resultados:                       │
│                                                                      │
│  ✅ Extracción completada en 1m 47s                                 │
│  ✅ Contrato de datos: todos los campos presentes                   │
│  ✅ Volumen: 12.340 registros (dentro del rango histórico)          │
│  ✅ Publicación en Blob: OK · 195 MB                                │
│                                                                      │
│  Comentario opcional: ___________________________                   │
│                                                                      │
│                           [Confirmar y pasar a Fase 4 — Dashboard]  │
└─────────────────────────────────────────────────────────────────────┘
```

### Principios de diseño del Agent Workspace

**1. El estado siempre es visible.**
El usuario sabe en todo momento en qué fase está el proceso, qué hicieron los agentes solos y qué espera su atención. No necesita leer una conversación para reconstruir el contexto.

**2. El panel derecho refleja el estado del sistema.**
Cuando un agente trabaja autónomamente: el panel muestra el streaming en tiempo real de su actividad (igual al patrón de logs en vivo del ProcessMonitor existente). Cuando el grafo alcanza un nodo HITL: el panel renderiza el widget adecuado para ese tipo de decisión.

**3. El chat es un mecanismo de entrada, no la metáfora principal.**
El input de lenguaje natural está presente en los widgets HITL, pero embebido en un contexto estructurado. El usuario no escribe en un chat vacío esperando saber qué decir — escribe en un campo junto a una tabla de KPIs que ya puede ver y editar.

**4. El agente propone, el humano decide.**
Ninguna acción irreversible (generar código, registrar el proceso, configurar el scheduler) ocurre sin aprobación explícita. Los botones de "Aprobar y continuar" son la manifestación visual de ese principio.

**5. Contexto persistente entre sesiones.**
El estado completo del workspace (fases completadas, KPIs aprobados, HU refinada, comentarios) se persiste en Redis. Si el usuario cierra el navegador, al regresar el workspace muestra exactamente el mismo estado.

**6. Múltiples sesiones simultáneas.**
El badge `[2]` en la pestaña indica que hay dos procesos en onboarding simultáneamente, uno de los cuales espera input. El usuario puede cambiar entre sesiones desde el panel izquierdo.

### Flujo completo de una sesión desde el Workspace

```
SESIÓN AGENT WORKSPACE — ONBOARDING "OPERACIONES FIBRA"
────────────────────────────────────────────────────────────────────────

FASE 1 — ANÁLISIS (panel derecho: streaming AG-1)
  → AG-1 clasifica dominio, consulta wiki, redacta HU
  → Panel: actividad en tiempo real del agente
  → Nodo interrupt: panel cambia a Widget 1 (Editor de HU)
  → Usuario refina HU en lenguaje natural (1–3 turnos)
  → Usuario hace clic en [Aprobar HU] → LangGraph resume
  → Fase 1 pasa a ✅ en panel izquierdo

FASE 2 — KPIs (panel derecho: streaming AG-2 · luego Widget 2)
  → AG-2 escanea wiki y hace matching semántico
  → Panel: streaming "encontrando candidatos..."
  → Nodo interrupt: panel cambia a Widget 2 (Validador de KPIs)
  → Usuario ajusta umbrales y KPIs (1–3 turnos)
  → Usuario hace clic en [Aprobar y seguir] → LangGraph resume
  → AG-2 genera dataProcessor automáticamente (sin más input)
  → Fase 2 pasa a ✅

FASE 3 — PRUEBA DE EXTRACCIÓN (panel derecho: streaming AG-4)
  → AG-6 lanza ejecución, AG-4 valida el artefacto
  → Panel: streaming del Data Health Monitor
  → Si artefacto OK: Nodo interrupt cambia a Widget 4 (Confirmación)
  → Si hay problema: panel muestra diagnóstico + opciones ("reintentar",
    "ajustar query", "escalar a desarrollador")
  → Usuario confirma → LangGraph resume
  → Fase 3 pasa a ✅

FASE 4 — DASHBOARD (panel derecho: streaming AG-3 · luego Widget 3)
  → AG-3 genera dashboard (el dev server arranca automáticamente)
  → Nodo interrupt: panel cambia a Widget 3 (Revisor de Dashboard)
  → Usuario ve la lista de componentes + URL del dev server
  → Usuario pide ajustes si los necesita (0–2 turnos)
  → Usuario hace clic en [Aprobar · Gate E2E ✓] → LangGraph resume
  → Fase 4 pasa a ✅

FASE 5 — CIERRE (automático, sin input)
  → AG-6 registra en scheduler, catálogo y lineage
  → Panel: streaming del registro automático
  → Fase 5 pasa a ✅

RESUMEN FINAL (panel derecho)
  → URL del dashboard en producción
  → Recordatorio de revisión de adopción (Nivel 3 HU): programada a 30 días
  → Registro completo de la sesión descargable (JSON / PDF)
────────────────────────────────────────────────────────────────────────
Duración típica (Nivel 2): 2–4 horas de trabajo real
```

### Componentes técnicos del Agent Workspace

| Componente | Tecnología | Función |
|---|---|---|
| **Panel de estado** | React + estado derivado de eventos SSE | Visualiza fases, agentes activos y badges de input pendiente |
| **Panel de actividad** | React + WebSocket streaming | Muestra log en tiempo real del agente activo (igual a logs en vivo del monitor) |
| **Widgets HITL** | React (componentes por tipo de widget) | Renderizado dinámico según el tipo de nodo interrupt emitido por LangGraph |
| **Input de lenguaje natural** | React + Vercel AI SDK (useChat) | Campo de chat embebido en cada widget que permite refinamientos textuales |
| **Backend de sesión** | FastAPI + SSE + WebSocket | Suscribe al grafo LangGraph y hace broadcast de eventos al frontend |
| **Orquestador** | LangGraph (AG-6) | Máquina de estados; emite `state_changed` y `waiting_for_human(widget_type)` |
| **Estado de sesión** | Redis | Persistencia del estado completo entre turnos y sesiones |
| **Dev server de preview** | Vite (arrancado por AG-3) | Permite al usuario ver el dashboard generado antes de aprobarlo |

### Eventos SSE del grafo hacia el frontend

```
EVENTOS EMITIDOS POR LANGGRAPH → FRONTEND

agent_started     { phase, agent_id, agent_name }
agent_log         { phase, agent_id, message, timestamp }
agent_completed   { phase, agent_id, duration_s, summary }
phase_completed   { phase, status: "ok" | "warning" | "error", artifacts }
waiting_for_human { phase, widget_type, payload }
  widget_type:
    "hu_editor"        → renderizar Widget 1
    "kpi_validator"    → renderizar Widget 2
    "dashboard_review" → renderizar Widget 3
    "checkpoint"       → renderizar Widget 4
session_completed { summary, dashboard_url, scheduled_review_date }
session_error     { phase, agent_id, error, recovery_options }
```

### Integración en el ProcessMonitor

El Agent Workspace se integra como una **pestaña nueva** en el ProcessMonitor existente, con badge de notificación cuando hay sesiones con input pendiente. Comparte el mismo backend WebSocket ya implementado para los logs en vivo — el patron de streaming no es nuevo en la infraestructura.

---

## 7. Stack tecnológico

### Backbone LLM

| Componente | Tecnología | Justificación |
|---|---|---|
| **LLM principal** | Azure OpenAI GPT-4o | Razonamiento complejo, generación de código, matching semántico |
| **LLM embeddings** | Azure OpenAI text-embedding-3-large | Vectorización de la Wiki para búsqueda semántica |
| **LLM ligero (clasificación)** | GPT-4o-mini | Tareas de baja complejidad (clasificar dominio, validar HU) |

### Framework agéntico

| Componente | Tecnología | Justificación |
|---|---|---|
| **Orquestación multi-agente** | LangGraph | Flujos stateful con bifurcaciones, ciclos y checkpoints humanos; ideal para el Onboarding Orchestrator |
| **Agentes reactivos** | LangChain Agents | AG-4 y AG-5 siguen un patrón ReAct más simple; LangChain es suficiente |
| **Protocolo de herramientas** | MCP (Model Context Protocol) | Estándar abierto para exponer el framework como herramientas invocables por LLMs |
| **Memoria de trabajo** | Redis | Estado de sesión de agentes entre turnos; contexto del Orchestrator entre fases |

### Almacenamiento especializado

| Componente | Tecnología | Uso |
|---|---|---|
| **Wiki vectorial** | Azure AI Search | Índice semántico de los 41+ indicadores para búsqueda por similitud |
| **Grafo de linaje** | Azure Cosmos DB (API Gremlin) | Grafo de relaciones KPI ↔ campo ↔ artefacto ↔ proceso |
| **Catálogo de datos** | Azure Cosmos DB (API NoSQL) | Inventario de procesos, contratos, consumidores |
| **Estado de agentes** | Redis | Memoria de trabajo, sesiones en curso |
| **Artefactos de datos** | Azure Blob Storage (existente) | Sin cambio — los agentes acceden vía blob-mcp-server |

### Mensajería y eventos

| Componente | Tecnología | Uso |
|---|---|---|
| **Bus de eventos** | Azure Service Bus | Disparadores event-driven para AG-4 y AG-5 |
| **Tópicos** | `artifact_published` · `execution_completed` · `contract_changed` · `hu_submitted` | Eventos del ciclo de vida del framework |

### Infraestructura de agentes

| Componente | Tecnología | Uso |
|---|---|---|
| **Runtime de agentes** | Azure Container Apps | Hosting de cada agente como servicio independiente |
| **API gateway** | Azure API Management | Punto de entrada unificado para los MCP servers |
| **Secretos** | Azure Key Vault | Credenciales de BD, SAS tokens, API keys de OpenAI |
| **Observabilidad agentes** | Azure Application Insights | Trazas, latencias, errores de los agentes |
| **CI/CD** | GitHub Actions | Deploy de agentes al actualizar el código |

---

## 8. Infraestructura y modelo de despliegue

### Diagrama de infraestructura

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         Azure Cloud                                       │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │                    Azure Container Apps                              │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │ │
│  │  │  AG-1    │ │  AG-2    │ │  AG-3    │ │  AG-4    │ │  AG-5    │ │ │
│  │  │HU Analyst│ │KPI Recomm│ │Dashboard │ │DataHealth│ │Lineage   │ │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │ │
│  │                                                                       │ │
│  │  ┌──────────────────────────────────────────────────────────────┐   │ │
│  │  │                AG-6 Onboarding Orchestrator                   │   │ │
│  │  └──────────────────────────────────────────────────────────────┘   │ │
│  │                                                                       │ │
│  │  MCP Servers: wiki · blob · monitor · lineage                        │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────────────────┐  │
│  │  Azure OpenAI  │  │  Azure AI Search │  │  Azure Service Bus       │  │
│  │  GPT-4o        │  │  (Wiki vectors)  │  │  (Event bus)             │  │
│  └────────────────┘  └─────────────────┘  └──────────────────────────┘  │
│                                                                            │
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────────────────┐  │
│  │  Azure Cosmos  │  │  Azure Blob      │  │  Azure Key Vault         │  │
│  │  DB (Lineage + │  │  Storage         │  │  (Secretos)              │  │
│  │  Catálogo)     │  │  (existente)     │  │                          │  │
│  └────────────────┘  └─────────────────┘  └──────────────────────────┘  │
│                                                                            │
│  ┌───────────────────────────────────────────────────────────────────┐   │
│  │              Redis Cache (Estado y memoria de agentes)             │   │
│  └───────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
         │
         │  (API / WebSocket)
         ▼
┌────────────────────────────────────────────────────────┐
│           Infraestructura local existente               │
│  ProcessMonitor (Flask:5052 · React:5173)              │
│  Motor de extracción (Python)                          │
│  Dashboards de presentación (React/Svelte Vite)        │
│  Windows Task Scheduler (→ en migración)               │
└────────────────────────────────────────────────────────┘
```

### Modelo de escala de los agentes

Los agentes no requieren escala continua. El patrón de carga es:

| Agente | Patrón de carga | Escala |
|---|---|---|
| AG-1 HU Analyst | Bajo y esporádico (una solicitud a la vez) | Scale-to-zero (Container Apps) |
| AG-2 KPI Recommender | Bajo y esporádico | Scale-to-zero |
| AG-3 Dashboard Composer | Bajo y esporádico | Scale-to-zero |
| AG-4 Data Health Monitor | Frecuente pero corto (post-publicación + scheduled) | Min 1 instancia en horario laboral |
| AG-5 Lineage Tracker | Frecuente pero corto (post-ejecución) | Min 1 instancia en horario laboral |
| AG-6 Orchestrator | Bajo y esporádico; puede durar horas (checkpoints) | Scale-to-zero + estado en Redis |

**Container Apps** con scale-to-zero es la opción correcta para este perfil: costo mínimo en reposo, escala automática ante demanda.

### Seguridad y acceso

| Aspecto | Implementación |
|---|---|
| **Identidad de los agentes** | Managed Identity por Container App |
| **Acceso a Azure OpenAI** | Via Managed Identity (sin API key en código) |
| **Acceso a Blob** | Via Managed Identity + RBAC (avanza hacia el objetivo del framework) |
| **Secretos de BD** | Azure Key Vault + referencias en Container Apps |
| **Acceso entre agentes** | Internal ingress de Container Apps (no expuesto a internet) |
| **MCP servers** | Acceso interno; AG-X son los únicos clientes |

---

## 9. Integración con el framework existente

La capa agéntica se integra con el framework existente **sin reemplazar** ningún componente. Los puntos de integración son:

### Integración con el ProcessMonitor

El `monitor-mcp-server` consume la API REST existente del ProcessMonitor (Flask:5052). Las nuevas secciones "Salud del dato" y "Salud del consumo" que define el framework v1.1 son alimentadas por el AG-4 vía este server.

El ProcessMonitor también gana una nueva sección: **"Agentes"**, que muestra el estado de los agentes activos, las sesiones de onboarding en curso y los últimos health reports.

### Integración con el Motor de Extracción

El motor de extracción emite eventos a Azure Service Bus al completar cada ejecución. El AG-5 (Lineage Tracker) y el AG-4 (Data Health Monitor) son suscriptores de estos eventos.

El `processes.json` es tanto leído (por los agentes para determinar nivel de madurez) como escrito (por el AG-6 Orchestrator al registrar un nuevo proceso).

### Integración con los Dashboards

Los dashboards del stack canónico exponen un endpoint `/health` que el AG-4 consulta en el chequeo sintético. El AG-3 (Dashboard Composer) genera código para el stack canónico y lo deposita en el directorio del dashboard correspondiente.

### Qué no cambia

- El motor Python de extracción (`ExecutionEngine`, `ExtractorRegistry`) — los agentes no lo reemplazan.
- Azure Blob Storage como destino de artefactos — los agentes leen desde él, no lo reemplazan.
- El ProcessMonitor como interfaz de control — los agentes lo amplían, no lo sustituyen.
- La Wiki de Indicadores como catálogo — los agentes la hacen ejecutable, no la redefinen.

---

## 10. Roadmap de implementación

El roadmap está ordenado por valor entregado y dependencias técnicas. Los MCP servers son la base: sin ellos, los agentes no tienen herramientas.

```
FASE 0 — FUNDACIÓN (Semanas 1–3)
├── Implementar wiki-mcp-server
│     - Cargar los 41 indicadores en Azure AI Search (índice vectorial)
│     - Exponer tools: wiki_search, wiki_kpi_get, wiki_field_match
│     - Exponer tools: wiki_formula_instantiate (proto N2)
├── Implementar blob-mcp-server
│     - contract_get / contract_validate / freshness_check
├── Conectar monitor-mcp-server a la API Flask existente
└── Configurar Azure Service Bus con los tópicos de eventos

FASE 1 — OBSERVABILIDAD DEL DATO (Semanas 4–6)
├── Implementar AG-4 Data Health Monitor
│     - Validación de contrato post-publicación (disparo event-driven)
│     - Chequeo sintético de dashboards (disparo scheduled)
│     - Alertas a Teams / Slack
│     - Sección "Salud del dato" en ProcessMonitor
└── Valor entregado: 0 incidentes de contrato llegan al usuario final

FASE 2 — GOBIERNO Y LINAJE (Semanas 6–9)
├── Implementar lineage-mcp-server
│     - Provisionar Azure Cosmos DB (API Gremlin)
│     - Modelo del grafo de linaje
├── Implementar AG-5 Lineage Tracker
│     - Construcción automática del grafo post-ejecución
│     - Detección de breaking changes en contratos
│     - Catálogo de datos básico
└── Valor entregado: 100% de KPIs productivos con linaje trazable

FASE 3 — WIKI EJECUTABLE + HU ASISTIDA + AGENT WORKSPACE (Semanas 9–13)
├── Implementar AG-2 KPI Recommender (Wiki N2/N3) con HITL
│     - Matching semántico campo ↔ KPI (Fase 1 — automática)
│     - Bucle de validación iterativa (Fase 2 — HITL via chat)
│     - Generación de dataProcessor post-aprobación (Fase 3 — automática)
│     - Elevar indicadores de industria a N2 ejecutable
├── Implementar AG-1 HU Analyst con refinamiento conversacional
│     - Clasificación de dominio
│     - Generación de HU completa (Nivel 1+2+3) desde lenguaje natural
│     - Bucle de refinamiento de la HU via chat
├── Implementar Agent Workspace (§6)
│     - Backend FastAPI + SSE/WebSocket (chat-api-server)
│     - Frontend React + Vercel AI SDK integrado en ProcessMonitor
│     - Estado de sesión en Redis
│     - Renderizado rico: tablas de KPIs, tarjetas de confianza, bloques HU
└── Valor entregado: HU completa en 1 ciclo de revisión; KPIs validados
    por el experto de negocio; dataProcessor generado post-aprobación

FASE 4 — COMPOSICIÓN DE DASHBOARDS (Semanas 13–17)
├── Definir y publicar stack canónico de producción
├── Construir biblioteca de componentes del stack canónico
│     (tarjeta de valor único, serie temporal, distribución, gauge SLA, tabla)
├── Implementar AG-3 Dashboard Composer
│     - Clasificación de KPIs por tipo de visualización
│     - Generación de types.ts, dataProcessor.ts, blobService.ts
│     - Ensamblado de página principal del dashboard
└── Valor entregado: dashboard generado automáticamente para procesos
    con KPIs del catálogo

FASE 5 — ORQUESTADOR DE ONBOARDING (Semanas 17–21)
├── Implementar AG-6 Onboarding Orchestrator (LangGraph)
│     - Grafo de flujo con 7 fases y checkpoints humanos
│     - Integración con AG-1, AG-2, AG-3, AG-4, AG-5
│     - Interfaz en ProcessMonitor: "Nueva solicitud"
├── Activar HU Nivel 3: revisión de adopción a 30 días
└── Valor entregado: ciclo de vida de onboarding < 4 horas para
    procesos Nivel 2; framework opera en su estado objetivo v1.1
```

### Resumen del roadmap

| Fase | Semanas | Agentes | Valor principal |
|---|---|---|---|
| 0 — Fundación | 1–3 | MCP servers | Base técnica para todos los agentes |
| 1 — Observabilidad | 4–6 | AG-4 | Cero incidentes de contrato llegan al usuario |
| 2 — Gobierno | 6–9 | AG-5 | Linaje 100% trazable, breaking changes detectados |
| 3 — Wiki + HU | 9–13 | AG-1, AG-2 | HU asistida, KPIs generados por config |
| 4 — Dashboards | 13–17 | AG-3 | Dashboard generado automáticamente |
| 5 — Orquestador | 17–21 | AG-6 | Ciclo de vida completo automatizado |

**Tiempo total estimado: ~21 semanas** para el sistema multi-agente completo operativo.

---

## 11. Métricas de éxito de la capa agéntica

| Métrica | Objetivo | Agente responsable |
|---|---|---|
| Incidentes de contrato detectados antes del usuario | 100% | AG-4 |
| Cobertura de linaje KPI→origen | 100% procesos productivos | AG-5 |
| Breaking changes detectados antes de despliegue | 100% | AG-5 |
| HUs completadas en ≤ 1 ciclo de revisión | > 85% | AG-1 |
| KPIs generados automáticamente sin código a medida | > 70% (dominios conocidos) | AG-2 |
| Dashboards generados automáticamente | > 70% (KPIs del catálogo) | AG-3 |
| Tiempo del ciclo de onboarding (Nivel 2) | < 4 horas | AG-6 |
| % procesos incorporados en Nivel 2 (solo config) | Creciente trimestre a trimestre | AG-6 |

---

## 12. Glosario

| Término | Definición |
|---|---|
| **Capa agéntica** | Conjunto de agentes LLM que operan sobre el framework BPA DataCentric para automatizar tareas de razonamiento, generación y coordinación |
| **MCP server** | Servidor que expone capacidades del framework como herramientas invocables por agentes LLM, siguiendo el Model Context Protocol |
| **LangGraph** | Framework de orquestación de agentes LLM basado en grafos de flujo con estado; usado para el Onboarding Orchestrator |
| **Agent Workspace** | Superficie de trabajo integrada en el ProcessMonitor que visualiza el estado del proceso de onboarding en tiempo real y renderiza widgets HITL contextuales cuando el grafo requiere input humano |
| **Widget HITL** | Componente de UI específico para cada tipo de decisión humana: Editor de HU, Validador de KPIs, Revisor de Dashboard, Confirmación de Checkpoint |
| **Nodo interrupt** | Nodo de LangGraph que pausa la ejecución del grafo y emite un evento `waiting_for_human` con el tipo de widget requerido |
| **Evento SSE agéntico** | Evento server-sent emitido por LangGraph al frontend: `agent_log`, `phase_completed`, `waiting_for_human`, `session_completed` |
| **Chat Agéntico** | Input de lenguaje natural embebido en los widgets HITL que permite refinamientos textuales; componente de los widgets, no la metáfora principal |
| **Sesión de chat** | Contexto conversacional persistente que cubre todas las fases HITL de un onboarding, mantenido en Redis entre turnos |
| **Output estructurado** | Respuesta del agente en formato rico (tabla de KPIs, bloque de HU, código) renderizada visualmente en el workspace |
| **Human-in-the-loop** | Patrón de diseño agéntico donde el flujo automatizado se pausa en checkpoints para requerir confirmación humana |
| **Scale-to-zero** | Patrón de hosting en Azure Container Apps donde los servicios no consumen recursos cuando no están activos |
| **Event-driven agent** | Agente que se dispara por eventos del sistema (vs. por solicitud directa); patrón de AG-4 y AG-5 |
| **Matching semántico** | Técnica de correspondencia entre campos/conceptos basada en similitud de significado (embeddings), no en igualdad de nombres |
| **ReAct** | Patrón de razonamiento agéntico (Reasoning + Acting) donde el agente alterna entre pensar y usar herramientas |
| **Managed Identity** | Identidad de Azure asignada a un servicio (Container App) para acceder a otros recursos sin credenciales en código |
| **API Gremlin** | API de Azure Cosmos DB para operaciones sobre bases de datos de grafos |
| **Azure AI Search** | Servicio de búsqueda cognitiva de Azure; usado como vector store para la Wiki de Indicadores |
| **Breaking change** | Cambio en un contrato de datos incompatible con las versiones anteriores; requiere notificación a consumidores |

---

*Documento generado: 2026-06-04 · BPA DataCentric · Versión 1.0*
*Referencia: 22_FRAMEWORK_BPA_DATACENTRIC_VISION_EJECUTIVA_v1.1.md*
