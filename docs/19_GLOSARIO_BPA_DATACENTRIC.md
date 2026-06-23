# Glosario BPA_DataCentric

## Terminos funcionales

1. BPA_DataCentric
   - Estructura monorepo objetivo para organizar configuracion, entrypoints, datos y operacion.
2. Monitor
   - Aplicacion de observabilidad y control de procesos (backend API + frontend UI).
3. Proceso
   - Unidad ejecutable de extraccion (Titania u ONNET) definida en configuracion.
4. Corrida
   - Ejecucion individual de un proceso, identificada por execution_id.

## Terminos tecnicos de ejecucion

1. ExecutionEngine
   - Motor unificado que coordina configuracion, validacion de parametros y ejecucion de extractores.
2. ProcessEngine
   - Capa del monitor que administra contextos y delega al motor unificado.
3. Extractor
   - Implementacion de adaptacion por sistema (TitaniaExtractor, ONNETExtractor).
4. Entry point
   - Script de entrada estable en DataCentric para invocar el proceso fuente con contrato estandar.
5. Bridge
   - Script intermedio de estabilidad que reemplaza/acompaña el script legacy cuando aplica.

## Terminos de configuracion

1. processes.json
   - Archivo canonico que define proyectos, ejecucion, parametros, outputs y scheduling.
2. runtime_env_contract.json
   - Contrato de variables de entorno criticas y recomendadas.
3. Profile
   - Plantilla de entorno (dev, stage, prod) con rutas y variables runtime.
4. ConfigLoader
   - Componente que carga JSON y resuelve variables ${VAR}.

## Terminos de datos y artefactos

1. Querys
   - Directorio de sentencias SQL por sistema.
2. Outputs
   - Directorio de CSV generados por cada corrida.
3. Parametros
   - Directorio de configuraciones operativas, credenciales y .env por sistema.
4. Artefacto
   - Archivo generado por extraccion (CSV) y validado en evidencia local/remota.

## Terminos de observabilidad y operacion

1. API health
   - Endpoint de salud del backend monitor.
2. Historial
   - Registro de corridas previas por proceso (estado, duracion, errores).
3. Logs en tiempo real
   - Flujo de eventos de ejecucion emitidos por backend y consumidos por frontend.
4. Evidence gate
   - Criterio de validacion por evidencia API + archivo local + Blob remoto.

## Terminos de control de concurrencia

1. Lock
   - Mecanismo para evitar solapes de ejecucion sobre el mismo proceso.
2. Lock stale
   - Lock huerfano o vencido que ya no representa una ejecucion activa.
3. Scheduler integrado
   - Programador en backend monitor que dispara corridas por expresion cron.
4. Scheduler externo
   - Programacion por fuera del monitor (ejemplo: tareas del sistema operativo).

## Terminos de conexion

1. API_BASE_URL
   - URL base del backend usada por frontend para consumir endpoints.
2. PROCESS_MONITOR_PORT
   - Puerto de exposicion del backend monitor.
3. AZURE_BLOB_ACCOUNT_URL
   - URL de cuenta Blob para transferencia de artefactos.
4. AZURE_BLOB_SAS_TOKEN
   - Token SAS para autenticacion a Blob.
5. AZURE_BLOB_CONTAINER
   - Contenedor destino de artefactos.

## Terminos de soporte

1. L1
   - Soporte operativo de primera linea (monitoreo, verificacion, escalamiento).
2. L2
   - Soporte tecnico especializado (diagnostico de codigo, configuracion y runtime).
3. Smoke test
   - Prueba corta de validacion de salud funcional despues de un cambio.
4. Rollback
   - Reversion controlada a configuracion/estado anterior estable.
