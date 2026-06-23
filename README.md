---
title: "🏗️ BPA_DataSolution - Ecosistema Unificado de Extracción"
date: "2024-04-24"
---

# 🏗️ BPA_DataSolution

**Business Process Automation - Data Solution**

Ecosistema parametrizable y unificado para la extracción, transformación y distribución de datos desde Titania y ONNET.

---

## 🎯 Objetivo

Crear **una única fuente de verdad** para definir, ejecutar y monitorear procesos de extracción de datos desde múltiples proyectos sin cambios de código.

---

## 📚 Documentacion Central del Proyecto

La documentacion viva del proyecto esta en:

- `docs/README.md` (hub principal)
- `docs/00_MEMORIA_PROYECTO.md`
- `docs/01_ARQUITECTURA_SOLUCION.md`
- `docs/02_DEFINICION_SOLUCION_COMO_Y_PARA_QUE.md`
- `docs/03_HISTORIA_USUARIO_SOLICITUD_NUEVO_PROCESO.md`
- `docs/04_BD_Y_REPOSITORIOS_MAS_USADOS_2026.md`

```
┌─────────────────────────────────────────────┐
│      BPA_DataSolution                       │
│  (Ecosistema Parametrizable)                │
├─────────────────────────────────────────────┤
│                                              │
│  Titania         ONNET         Future       │
│     ↓              ↓              ↓         │
│   queries      models         projects     │
│     ↓              ↓              ↓         │
│  ╭──────────────────────────────────────╮  │
│  │   processes.json                     │  │
│  │   (Configuración Parametrizable)     │  │
│  ╰──────────────────────────────────────╯  │
│     ↓                                       │
│  ╭──────────────────────────────────────╮  │
│  │   Unified Extraction Engine          │  │
│  │   • Validación                       │  │
│  │   • Ejecución                        │  │
│  │   • Monitoreo                        │  │
│  ╰──────────────────────────────────────╯  │
│     ↓                                       │
│  ╭──────────────────────────────────────╮  │
│  │   Process Monitor v2                 │  │
│  │   • Dashboard                        │  │
│  │   • Logs en tiempo real              │  │
│  │   • Analytics                        │  │
│  ╰──────────────────────────────────────╯  │
│                                              │
└─────────────────────────────────────────────┘
```

---

## 📦 Estructura del Repositorio

```
BPA_DataSolution/
│
├── unified_extraction/              # Motor de extracción unificado
│   ├── config/
│   │   ├── processes.json           # ⭐ Configuración única centralizada
│   │   ├── processes.schema.json    # Validación JSON Schema
│   │   └── examples/
│   │       └── processes.example.json
│   │
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── base.py                  # BaseExtractor (clase abstracta)
│   │   ├── titania.py               # TitaniaExtractor
│   │   ├── onnet.py                 # ONNETExtractor
│   │   └── registry.py              # Registro de extractores
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config_loader.py         # ProcessDefinitionLoader
│   │   ├── parameter_validator.py   # ParameterValidator
│   │   ├── command_builder.py       # CommandBuilder
│   │   └── execution_engine.py      # ExecutionEngine
│   │
│   ├── connectors/
│   │   ├── __init__.py
│   │   ├── titania_connector.py     # Conecta a Titania
│   │   └── onnet_connector.py       # Conecta a ONNET
│   │
│   ├── scripts/
│   │   ├── migrate_from_monitor.py  # Extrae config de monitor_app.py
│   │   ├── validate_config.py       # Valida processes.json
│   │   ├── test_extraction.py       # Testing manual
│   │   └── generate_docs.py         # Genera documentación
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_config_loader.py
│   │   ├── test_parameter_validator.py
│   │   ├── test_command_builder.py
│   │   ├── test_extractors.py
│   │   └── test_integration.py
│   │
│   ├── docs/
│   │   ├── ARCHITECTURE.md
│   │   ├── CONFIGURATION.md
│   │   ├── QUICK_START.md
│   │   └── DEVELOPER_GUIDE.md
│   │
│   ├── logs/                        # Logs de ejecución
│   │   └── .gitkeep
│   │
│   ├── __init__.py
│   ├── requirements.txt
│   ├── setup.py
│   └── pytest.ini
│
├── connectors/                      # Conectores a sistemas externos
│   ├── titania/
│   │   └── symlink o referencia a ../Titania
│   │
│   └── onnet/
│       └── symlink o referencia a ../ONNET
│
├── examples/
│   ├── basic_usage.py
│   ├── custom_extractor.py
│   └── monitoring_integration.py
│
├── .gitignore
├── .env.example
├── README.md                        # Este archivo
├── CONTRIBUTING.md
├── LICENSE
└── TODO.md                          # Próximos pasos
```

---

## 🚀 Quick Start

### 1. Instalación

```bash
cd BPA_DataSolution/unified_extraction

# Crear venv
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Validar Configuración

```bash
python scripts/validate_config.py
# ✓ processes.json es válido
# ✓ 2 extractores detectados (titania, onnet)
```

### 3. Ejecutar Extracción (Manual)

```bash
python -m unified_extraction.core.execution_engine \
  --project titania \
  --query "VW_n8n_chat_histories_classfication"
```

### 4. Integrar con Process Monitor v2

```bash
# En process_engine.py de ProcessMonitor v2
from BPA_DataSolution.unified_extraction.core import ExecutionEngine

