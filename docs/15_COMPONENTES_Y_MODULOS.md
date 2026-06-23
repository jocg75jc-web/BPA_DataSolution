# Componentes y Modulos

## Vista general de componentes

1. Monitor Backend (API + Socket.IO)
2. Monitor Frontend (UI React)
3. Motor Unificado de Extraccion (Execution Engine)
4. Extractores (Titania y ONNET)
5. Entry points unificados en BPA_DataCentric
6. Capa de configuracion y contratos runtime
7. Fuentes externas (BD Titania/ONNET)
8. Almacenamiento externo (Azure Blob)

## Componente 1: Monitor Backend

Ubicacion de codigo activo:

1. C:/Users/javier.castaneda/botsquad/ProcessMonitor/backend/api.py
2. C:/Users/javier.castaneda/botsquad/ProcessMonitor/backend/process_engine.py

Responsabilidad:

1. Exponer API REST de procesos, ejecuciones, logs, health e historia.
2. Publicar eventos en tiempo real mediante Socket.IO.
3. Delegar ejecucion al motor parametrizable (ProcessEngine).
4. Gestionar scheduler integrado (si ENABLE_INTEGRATED_SCHEDULER=true).

Modulos y objetos clave:

1. app (Flask), socketio (Flask-SocketIO)
2. engine (instancia ProcessEngine)
3. Endpoints principales:
   - GET /api/health
   - GET /api/unified/processes
   - GET /api/unified/processes/<process_id>
   - POST /api/unified/execute/<process_id>
   - GET /api/status/<execution_id>
   - GET /api/logs/<execution_id>
   - GET /api/history/<process_id>

## Componente 2: Monitor Frontend

Ubicacion de codigo activo:

1. C:/Users/javier.castaneda/botsquad/ProcessMonitor/components/ProcessDashboard.tsx
2. C:/Users/javier.castaneda/botsquad/ProcessMonitor/components/ProcessGrid.tsx
3. C:/Users/javier.castaneda/botsquad/ProcessMonitor/components/ProcessCard.tsx
4. C:/Users/javier.castaneda/botsquad/ProcessMonitor/components/LogViewer.tsx

Responsabilidad:

1. Mostrar procesos, estado, historial, logs y analitica operativa.
2. Disparar ejecuciones manuales via API del backend.
3. Visualizar progreso y resultados en tiempo real.

Modulos clave:

1. ProcessDashboard: orquestacion de pantalla, tabs, analytics y sincronizacion.
2. ProcessGrid: filtros y render de tarjetas de proceso.
3. ProcessCard: acciones de ejecutar/detener/detalles.
4. LogViewer: seguimiento de logs con filtros y descarga.

## Componente 3: Motor Unificado de Extraccion

Ubicacion de codigo activo:

1. C:/Users/javier.castaneda/botsquad/BPA_DataSolution/unified_extraction/core/execution_engine.py
2. C:/Users/javier.castaneda/botsquad/BPA_DataSolution/unified_extraction/core/config_loader.py
3. C:/Users/javier.castaneda/botsquad/BPA_DataSolution/unified_extraction/core/parameter_validator.py
4. C:/Users/javier.castaneda/botsquad/BPA_DataSolution/unified_extraction/core/runtime_env_validator.py

Responsabilidad:

1. Cargar y resolver configuracion de procesos.
2. Validar parametros por proceso.
3. Ejecutar extractor correspondiente.
4. Devolver resultado uniforme con execution_id, status, success y duracion.

Objetos clave:

1. ExecutionEngine
2. ConfigLoader
3. ParameterValidator
4. validate_runtime_environment

## Componente 4: Extractores

Ubicacion de codigo activo:

1. C:/Users/javier.castaneda/botsquad/BPA_DataSolution/unified_extraction/extractors/base.py
2. C:/Users/javier.castaneda/botsquad/BPA_DataSolution/unified_extraction/extractors/titania.py
3. C:/Users/javier.castaneda/botsquad/BPA_DataSolution/unified_extraction/extractors/onnet.py
4. C:/Users/javier.castaneda/botsquad/BPA_DataSolution/unified_extraction/extractors/registry.py

Responsabilidad:

1. Construir comando de ejecucion por sistema.
2. Ejecutar subprocess con timeout.
3. Validar resultado post-run (existencia, tamano y frescura de archivos).

Objetos clave:

1. BaseExtractor
2. TitaniaExtractor
3. ONNETExtractor
4. ExtractorRegistry

## Componente 5: Entry points unificados DataCentric

Ubicacion:

1. C:/Users/javier.castaneda/botsquad/BPA_DataCentric/services/extraction-runner/entrypoints/titania_entrypoint.py
2. C:/Users/javier.castaneda/botsquad/BPA_DataCentric/services/extraction-runner/entrypoints/onnet_entrypoint.py

Responsabilidad:

1. Resolver python y script objetivo por sistema.
2. Priorizar bridge estable si existe.
3. Reenviar argumentos estandarizados desde el motor.
4. Uniformar punto de entrada operativo para monorepo.

## Componente 6: Configuracion y contratos

Ubicacion:

1. C:/Users/javier.castaneda/botsquad/BPA_DataSolution/unified_extraction/config/processes.json
2. C:/Users/javier.castaneda/botsquad/BPA_DataSolution/unified_extraction/config/processes.schema.json
3. C:/Users/javier.castaneda/botsquad/BPA_DataSolution/unified_extraction/config/runtime_env_contract.json
4. C:/Users/javier.castaneda/botsquad/BPA_DataCentric/config/profiles/dev.env.example
5. C:/Users/javier.castaneda/botsquad/BPA_DataCentric/config/profiles/stage.env.example
6. C:/Users/javier.castaneda/botsquad/BPA_DataCentric/config/profiles/prod.env.example

Responsabilidad:

1. Definir procesos, parametros, scheduling y rutas.
2. Estandarizar variables por entorno.
3. Aplicar fail-fast sobre variables criticas/recomendadas.
