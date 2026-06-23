# Sprint 1 - Inicio (2026-05-14)

## Objetivo del sprint

Converger a una estructura de monorepo unica para ejecucion y despliegue, reduciendo acoplamientos por rutas absolutas y preparando la base para Docker.

## Estado de inicio

- Sprint 0: cerrado (gate local y remoto aprobados).
- Base operativa activa en BPA_DataCentric:
  - Querys/Titania y Querys/Onnet
  - Outputs/Titania y Outputs/Onnet
  - Parametros/Titania y Parametros/Onnet

## Backlog Sprint 1

1. S1-01 - Definir mapa de carpetas final del monorepo. [COMPLETADO]
2. S1-02 - Crear estructura base no destructiva del monorepo en BPA_DataCentric. [COMPLETADO]
3. S1-03 - Definir perfiles de entorno (dev/stage/prod) para rutas y runtime. [COMPLETADO]
4. S1-04 - Unificar entrypoints operativos de Titania/ONNET contra estructura DataCentric. [COMPLETADO]
5. S1-05 - Validar ejecucion desde monitor con rutas sin hardcode externo. [COMPLETADO]
6. S1-06 - Cerrar documento de migracion de rutas legacy a rutas monorepo. [COMPLETADO]

## Ejecucion de hoy

- Confirmado por continuidad: S1-01, S1-02 y S1-03 ya estaban ejecutados desde ayer.
- S1-04 completado: entrypoints unificados en BPA_DataCentric y config del engine redirigida.
- Evidencia smoke test:
  - ONNET `model=modelo4` -> status completed (~111.55s).
  - Titania `query=VW_n8n_chat_user_banned` -> status completed (~9.88s).
- S1-05 completado con evidencia desde API del monitor:
  - Backend reiniciado en puerto 5052 para recargar configuracion unificada vigente.
  - `GET /api/unified/processes` expone scripts en `BPA_DataCentric/services/extraction-runner/entrypoints` para Titania y ONNET.
  - `POST /api/unified/execute/titania` con `query=VW_n8n_chat_user_banned` -> `execution_id=exec-1778762209432`.
  - `GET /api/status/exec-1778762209432` -> `status=success`, `exit_code=0`.
- S1-06 completado: documento de cierre generado en `BPA_DataCentric/docs/13_MIGRACION_RUTAS_LEGACY_A_MONOREPO_2026-05-14.md`.

## Criterio de avance del sprint

1. Estructura monorepo creada y documentada.
2. Rutas criticas externalizadas por profile.
3. ONNET y Titania ejecutan sin dependencia de path absoluto hardcodeado fuera de DataCentric.
