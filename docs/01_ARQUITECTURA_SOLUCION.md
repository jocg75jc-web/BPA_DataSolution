# Arquitectura de la Solucion

## 1. Vision general
BPA_DataSolution centraliza la definicion y ejecucion de procesos de extraccion y descarga de informacion para multiples proyectos.

## 2. Capas
1. Capa de configuracion:
- `processes.json`
- `processes.schema.json`

2. Capa de orquestacion:
- `ConfigLoader`
- `ParameterValidator`
- `ExecutionEngine`

3. Capa de implementacion por conector:
- `BaseExtractor`
- `TitaniaExtractor`
- `ONNETExtractor`
- `ExtractorRegistry`

4. Capa de integracion:
- Scripts de migracion/validacion.
- Integracion con ProcessMonitor.

## 3. Flujo funcional
1. Usuario define proyecto y parametros.
2. Engine carga configuracion.
3. Validator valida y normaliza parametros.
4. Registry selecciona extractor.
5. Extractor construye comando.
6. Engine ejecuta y captura resultado.
7. Monitor consume estado y logs.

## 4. Diagrama textual
- ProcessMonitor -> API/Engine -> ConfigLoader -> ParameterValidator -> ExtractorRegistry -> Extractor -> Source DB/API -> Archivo de salida -> Destino de almacenamiento.

## 5. Principios de diseno
- Configuracion sobre codigo hardcoded.
- Desacople por extractor.
- Extension por contrato estable.
- Observabilidad desde el inicio.
- Compatibilidad con pipelines legados.

## 6. Patrones para crecer
- Nuevo origen: agregar extractor + definicion en config.
- Nuevo destino: agregar estrategia de entrega (blob/s3/sftp/sharepoint/etc).
- Nueva validacion: ampliar tipos en validator sin romper extractores.

## 7. Requisitos no funcionales
- Trazabilidad completa por ejecucion.
- Idempotencia de salidas por ventana de tiempo.
- Seguridad de credenciales y secretos.
- Recuperacion ante fallos transitorios.
- Alertamiento accionable.

## 8. Riesgos tecnicos
- Dependencia de red/DNS para DB remota.
- Saturacion por procesos largos o paralelos.
- Error humano por solicitudes incompletas.
- Diferencias de drivers entre motores de base de datos.

## 9. Estrategia de mitigacion
- Timeout y retry configurables.
- Health checks previos de conectividad.
- Plantilla obligatoria de solicitud.
- Matriz de compatibilidad por origen y destino.
