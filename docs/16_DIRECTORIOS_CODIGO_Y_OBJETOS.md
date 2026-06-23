# Directorios, Codigo y Objetos

## Estructura principal BPA_DataCentric

1. apps
2. config
3. data
4. docs
5. ops
6. Outputs
7. Parametros
8. Querys
9. scripts
10. services
11. shared

## Directorios funcionales y uso

### apps

1. apps/monitor-backend: reservado para contener backend del monitor en consolidacion futura.
2. apps/monitor-frontend: reservado para contener frontend del monitor en consolidacion futura.

Estado actual:

1. La implementacion activa del monitor se ejecuta desde ProcessMonitor.

### services

1. services/extraction-runner/entrypoints: contiene puntos de entrada unificados.

Archivos:

1. titania_entrypoint.py
2. onnet_entrypoint.py

### config

1. config/profiles: perfiles runtime por entorno.

Archivos:

1. dev.env.example
2. stage.env.example
3. prod.env.example

### data

1. data/querys: organizacion estandar de SQL por sistema.
2. data/outputs: organizacion estandar de CSV de salida por sistema.
3. data/parametros: organizacion estandar de parametros operativos por sistema.

### Querys, Outputs, Parametros (raiz)

1. Querys/Titania y Querys/Onnet: ubicaciones operativas vigentes de queries.
2. Outputs/Titania y Outputs/Onnet: evidencias locales de extraccion.
3. Parametros/Titania y Parametros/Onnet: credenciales y variables por sistema.

### scripts

1. bootstrap_sprint1_structure.ps1: crea estructura base de monorepo.
2. validate_blob_last_modified.py: valida last_modified en Azure Blob para artefactos esperados.

## Objetos de codigo clave

## Monitor Backend (ProcessMonitor/backend/process_engine.py)

1. ProcessEngine
   - Carga configuracion y mantiene contextos de ejecucion.
   - Integra motor unificado si esta disponible.
2. ExecutionContext
   - Objeto de estado por corrida (execution_id, status, logs, recursos, error).
3. ProcessStatus
   - Enum de estados: idle, running, success, failed, stopped.

## Motor Unificado (BPA_DataSolution/unified_extraction)

1. ExecutionEngine
   - Punto central de ejecucion de procesos.
2. ConfigLoader
   - Carga JSON, valida estructura y resuelve variables ${VAR}.
3. BaseExtractor
   - Contrato abstracto para ejecucion y validacion post-run.
4. TitaniaExtractor
   - Construye comando Titania y valida artefactos esperados.
5. ONNETExtractor
   - Construye comando ONNET y valida artefactos esperados.

## Contratos de configuracion

### Objeto Project (processes.json)

Campos criticos:

1. id
2. name
3. execution
4. parameters
5. outputs
6. scheduling
7. metadata

### Objeto execution

Campos criticos:

1. extractor
2. script
3. workdir
4. python
5. timeout_seconds
6. query_dir o env_file segun proceso
7. credentials_file en Titania

### Objeto result de ejecucion (salida del engine)

Campos:

1. execution_id
2. project_id
3. status
4. success
5. duration_seconds
6. parameters
7. result (returncode, stdout, stderr, command, workdir)

## Matriz de activos para mantenimiento

1. Activo: Config canonica
   - Ubicacion: BPA_DataSolution/unified_extraction/config/processes.json
   - Accion de mantenimiento: ajustar rutas/params/schedule con validacion previa.
2. Activo: Entry points DataCentric
   - Ubicacion: BPA_DataCentric/services/extraction-runner/entrypoints
   - Accion: mantener compatibilidad de args y fallback a bridge.
3. Activo: API monitor
   - Ubicacion: ProcessMonitor/backend/api.py
   - Accion: validar endpoints unificados y salud de scheduler.
4. Activo: Frontend monitor
   - Ubicacion: ProcessMonitor/components
   - Accion: mantener polling estable y visualizacion de estado/logs.
