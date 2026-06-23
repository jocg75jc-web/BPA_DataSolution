# Manual Operativo BPA_DataCentric

## Proposito

Este manual consolida la documentacion operativa y tecnica para transferencia al equipo encargado de mantenimiento de la plataforma BPA DataCentric.

Objetivos del manual:

1. Definir componentes funcionales y tecnicos.
2. Describir modulos, directorios y codigo relevante.
3. Documentar objetos operativos y estructuras de conexion.
4. Explicar interrelaciones y flujo end-to-end.
5. Estandarizar operacion, monitoreo, soporte y troubleshooting.
6. Unificar terminologia mediante glosario.

## Alcance

Incluye:

1. Arquitectura actual operativa (monitor + motor unificado + entrypoints DataCentric + fuentes externas + Blob).
2. Estructura del monorepo BPA_DataCentric y su relacion con repositorios de ejecucion activos.
3. Procedimientos de mantenimiento de primer y segundo nivel.

Excluye:

1. Provisionamiento cloud especifico.
2. Rotacion de secretos en gestor externo (se referencia, pero no se exponen valores).

## Documento de lectura recomendada

1. [15_COMPONENTES_Y_MODULOS.md](15_COMPONENTES_Y_MODULOS.md)
2. [16_DIRECTORIOS_CODIGO_Y_OBJETOS.md](16_DIRECTORIOS_CODIGO_Y_OBJETOS.md)
3. [17_CONEXIONES_E_INTERRELACIONES.md](17_CONEXIONES_E_INTERRELACIONES.md)
4. [18_OPERACION_Y_MANTENIMIENTO.md](18_OPERACION_Y_MANTENIMIENTO.md)
5. [19_GLOSARIO_BPA_DATACENTRIC.md](19_GLOSARIO_BPA_DATACENTRIC.md)
6. [20_BITACORA_CAMBIOS_DOCUMENTACION.md](20_BITACORA_CAMBIOS_DOCUMENTACION.md)

## Artefactos de referencia historica en docs

1. [10_GATE_E2E_CIERRE_REMOTO_2026-05-14.md](10_GATE_E2E_CIERRE_REMOTO_2026-05-14.md)
2. [11_SPRINT1_INICIO_2026-05-14.md](11_SPRINT1_INICIO_2026-05-14.md)
3. [12_MAPA_CARPETAS_MONOREPO.md](12_MAPA_CARPETAS_MONOREPO.md)
4. [13_MIGRACION_RUTAS_LEGACY_A_MONOREPO_2026-05-14.md](13_MIGRACION_RUTAS_LEGACY_A_MONOREPO_2026-05-14.md)

## Estado operativo base (checkpoint)

1. Entry points unificados Titania y ONNET activos en BPA_DataCentric.
2. Configuracion canonica del motor en BPA_DataSolution/unified_extraction/config/processes.json.
3. Backend monitor expuesto en puerto 5052.
4. Validacion API de ejecucion unificada realizada en Sprint 1 con estado success.

## Criterio de actualizacion del manual

Actualizar este paquete documental cuando ocurra cualquiera de los siguientes cambios:

1. Se agregue/modifique un proceso de extraccion.
2. Se modifiquen contratos de configuracion o variables runtime.
3. Se altere topologia de despliegue.
4. Se introduzcan nuevos componentes de persistencia, scheduler o cola.
5. Se detecte un incidente que derive en cambio estructural de operacion.

## Politica de actualizacion continua

Esta documentacion se actualiza con cada avance del plan de desarrollo.

Regla obligatoria:

1. Ningun avance tecnico se considera cerrado si no deja traza documental en docs.

Eventos minimos que exigen actualizacion:

1. Cierre de una tarea de sprint.
2. Cambio de configuracion, rutas o variables de entorno.
3. Incorporacion o retiro de modulo/componente.
4. Cambio en flujo de ejecucion, monitoreo o troubleshooting.
5. Hallazgo de incidente con accion correctiva permanente.

## Flujo de gobernanza documental

1. Implementar cambio tecnico.
2. Validar tecnica y operativamente (API + evidencia local + Blob cuando aplique).
3. Actualizar el archivo funcional correspondiente (15, 16, 17, 18 o 19).
4. Registrar entrada en [20_BITACORA_CAMBIOS_DOCUMENTACION.md](20_BITACORA_CAMBIOS_DOCUMENTACION.md).
5. Actualizar estado en documento de sprint o gate que corresponda.

## SLA de actualizacion

1. La actualizacion documental debe realizarse en la misma sesion del avance.
2. Si no es posible por bloqueo, debe registrarse pendiente con fecha compromiso en la bitacora.
