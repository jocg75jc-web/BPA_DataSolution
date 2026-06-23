---
version: "3.0"
title: "Plan de Migración: Monitor Actual → Process Monitor v2"
date: "2024-04-24"
---

# 📋 Plan de Migración - Monitor Actual → v2

## 🎯 Objetivo

Reemplazar `monitor_app.py` (Titania) y su variante (ONNET) con **Process Monitor v2** manteniendo continuidad operacional.

---

## 📊 Fase 0: Preparación (1 semana)

### Tareas
- [ ] Setup repositorio ProcessMonitor
- [ ] Instalar dependencias frontend/backend
- [ ] Setup dev environment
- [ ] Documentación para equipo

**Output**: Environment listo, equipo capacitado

---

## 🔧 Fase 1: Extracción de Configuración (2-3 días)

### 1.1 Analizar `monitor_app.py`

Extraer información de:
```python
PROJECT_CONFIG = {
    "Titania": { "script": ..., "output_dir": ..., "log_file": ... },
    "ONNET": { "script": ..., "output_dir": ..., "log_file": ... }
}

PROJECT_SCHEDULE_TASKS = {
    "Titania": ["Titania_Export_SFTP_Cada2Horas_FIX", ...],
    "ONNET": ["ONNET_Export_SFTP_Cada4Horas_FIX", ...]
}

PROJECT_QUERIES = {
    "Titania": { "VW_n8n_chat_histories_classfication": {...}, ... },
    "ONNET": { "modelo3": {...}, "modelo4": {...} }
}
```

### 1.2 Crear `processes.json`

```json
{
  "processes": [
    {
      "id": "titania-export-sftp",
      "name": "Titania Export SFTP",
      "description": "Exporta queries de Titania a CSV y carga vía SFTP",
      "project": "Titania",
      "type": "python_script",
      "enabled": true,
      "priority": 1,
      
      "command": {
        "script": "export_queries_to_csv.py",
        "workdir": "${PROJECT_ROOT}/Titania",
        "timeout_seconds": 1800,
        "env_vars": {
          "EXPORT_MODE": "sftp",
          "LOG_LEVEL": "INFO"
        }
      },
      
      "parameters": [
        {
          "name": "queries",
          "type": "multi_select",
          "values": ["all", "chat_histories", "user_banned", ...],
          "default": "all",
          "required": true
        }
      ],
      
      "schedule": {
        "type": "cron",
        "expression": "0 */2 * * *",
        "enabled": true,
        "timezone": "America/Bogota"
      },
      
      "notifications": {
        "on_failure": {
          "enabled": true,
          "channels": ["email", "slack"],
          "retry_count": 3
        }
      }
    },
    
    {
      "id": "onnet-export-modelo3",
      "name": "ONNET Export Modelo 3",
      "project": "ONNET",
      "type": "python_script",
      "command": {
        "script": "export_onnet_csv.py",
        "workdir": "${PROJECT_ROOT}/ONNET",
        "timeout_seconds": 3600,
        "env_vars": { "MODELO": "3" }
      },
      "schedule": {
        "type": "cron",
        "expression": "0 */4 * * *",
        "enabled": true
      }
    },
    
    {
      "id": "onnet-export-modelo4",
      "name": "ONNET Export Modelo 4",
      "project": "ONNET",
      "type": "python_script",
      "command": {
        "script": "export_onnet_csv.py",
        "workdir": "${PROJECT_ROOT}/ONNET",
        "timeout_seconds": 3600,
        "env_vars": { "MODELO": "4" }
      },
      "schedule": {
        "type": "cron",
        "expression": "0 */4 * * *",
        "enabled": true
      }
    }
  ],
  
  "defaults": {
    "timeout_seconds": 1800,
    "timezone": "America/Bogota",
    "log_retention_days": 30
  }
}
```

**Tasks**:
- [ ] Extraer todos los procesos
- [ ] Validar structure
- [ ] Crear schema JSON
- [ ] Documentar cada proceso

---

## 🗄️ Fase 2: Migración de Datos Históricos (1-2 días)

### 2.1 Exportar Historial

