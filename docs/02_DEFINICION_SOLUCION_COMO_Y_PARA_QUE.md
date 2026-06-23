# Definicion de la Solucion: Como y Para Que

## 1. Para que construimos esta solucion
Construimos BPA_DataSolution para resolver tres problemas:
1. Duplicidad de logica entre proyectos (Titania y ONNET).
2. Alta dependencia de cambios de codigo para nuevas solicitudes.
3. Falta de estandar para escalar a nuevas fuentes y destinos.

Adicionalmente, el objetivo principal es construir un framework E2E de informacion clave que cubra:
- Adquisicion desde multiples fuentes.
- Procesamiento con reglas de calidad y trazabilidad.
- Publicacion hacia multiples destinos de consumo.
- Presentacion en capas de dashboard para operacion y negocio.

Titania y ONNET se consideran sujetos de prueba para validar patrones reutilizables antes de escalar a nuevas aplicaciones.

## 2. Que valor entrega
- Menor tiempo de implementacion de nuevos procesos.
- Menor riesgo operativo por estandarizacion.
- Mayor visibilidad y control de ejecuciones.
- Plataforma escalable para nuevas lineas de negocio.

## 3. Como se construye un proceso en esta solucion
1. Levantar necesidad de negocio con historia de usuario.
2. Definir origen de datos (BD/API/archivo).
3. Definir regla de extraccion y filtros.
4. Definir formato de salida.
5. Definir destino de almacenamiento.
6. Definir horario, SLA y alertas.
7. Definir capa de presentacion (KPIs, vistas, filtros, consumidores y latencia esperada).
8. Configurar proceso en `processes.json`.
9. Implementar o reutilizar extractor.
10. Validar con pruebas tecnicas y funcionales.
11. Publicar y monitorear.
12. Verificar consumo en dashboard y registrar evidencia E2E.

## 4. Alcance actual
- Origenes activos: Titania y ONNET.
- Patrón de ejecucion: scripts Python con motor unificado.
- Integracion objetivo: ProcessMonitor como capa de observabilidad.

## 5. Alcance esperado
- Multiples motores de base de datos.
- Multiples destinos de almacenamiento.
- Criterios de calidad de datos por proceso.
- Gobierno de cambios y versionado de definiciones.
- Capa de presentacion estandar reutilizable para nuevos procesos.
- Contrato de datos comun para dashboards cross-proceso.

## 6. Criterios de exito
- Tiempo de alta de un nuevo proceso < 2 dias habiles.
- Reuso de componentes > 80 por ciento.
- Tasa de fallos por configuracion incompleta < 5 por ciento.
- Trazabilidad completa en 100 por ciento de ejecuciones.

## 7. Criterios de no exito
- Solicitudes sin plantilla estandar.
- Procesos sin owner tecnico y owner funcional.
- Procesos sin politica de reintentos y alertas.
