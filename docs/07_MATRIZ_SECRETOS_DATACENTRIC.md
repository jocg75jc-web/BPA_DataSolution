# Matriz de secretos - BPA DataCentric

## Objetivo

Centralizar las variables y credenciales criticas para Titania, ONNET y Monitor bajo un esquema de gestion segura por entorno.

## Matriz

| Sistema | Variable/Secreto | Uso | Ubicacion actual | Destino recomendado | Rotacion | Criticidad |
|---|---|---|---|---|---|---|
| Titania | Cred_Con.txt | Conexion BD Titania | BPA_DataCentric/Parametros/Titania/Cred_Con.txt | Secret manager + archivo montado en runtime | 90 dias | Alta |
| Titania | TITANIA_DB_* | Conexion BD (si aplica por env) | Parametros o entorno local | Secret manager (key/value) | 90 dias | Alta |
| ONNET | .env (DB creds) | Conexion BD ONNET y parametros de export | BPA_DataCentric/Parametros/Onnet/.env | Secret manager + inyeccion runtime | 90 dias | Alta |
| Runner | AZURE_STORAGE_CONNECTION_STRING | Upload a Blob | Entorno local | Secret manager | 60 dias | Critica |
| Runner | AZURE_STORAGE_CONTAINER | Contenedor destino | Config runtime | Config no secreta por entorno | Bajo cambio | Media |
| Monitor | PROCESS_MONITOR_API_BASE_URL | Enrutamiento API | Config runtime | Config por entorno | Bajo cambio | Media |
| Monitor | PROCESS_MONITOR_PORT | Puerto backend | Config runtime | Config por entorno | Bajo cambio | Media |

## Politica operativa

1. Ningun secreto real en archivos versionados.
2. Solo plantillas `.example` en repositorio.
3. En prod, secretos via variables de entorno o volumen seguro.
4. Cualquier rotacion debe incluir prueba ONNET y Titania post-cambio.

## Plan de rotacion inicial

1. Inventariar secretos vigentes y responsables por sistema.
2. Rotar primero Blob connection string.
3. Rotar despues credenciales ONNET y Titania.
4. Ejecutar E2E de validacion y actualizar evidencia.
