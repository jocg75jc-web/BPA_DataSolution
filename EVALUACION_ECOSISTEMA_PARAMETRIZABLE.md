---
title: "🏗️ Evaluación - Ecosistema Unificado de Extracción"
date: "2024-04-24"
---

# 🏗️ Evaluación: Ecosistema Unificado de Extracción Parametrizable

## 📊 Situación Actual Analizada

### Estructura Existente (monitor_app.py)

```
PROJECT_CONFIG
├── Titania
│   ├── script: export_queries_to_csv.py
│   ├── output_dir: ./output
│   └── queries: 6 queries VW_n8n_*
│
└── ONNET
    ├── script: export_onnet_csv.py
    ├── output_dir: ./ONNET/output
    └── queries: 3 queries (all, modelo3, modelo4)
```

**Problemas Identificados**:
1. ❌ Hardcoded en PROJECT_CONFIG (dict de Python)
2. ❌ Procesos independientes sin parámetros comunes
3. ❌ Queries duplicadas en TITANIA_QUERIES + ONNET_QUERIES
4. ❌ Lógica de ejecución mezclada (Titania vs ONNET)
5. ❌ No escalable (agregar proyecto = modificar código)
6. ❌ Sin versionado de configuración

---

## 🎯 Visión: Ecosistema Parametrizable

### Objetivo

```
Crear UNA configuración JSON que:
✅ Defina TODOS los procesos (Titania, ONNET, futuras)
✅ Sea parametrizable (sin código)
✅ Sea versionada y auditable
✅ Soporte diferentes tipos de extracción
✅ Permita reutilización de configuración
```

---

## 🏛️ Propuesta de Arquitectura

### Nivel 1: Configuración Base (`processes.json`)

```json
{
  "version": "2.0",
  "environment": "production",
  "projects": [
    {
      "id": "titania",
      "name": "Titania",
      "description": "Sistema de chat - Extracción de queries",
      "type": "sql_export",
      "enabled": true,
      
      "execution": {
        "script": "export_queries_to_csv.py",
        "workdir": "${PROJECT_ROOT}/Titania",
        "python": ".venv/Scripts/python.exe",
        "timeout_seconds": 1800,
        "retry_count": 2,
        "retry_delay_seconds": 60
      },
      
      "parameters": {
        "query": {
          "type": "select",
          "required": true,
          "default": "all",
          "options": ["all", "VW_n8n_chat_histories_classfication", ...]
        },
        "database": {
          "type": "text",
          "required": false,
          "default": null,
          "placeholder": "Leave empty for default"
        },
        "output_format": {
          "type": "select",
          "required": false,
          "default": "csv",
          "options": ["csv", "parquet", "xlsx"]
        }
      },
      
      "outputs": {
        "directory": "${PROJECT_ROOT}/Titania/output",
        "pattern": "${QUERY_NAME}_${TIMESTAMP}.csv",
        "retention_days": 30
      },
      
      "scheduling": {
        "enabled": true,
        "expressions": [
          "0 */2 * * *"  # Cada 2 horas
        ],
        "windows_task": "Titania_Export_SFTP_Cada2Horas"
      },
      
      "notifications": {
        "on_failure": {
          "enabled": true,
          "channels": ["email"]
        },
        "on_success": {
          "enabled": false,
          "channels": []
        }
      }
    },
    
    {
      "id": "onnet",
      "name": "ONNET",
      "description": "Sistema de operaciones - Modelos 3 y 4",
      "type": "sql_export",
      "enabled": true,
      
      "execution": {
        "script": "export_onnet_csv.py",
        "workdir": "${PROJECT_ROOT}/ONNET",
        "python": ".venv/Scripts/python.exe",
        "timeout_seconds": 3600,
        "retry_count": 2,
        "retry_delay_seconds": 60
      },
      
      "parameters": {
        "model": {
          "type": "select",
          "required": true,
          "default": "all",
          "options": ["all", "modelo3", "modelo4"]
        },
        "date_filter": {
          "type": "date",
          "required": false,
          "default": null
        }
      },
      
      "outputs": {
        "directory": "${PROJECT_ROOT}/ONNET/output",
        "pattern": "${MODEL}_${TIMESTAMP}.csv",
        "retention_days": 7
      },
      
      "scheduling": {
        "enabled": true,
        "expressions": [
          "0 */4 * * *"  # Cada 4 horas
        ],
        "windows_task": "ONNET_Export_SFTP_Cada4Horas"
      },
      
      "notifications": {
        "on_failure": {
          "enabled": true,
          "channels": ["email", "slack"]
        }
      }
    }
  ],
  
  "parameters_schema": {
    "types": {
      "select": {
        "ui": "dropdown",
        "validation": "options[]"
      },
      "text": {
        "ui": "textinput",
        "validation": "regex or none"
      },
      "date": {
        "ui": "datepicker",
        "validation": "ISO8601"
      },
      "number": {
        "ui": "numberinput",
        "validation": "min/max"
      }
    }
  }
}
```

---

## 🔧 Nivel 2: Procesador de Configuración

### `unified_extraction.py`

