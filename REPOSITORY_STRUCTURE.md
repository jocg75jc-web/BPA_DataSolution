---
title: "📁 Estructura del Repositorio BPA_DataSolution"
date: "2024-04-24"
---

# 📁 Estructura del Repositorio BPA_DataSolution

## 🎯 Propósito

**BPA_DataSolution** es el ecosistema parametrizable de extracción de datos que integra:
- Titania (chat analytics)
- ONNET (operaciones)
- Y futuros proyectos

---

## 📂 Árbol de Directorios

```
BPA_DataSolution/
│
├── 📄 README.md                     ← LEER PRIMERO
├── 📄 .gitignore
│
├── unified_extraction/              ← 🔴 MOTOR PRINCIPAL
│   │
│   ├── config/                      ← 🔴 CONFIGURACIÓN
│   │   ├── processes.json           ← ⭐ ÚNICA FUENTE DE VERDAD
│   │   ├── processes.schema.json    ← Validación
│   │   └── examples/
│   │       └── processes.example.json
│   │
│   ├── core/                        ← 🔴 LÓGICA CENTRAL
│   │   ├── __init__.py
│   │   ├── config_loader.py         ← Carga y parsea configuración
│   │   ├── parameter_validator.py   ← Valida parámetros
│   │   ├── command_builder.py       ← Construye comandos
│   │   └── execution_engine.py      ← Ejecuta procesos
│   │
│   ├── extractors/                  ← 🔴 IMPLEMENTACIONES
│   │   ├── __init__.py
│   │   ├── base.py                  ← BaseExtractor (abstract)
│   │   ├── titania.py               ← TitaniaExtractor
│   │   ├── onnet.py                 ← ONNETExtractor
│   │   └── registry.py              ← Registro de extractores
│   │
│   ├── connectors/                  ← Conectores a sistemas
│   │   ├── __init__.py
│   │   ├── titania_connector.py
│   │   └── onnet_connector.py
│   │
│   ├── scripts/                     ← 🟢 SCRIPTS ÚTILES
│   │   ├── migrate_from_monitor.py  ← Extrae config de monitor_app.py
│   │   ├── validate_config.py       ← Valida processes.json
│   │   ├── test_extraction.py       ← Testing manual
│   │   └── generate_docs.py         ← Genera documentación
│   │
│   ├── tests/                       ← 🟢 TESTS
│   │   ├── __init__.py
│   │   ├── test_config_loader.py
│   │   ├── test_parameter_validator.py
│   │   ├── test_command_builder.py
│   │   ├── test_extractors.py
│   │   └── test_integration.py
│   │
│   ├── docs/                        ← 🟢 DOCUMENTACIÓN
│   │   ├── QUICK_START.md           ← Este archivo
│   │   ├── ARCHITECTURE.md
│   │   ├── CONFIGURATION.md
│   │   └── DEVELOPER_GUIDE.md
│   │
│   ├── logs/                        ← Logs de ejecución
│   │   └── .gitkeep
│   │
│   ├── __init__.py
│   ├── requirements.txt
│   ├── setup.py
│   └── pytest.ini
│
├── connectors/                      ← Referencias a proyectos externos
│   ├── titania/                     ← Symlink a ../Titania
│   └── onnet/                       ← Symlink a ../ONNET
│
├── examples/                        ← 🟢 EJEMPLOS
│   ├── basic_usage.py
│   ├── custom_extractor.py
│   └── monitoring_integration.py
│
└── .env.example
```

---

## 🎨 Flujo de Datos

```
Usuario → Browser
   ↓
ProcessMonitor v2 (React Dashboard)
   ↓
Flask API (/api/execute)
   ↓
BPA_DataSolution.ExecutionEngine
   ↓
ConfigLoader → processes.json
   ↓
ParameterValidator → valida parámetros
   ↓
ExtractorRegistry → elige TitaniaExtractor | ONNETExtractor
   ↓
CommandBuilder → construye comando
   ↓
subprocess.Popen() → ejecuta script
   ↓
Logs streaming → WebSocket → Dashboard
   ↓
Output CSV/Parquet → output/
```

---

## 🔑 Archivos Clave

| Archivo | Propósito | Criticidad |
|---------|-----------|-----------|
| `processes.json` | Configuración centralizada | ⭐⭐⭐ |
| `core/config_loader.py` | Lee y parsea config | ⭐⭐⭐ |
| `core/execution_engine.py` | Ejecuta procesos | ⭐⭐⭐ |
| `extractors/base.py` | Clase base extensible | ⭐⭐ |
| `extractors/titania.py` | Implementación Titania | ⭐⭐ |
| `extractors/onnet.py` | Implementación ONNET | ⭐⭐ |
| `scripts/migrate_from_monitor.py` | Migración | ⭐ |

---

## 📊 Componentes

### 1. ConfigLoader
```python
loader = ConfigLoader("config/processes.json")
project = loader.get_project("titania")
params = loader.get_parameters("titania")
```

