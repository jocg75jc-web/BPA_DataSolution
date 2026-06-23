# Monitor de Procesos v2 - Diseño Arquitectónico

## 📋 Resumen Ejecutivo

Sistema modular y parametrizable de monitoreo de procesos para ecosistema multi-proyecto (Titania, ONNET, y futuros). Soporta ejecución en tiempo real, historial, estadísticas, y alertas con configuración por archivo (JSON/YAML).

---

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                   Process Monitor v2                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Frontend (React 19 + MUI 5 + TypeScript)             │   │
│  │  ├─ Dashboard dinámico                               │   │
│  │  ├─ Monitoreo en tiempo real (WebSocket)             │   │
│  │  ├─ Gestión de procesos                              │   │
│  │  └─ Histórico y analytics                            │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Backend API (Python Flask)                          │   │
│  │  ├─ /api/processes (CRUD)                            │   │
│  │  ├─ /api/execute/:process-id                         │   │
│  │  ├─ /api/status/:process-id                          │   │
│  │  ├─ /api/logs/:process-id (WebSocket)                │   │
│  │  ├─ /api/history                                     │   │
│  │  └─ /api/config (validación y reload)                │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Process Configuration Engine                        │   │
│  │  ├─ Config file parser (JSON/YAML)                   │   │
│  │  ├─ Process definition validator                     │   │
│  │  ├─ Parameter interpolation                          │   │
│  │  └─ Dependency resolver                              │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Execution Engine                                    │   │
│  │  ├─ Process runner (script/command)                  │   │
│  │  ├─ Real-time log streamer                           │   │
│  │  ├─ Resource monitor (CPU, memory)                   │   │
│  │  └─ Error handler & recovery                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↓                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Storage Layer                                       │   │
│  │  ├─ Execution history (SQLite/PostgreSQL)            │   │
│  │  ├─ Log archive                                      │   │
│  │  └─ Metrics & analytics                              │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Estructura de Configuración

### 1. **Process Definition (processes.json)**

```json
{
  "processes": [
    {
      "id": "titania-export-sftp",
      "name": "Titania Export SFTP",
      "description": "Export queries to CSV and upload via SFTP",
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
          "description": "Queries to export",
          "values": ["all", "chat_histories", "user_banned"],
          "default": "all",
          "required": true
        },
        {
          "name": "batch_size",
          "type": "number",
          "description": "Batch size for processing",
          "min": 100,
          "max": 10000,
          "default": 1000,
          "required": false
        }
      ],
      
      "schedule": {
        "type": "cron",
        "expression": "0 */2 * * *",  // Cada 2 horas
        "enabled": true,
        "timezone": "America/Bogota"
      },
      
      "notifications": {
        "on_success": {
          "enabled": true,
          "channels": ["email", "slack"]
        },
        "on_failure": {
          "enabled": true,
          "channels": ["email", "slack", "dashboard_alert"],
          "retry_count": 3,
          "retry_delay_seconds": 300
        }
      },
      
      "dependencies": [
        {
          "process_id": "db-health-check",
          "type": "must_succeed"
        }
      ],
      
      "monitoring": {
        "track_duration": true,
        "track_resources": true,
        "alert_if_duration_exceeds_seconds": 1800,
        "max_concurrent_runs": 1
      }
    },
    
    {
      "id": "onnet-export-modelo3",
      "name": "ONNET Export Modelo 3",
      "description": "Export Modelo 3 data (Transacciones)",
      "project": "ONNET",
      "type": "python_script",
      "enabled": true,
      "priority": 2,
      
      "command": {
        "script": "export_onnet_csv.py",
        "workdir": "${PROJECT_ROOT}/ONNET",
        "timeout_seconds": 3600,
        "env_vars": {
          "MODELO": "3",
          "LOG_LEVEL": "INFO"
        }
      },
      
      "parameters": [
        {
          "name": "modelo",
          "type": "select",
          "description": "Data model to export",
          "values": ["modelo3", "modelo4", "all"],
          "default": "modelo3",
          "required": true
        },
        {
          "name": "date_range",
          "type": "date_range",
          "description": "Date range for export",
          "default": "last_7_days",
          "required": false
        }
      ],
      
      "schedule": {
        "type": "cron",
        "expression": "0 */4 * * *",  // Cada 4 horas
        "enabled": true,
        "timezone": "America/Bogota"
      },
      
      "notifications": {
        "on_failure": {
          "enabled": true,
          "channels": ["email", "slack"],
          "retry_count": 2
        }
      },
      
      "monitoring": {
        "track_duration": true,
        "track_resources": true,
        "alert_if_duration_exceeds_seconds": 3600
      }
    }
  ],
  
  "defaults": {
    "timeout_seconds": 1800,
    "log_retention_days": 30,
    "timezone": "America/Bogota",
    "max_log_size_mb": 50
  }
}
```

### 2. **Alertas y Notificaciones**

```json
{
  "alerts": [
    {
      "id": "alert-process-timeout",
      "name": "Process Timeout Alert",
      "condition": "execution_duration > process.alert_threshold",
      "severity": "warning",
      "channels": ["email", "slack", "dashboard"],
      "template": "El proceso {process_name} excedió {alert_threshold}s (duración actual: {duration}s)"
    },
    {
      "id": "alert-process-failure",
      "name": "Process Failure Alert",
      "condition": "execution_status == 'failed'",
      "severity": "critical",
      "channels": ["email", "slack", "dashboard", "pagerduty"],
      "template": "Error en {process_name}: {error_message}"
    },
    {
      "id": "alert-resource-spike",
      "name": "Resource Spike Alert",
      "condition": "cpu_percent > 80 OR memory_percent > 85",
      "severity": "warning",
      "channels": ["slack", "dashboard"]
    }
  ]
}
```

