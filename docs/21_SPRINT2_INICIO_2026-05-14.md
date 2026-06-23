# Sprint 2 - Inicio (2026-05-14)

## Objetivo del sprint

Dejar lista la base de ejecucion portable en Docker para monitor y runner, con configuracion de entorno desacoplada y camino habilitado para quality gates.

## Backlog Sprint 2

1. S2-01 - Crear Dockerfiles para monitor-backend, monitor-frontend y extraction-runner. [COMPLETADO]
2. S2-02 - Definir orquestacion base con docker-compose y perfiles de entorno. [COMPLETADO]
3. S2-03 - Eliminar dependencias rigidas de python local/venv en config para contenedores. [COMPLETADO]
4. S2-04 - Ejecutar validacion de build/arranque local de servicios docker. [BLOQUEADO]
5. S2-05 - Definir y ejecutar gate de calidad (schema/config + type-check + tests core). [COMPLETADO]
6. S2-06 - Preparar gate E2E release con evidencia API + local + Blob. [PENDIENTE]

## Artefactos creados en este arranque

1. `ops/docker/Dockerfile.monitor-backend`
2. `ops/docker/Dockerfile.monitor-frontend`
3. `ops/docker/Dockerfile.extraction-runner`
4. `ops/docker/docker-compose.yml`

## Notas operativas

1. El backend se mantiene en modo unificado (`ENABLE_LEGACY_V1=false`).
2. El scheduler integrado inicia desactivado en compose para evitar solape durante estabilizacion.
3. El runner se deja como servicio base de validacion/configuracion para iterar hacia ejecucion E2E en sprint.
4. `processes.json` queda parametrizado con `UNIFIED_PYTHON` para compatibilidad host/contenedor.
5. Bloqueo actual S2-04: Docker CLI no disponible en el host de trabajo (`docker` no reconocido por terminal).
6. S2-05 validado localmente:
	- `npm run type-check` en ProcessMonitor: OK.
	- `pytest -q` en unified_extraction: 4 passed.
	- `python scripts/validate_config.py`: status ok.
	- `python scripts/validate_runtime_env.py`: status ok (solo faltantes recomendadas no bloqueantes).

## Siguiente foco inmediato

1. Habilitar Docker CLI en host (Docker Desktop/engine) para desbloquear S2-04.
2. Ejecutar `docker compose up --build -d` en `ops/docker` y validar health de servicios.