engine = ExecutionEngine("config/processes.json")
result = engine.execute("titania", {"query": "all"})
```

---

## 📋 Archivos Clave

### `processes.json` (Configuración)
```json
{
  "version": "2.0",
  "projects": [
    {
      "id": "titania",
      "name": "Titania",
      "type": "sql_export",
      "execution": {
        "script": "export_queries_to_csv.py",
        "timeout_seconds": 1800
      },
      "parameters": {
        "query": {
          "type": "select",
          "options": ["VW_n8n_chat_histories_classfication", ...]
        }
      }
    },
    {
      "id": "onnet",
      "name": "ONNET",
      "type": "sql_export",
      "execution": {
        "script": "export_onnet_csv.py",
        "timeout_seconds": 3600
      },
      "parameters": {
        "model": {
          "type": "select",
          "options": ["all", "modelo3", "modelo4"]
        }
      }
    }
  ]
}
```

### `BaseExtractor` (Extensible)
```python
class BaseExtractor(ABC):
    """Clase base para todos los extractores"""
    
    @abstractmethod
    def validate_parameters(self, params: dict) -> bool:
        pass
    
    @abstractmethod
    def build_command(self, params: dict) -> list[str]:
        pass
    
    @abstractmethod
    def execute(self, params: dict) -> dict:
        pass
```

---

## 🔧 Capacidades

### ✅ Parametrización
- [x] Queries/modelos por proyecto
- [x] Parámetros opcionales y requeridos
- [x] Validación de tipos
- [x] Interpolación de variables

### ✅ Ejecución
- [x] Subprocess management
- [x] Timeout handling
- [x] Resource monitoring
- [x] Error handling

### ✅ Monitoreo
- [x] Logs en tiempo real
- [x] Status tracking
- [x] Métricas (CPU, memoria)
- [x] Historial

### ✅ Extensibilidad
- [x] Fácil agregar nuevo extractor
- [x] Fácil agregar nuevo proyecto
- [x] Plugin architecture
- [x] Custom validators

---

## 🎯 Integración con Process Monitor v2

Este repositorio proporciona el **engine de extracción** que Process Monitor v2 consume:

```
User interacts with Dashboard
           ↓
Process Monitor v2 (React + Flask)
           ↓
/api/execute endpoint
           ↓
BPA_DataSolution.ExecutionEngine
           ↓
Titania/ONNET scripts
           ↓
Output (CSV/Parquet)
```

---

## 📚 Documentación

- [ARCHITECTURE.md](./unified_extraction/docs/ARCHITECTURE.md) - Diseño técnico
- [CONFIGURATION.md](./unified_extraction/docs/CONFIGURATION.md) - Guía de configuración
- [QUICK_START.md](./unified_extraction/docs/QUICK_START.md) - Inicio rápido
- [DEVELOPER_GUIDE.md](./unified_extraction/docs/DEVELOPER_GUIDE.md) - Guía de desarrollo

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=unified_extraction

# Tests específicos
pytest tests/test_config_loader.py -v
```

---

## 🔄 Workflow de Desarrollo

### 1. Agregar nuevo proyecto (ej: SAP)
```python
# 1. Crear extractor en extractors/sap.py
class SAPExtractor(BaseExtractor):
    pass

# 2. Registrar en registry.py
EXTRACTORS["sap"] = SAPExtractor

# 3. Agregar a processes.json
{
  "id": "sap",
  "name": "SAP",
  ...
}

# 4. Testing
pytest tests/test_extractors.py

# 5. Listo - aparece en dashboard
```

### 2. Agregar nueva query a Titania
```json
// En processes.json -> titania -> parameters -> query -> options
"options": [
  "VW_n8n_chat_histories_classfication",
  ...
  "MI_NUEVA_QUERY"  // ← Agregar aquí
]
```

---

## 📊 Roadmap

### Fase 1 (Semana 1) ✅
- [x] Estructura base del repositorio
- [x] ConfigLoader y ParameterValidator
- [x] BaseExtractor architecture
- [x] Tests básicos

### Fase 2 (Semana 2)
- [ ] TitaniaExtractor implementation
- [ ] ONNETExtractor implementation
- [ ] Integration con Process Monitor v2
- [ ] Migration script

### Fase 3 (Semana 3)
- [ ] APScheduler integration
- [ ] Alerting engine
- [ ] Analytics
- [ ] Dashboard enhancements

### Fase 4 (Semana 4)
- [ ] Multi-cloud support
- [ ] Advanced scheduling
- [ ] API Gateway integration
- [ ] Documentation completa

---

## 🤝 Contributing

Ver [CONTRIBUTING.md](./CONTRIBUTING.md) para guía de contribuciones.

**Estándares**:
- Code style: Black + isort
- Type hints: 100%
- Test coverage: >80%
- Documentación: Docstrings + Markdown

---

## 📝 Configuración del Entorno

```bash
# Crear .env
cp .env.example .env

# Editar con valores reales
# TITANIA_SCRIPT_PATH=...
# ONNET_SCRIPT_PATH=...
```

---

## 🔐 Seguridad

- [x] No se exponen paths absolutos
- [x] Parámetros validados
- [x] Logs sanitizados
- [x] Timeout para hung processes
- [x] Error messages genéricos en API

---

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: `/docs` folder
- **Examples**: `/examples` folder

---

## 📄 License

MIT License - Ver LICENSE

---

## 🎉 Estado

**Prototipo**: En desarrollo  
**Versión**: 0.1.0-alpha  
**Última actualización**: 24/04/2024  

---

**¿Listo para empezar?** Ver [QUICK_START.md](./unified_extraction/docs/QUICK_START.md)