```python
class ProcessDefinitionLoader:
    """Carga y valida configuración de procesos"""
    
    def __init__(self, config_path: str):
        self.config = self._load_and_validate(config_path)
    
    def get_all_projects(self) -> list[ProjectDefinition]:
        """Retorna todos los proyectos habilitados"""
        return [p for p in self.config["projects"] if p["enabled"]]
    
    def get_project(self, project_id: str) -> ProjectDefinition:
        """Retorna configuración de un proyecto"""
        for p in self.config["projects"]:
            if p["id"] == project_id:
                return p
        raise ValueError(f"Proyecto no encontrado: {project_id}")
    
    def get_parameters(self, project_id: str) -> ParametersDefinition:
        """Retorna definición de parámetros de un proyecto"""
        project = self.get_project(project_id)
        return project["parameters"]
    
    def validate_parameters(self, project_id: str, params: dict) -> bool:
        """Valida parámetros contra schema"""
        params_def = self.get_parameters(project_id)
        # Validación contra schema
        return True
    
    def build_command(self, project_id: str, user_params: dict) -> list[str]:
        """Construye comando a ejecutar desde parámetros"""
        project = self.get_project(project_id)
        
        cmd = [
            self._get_python_exe(project),
            project["execution"]["script"]
        ]
        
        # Interpolación de parámetros
        for param_name, param_value in user_params.items():
            cmd.extend([f"--{param_name}", str(param_value)])
        
        return cmd
```

---

## 📦 Nivel 3: Mapper de Configuración Actual → Nueva

### Extractor de Configuración

```python
def extract_current_configuration() -> dict:
    """
    Lee monitor_app.py actual y genera processes.json equivalente
    
    Mapea:
    - PROJECT_CONFIG → projects[].execution
    - PROJECT_QUERIES → projects[].parameters.options
    - PROJECT_SCHEDULE_TASKS → projects[].scheduling.windows_task
    """
    
    config = {
        "version": "2.0",
        "projects": []
    }
    
    # Titania
    titania = {
        "id": "titania",
        "name": "Titania",
        "execution": {
            "script": "export_queries_to_csv.py",
            "workdir": "${PROJECT_ROOT}/Titania",
            "timeout_seconds": 1800
        },
        "parameters": {
            "query": {
                "type": "select",
                "options": list(TITANIA_QUERIES.keys()),
                "default": "all"
            },
            "database": {
                "type": "text",
                "required": false,
                "default": null
            }
        },
        "scheduling": {
            "windows_task": PROJECT_SCHEDULE_TASKS["Titania"][0]
        }
    }
    config["projects"].append(titania)
    
    # ONNET
    onnet = {
        "id": "onnet",
        "name": "ONNET",
        "execution": {
            "script": "export_onnet_csv.py",
            "workdir": "${PROJECT_ROOT}/ONNET",
            "timeout_seconds": 3600
        },
        "parameters": {
            "model": {
                "type": "select",
                "options": list(ONNET_QUERIES.keys()),
                "default": "all"
            }
        },
        "scheduling": {
            "windows_task": PROJECT_SCHEDULE_TASKS["ONNET"][0]
        }
    }
    config["projects"].append(onnet)
    
    return config
```

---

## 🎨 Nivel 4: Integración con ProcessMonitor v2

### Cómo se conecta

```
processes.json (NUEVO)
    ↓
ProcessDefinitionLoader
    ↓
UnifiedExtraction.py
    ↓
ProcessEngine (ProcessMonitor v2)
    ↓
Web Dashboard (React)
```

### Flujo

```
1. Usuario abre Dashboard
   ↓
2. Dashboard carga /api/processes
   ↓
3. ProcessEngine carga processes.json
   ↓
4. Renderiza tarjetas para cada proyecto
   ↓
5. Usuario selecciona parámetros
   ↓
6. Ejecuta POST /api/execute con parámetros
   ↓
7. UnifiedExtraction.build_command()
   ↓
8. subprocess.Popen()
   ↓
9. Logs en tiempo real via WebSocket
```

---

## 🔄 Opciones de Implementación

### Opción A: Reuso Completo (Recomendada)
```
✅ Usar processes.json como única fuente de verdad
✅ Eliminar PROJECT_CONFIG de monitor_app.py
✅ Migración gradual
✅ Compatibilidad total con v2
⏱️ Tiempo: 3-4 días
```

### Opción B: Migración Dual (Transición)
```
✅ Mantener monitor_app.py funcionando
✅ Agregar unified_extraction.py paralelo
✅ Datos sincronizados bidireccionales
⏱️ Tiempo: 5-6 días
```

### Opción C: Wrapper (Rápido)
```
✅ Generar processes.json automáticamente de monitor_app.py
✅ Sin cambios en Titania/ONNET
✅ Transición más lenta
⏱️ Tiempo: 1-2 días
```

---

## 📋 Comparativa de Opciones

