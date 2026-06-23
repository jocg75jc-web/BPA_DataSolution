---
title: "📝 TODO - BPA_DataSolution Roadmap"
date: "2024-04-24"
---

# 📝 TODO - BPA_DataSolution Roadmap

## 🚀 Próximas Fases

### Fase 1: Fundación (Semana 1) ✅ COMPLETED
- [x] Estructura base del repositorio
- [x] ConfigLoader skeleton
- [x] ParameterValidator skeleton
- [x] BaseExtractor abstract class
- [x] JSON Schema validation
- [x] processes.json con Titania y ONNET
- [x] Documentación inicial

### Fase 2: Implementación Core (Semana 2) ✅ COMPLETED
- [x] ConfigLoader full implementation
- [x] ParameterValidator full implementation
- [x] ExecutionEngine implementation
- [x] TitaniaExtractor implementation
- [x] ONNETExtractor implementation
- [x] ExtractorRegistry implementation
- [x] Unit tests para core/
- [x] Migration script (monitor_app.py → processes.json)
- [ ] Integration tests end-to-end (pendiente validar en entorno estable)

### Fase 3: Integración (Semana 3) 🟡 PENDING
- [ ] Integración con ProcessMonitor v2
- [ ] API endpoints (GET /api/processes, POST /api/execute)
- [ ] WebSocket integration
- [ ] Dashboard integration (React)
- [ ] End-to-end testing
- [ ] Performance testing

### Fase 4: Productionización (Semana 4) 🟡 PENDING
- [ ] Error handling robusto
- [ ] Logging comprehensivo
- [ ] Monitoring y alerting
- [ ] Security review
- [ ] Documentation completa
- [ ] Deployment procedures
- [ ] Training materials

### Fase 5: Enhancements (Semana 5+) 🟡 PENDING
- [ ] Scheduler (APScheduler)
- [ ] Notification engine
- [ ] Analytics dashboard
- [ ] Multi-cloud support
- [ ] Advanced scheduling
- [ ] Custom extractors (user-provided)

---

## 🎯 Tareas por Prioridad

### 🔴 CRÍTICAS (Bloquean integración)

```
Fase 3:
- [ ] Endpoints API para ejecutar/listar procesos
- [ ] Sincronización de estado con ProcessMonitor
- [ ] Integration tests pass (motor + monitor)
- [ ] Hardening de timeouts/reintentos para ejecuciones largas
```

**Deadline**: Viernes próximo

### 🟠 ALTOS (Necesarios para MVP)

```
Fase 3:
- [ ] Flask API endpoints
- [ ] WebSocket integration
- [ ] Dashboard component updates
- [ ] End-to-end testing
```

**Deadline**: Próxima semana

### 🟡 MEDIOS (Nice to have)

```
Fase 4:
- [ ] APScheduler integration
- [ ] Notification templates
- [ ] Analytics charts
- [ ] Admin panel
```

**Deadline**: Después de MVP

### 🟢 BAJOS (Futuros)

```
Fase 5+:
- [ ] Multi-cloud
- [ ] Custom extractors
- [ ] REST API (sin Flask)
- [ ] GraphQL support
```

**Deadline**: TBD

---

## 📋 Tareas Detalladas

### Estado actualizado (2026-04-27)

- Core funcional validado con config cargada y proyectos detectados.
- Scripts CLI actualizados para listar proyectos con --list.
- Pendiente principal: integración operativa con ProcessMonitor y pruebas E2E.

---

### Implementar ConfigLoader

**Descripción**: Cargar y validar `processes.json`

**Requisitos**:
```python
class ConfigLoader:
    def __init__(self, config_path: str)
    def get_all_projects() -> List[ProjectDefinition]
    def get_project(project_id: str) -> ProjectDefinition
    def get_parameters(project_id: str) -> Dict
    def validate_config() -> bool
```

**Tests**:
- [x] Load válido JSON
- [ ] Validate contra schema
- [ ] Interpolate environment variables
- [ ] Handle missing files
- [ ] Handle invalid JSON

**Estimate**: 4 horas

### Implementar ParameterValidator

**Descripción**: Validar parámetros contra schema

**Requisitos**:
```python
class ParameterValidator:
    def __init__(self, params_definition: Dict)
    def validate(params: Dict) -> bool
    def validate_and_clean(params: Dict) -> Dict
```

**Tipos de validación**:
- [ ] select (opciones pre-definidas)
- [ ] text (regex)
- [ ] number (min/max)
- [ ] date (ISO8601)
- [ ] boolean (true/false)
- [ ] multiselect (array)

**Tests**:
- [ ] Valid parameters pass
- [ ] Invalid parameters fail
- [ ] Required fields checked
- [ ] Type coercion
- [ ] Error messages útiles

**Estimate**: 6 horas

### Implementar ExecutionEngine

