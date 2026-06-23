# Gate de aceptacion BPA_DataCentric - 2026-05-13

## Objetivo

Validar que el motor unificado opera correctamente con rutas migradas a BPA_DataCentric, bajo criterio de continuidad operativa.

## Alcance

1. Dos ciclos consecutivos ONNET + Titania ejecutados manualmente desde el engine.
2. Verificacion de outputs en rutas nuevas BPA_DataCentric.
3. Verificacion de estado de locks huerfanos.
4. Verificacion de guardrail fail-fast de entorno.

## Ejecuciones realizadas

### Ciclo 1

1. ONNET
- execution_id: 98e82088-c88d-4960-b158-456d0dca7e1f
- status: completed
- duration_seconds: 272.321

2. Titania
- execution_id: 62ecc5aa-721f-441d-994b-d3c7d9844ad8
- status: completed
- duration_seconds: 51.972

### Ciclo 2

1. ONNET
- execution_id: 5168938c-fb58-4458-8998-9213c41acc83
- status: completed
- duration_seconds: 250.886

2. Titania
- execution_id: b322443a-0a3d-4611-a01d-500b5afad808
- status: completed
- duration_seconds: 49.771

## Evidencia local de outputs (rutas migradas)

### ONNET
- BPA_DataCentric/Outputs/Onnet/1070_TRANSACCIONES_ONNET.csv
- BPA_DataCentric/Outputs/Onnet/1070_TRANSACCIONES_ONNET_ticketes.csv
- Ambos archivos actualizados en ventana 17:06-17:08 local aprox.

### Titania
- BPA_DataCentric/Outputs/Titania/VW_n8n_chat_histories_classfication.csv
- BPA_DataCentric/Outputs/Titania/VW_n8n_chat_histories_textual_all.csv
- BPA_DataCentric/Outputs/Titania/VW_n8n_chat_history_textual.csv
- BPA_DataCentric/Outputs/Titania/VW_n8n_chat_history_textual_analisis_respuestas.csv
- BPA_DataCentric/Outputs/Titania/VW_n8n_chat_history_textual_analisis_WordCloud_2.csv
- BPA_DataCentric/Outputs/Titania/VW_n8n_chat_user_banned.csv
- Archivos actualizados en ventana 17:09-17:10 local aprox.

## Estado de locks

1. ONNET lock: no presente stale.
2. Titania lock: no presente stale.

## Guardrail runtime

1. validate_runtime_env: status ok.
2. Variables recomendadas faltantes reportadas como warning (no bloqueante):
- AZURE_STORAGE_CONNECTION_STRING
- AZURE_STORAGE_CONTAINER
- PROCESS_MONITOR_PORT
- PROCESS_MONITOR_API_BASE_URL
- EXPORT_ENABLE_LOCK

## Hallazgo pendiente

No se pudo automatizar evidencia de Blob last_modified desde el entorno actual porque la cadena de conexion de Blob no esta disponible en BPA_DataCentric/Parametros/Onnet/.env.

## Veredicto del gate

1. Gate tecnico local: APROBADO (2 ciclos consecutivos completed, outputs actualizados, locks sanos).
2. Gate E2E completo con evidencia remota: APROBADO CONDICIONAL (pendiente cerrar inyeccion segura de credencial Blob para validacion automatizada de last_modified).

## Siguiente accion obligatoria

1. Inyectar AZURE_STORAGE_CONNECTION_STRING y AZURE_STORAGE_CONTAINER por entorno (secret manager o runtime env).
2. Re-ejecutar verificacion remota de Blob como paso final de cierre de gate.
