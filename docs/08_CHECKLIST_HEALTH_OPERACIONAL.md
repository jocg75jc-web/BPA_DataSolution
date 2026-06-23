# Checklist de health operacional diario

## Objetivo

Verificar continuidad operativa de ONNET y Titania en el flujo monitor -> engine -> outputs -> Blob.

## Frecuencia

1. Inicio de jornada.
2. Mitad de jornada.
3. Cierre de jornada.
4. Siempre despues de cambios en configuracion/credenciales.

## Checklist

1. Monitor backend responde health (`/api/health`) en puerto esperado.
2. Dashboard carga procesos ONNET y Titania sin errores de fetch.
3. No hay doble scheduler activo (una sola instancia disparando).
4. No hay locks stale (`onnet_export.lock`, `titania_export.lock`).
5. Ultima corrida ONNET en estado success con duracion esperada.
6. Ultima corrida Titania en estado success con duracion esperada.
7. CSV ONNET actualizados en `BPA_DataCentric/Outputs/Onnet`.
8. CSV Titania actualizados en `BPA_DataCentric/Outputs/Titania`.
9. Blob refleja last_modified reciente para archivos principales.
10. Logs recientes no muestran errores recurrentes de conexion o permisos.

## Umbrales de alerta

1. 2 fallos consecutivos de un mismo proceso.
2. Ausencia de actualizacion de CSV en la ventana esperada del scheduler.
3. Divergencia entre estado API y evidencia local/remota.
4. Reaparicion de locks huérfanos tras limpieza.

## Acciones de contingencia

1. Ejecutar corrida manual controlada desde motor unificado.
2. Validar conectividad a BD y credenciales activas.
3. Validar permisos de escritura en Outputs y subida a Blob.
4. Si persiste, activar fallback documentado y escalar incidente.