**Descripción**: Orquestar ejecución de procesos

**Requisitos**:
```python
class ExecutionEngine:
    def __init__(self, config_path: str)
    def execute(project_id: str, parameters: Dict) -> ExecutionResult
    def stop_execution(execution_id: str) -> bool
    def get_status(execution_id: str) -> ExecutionStatus
```

**Features**:
- [ ] Subprocess execution
- [ ] Timeout handling
- [ ] Log streaming
- [ ] Resource monitoring
- [ ] Retry logic
- [ ] Error handling

**Tests**:
- [ ] Execute successfully
- [ ] Handle timeout
- [ ] Capture logs
- [ ] Monitor resources
- [ ] Retry on failure
- [ ] Stop execution

**Estimate**: 10 horas

### Implementar TitaniaExtractor

**Descripción**: Extractor para Titania

**Requisitos**:
```python
class TitaniaExtractor(BaseExtractor):
    def validate_parameters(params) -> bool
    def build_command(params) -> List[str]
    def execute(params) -> ExecutionResult
```

**Parámetros**:
- [ ] query (select)
- [ ] database (text, optional)
- [ ] output_format (select)

**Tests**:
- [ ] Valid parameters
- [ ] Command building
- [ ] Execution
- [ ] Error handling

**Estimate**: 6 horas

### Implementar ONNETExtractor

**Descripción**: Extractor para ONNET

**Requisitos**: Similar a TitaniaExtractor

**Parámetros**:
- [ ] model (select)
- [ ] date_filter (date, optional)
- [ ] include_history (boolean)

**Tests**: Similar a Titania

**Estimate**: 6 horas

### Migración de monitor_app.py

**Descripción**: Generar `processes.json` de configuración actual

**Script**: `scripts/migrate_from_monitor.py`

**Tareas**:
- [ ] Parse PROJECT_CONFIG
- [ ] Parse PROJECT_QUERIES
- [ ] Parse PROJECT_SCHEDULE_TASKS
- [ ] Generate processes.json
- [ ] Validar output
- [ ] Documentation

**Estimate**: 4 horas

---

## 🧪 Testing Plan

### Unit Tests

```bash
pytest tests/test_config_loader.py -v
pytest tests/test_parameter_validator.py -v
pytest tests/test_command_builder.py -v
pytest tests/test_extractors.py -v
```

**Cobertura Target**: > 80%

### Integration Tests

```bash
pytest tests/test_integration.py -v
# Test: ConfigLoader → ParameterValidator → ExecutionEngine → TitaniaExtractor
```

### End-to-End Tests

```bash
# Test: UI → API → ExecutionEngine → Script → Output
# Manual testing con Process Monitor v2
```

---

## 📚 Documentación Por Hacer

- [ ] ARCHITECTURE.md completo
- [ ] CONFIGURATION.md detallado
- [ ] DEVELOPER_GUIDE.md
- [ ] API.md
- [ ] TROUBLESHOOTING.md
- [ ] DEPLOYMENT.md
- [ ] CONTRIBUTING.md

---

## 🔗 Dependencias Externas

### De Titania
- [ ] `export_queries_to_csv.py` disponible
- [ ] Queries mapeadas correctamente
- [ ] Directorio de output accesible

### De ONNET
- [ ] `export_onnet_csv.py` disponible
- [ ] Modelos identificados
- [ ] Directorio de output accesible

### De ProcessMonitor v2
- [ ] API endpoints disponibles
- [ ] WebSocket funcionando
- [ ] Dashboard actualizado

---

## 📊 Métricas de Éxito

| Métrica | Target | Status |
|---------|--------|--------|
| **Tests** | >80% coverage | ⏳ |
| **Config** | Valid JSON | ✅ |
| **Docs** | >50 pages | ⏳ |
| **Performance** | <2s execution setup | ⏳ |
| **Reliability** | Zero data loss | ⏳ |

---

## 👥 Asignación de Tareas

| Tarea | Owner | Status |
|-------|-------|--------|
| ConfigLoader | Backend Dev 1 | 🔴 |
| ParameterValidator | Backend Dev 1 | 🔴 |
| ExecutionEngine | Backend Dev 1 | 🔴 |
| TitaniaExtractor | Backend Dev 2 | 🔴 |
| ONNETExtractor | Backend Dev 2 | 🔴 |
| Tests | QA | 🔴 |
| Documentation | Tech Writer | 🔴 |
| Integration | Backend Lead | 🔴 |

---

## 🚨 Bloqueadores Actuales

Ninguno identificado hasta el momento.

---

## 💬 Notas

- Proceder con Fase 2 una vez que Fase 1 sea revisada y aprobada
- Enfatizar testing en cada fase
- Documentación en paralelo con código
- Reuniones de sincronización bi-diarias

---

**Última actualización**: 24/04/2024  
**Próxima revisión**: 25/04/2024