---

## 🔄 Flujo de Ejecución

### Manual Execution (Dashboard)
```
1. User selects process & parameters in UI
2. Frontend sends POST /api/execute/:process-id
3. Backend validates config + dependencies
4. Execution Engine starts process
5. Real-time logs streamed via WebSocket
6. Frontend displays live dashboard
7. On completion: update history + send notifications
```

### Scheduled Execution
```
1. Scheduler (APScheduler) reads cron expressions
2. At scheduled time, initiates execution
3. Same flow as manual execution
4. On failure, applies retry policy
5. Logs and metrics persisted
```

---

## 🎨 Frontend Components (React + MUI v5)

### Component Hierarchy

```
ProcessMonitor (Page)
├─ ProcessGrid (responsive grid of cards)
│  └─ ProcessCard (each process)
│     ├─ ProcessStatus (status badge)
│     ├─ ProcessMetrics (duration, CPU, memory)
│     ├─ ProcessActions (run, schedule, logs)
│     └─ LastRun (timestamp, status)
│
├─ ProcessDetails (drawer/modal)
│  ├─ ExecutionTimeline
│  ├─ ParameterForm
│  ├─ LogViewer (live + historical)
│  ├─ ScheduleEditor
│  └─ NotificationSettings
│
├─ Dashboard (analytics)
│  ├─ ExecutionStats (success rate, avg duration)
│  ├─ TimelineChart (execution history)
│  ├─ ResourceMetrics (CPU, memory over time)
│  └─ AlertsFeed
│
└─ Settings (global config)
   ├─ ConfigEditor
   ├─ AlertRules
   └─ NotificationChannels
```

---

## 🔌 API Endpoints

### Process Management
- `GET /api/processes` - List all processes
- `GET /api/processes/:id` - Get process details
- `POST /api/processes` - Create new process (admin)
- `PUT /api/processes/:id` - Update process (admin)
- `DELETE /api/processes/:id` - Delete process (admin)

### Execution
- `POST /api/execute/:process-id` - Start execution with parameters
- `GET /api/status/:process-id` - Current execution status
- `POST /api/stop/:process-id` - Stop running process
- `GET /api/history/:process-id` - Execution history

### Logs & Monitoring
- `WS /api/logs/:process-id/:execution-id` - Real-time log stream
- `GET /api/logs/:process-id/:execution-id` - Historical logs
- `GET /api/metrics/:process-id` - Process metrics

### Configuration
- `GET /api/config` - Get current configuration
- `POST /api/config/validate` - Validate config file
- `POST /api/config/reload` - Reload processes from file
- `GET /api/config/schema` - JSON Schema for validation

---

## 📊 Data Models

### Execution Record
```typescript
interface Execution {
  id: string;
  process_id: string;
  project: string;
  start_time: ISO8601;
  end_time?: ISO8601;
  status: 'running' | 'success' | 'failed' | 'stopped';
  exit_code?: number;
  error_message?: string;
  parameters: Record<string, any>;
  resources: {
    cpu_percent: number;
    memory_mb: number;
    peak_memory_mb: number;
  };
  output_files?: string[];
}
```

### Process Definition (runtime)
```typescript
interface ProcessDefinition {
  id: string;
  name: string;
  project: string;
  type: 'python_script' | 'bash' | 'powershell' | 'http_request';
  command: CommandConfig;
  parameters?: ParameterDefinition[];
  schedule?: ScheduleConfig;
  notifications?: NotificationConfig;
  dependencies?: Dependency[];
  monitoring?: MonitoringConfig;
  enabled: boolean;
}
```

---

## 🔐 Security & Best Practices

1. **Process Validation**: All configs validated against JSON Schema
2. **Parameter Sanitization**: No shell injection via parameter interpolation
3. **Access Control**: Role-based access (viewer, executor, admin)
4. **Audit Log**: All manual executions logged with user info
5. **Secret Management**: Sensitive env vars stored in .env, not in config
6. **Process Isolation**: Each execution runs in separate process group
7. **Resource Limits**: Memory and CPU limits per process

---

## 📈 Escalability & Performance

- **Async Execution**: All long-running operations are async
- **WebSocket**: Real-time updates without polling
- **Log Streaming**: Efficient streaming to multiple clients
- **Database Indexes**: On process_id, start_time for quick queries
- **Archival**: Old logs moved to archive storage after 30 days
- **Horizontal**: Multiple monitor instances can share DB with lock mechanism

---

## 🚀 Migration Path (Titania + ONNET)

### Phase 1: Extraction
1. Extract current `PROJECT_CONFIG` to `processes.json`
2. Extract `PROJECT_QUERIES` to parameter definitions
3. Extract `PROJECT_SCHEDULE_TASKS` to schedule config

### Phase 2: Backend Enhancement
1. Implement config file parser
2. Implement parameter interpolation
3. Add WebSocket support for logs
4. Migrate database schema

### Phase 3: Frontend Redesign
1. Build new React components with MUI
2. Implement real-time dashboard
3. Add process management UI
4. Migration to new UI (keep old as fallback)

### Phase 4: Automation
1. Implement scheduler integration
2. Add notification channels
3. Implement alerting engine
4. Beta testing with subset of processes

---

## ✅ Benefits

✓ **Parametrizable**: Add new processes without code changes  
✓ **Flexible**: Supports Python, Bash, PowerShell, HTTP calls  
✓ **Real-time**: WebSocket-based live monitoring  
✓ **Scalable**: Horizontal scaling support  
✓ **Observable**: Rich metrics, logs, and analytics  
✓ **User-friendly**: Modern React + MUI interface  
✓ **Maintainable**: Centralized config, clear separation of concerns  
✓ **Extensible**: Easy to add new notification channels, process types, etc.

