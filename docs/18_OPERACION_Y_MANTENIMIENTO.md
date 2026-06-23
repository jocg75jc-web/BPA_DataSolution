# Operacion y Mantenimiento

## Objetivo operativo

Asegurar continuidad de ejecucion Titania/ONNET, observabilidad en monitor y trazabilidad de artefactos locales/remotos.

## Checklist diario de primer nivel

1. Verificar health backend (GET /api/health).
2. Verificar disponibilidad de procesos (GET /api/unified/processes).
3. Confirmar scheduler en modo esperado (activo o desactivado segun operacion).
4. Confirmar no existencia de locks stale.
5. Validar ultima corrida ONNET en success y con artefactos actualizados.
6. Validar ultima corrida Titania en success y con artefactos actualizados.
7. Confirmar sincronia de historial y logs en dashboard.

## Procedimiento de ejecucion manual controlada

1. Seleccionar proceso desde monitor.
2. Ejecutar con parametros validos (query/model).
3. Registrar execution_id.
4. Consultar estado con GET /api/status/<execution_id> hasta estado terminal.
5. Revisar logs en API/monitor para errores o warnings.
6. Confirmar artefactos en Outputs locales correspondientes.
7. Confirmar artefactos en Azure Blob (last_modified actualizado).

## Procedimiento de cambio de configuracion

1. Editar config canonica en BPA_DataSolution/unified_extraction/config/processes.json.
2. Validar configuracion con scripts de validacion de unified_extraction.
3. Reiniciar backend monitor para recargar configuracion en memoria.
4. Verificar respuesta de /api/unified/processes con rutas esperadas.
5. Ejecutar prueba smoke ONNET y Titania.
6. Registrar evidencia en documento de cambio.
7. Actualizar documentacion tecnica y operacional del paquete docs segun impacto del cambio.
8. Registrar entrada de avance en 20_BITACORA_CAMBIOS_DOCUMENTACION.md.

## Troubleshooting L1/L2

## Caso A: /api/unified/processes muestra rutas antiguas

1. Causa probable: backend con configuracion cacheada en memoria.
2. Accion:
   - Reiniciar backend monitor.
   - Reconsultar endpoint.

## Caso B: execution_id queda en running por tiempo anomalo

1. Revisar timeout configurado en execution.timeout_seconds.
2. Revisar logs de subprocess y conectividad a BD.
3. Validar lock de proceso.
4. Si aplica, detener ejecucion y limpiar lock stale de forma controlada.

## Caso C: status=success pero sin evidencia de actualizacion

1. Verificar validacion post-run en extractor.
2. Verificar mtime y tamano de archivos en Outputs.
3. Verificar last_modified en Blob remoto.
4. Tratar como falso exito si falta evidencia de frescura.

## Caso D: unified_engine_available=false

1. Verificar arranque del backend con use_reloader=False.
2. Verificar rutas y permisos de BPA_DataSolution/unified_extraction.
3. Verificar importacion de modulos en process_engine.py.

## Caso E: conflictos por doble scheduler

1. Garantizar una sola fuente de scheduler activa.
2. Si se usa scheduler integrado, desactivar ejecuciones duplicadas externas.
3. Auditar locks y corridas solapadas en historial.

## Runbook de respaldo y recuperacion

1. Respaldo de configuracion:
   - processes.json
   - runtime_env_contract.json
   - perfiles de entorno
2. Respaldo de querys y parametros:
   - Querys/Titania y Querys/Onnet
   - Parametros/Titania y Parametros/Onnet
3. Recuperacion:
   - Restaurar configuracion y perfiles.
   - Reiniciar backend.
   - Ejecutar smoke tests ONNET y Titania.
   - Confirmar estado, logs y evidencia de artefactos.

## Indicadores operativos recomendados

1. Tasa de ejecuciones success por proceso.
2. Duracion promedio por proceso.
3. Cantidad de fallos por causa (conexion, lock, timeout, validacion).
4. Tiempo de deteccion y resolucion de incidentes.
5. Cantidad de ejecuciones con evidencia completa local+Blob.

## Reglas de oro de mantenimiento

1. No introducir secretos en codigo versionado.
2. No cambiar rutas sin validar procesos y monitor.
3. No cerrar incidente sin evidencia API + local + Blob.
4. No operar con dos schedulers activos sobre el mismo proceso.
5. Documentar cada cambio operativo con fecha, causa y evidencia.
