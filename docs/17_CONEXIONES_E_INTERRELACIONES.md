# Conexiones e Interrelaciones

## Flujo end-to-end de ejecucion

1. Usuario ejecuta proceso desde frontend monitor.
2. Frontend invoca endpoint POST /api/unified/execute/<process_id> en backend.
3. Backend delega a ProcessEngine.execute_process.
4. ProcessEngine delega a ExecutionEngine.execute (motor unificado).
5. ExecutionEngine selecciona extractor por id.
6. Extractor arma comando usando entrypoint en BPA_DataCentric.
7. Entry point invoca script/bridge del sistema fuente (Titania u ONNET).
8. Script ejecuta consultas en base de datos y genera CSV.
9. Script realiza upload de artefactos a Azure Blob (segun configuracion/credencial).
10. Backend publica estado y logs en API/Socket.IO.
11. Frontend refleja progreso, estado final e historial.

## Estructuras de conexion

## Conexion Frontend -> Backend

1. Protocolo: HTTP/REST y Socket.IO.
2. URL base por defecto en frontend: http://127.0.0.1:5052.
3. Puerto operativo backend: 5052.
4. Endpoints de control: health, processes, execute, status, logs, history.

## Conexion Backend -> Motor unificado

1. Integracion en memoria (import Python).
2. Punto de carga: ProcessEngine._try_init_unified_engine().
3. Configuracion usada: BPA_DataSolution/unified_extraction/config/processes.json.

## Conexion Motor -> Extractores

1. Resolucion por registry segun execution.extractor.
2. Validacion previa de parametros y runtime contract.
3. Ejecucion en subprocess con timeout configurable.

## Conexion Extractores -> Entry points

1. Script de ejecucion configurado en processes.json apunta a:
   - BPA_DataCentric/services/extraction-runner/entrypoints/titania_entrypoint.py
   - BPA_DataCentric/services/extraction-runner/entrypoints/onnet_entrypoint.py
2. Workdir de ejecucion apuntado a services/extraction-runner.

## Conexion Entry points -> Scripts fuente

1. Titania: prioriza export_queries_bridge.py, fallback a export_queries_to_csv.py.
2. ONNET: prioriza export_onnet_bridge.py, fallback a export_onnet_csv.py.
3. Python de ejecucion por sistema configurable por variables de entorno.

## Conexion Scripts fuente -> Datos externos

1. Titania: conexion a PostgreSQL para ejecutar SQL.
2. ONNET: conexion a fuente operativa segun .env.
3. Ambos: upload a Azure Blob con credenciales runtime.

## Interrelacion de configuracion y datos

1. profiles (*.env.example) define rutas y variables de entorno por entorno.
2. processes.json consume variables y resuelve rutas finales por ConfigLoader.
3. Parametros/Titania y Parametros/Onnet proveen credenciales operativas.
4. Querys/Titania y Querys/Onnet proveen SQL de extraccion.
5. Outputs/Titania y Outputs/Onnet conservan evidencia local de corridas.

## Contratos de interoperabilidad

1. Contrato de parametros de API
   - Titania: query, database (opcional).
   - ONNET: model.
2. Contrato de estado de ejecucion
   - status, start_time, end_time, exit_code, error_message.
3. Contrato de logs
   - timestamp, level, message, source.
4. Contrato de runtime
   - validacion de variables criticas y recomendadas.

## Dependencias operativas criticas

1. use_reloader=False en backend Flask para evitar perdida de disponibilidad del motor unificado.
2. Reinicio controlado del backend cuando cambie processes.json (recarga de configuracion en memoria).
3. Coherencia de puerto/API base entre frontend y backend.
4. Unica instancia activa de scheduler para evitar solapes y conflictos de lock.

## Diagrama textual de interrelacion

1. Frontend Monitor -> Backend API/Socket
2. Backend API -> ProcessEngine
3. ProcessEngine -> ExecutionEngine
4. ExecutionEngine -> Extractor (Titania/ONNET)
5. Extractor -> Entry point DataCentric
6. Entry point -> Script/Bridge fuente
7. Script/Bridge -> DB + CSV local + Azure Blob
8. Backend <- logs/estado/resultados -> Frontend
