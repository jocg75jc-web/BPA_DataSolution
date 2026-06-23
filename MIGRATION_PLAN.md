# Plan de Migración de Procesos a BPA Schema v2.0

## Fecha: 2026-04-27
## Estado: EN PROGRESO

---

## 1. AUDITORÍA DE PROCESOS ACTUALES

### Procesos en MOCK_PROCESSES (ProcessMonitor/App.tsx)

| ID | Nombre | Proyecto | Tipo | Estado | Script | Timeout |
|---|---|---|---|---|---|---|
| titania-export-sftp | Titania Export SFTP | Titania | python_script | enabled | export_queries_to_csv.py | 1800s |
| onnet-export-modelo3 | ONNET Export Modelo 3 | ONNET | python_script | enabled | export_onnet_csv.py | 3600s |
| onnet-export-modelo4 | ONNET Export Modelo 4 | ONNET | python_script | enabled | export_onnet_csv.py | 3600s |
| db-health-check | Database Health Check | Infrastructure | bash | enabled | check_db_health.sh | 300s |
| pbi-refresh-dashboards | Refresh PBI Dashboards | Titania | powershell | enabled | refresh_pbi_dashboards.ps1 | 900s |

---

## 2. PROCESOS EN NUEVO SCHEMA BPA (processes.json)

### Procesos Existentes
- ✅ **titania** - Sistema de chat - Extracción de queries SQL
- ✅ **onnet** - Sistema de operaciones - Modelos 3 y 4

### Gaps Identificados (No Existen en BPA)
- ❌ **db-health-check** - No existe en BPA
- ❌ **pbi-refresh-dashboards** - No existe en BPA

---

## 3. MAPEO DE MIGRACIÓN

### 3.1 Procesos Migrables Directamente

#### TITANIA
```
De: titania-export-sftp (MOCK_PROCESSES)
A:  titania (processes.json)

Cambios:
- ID: titania-export-sftp → titania
- Nombre: "Titania Export SFTP" → "Titania"
- Estructura: ProcessDefinition → BPA Project
- Parámetros: Agregar "query" como select (all, individual queries)
- Scheduling: Mantener "0 */2 * * *" (cada 2 horas)

Validación:
✅ Script coincide: export_queries_to_csv.py
✅ Timeout compatible: 1800s (30 min)
✅ Variables de entorno mapeadas: ${TITANIA_ROOT}
✅ Ejecutor disponible: titania.py en extractors/
```

#### ONNET
```
De: onnet-export-modelo3 + onnet-export-modelo4 (MOCK_PROCESSES)
A:  onnet (processes.json)

Cambios:
- ID: onnet-export-modelo3, onnet-export-modelo4 → onnet
- Nombre: "ONNET Export Modelo X" → "ONNET"
- Estructura: 2 procesos separados → 1 proceso parametrizado
- Parámetros: Agregar "model" como select (modelo3, modelo4, all)
- Scheduling: Mantener "0 */4 * * *" (cada 4 horas)

Validación:
✅ Script coincide: export_onnet_csv.py
✅ Timeout compatible: 3600s (60 min)
✅ Variables de entorno mapeadas: ${ONNET_ROOT}
✅ Ejecutor disponible: onnet.py en extractors/
✅ Parámetros en processes.json: model (modelo3, modelo4, all)
```

### 3.2 Procesos No Migrables (Fuera de Alcance Actual)

#### DB-HEALTH-CHECK
```
Estado: NOT MIGRATABLE (v1)
Razón: No existe extractor en BPA_DataSolution
Acción: Mantener en MOCK_PROCESSES como fallback
Nota: Pendiente para v2.1 (infraestructura)
```

#### PBI-REFRESH-DASHBOARDS
```
Estado: NOT MIGRATABLE (v1)
Razón: No existe extractor en BPA_DataSolution
Acción: Mantener en MOCK_PROCESSES como fallback
Nota: Pendiente para v2.2 (Power BI integration)
```

---

## 4. PLAN DE EJECUCIÓN

### Fase 1: Preparación (HECHO)
- [x] Auditar procesos actuales
- [x] Analizar processes.json
- [x] Crear mapeo de migración
- [ ] Crear este documento de plan

### Fase 2: Migración Backend (✅ COMPLETADA)
- [x] Actualizar process_engine.py para cargar de processes.json
- [x] Verificar que BPA_DataSolution cargar correctamente
- [x] Validar parametrización en backend
- [x] Métodos `list_unified_processes()` y `get_unified_process()` ya implementados

### Fase 3: Integración Frontend (✅ COMPLETADA)
- [x] Actualizar App.tsx para cargar procesos migrables de BPA
- [x] Remover procesos migrables de MOCK_PROCESSES (titania-export-sftp, onnet-export-modelo3/4)
- [x] Mantener MOCK_PROCESSES solo para procesos no migrables
- [x] Mostrar source=bpa_unified en UI via ProcessCard

### Fase 4: Validación E2E (✅ COMPLETADA)
- [x] Crear script de validación: ProcessMonitor/backend/validate_migration.ps1
- [x] Ejecutar titania via /api/unified/execute (exit_code=0)
- [x] Ejecutar onnet (modelo3) via /api/unified/execute (exit_code=0)
- [x] Ejecutar onnet (modelo4) via /api/unified/execute (exit_code=0)
- [x] Verificar logs completos (export + SFTP)
- [x] Verificar source badges en UI (implementado en ProcessCard: BPA Unified / Local)

