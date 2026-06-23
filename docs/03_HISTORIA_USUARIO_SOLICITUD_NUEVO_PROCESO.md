# Plantilla de Historia de Usuario para Nuevo Proceso (E2E + Presentacion)

## 1. Objetivo
Este documento define como solicitar un nuevo proceso en BPA_DataSolution bajo enfoque de framework end to end: adquisicion, procesamiento, publicacion y presentacion de informacion clave para consumo operativo y de negocio.

## 2. Historia de usuario base (nivel proceso)
Como [rol solicitante]
quiero [nuevo proceso de extraccion/generacion/descarga]
para [objetivo de negocio medible].

## 2.1 Historia de usuario complementaria (nivel presentacion)
Como [rol consumidor de informacion]
quiero [visualizar indicadores y tendencias del proceso en dashboard]
para [tomar decisiones y detectar desvio operativo en tiempo objetivo].

## 3. Informacion obligatoria de la solicitud
### 3.1 Datos del solicitante
- Area:
- Responsable funcional:
- Responsable tecnico:
- Fecha requerida:
- Prioridad: Alta | Media | Baja

### 3.2 Definicion funcional
- Nombre del proceso:
- Descripcion corta:
- Frecuencia esperada: on-demand | horario | diario | semanal | mensual
- Ventana de datos: fecha inicio/fin o regla relativa
- SLA esperado (ejecucion):
- SLA esperado (disponibilidad del archivo):

### 3.3 Origen de datos
- Tipo de origen: PostgreSQL | SQL Server | MySQL | Oracle | MongoDB | API REST | Archivo
- Motor/version:
- Host/endpoint:
- Base/schema/coleccion:
- Metodo de autenticacion:
- Driver requerido:
- Volumen estimado por corrida:

### 3.4 Logica de extraccion
- Query o criterio de filtro:
- Campos requeridos:
- Campos opcionales:
- Reglas de calidad (nulos, duplicados, llaves):
- Reglas de anonimizado (si aplica):

### 3.5 Salida
- Formato: CSV | JSON | Parquet | Excel
- Convencion de nombre de archivo:
- Particionado (si aplica):
- Compresion (si aplica):
- Retencion requerida:

### 3.6 Destino de almacenamiento
- Destino: Azure Blob | ADLS Gen2 | AWS S3 | Google Cloud Storage | SFTP | SharePoint | OneDrive | File Share SMB/NFS
- Ruta/bucket/contenedor:
- Region:
- Cifrado requerido:
- Politica de acceso:

### 3.7 Operacion y observabilidad
- Horario permitido de ejecucion:
- Reintentos requeridos:
- Notificaciones: email | webhook | teams | slack
- Criterio de exito:
- Criterio de fallo:

### 3.8 Metricas y dashboard (obligatorio)
- Objetivo de monitoreo: Operacion diaria | Cumplimiento SLA | Capacidad | Calidad de datos
- Nivel de criticidad: Critico | Alto | Medio | Bajo
- KPIs minimos requeridos:
	- Volumen: total de registros por corrida
	- Latencia: duracion de corrida (inicio-fin)
	- Confiabilidad: tasa de exito/fallo por periodo
	- Calidad: completitud de campos criticos
- SLI/SLO definidos (formato sugerido):
	- SLI 1:
	- Meta SLO 1:
	- SLI 2:
	- Meta SLO 2:
- Baseline y umbrales:
	- Baseline historico (ultimos 30 dias):
	- Umbral warning:
	- Umbral critico:
- Ventanas de evaluacion:
	- Operativa: 1h o por corrida
	- Tactica: diario
	- Ejecutiva: semanal/mensual
- Evidencia en dashboard:
	- Pagina/tablero objetivo:
	- Visuales minimos: KPI cards, tendencia temporal, distribucion, top fallos
	- Filtros minimos: fecha, proceso, estado, origen/destino

### 3.9 Capa de presentacion (obligatorio)
- Tipo de consumidor: Operaciones | Lider tecnico | Analista negocio | Direccion
- Decisiones que habilita el dashboard:
- Preguntas clave que debe responder:
- Latencia maxima de visualizacion (SLA de presentacion):
- Nivel de detalle requerido: ejecutivo | operativo | diagnostico
- Navegacion esperada: resumen -> detalle de corrida -> evidencia de logs
- Contrato de datos para visualizacion:
	- Entidades: ejecucion, KPI, evento, alerta
	- Campos minimos por entidad:
	- Reglas de refresco (push/polling/manual):
- Requisitos UX minimos:
	- Estado sin datos
	- Estado de error recuperable
	- Indicador de ultima actualizacion
	- Consistencia de etiquetas entre procesos

## 4. Criterios de aceptacion
1. El proceso ejecuta con parametros definidos y validados.
2. La salida llega al destino correcto con formato correcto.
3. Se registra trazabilidad completa (inicio, fin, estado, error, volumen).
4. Las alertas se disparan ante fallo o retraso.
5. Existe evidencia de prueba funcional y tecnica.
6. Existen SLI/SLO definidos y visibles en dashboard con umbrales warning/critico.
7. Se puede identificar en menos de 5 minutos la causa probable de una falla (error, timeout, calidad, capacidad).
8. La capa de presentacion permite lectura ejecutiva y diagnostico operativo sin depender de consultas manuales.
9. El dashboard muestra evidencia de actualizacion de datos (timestamp y fuente).
10. Los indicadores criticos mantienen definicion unica y consistente para todos los procesos del framework.

## 5. Definicion de listo (DoR)
- Solicitud completa en esta plantilla.
- Credenciales y permisos validados.
- Query/filtros aprobados por negocio.
- Destino de almacenamiento confirmado.
- Alcance de presentacion definido (consumidor, decisiones, KPIs y vistas).

## 6. Definicion de terminado (DoD)
- Configuracion en `processes.json` aplicada.
- Extractor implementado o reutilizado.
- Pruebas exitosas.
- Monitoreo visible en ProcessMonitor.
- Documento de memoria actualizado.
- KPIs minimos publicados y validados contra una corrida real.
- Alertas probadas (warning y critico) con evidencia.
- Capa de presentacion validada por usuario consumidor (operaciones/negocio).
- Evidencia E2E registrada: origen -> procesamiento -> destino -> dashboard.

## 7. Ejemplo corto (base Titania/ONNET)
Como Analista de Operaciones,
quiero exportar transacciones ONNET por modelo y fecha,
para publicar un archivo diario en ADLS usado por BI.

Como Lider de Operaciones,
quiero visualizar en dashboard la ejecucion, cumplimiento SLA y calidad del proceso ONNET,
para detectar desvio en menos de 5 minutos y accionar correccion.

Criterios:
- Frecuencia diaria 07:30.
- Formato CSV UTF-8.
- Destino ADLS contenedor bi-raw/onnet/daily.
- Alertar por webhook si falla dos veces consecutivas.
- SLI Tasa de exito diaria >= 99%.
- SLI Duracion p95 por corrida <= 15 min.
- Dashboard con KPI de volumen, latencia, tasa de exito y ultima actualizacion por fuente.