```python
# Script para migrar datos de history_db.py → PostgreSQL (próximo)

import json
from pathlib import Path
from datetime import datetime

source_db = "Titania/logs/history.db"  # SQLite actual
output = "migration_export.jsonl"

# Extraer ejecuciones
with open(output, 'w') as f:
    for execution in get_all_executions(source_db):
        f.write(json.dumps({
            "execution_id": execution.id,
            "process_id": execution.process_id,
            "project": execution.project,
            "status": execution.status,
            "start_time": execution.start_time.isoformat(),
            "end_time": execution.end_time.isoformat(),
            "duration_seconds": execution.duration_seconds,
            "exit_code": execution.exit_code,
            "output_files": execution.output_files,
        }) + '\n')
```

### 2.2 Validar Integridad

```bash
# Verificar que no hay pérdida de datos
echo "Registros antiguos: $(sqlite3 Titania/logs/history.db 'SELECT COUNT(*) FROM executions')"
echo "Registros exportados: $(wc -l < migration_export.jsonl)"
```

**Tasks**:
- [ ] Crear script de exportación
- [ ] Validar integridad
- [ ] Backup de BD anterior
- [ ] Documentar proceso

---

## 🚀 Fase 3: Deploy en DEV (3-5 días)

### 3.1 Frontend

```bash
cd ProcessMonitor
npm install
npm run dev
# Acceder a http://localhost:5173
```

### 3.2 Backend

```bash
cd ProcessMonitor/backend
pip install -r requirements.txt
python api.py
# API en http://localhost:5000
```

### 3.3 Cargar Configuración

```bash
cp config/processes.json.template ProcessMonitor/config/processes.json
# Editar con procesos reales
```

**Tasks**:
- [ ] Deploy frontend en dev
- [ ] Deploy backend en dev
- [ ] Cargar processes.json
- [ ] Verificar conectividad REST + WebSocket

---

## ✅ Fase 4: Testing (1 semana)

### 4.1 Funcional

```bash
# Test ejecución manual
curl -X POST http://localhost:5000/api/execute/titania-export-sftp \
  -H "Content-Type: application/json" \
  -d '{"queries": "all"}'

# Verificar en dashboard
# Debe aparecer el proceso ejecutándose en tiempo real
# Logs en vivo vía WebSocket
```

### 4.2 Regression

Ejecutar procesos actuales en ambos sistemas y comparar:
- [ ] Titania export CSV (validar archivos)
- [ ] ONNET export M3 (validar rowcount)
- [ ] ONNET export M4 (validar rowcount)
- [ ] Comparar output con versión anterior

### 4.3 Performance

```bash
# Load test: 10 procesos simultáneos
for i in {1..10}; do
  curl -X POST http://localhost:5000/api/execute/onnet-export-modelo3 &
done
wait

# Verificar:
# - CPU no excede 80%
# - Memory estable
# - Logs fluyen en tiempo real
# - Todos completaron exitosamente
```

**Tasks**:
- [ ] Test manual de procesos
- [ ] Validar outputs
- [ ] Comparar con versión anterior
- [ ] Load testing
- [ ] Documentar issues encontrados

---

## 🔄 Fase 5: Staging (Paralelo con producción actual)

### 5.1 Setup Staging

- Clonar infraestructura de prod
- Deploy v2 en staging
- Configurar Windows Task Scheduler para ejecutar v2 en paralelo

### 5.2 Ejecución Dual

```
Titania/monitor_app.py  ← Continúa en prod
ProcessMonitor v2       ← Corre en paralelo en staging
                         (sin afectar procesos reales)
```

### 5.3 Validación

- [ ] Ejecutar procesos en ambos sistemas
- [ ] Comparar outputs diarios
- [ ] Validar logs
- [ ] Monitorear performance

**Duración**: 1-2 semanas (hasta validar 100% match)

---

## 🚢 Fase 6: Cutover (Día D)

### 6.1 Pre-cutover (día anterior)

```bash
# Backup de todo
tar -czf monitor_backup_$(date +%Y%m%d).tar.gz \
  Titania/logs/ \
  ONNET/logs/ \
  ProcessMonitor/

# Última ejecución en monitor_app.py
# Verificar que procesos completaron exitosamente
```

### 6.2 Cutover Steps

**08:00 - Stop old monitor**
```bash
# Detener monitor_app.py
taskkill /IM python.exe /F  # (o gestionar gracefully)

# Esperar a que se completen procesos activos
```