### Fase 5: Cleanup & Documentation
- [x] Remover procesos migrables de MOCK_PROCESSES
- [x] Documentar cambios en BPA_DataSolution/docs
- [x] Crear runbook para nuevas migraciones (integrado en docs existentes)

---

## 5. CAMBIOS EN CÓDIGO

### 5.1 Backend (process_engine.py)
```python
# Agregar en is_unified_available():
# Verificar que processes.json tiene al menos 2 proyectos (titania, onnet)

# Actualizar list_unified_processes():
# Retornar solo procesos habilitados (enabled=true)
# Filtrar procesos migrables (excluir db-health-check, pbi-refresh)
```

### 5.2 Frontend (App.tsx)
```typescript
// Actualizar MOCK_PROCESSES:
// - Remover: titania-export-sftp, onnet-export-modelo3, onnet-export-modelo4
// - Mantener: db-health-check, pbi-refresh-dashboards
// - Estas se cargarán desde BPA si disponible

// Actualizar loadUnifiedProcesses():
// - Ya carga de /api/unified/processes
// - Mapea correctamente id, name, description, parameters
```

### 5.3 Frontend (ProcessGrid.tsx)
```typescript
// Ya soporta source field
// Mostrar badge "BPA Unified" para procesos migrables
```

---

## 6. VALIDACIÓN DE MIGRACIÓN

### 6.1 Checklist de Validación

#### Titania Migrado
```
Pre-migración:
- [ ] Ejecutable vía /api/unified/execute/titania
- [ ] Parámetro "query" accept "all", "VW_n8n_chat_histories_classfication", etc.
- [ ] Timeout = 1800s
- [ ] Retry count = 2
- [ ] Schedule expression = "0 */2 * * *"

Post-migración:
- [ ] Ejecución completa sin errores
- [ ] Exit code = 0
- [ ] Logs capturados correctamente
- [ ] Status transition: running → success
- [ ] Source badge = "BPA Unified"
- [ ] Parámetros visibles en UI
```

#### ONNET Migrado
```
Pre-migración:
- [ ] Ejecutable vía /api/unified/execute/onnet
- [ ] Parámetro "model" accept "modelo3", "modelo4", "all"
- [ ] Timeout = 3600s
- [ ] Retry count = 2
- [ ] Schedule expression = "0 */4 * * *"

Post-migración:
- [ ] Ejecución modelo3 completa
- [ ] Ejecución modelo4 completa
- [ ] Ejecución "all" completa
- [ ] Exit code = 0 para todas
- [ ] Logs capturados correctamente
- [ ] Source badge = "BPA Unified"
- [ ] Parámetros visibles en UI
```

#### Procesos No Migrables
```
- [ ] db-health-check accesible vía UI
- [ ] pbi-refresh-dashboards accesible vía UI
- [ ] Source badge = "Local"
- [ ] Simulados correctamente en contexto local
```

---

## 7. ROLLBACK PLAN

Si algo sale mal:

```
1. Restaurar MOCK_PROCESSES en App.tsx
2. Restaurar process_engine.py a versión anterior
3. Desactivar /api/unified/* en api.py (comentar)
4. Verificar frontend vuelve a comportamiento anterior
5. Investigar problema en logs
```

---

## 8. TIMELINE ESTIMADO

| Fase | Tareas | Tiempo | Fecha Estimada |
|---|---|---|---|
| 1 | Preparación | 1h | ✅ HECHO |
| 2 | Backend | 1.5h | 2026-04-27 12:00 |
| 3 | Frontend | 1h | 2026-04-27 13:00 |
| 4 | Validación | 2h | 2026-04-27 15:00 |
| 5 | Cleanup | 1h | 2026-04-27 16:00 |
| **TOTAL** | | **6.5h** | |

---

## 9. RIESGOS & MITIGACIONES

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Parámetros no mapeados correctamente | Media | Alto | Validar processes.json antes de migración |
| Scripts no encontrados | Baja | Alto | Verificar ${TITANIA_ROOT}, ${ONNET_ROOT} |
| Ejecuciones previas fallidas | Media | Medio | Limpiar archivos temp antes |
| Frontend no muestra procesos | Media | Medio | Verificar /api/health retorna true |
| Timeout insuficiente | Baja | Medio | Ejecutar pruebas timing antes |

---

## 10. NOTAS IMPORTANTES

1. **Variables de Entorno**: Asegurarse que ${TITANIA_ROOT} y ${ONNET_ROOT} se resuelvan correctamente en backend
2. **Parámetros Mapeados**: Los parámetros en processes.json están bien estructurados, solo necesitan ser usados por el extractor
3. **Backwards Compatibility**: MOCK_PROCESSES se mantiene para procesos no migrables
4. **Source Field**: Permite tracking de dónde vino cada proceso en el frontend
5. **Scheduling**: Ya está soportado en processes.json, puede integrarse en futuro
6. **Logging**: Los logs actuales funcionan bien, solo necesitan ser capturados vía API

---

## Próximos Pasos

→ **IR A FASE 2: Actualizar backend para carga desde processes.json**
