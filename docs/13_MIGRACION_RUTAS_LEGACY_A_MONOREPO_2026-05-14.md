# Cierre S1-06 - Migracion rutas legacy a monorepo (2026-05-14)

## Objetivo

Documentar el cierre de migracion de rutas de ejecucion y artefactos desde estructura legacy (`Titania/`, `ONNET/`) hacia estructura monorepo en `BPA_DataCentric`, manteniendo continuidad operativa.

## Alcance

- Incluye rutas de ejecucion, queries, parametros y outputs operativos.
- Incluye validacion desde monitor/API y motor unificado.
- Excluye `front_pbi` por decision de scope.

## Estado final

- S1-04: COMPLETADO (entrypoints unificados en DataCentric).
- S1-05: COMPLETADO (monitor ejecuta contra rutas DataCentric sin hardcode legacy activo).
- S1-06: COMPLETADO (este documento).

## Mapeo de rutas (antes -> ahora)

1. Titania script
   - Antes: `C:/Users/javier.castaneda/botsquad/Titania/export_queries_to_csv.py`
   - Ahora: `C:/Users/javier.castaneda/botsquad/BPA_DataCentric/services/extraction-runner/entrypoints/titania_entrypoint.py`
2. ONNET script
   - Antes: `C:/Users/javier.castaneda/botsquad/ONNET/export_onnet_csv.py`
   - Ahora: `C:/Users/javier.castaneda/botsquad/BPA_DataCentric/services/extraction-runner/entrypoints/onnet_entrypoint.py`
3. Titania queries
   - Antes: `C:/Users/javier.castaneda/botsquad/Titania/querys`
   - Ahora: `C:/Users/javier.castaneda/botsquad/BPA_DataCentric/Querys/Titania`
4. ONNET queries
   - Antes: `C:/Users/javier.castaneda/botsquad/ONNET/querys`
   - Ahora: `C:/Users/javier.castaneda/botsquad/BPA_DataCentric/Querys/Onnet`
5. Titania parametros
   - Antes: `C:/Users/javier.castaneda/botsquad/Titania/Cred_Con.txt`
   - Ahora: `C:/Users/javier.castaneda/botsquad/BPA_DataCentric/Parametros/Titania/Cred_Con.txt`
6. ONNET parametros
   - Antes: `C:/Users/javier.castaneda/botsquad/ONNET/.env`
   - Ahora: `C:/Users/javier.castaneda/botsquad/BPA_DataCentric/Parametros/Onnet/.env`
7. Outputs Titania
   - Antes: `C:/Users/javier.castaneda/botsquad/Titania/output`
   - Ahora: `C:/Users/javier.castaneda/botsquad/BPA_DataCentric/Outputs/Titania`
8. Outputs ONNET
   - Antes: `C:/Users/javier.castaneda/botsquad/ONNET/output`
   - Ahora: `C:/Users/javier.castaneda/botsquad/BPA_DataCentric/Outputs/Onnet`

## Evidencia tecnica de cierre

1. Config canonica del engine (`BPA_DataSolution/unified_extraction/config/processes.json`) apunta a entrypoints de DataCentric para Titania y ONNET.
2. `scripts/validate_config.py` en `unified_extraction` en estado OK tras cambios de rutas.
3. Smoke tests directos del engine en estado `completed` para ONNET y Titania.
4. Validacion desde monitor (S1-05):
   - `GET /api/unified/processes` muestra scripts en DataCentric entrypoints.
   - `POST /api/unified/execute/titania` (`query=VW_n8n_chat_user_banned`) inicia ejecucion.
   - `GET /api/status/exec-1778762209432` finaliza en `status=success`, `exit_code=0`.

## Riesgos y controles residuales

1. Riesgo: backend monitor puede quedar con cache de configuracion previa si no se reinicia.
   - Control: reinicio controlado del backend al aplicar cambios de rutas en config unificada.
2. Riesgo: variables recomendadas faltantes (no bloqueantes) en runtime.
   - Control: mantener validacion de contrato y checklist operativo diario.
3. Riesgo: regresion por ejecuciones legacy fuera del monitor.
   - Control: mantener entrypoints unificados como unica via documentada para operacion estandar.

## Criterio de aceptacion Sprint 1

- ONNET y Titania ejecutan desde monitor contra rutas monorepo.
- No hay dependencia operativa activa de rutas legacy hardcodeadas para el flujo principal.
- Historial y estado en API reflejan ejecucion real de los procesos.

## Decision de cierre

Sprint 1 queda listo para cierre tecnico, sujeto a aprobacion operativa final del equipo.
