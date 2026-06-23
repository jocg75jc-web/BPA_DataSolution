# Memoria del Proyecto BPA_DataSolution

## 1. Resumen ejecutivo
BPA_DataSolution nace para unificar los procesos de extraccion que estaban dispersos en Titania y ONNET, y para ofrecer un modelo parametrizable que reduzca cambios de codigo por cada nueva solicitud.

## 2. Punto de partida
- Proyecto origen 1: Titania (extraccion SQL, generacion de archivos, carga SFTP, monitoreo).
- Proyecto origen 2: ONNET (extraccion por modelos, export de archivos, monitoreo operativo).
- Necesidad transversal: un solo motor para definir, validar, ejecutar y observar procesos.

## 3. Objetivos iniciales
- Crear una fuente de verdad unica para configuracion de procesos.
- Estandarizar validacion de parametros.
- Reducir tiempo de alta de nuevos procesos.
- Integrar ejecucion con ProcessMonitor.
- Facilitar escalado a mas fuentes y destinos.

## 4. Componentes implementados (estado actual)
- ConfigLoader funcional.
- ParameterValidator funcional.
- ExecutionEngine funcional.
- Extractores Titania y ONNET funcionales.
- Registry de extractores funcional.
- Scripts de validacion y migracion funcionales.
- Pruebas base creadas (pendiente consolidar ejecucion automatizada en entorno estable).

## 5. Decisiones de arquitectura relevantes
- Configuracion declarativa basada en JSON (`unified_extraction/config/processes.json`).
- Motor de ejecucion desacoplado por extractores (patron registry).
- Parametros por tipo (text, number, boolean, date, select, multiselect).
- Integracion por subprocess para compatibilidad con scripts existentes.
- Foco inicial en estabilidad operativa sobre complejidad.

## 6. Lecciones aprendidas
- Un proceso puede figurar como fallido en monitor por inactividad y no por fin real; se requiere categoria stalled.
- La trazabilidad real depende de logs tecnicos detallados, no solo de estado resumido.
- La robustez de conectividad (DNS, timeout, retry, keepalive) es critica para procesos largos.
- El webhook de alerta debe mantenerse valido para evitar perdida de notificaciones en incidentes.

## 7. Incidentes y hallazgos operativos relevantes
- Titania presento intermitencia por resolucion DNS y cierres de conexion DB.
- Se observaron ejecuciones colgadas que bloquearon archivos de log.
- Se confirmo la necesidad de mejorar manejo de timeout y reintentos.

## 8. Pendientes estrategicos
- Integracion API completa en ProcessMonitor para listar y ejecutar procesos del motor unificado.
- End-to-end tests entre motor y monitor.
- Politica de reintentos por tipo de error (transitorio vs permanente).
- Clasificacion de estados de ejecucion: running, completed, failed, stalled, cancelled.

## 9. Politica de actualizacion de memoria
Cada entrada nueva debe incluir:
- Fecha
- Cambio aplicado
- Problema que resuelve
- Impacto esperado
- Riesgo residual

## 10. Bitacora (plantilla)
### [YYYY-MM-DD] Titulo corto
- Contexto:
- Cambio:
- Resultado:
- Riesgo residual:
- Siguiente accion:

## 11. Bitacora (real)
### [2026-04-27] Cierre migracion a esquema unificado
- Contexto: Se migro la ejecucion operativa desde procesos locales del monitor hacia el esquema BPA unificado.
- Cambio:
	- ProcessMonitor consume `/api/unified/processes` para procesos migrables.
	- Titania y ONNET ejecutan con interpretes dedicados por proyecto (`.venv/Scripts/python.exe`).
	- Se mantuvieron solo procesos no migrables en `MOCK_PROCESSES`.
- Resultado:
	- `titania(query=all)` validado con `exit_code=0`.
	- `onnet(modelo3)` validado con `exit_code=0`.
	- `onnet(modelo4)` validado con `exit_code=0`.
	- Logs completos de export y SFTP disponibles via API de monitoreo.
- Riesgo residual:
	- Dependencias del backend pueden variar entre versiones de Python (ejemplo: `pydantic`, `psycopg2-binary`).
	- Persisten procesos locales no migrados (infra y refresh PBI) fuera del engine unificado.
- Siguiente accion:
	- Completar migracion de procesos no migrables o documentar excepciones permanentes.
	- Agregar verificacion visual automatizada de badges `BPA Unified/Local` en pruebas UI.

### [2026-04-27] Separacion de dependencias runtime/dev en backend
- Contexto: La instalacion unificada en `requirements.txt` mezclaba runtime y toolchain de desarrollo, generando friccion en despliegues.
- Cambio:
	- Se crearon `ProcessMonitor/backend/requirements-runtime.txt` y `ProcessMonitor/backend/requirements-dev.txt`.
	- `ProcessMonitor/backend/requirements.txt` ahora apunta al set runtime por defecto.
- Resultado:
	- `pip install -r requirements.txt` queda estable para ejecucion/despliegue.
	- El stack de desarrollo queda aislado en `requirements-dev.txt`.
- Riesgo residual:
	- Se requiere disciplina para agregar nuevas dependencias en el archivo correcto.
- Siguiente accion:
	- Incluir validacion CI separada para runtime y dev (instalacion + smoke checks).
