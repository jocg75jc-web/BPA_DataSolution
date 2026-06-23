# Mapa de carpetas objetivo - Monorepo BPA_DataCentric

## Principio

Mantener continuidad operativa mientras se converge a una estructura unica por dominios (apps, services, shared, data, ops).

## Estructura objetivo

```
BPA_DataCentric/
  apps/
    monitor-frontend/
    monitor-backend/
  services/
    extraction-runner/
  shared/
    unified-extraction/
    contracts/
  data/
    querys/
      titania/
      onnet/
    outputs/
      titania/
      onnet/
    parametros/
      titania/
      onnet/
  config/
    profiles/
      dev.env.example
      stage.env.example
      prod.env.example
  ops/
    docker/
    scripts/
    runbooks/
  docs/
  scripts/
```

## Equivalencia con estado actual

1. Querys/Titania -> data/querys/titania
2. Querys/Onnet -> data/querys/onnet
3. Outputs/Titania -> data/outputs/titania
4. Outputs/Onnet -> data/outputs/onnet
5. Parametros/Titania -> data/parametros/titania
6. Parametros/Onnet -> data/parametros/onnet

## Estrategia de migracion (sin corte)

1. Fase A: crear estructura target en paralelo.
2. Fase B: apuntar runtime por profile al target.
3. Fase C: ejecutar doble validacion (local + Blob).
4. Fase D: retirar rutas legacy una vez estabilizado.

## Reglas

1. Ninguna eliminacion de carpetas legacy sin validacion E2E.
2. No mover secretos a repositorio; solo plantillas o referencias.
3. Toda nueva construccion del contexto dockerizado queda en BPA_DataCentric.