### 2. ParameterValidator
```python
validator = ParameterValidator(params_def)
is_valid = validator.validate({"query": "all"})
```

### 3. ExecutionEngine
```python
engine = ExecutionEngine("config/processes.json")
result = engine.execute("titania", {"query": "all"})
```

### 4. Extractors
```python
# Automático por extractor type
extractor = registry.get("titania")
result = extractor.execute({"query": "all"})
```

---

## 🔄 Ciclo de Vida de un Proceso

```
1. Usuario selecciona proyecto y parámetros en Dashboard
   ↓
2. POST /api/execute {project, parameters}
   ↓
3. ExecutionEngine.execute(project, parameters)
   ↓
4. ConfigLoader.get_project(project)
   ↓
5. ParameterValidator.validate(parameters)
   ↓
6. ExtractorRegistry.get(project).execute()
   ↓
7. CommandBuilder.build_command()
   ↓
8. subprocess.Popen(command)
   ↓
9. Captura stdout/stderr línea por línea
   ↓
10. WebSocket emit → Dashboard actualiza logs
    ↓
11. Proceso termina → status_update
    ↓
12. output/*.csv generado
    ↓
13. Dashboard muestra resultado
```

---

## 🎯 Responsabilidades por Módulo

| Módulo | Responsabilidad |
|--------|-----------------|
| `core/` | Lógica de orquestación |
| `extractors/` | Implementaciones específicas |
| `connectors/` | Conectividad a sistemas |
| `scripts/` | Utilidades y migración |
| `tests/` | Validación |
| `docs/` | Documentación |
| `config/` | Configuración |

---

## 🚀 Cómo Agregar Nuevo Proyecto

### Opción 1: Extractor SQL (Recomendado)

```python
# extractors/my_db.py
class MyDBExtractor(BaseExtractor):
    def validate_parameters(self, params):
        return "database" in params
    
    def build_command(self, params):
        return ["python", "export_my_db.py", "--db", params["database"]]
```

```json
// processes.json
{
  "id": "my_db",
  "name": "Mi Base de Datos",
  "parameters": { ... }
}
```

### Opción 2: Extractor API

```python
# extractors/external_api.py
class ExternalAPIExtractor(BaseExtractor):
    def execute(self, params):
        # Lógica personalizada (sin subprocess)
        import requests
        response = requests.get(params["url"])
        return {"status": "success", "data": response.json()}
```

---

## 📋 Checklist de Implementación

### Fase 1: Setup
- [ ] Clonar repositorio
- [ ] `pip install -r requirements.txt`
- [ ] Validar `processes.json`
- [ ] Ejecutar tests

### Fase 2: Integración
- [ ] Conectar TitaniaExtractor
- [ ] Conectar ONNETExtractor
- [ ] Integrar con ProcessMonitor v2
- [ ] Testing end-to-end

### Fase 3: Deployment
- [ ] Setup en staging
- [ ] Setup en producción
- [ ] Monitoreo
- [ ] Backup y recovery

---

## 🔗 Referencias Cruzadas

- **Evaluación**: [EVALUACION_ECOSISTEMA_PARAMETRIZABLE.md](../ProcessMonitor/EVALUACION_ECOSISTEMA_PARAMETRIZABLE.md)
- **Process Monitor v2**: [ProcessMonitor/README.md](../ProcessMonitor/README.md)
- **Titania Monitor**: [Titania/monitor_app.py](../Titania/monitor_app.py)
- **ONNET Monitor**: [ONNET/export_onnet_csv.py](../ONNET/export_onnet_csv.py)

---

## 🎓 Guías de Aprendizaje

**Para Desarrolladores Python**:
1. Empezar: [QUICK_START.md](./docs/QUICK_START.md)
2. Entender: [ARCHITECTURE.md](./docs/ARCHITECTURE.md)
3. Aprender: [DEVELOPER_GUIDE.md](./docs/DEVELOPER_GUIDE.md)

**Para DevOps**:
1. Setup: [QUICK_START.md](./docs/QUICK_START.md)
2. Config: [CONFIGURATION.md](./docs/CONFIGURATION.md)
3. Deploy: [README.md](./README.md)

**Para PMs**:
1. Overview: [README.md](./README.md)
2. Benefits: [EVALUACION_ECOSISTEMA_PARAMETRIZABLE.md](../ProcessMonitor/EVALUACION_ECOSISTEMA_PARAMETRIZABLE.md)

---

## 💻 Comandos Útiles

```bash
# Validar configuración
python scripts/validate_config.py

# Ejecutar tests
pytest

# Tests con cobertura
pytest --cov=unified_extraction

# Verificar estilo
black --check unified_extraction
isort --check unified_extraction

# Testing manual
python -m core.execution_engine --project titania --query "all"
```

---

**¿Listo?** Lee [README.md](../README.md) o [QUICK_START.md](./docs/QUICK_START.md)

