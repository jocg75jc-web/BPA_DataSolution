# Verificacion E2E Monitor Integrado - 2026-05-13

## Objetivo
Asegurar continuidad operativa de produccion para el flujo integrado:
- Dashboard monitor (frontend)
- API monitor (backend)
- Ejecucion ONNET y Titania via motor unificado
- Consumo de datos en BD
- Generacion de CSV locales
- Transferencia de CSV a Azure Blob

## Alcance ejecutado
1. Validacion de salud de monitor en API:
- `/api/health`
- `/api/unified/processes`
- `/api/history/onnet`
- `/api/history/titania`
- `/api/analytics/unified`
- `/api/logs/recent?limit=20`

2. Validacion ONNET end-to-end via endpoint del dashboard:
- Trigger: `POST /api/unified/execute/onnet` con `{"model":"all"}`
- Execution ID validado: `exec-1778691551248`
- Resultado API: `success`, `exit_code=0`
- Duracion observada: `251.654684 s`

3. Validacion Titania end-to-end via endpoint del dashboard:
- Trigger: `POST /api/unified/execute/titania` con `{"query":"all"}`
- Execution ID validado: `exec-1778691965752`
- Resultado API: `success`, `exit_code=0`
- Duracion observada: `48.873087 s`

4. Validacion de archivos locales generados:
- ONNET:
  - `1070_TRANSACCIONES_ONNET.csv` actualizado `2026-05-13 12:01:15`
  - `1070_TRANSACCIONES_ONNET_ticketes.csv` actualizado `2026-05-13 12:02:27`
- Titania:
  - `VW_n8n_chat_histories_classfication.csv` actualizado `2026-05-13 12:06:17`
  - `VW_n8n_chat_histories_textual_all.csv` actualizado `2026-05-13 12:06:27`
  - `VW_n8n_chat_history_textual.csv` actualizado `2026-05-13 12:06:34`
  - `VW_n8n_chat_history_textual_analisis_respuestas.csv` actualizado `2026-05-13 12:06:34`
  - `VW_n8n_chat_history_textual_analisis_WordCloud_2.csv` actualizado `2026-05-13 12:06:41`
  - `VW_n8n_chat_user_banned.csv` actualizado `2026-05-13 12:06:41`

5. Validacion de Blob (propiedades remotas):
- ONNET
  - `1070_TRANSACCIONES_ONNET.csv` `2026-05-13T17:03:19+00:00`
  - `1070_TRANSACCIONES_ONNET_ticketes.csv` `2026-05-13T17:03:22+00:00`
- Titania
  - `VW_n8n_chat_histories_classfication.csv` `2026-05-13T17:06:44+00:00`
  - `VW_n8n_chat_histories_textual_all.csv` `2026-05-13T17:06:48+00:00`
  - `VW_n8n_chat_history_textual.csv` `2026-05-13T17:06:50+00:00`
  - `VW_n8n_chat_history_textual_analisis_respuestas.csv` `2026-05-13T17:06:50+00:00`
  - `VW_n8n_chat_history_textual_analisis_WordCloud_2.csv` `2026-05-13T17:06:53+00:00`
  - `VW_n8n_chat_user_banned.csv` `2026-05-13T17:06:54+00:00`

## Hallazgos y acciones correctivas

### 1) Desalineacion de puerto backend/frontend
- Hallazgo: backend podia quedar en `5000` mientras frontend consume `5052`.
- Impacto: ejecuciones disparadas sin visibilidad coherente en dashboard.
- Correccion aplicada:
  - En backend monitor se fijo el default de `PROCESS_MONITOR_PORT` a `5052`.

### 2) Polling redundante en dashboard (riesgo de saturacion)
- Hallazgo: polling de historial/descubrimiento con efectos redundantes y posibilidad de rafagas por re-render.
- Impacto: exceso de requests `GET /api/history/*`, degradando disponibilidad.
- Correcciones aplicadas:
  - Throttle temporal de sync de historial (ventana minima de 4s).
  - Eliminacion de efecto duplicado de `discoverActiveExecution` cada 2s.
  - Se mantiene un flujo de polling mas estable para logs/descubrimiento.

### 3) Segmento no usable detectado
- Hallazgo: `npm run type-check` no era operativo por ausencia de `tsconfig.json`.
- Correcciones aplicadas:
  - Se agrego `tsconfig.json` para habilitar chequeo real.
  - Se corrigio tipado en `ProcessCard` (`Chip.icon` esperaba `ReactElement`).
  - Resultado: `npm run type-check` ejecuta correctamente sin errores.

### 4) Locks huérfanos post-ejecucion
- Hallazgo: locks presentes con PID no vivo (`onnet_export.lock`, `titania_export.lock`).
- Correccion aplicada:
  - Validacion y limpieza de locks huérfanos.
  - Estado final: locks stale removidos.

## Verificacion de consumo de BD
Se evidencio consumo correcto por logs de ambos exportadores:
- Titania: lineas de conexion `Conectando a PostgreSQL ...` y secuencia de export.
- ONNET: secuencia `Combinando consulta ...`, `Exportando ...`, `Archivo generado ...`.

## Estado final
- API monitor: saludable y con endpoints criticos operativos.
- ONNET: E2E validado en success.
- Titania: E2E validado en success.
- CSV locales: actualizados.
- Blob: actualizado para todos los archivos principales.
- Dashboard: recibiendo historial/analytics/logs con backend en puerto alineado.

## Recomendaciones operativas (produccion)
1. Mantener backend monitor con `PROCESS_MONITOR_PORT=5052`.
2. Mantener una sola instancia de dashboard abierta durante validaciones operativas para evitar ruido de polling.
3. Monitorear periodicamente locks en Titania/ONNET y limpiar stale de forma automatizada.
4. Usar `api/history/{process}` + `api/status/{execution_id}` como fuente de verdad de estado en incidentes.
5. Conservar validacion por evidencia (mtime local + blob properties) como criterio de cierre de corrida.