**08:30 - Start new monitor**
```bash
cd ProcessMonitor/backend
nohup python api.py &
# Verificar http://localhost:5000/api/health
```

**08:45 - Verificación**
- [ ] Dashboard accesible
- [ ] Procesos visibles
- [ ] WebSocket funcionando
- [ ] Logs en tiempo real

**09:00 - Enable scheduled tasks**
```bash
# Cambiar Windows Task Scheduler para apuntar a v2
# O usar APScheduler (próximo)
```

**09:15 - Monitoring**
- [ ] Ejecutar procesos programados
- [ ] Validar outputs
- [ ] Alerta a equipo de que está vivo

### 6.3 Rollback Plan

Si algo falla:
```bash
# Revertir a monitor_app.py
taskkill /IM python.exe /F
python Titania/monitor_app.py

# O:
git checkout Titania/monitor_app.py
python Titania/monitor_app.py
```

**Tasks**:
- [ ] Backup pre-cutover
- [ ] Stop old monitor
- [ ] Start v2
- [ ] Verificación
- [ ] Enable scheduled tasks
- [ ] Team handoff

---

## 📊 Fase 7: Post-cutover (1-2 semanas)

### 7.1 Monitoring

- [ ] Dashboard 99.9% availability
- [ ] Logs capturados correctamente
- [ ] Performance dentro de SLA
- [ ] No regressions

### 7.2 Cleanup

```bash
# Archivar archivos antiguos
tar -czf archive/monitor_app_old_$(date +%Y%m%d).tar.gz \
  Titania/monitor_app.py.backup \
  Titania/static/

# Desactivar Windows Task Scheduler tasks antiguas
```

### 7.3 Documentation

- [ ] Actualizar runbooks
- [ ] Capacitación del team
- [ ] Wiki con FAQ
- [ ] Contactos de soporte

**Tasks**:
- [ ] Daily health checks
- [ ] Cleanup de archivos
- [ ] Documentación
- [ ] Capacitación team

---

## 🛑 Rollback Strategy

En cualquier fase, si algo crítico falla:

```
1. IMMEDIATE: Revertir a monitor_app.py
2. NOTIFICATION: Alertar a team y stakeholders
3. ROOT CAUSE: Investigar issue en v2
4. FIX: Corregir en dev
5. RETRY: Cuando esté ready, reintentar Phase
```

**Parámetros de rollback**:
- Pérdida >5 minutos de datos
- Más de 3 procesos fallidos consecutivos
- CPU/Memory excedidos
- WebSocket desconexión >10 min

---

## 📈 Cronograma Estimado

```
Week 1:  Fase 0 (prep) + Fase 1 (extracción)
Week 2:  Fase 2 (datos) + Fase 3 (dev deploy)
Week 3:  Fase 4 (testing) + fixes
Week 4:  Fase 5 (staging paralelo)
Week 5:  Fase 6 (cutover) + Fase 7 (post)

TOTAL: ~5 semanas
```

---

## 👥 Equipo Responsable

| Rol | Persona | Responsabilidades |
|-----|---------|-------------------|
| Backend | Python Dev | ProcessEngine, API, deployment |
| Frontend | React Dev | Dashboard, UX |
| DevOps | Infra | Environments, CI/CD, monitoring |
| QA | Tester | Testing, validation, docs |
| PM | Lead | Coordination, blockers |

---

## 📋 Checklist Final

- [ ] processes.json validado y completo
- [ ] Historial migrado y verificado
- [ ] Staging corriendo 2 semanas sin issues
- [ ] Runbooks actualizados
- [ ] Team capacitado
- [ ] Backup de ambiente actual
- [ ] Rollback plan documentado
- [ ] Communication plan listos (email, slack, wiki)

---

## 🎉 Success Criteria

✅ v2 reemplaza monitor_app.py 100%  
✅ Todos los procesos ejecutándose correctamente  
✅ Dashboard accesible y responsive  
✅ Logs en tiempo real sin latencia  
✅ Performance ≥ a versión anterior  
✅ Team adopta nueva interfaz sin issues  
✅ Cero data loss  

---

## 📞 Contactos & Escalation

- **Tech Lead**: [name] - Decisiones técnicas
- **Product**: [name] - Roadmap y prioridades
- **Ops**: [name] - Deployment y monitoring
- **Support**: [name] - Issues post-go-live