| Aspecto | Opción A | Opción B | Opción C |
|--------|---------|---------|---------|
| **Implementación** | Refactor completo | Dual track | Wrapper |
| **Tiempo** | 3-4 días | 5-6 días | 1-2 días |
| **Riesgo** | Medio | Bajo | Muy bajo |
| **Beneficio** | Alto | Medio | Bajo |
| **Limpieza código** | Excelente | Buena | Pobre |
| **Escalabilidad** | Excelente | Buena | Regular |
| **Recommended** | ✅ | | |

---

## 🚀 Plan de Acción (Opción A: Recomendada)

### Fase 1: Análisis Profundo (1 día)

```
☐ Revisar TITANIA_QUERIES completamente
☐ Revisar ONNET_QUERIES completamente
☐ Mapear parámetros de ambos scripts
☐ Entender opciones de cada query
☐ Documentar valores por defecto
☐ Identificar parámetros ocultos
```

### Fase 2: Diseño del Schema (1 día)

```
☐ Finalizar structure de processes.json
☐ Crear JSON Schema para validación
☐ Documentar convenciones de naming
☐ Definir variable interpolation (${VAR})
☐ Definir tipos de parámetros
☐ Crear ejemplos
```

### Fase 3: Implementación (1.5 días)

```
☐ Crear unified_extraction.py
☐ Crear ProcessDefinitionLoader
☐ Crear migration script (monitor_app.py → processes.json)
☐ Unit tests
☐ Validación de configuración
```

### Fase 4: Integración (0.5 días)

```
☐ Integrar con ProcessEngine v2
☐ Agregar endpoints REST
☐ Testing end-to-end
☐ Documentación
```

---

## 🎯 Beneficios de este Ecosistema

### Immediatamente
```
✅ Parámetros en UI (no código)
✅ Histórico de ejecuciones
✅ Reporte unificado
✅ Más fácil agregar procesos
```

### Corto Plazo (1 mes)
```
✅ Scheduler automático
✅ Alerting centralizado
✅ Auditoría de cambios
✅ Versionado de config
```

### Largo Plazo (3-6 meses)
```
✅ Agregar proyectos nuevos (0 código)
✅ Reproducibilidad de ejecuciones
✅ Optimización automática
✅ Analytics y predicción
```

---

## 🔍 Estructura de Directorios Final

```
botsquad/
├── Titania/
│   ├── export_queries_to_csv.py (sin cambios)
│   └── output/
│
├── ONNET/
│   ├── export_onnet_csv.py (sin cambios)
│   └── output/
│
└── ProcessMonitor/
    ├── ENTREGA_FINAL.md
    ├── QUICK_START.md
    ├── ... (resto de docs)
    │
    ├── backend/
    │   ├── process_engine.py (existente)
    │   ├── api.py (existente)
    │   │
    │   ├── unified_extraction.py      ← NUEVO
    │   ├── config_loader.py            ← NUEVO
    │   ├── parameter_validator.py      ← NUEVO
    │   │
    │   └── config/
    │       ├── processes.json          ← NUEVO (única fuente de verdad)
    │       ├── processes.schema.json   ← NUEVO (validación)
    │       └── examples/
    │           └── processes.example.json
    │
    ├── scripts/
    │   └── migrate_config.py           ← NUEVO (extractor)
    │
    └── tests/
        ├── test_config_loader.py       ← NUEVO
        └── test_unified_extraction.py  ← NUEVO
```

---

## 💡 Ejemplo de Uso (Una vez implementado)

### Agregar Nuevo Proceso (ANTES)
```python
# monitor_app.py
PROJECT_CONFIG = {
    # ... copiar todo, modificar...
    "MiNuevoProyecto": {
        "script": ...,
        "queries": {...},
        # ... más cambios
    }
}
# Reiniciar monitor_app.py
```

### Agregar Nuevo Proceso (DESPUÉS)
```json
// processes.json
{
  "id": "mi-nuevo-proyecto",
  "name": "Mi Nuevo Proyecto",
  "execution": { ... },
  "parameters": { ... }
}
// Listo - aparece automáticamente en dashboard
```

---

## ✅ Recomendación Final

### 🎯 Implementar Opción A (Completa)

**Razones**:
1. ✅ Limpia la arquitectura
2. ✅ Habilita Process Monitor v2
3. ✅ Escalable para el futuro
4. ✅ Facilita auditoría y cambios
5. ✅ Prepara para scheduler automático

**Timeline**:
- Fase 1: 1 día
- Fase 2: 1 día
- Fase 3: 1.5 días
- Fase 4: 0.5 días
- **Total: 4 días**

**Equipo requerido**:
- 1 Backend Dev (lead)
- 1 QA (validación)

**Dependencias**:
- Acceso a código actual
- Acceso a scripts de extracción
- Base de datos de testing

---

## 📞 Próximos Pasos

1. **Revisar esta evaluación** ← Aquí
2. **Aprobación de enfoque** (hoy)
3. **Fase 1: Análisis profundo** (mañana)
4. **Fase 2: Diseño schema** (día 2)
5. **Fase 3-4: Implementación** (días 3-4)
6. **Testing y validación** (día 5)
7. **Documentación y handoff** (día 6)

---

**¿Proceder con Opción A?** ✅

