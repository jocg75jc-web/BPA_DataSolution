---
title: "🚀 QUICK START - BPA_DataSolution"
date: "2024-04-24"
---

# 🚀 QUICK START - BPA_DataSolution

## ⏱️ 5 Minutos para Empezar

### 1. Setup (2 min)

```bash
cd BPA_DataSolution/unified_extraction

# Crear virtual environment
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Validar Configuración (1 min)

```bash
python scripts/validate_config.py
```

**Salida esperada**:
```
✓ processes.json válido
✓ Schema validation OK
✓ 2 proyectos detectados: titania, onnet
✓ Parámetros validados
```

### 3. Listar Proyectos (1 min)

```bash
python -c "
from core.config_loader import ConfigLoader

loader = ConfigLoader('config/processes.json')
for project in loader.get_all_projects():
    print(f'{project[\"id\"]}: {project[\"name\"]}')
"
```

### 4. Ejecutar Extracción (1 min)

```bash
python -m core.execution_engine \
  --project titania \
  --query "VW_n8n_chat_histories_classfication"
```

---

## 📚 Próximos Pasos

### Para Desarrolladores
1. Leer [ARCHITECTURE.md](./ARCHITECTURE.md)
2. Revisar [CONFIGURATION.md](./CONFIGURATION.md)
3. Explorar `/extractors/base.py`

### Para DevOps/Operaciones
1. Leer [QUICK_START.md](./QUICK_START.md) (este)
2. Personalizar `config/processes.json`
3. Configurar scheduling en `scheduling` section

### Para PMs/Stakeholders
1. Leer [README.md](../../README.md)
2. Ver [EVALUACION_ECOSISTEMA_PARAMETRIZABLE.md](../../ProcessMonitor/EVALUACION_ECOSISTEMA_PARAMETRIZABLE.md)

---

## 🔧 Casos de Uso Comunes

### Agregar Nueva Query a Titania

```json
{
  "id": "titania",
  "parameters": {
    "query": {
      "options": {
        "MI_NUEVA_QUERY": {
          "value": "MI_NUEVA_QUERY",
          "label": "My New Query",
          "description": "Descripción de la query"
        }
      }
    }
  }
}
```

### Agregar Nuevo Proyecto

1. **Crear extractor**:
   ```python
   # extractors/my_project.py
   from base import BaseExtractor
   
   class MyProjectExtractor(BaseExtractor):
       def validate_parameters(self, params):
           pass
       
       def build_command(self, params):
           pass
   ```

2. **Registrar en `processes.json`**:
   ```json
   {
     "id": "my_project",
     "name": "My Project",
     "execution": { ... }
   }
   ```

3. **Validar**:
   ```bash
   python scripts/validate_config.py
   ```

---

## 🐛 Debugging

### Config no valida

```bash
# Validación detallada
python -c "
from core.config_loader import ConfigLoader
import traceback

try:
    loader = ConfigLoader('config/processes.json')
except Exception as e:
    print(f'Error: {e}')
    traceback.print_exc()
"
```

### Extracción falla

```bash
# Con logging detallado
export PYTHONVERBOSE=1
python scripts/test_extraction.py --project titania --query "all"
```

---

## 📊 Integración con Process Monitor v2

```python
from BPA_DataSolution.unified_extraction.core import ExecutionEngine

# En process_engine.py de ProcessMonitor v2
engine = ExecutionEngine("config/processes.json")
result = engine.execute(
    project_id="titania",
    parameters={"query": "VW_n8n_chat_histories_classfication"}
)
```

---

## ✅ Checklist Pre-Production

- [ ] Todos los proyectos en `processes.json`
- [ ] Validación de config pasa
- [ ] Scripts de extracción funcionan
- [ ] Parámetros validados
- [ ] Environment variables configuradas
- [ ] Tests pasan
- [ ] Documentation actualizada

---

**¿Listo?** Sigue a [CONFIGURATION.md](./CONFIGURATION.md)

