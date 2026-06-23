---
title: "🎨 Diagramas de Arquitectura - Process Monitor v2"
---

# 🎨 Diagramas Visuales - Process Monitor v2

## 1. Arquitectura de Componentes

```mermaid
graph TB
    User["👤 Usuario"]
    
    subgraph Frontend["🖥️ FRONTEND (React 19 + MUI 5)"]
        Dashboard["ProcessDashboard<br/>Página principal"]
        Grid["ProcessGrid<br/>Grilla responsive"]
        Card["ProcessCard<br/>Tarjeta individual"]
        Logs["LogViewer<br/>Visor logs"]
        Context["ProcessContext<br/>Global state"]
    end
    
    subgraph API["🌐 API LAYER (Flask + SocketIO)"]
        REST["REST Endpoints<br/>/api/processes<br/>/api/execute<br/>/api/status"]
        WS["WebSocket<br/>Real-time updates"]
    end
    
    subgraph Backend["⚙️ BACKEND"]
        Engine["ProcessEngine<br/>Orchestrator"]
        Runner["Process Runner<br/>Subprocess"]
        Monitor["Resource Monitor<br/>psutil"]
    end
    
    subgraph Config["📋 CONFIG"]
        Parser["JSON Parser<br/>Validator"]
        Interpolator["Parameter<br/>Interpolator"]
    end
    
    subgraph Storage["💾 STORAGE"]
        History["History DB<br/>SQLite/PostgreSQL"]
        Logs["Log Archive<br/>Files/Object Storage"]
    end
    
    User -->|Interacts| Dashboard
    Dashboard -->|uses| Context
    Dashboard -->|displays| Grid
    Grid -->|renders| Card
    Dashboard -->|displays| Logs
    
    Context -->|calls| REST
    Context -->|connects| WS
    
    REST -->|executes| Engine
    WS -->|updates| Frontend
    
    Engine -->|loads| Parser
    Parser -->|interpolates| Interpolator
    Engine -->|spawns| Runner
    Runner -->|monitors| Monitor
    
    Engine -->|persists| History
    Runner -->|streams| Logs
    
    style Frontend fill:#e3f2fd
    style API fill:#fff3e0
    style Backend fill:#f3e5f5
    style Config fill:#e8f5e9
    style Storage fill:#fce4ec
```

---

## 2. Flujo de Ejecución Manual

```mermaid
sequenceDiagram
    actor User
    participant UI as ProcessCard<br/>Dashboard
    participant API as Flask API
    participant Engine as ProcessEngine
    participant Runner as Process Runner
    participant Monitor as Resource Monitor
    participant WS as WebSocket
    
    User->>UI: Click "Ejecutar"
    UI->>UI: Mostrar dialog de parámetros
    User->>UI: Seleccionar parámetros
    UI->>API: POST /api/execute/:id { params }
    
    API->>Engine: execute_process(id, params)
    Engine->>Engine: Crear ExecutionContext
    Engine->>Runner: spawn thread _run_process()
    API-->>UI: return { execution_id }
    
    UI->>WS: connect ws://socket?exec_id
    WS->>Engine: on_join_execution
    
    Runner->>Runner: Build command
    Runner->>Runner: subprocess.Popen()
    
    loop Monitoreo (cada 2s)
        Runner->>Monitor: cpu_percent, memory_mb
        Monitor->>Engine: callback on_log_update
        Engine->>WS: emit log_update
        WS-->>UI: receive { logs }
    end
    
    Runner->>Runner: Capturar stdout/stderr
    Runner->>Runner: process.wait()
    
    Runner->>Engine: Actualizar status=success
    Engine->>WS: emit status_update
    WS-->>UI: receive { status, metrics }
    
    UI->>UI: Actualizar ProcessCard
    UI->>UI: Update stats cards
    UI->>UI: Update LogViewer
    
    Note over User: Proceso completado
```

---

## 3. Estructura de Datos

```mermaid
graph LR
    subgraph ProcessDefinition["ProcessDefinition"]
        id["id: string"]
        name["name: string"]
        project["project: string"]
        type["type: ProcessType"]
        command["command: CommandConfig"]
        parameters["parameters[]"]
        schedule["schedule: ScheduleConfig"]
        notifications["notifications"]
    end
    
    subgraph ExecutionContext["ExecutionContext"]
        exec_id["execution_id"]
        exec_status["status: ProcessStatus"]
        start["start_time"]
        end["end_time"]
        exec_parameters["parameters: Dict"]
        logs["logs: LogEntry[]"]
        resources["resources: ResourceMetrics"]
    end
    
    subgraph ResourceMetrics["ResourceMetrics"]
        cpu["cpu_percent"]
        mem["memory_mb"]
        peak["peak_memory_mb"]
    end
    
    subgraph LogEntry["LogEntry"]
        timestamp["timestamp: ISO8601"]
        level["level: 'debug'|'info'|'warning'|'error'"]
        message["message: string"]
        source["source: string"]
    end
    
    ProcessDefinition -.->|defines| ExecutionContext
    ExecutionContext -->|collects| ResourceMetrics
    ExecutionContext -->|streams| LogEntry
    
    style ProcessDefinition fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style ExecutionContext fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style ResourceMetrics fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style LogEntry fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
```

---

## 4. Flujo de Datos - Estado Global (React Context)

```mermaid
graph TB
    subgraph ProcessContext["ProcessContext (Global State)"]
        processes["processes: Map&lt;id, ProcessDefinition&gt;"]
        executions["executions: Map&lt;id, ExecutionRecord&gt;"]
        stats["stats: Map&lt;id, ProcessStats&gt;"]
        logs["currentLogs: LogEntry[]"]
    end
    
    subgraph Actions["Actions (useProcessContext)"]
        load["loadProcesses(definitions)"]
        exec["executeProcess(id, params)"]
        stop["stopExecution(id)"]
        addlog["addLogEntry(entry)"]
        updatestatus["updateExecutionStatus(id, status)"]
    end
    
    subgraph Consumers["Consumers (Components)"]
        dashboard["ProcessDashboard"]
        grid["ProcessGrid"]
        card["ProcessCard"]
        logs_viewer["LogViewer"]
    end
    
    ProcessContext -->|provides| Actions
    Actions -->|updates| ProcessContext
    
    dashboard -->|calls| Actions
    grid -->|calls| Actions
    card -->|calls| Actions
    logs_viewer -->|calls| Actions
    
    dashboard -->|reads| processes
    grid -->|reads| executions
    card -->|reads| executions
    logs_viewer -->|reads| logs
    
    style ProcessContext fill:#fff9c4,stroke:#f57f17,stroke-width:2px
    style Actions fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style Consumers fill:#bbdefb,stroke:#1565c0,stroke-width:2px
```

---

## 5. API REST Endpoints

```mermaid
graph LR
    Client["Client<br/>(Frontend)"]
    
    subgraph Processes["📦 Procesos"]
        GET_list["GET /api/processes<br/>→ ProcessDefinition[]"]
        GET_one["GET /api/processes/:id<br/>→ ProcessDefinition"]
    end
    
    subgraph Execution["🏃 Ejecución"]
        POST_exec["POST /api/execute/:id<br/>{ parameters }<br/>→ { execution_id }"]
        GET_status["GET /api/status/:exec_id<br/>→ ExecutionRecord"]
        GET_logs["GET /api/logs/:exec_id<br/>→ LogEntry[]"]
        GET_hist["GET /api/history/:id<br/>→ ExecutionRecord[]"]
    end
    
    subgraph Configuration["⚙️ Configuración"]
        GET_cfg["GET /api/config<br/>→ Config"]
        POST_reload["POST /api/config/reload<br/>→ { status }"]
    end
    
    subgraph Health["🏥 Health"]
        GET_health["GET /api/health<br/>→ { status, running_count }"]
    end
    
    Client -->|GET| GET_list
    Client -->|GET| GET_one
    Client -->|POST| POST_exec
    Client -->|GET| GET_status
    Client -->|GET| GET_logs
    Client -->|GET| GET_hist
    Client -->|GET| GET_cfg
    Client -->|POST| POST_reload
    Client -->|GET| GET_health
    
    style Processes fill:#e3f2fd,stroke:#1976d2
    style Execution fill:#fff3e0,stroke:#f57c00
    style Configuration fill:#f3e5f5,stroke:#7b1fa2
    style Health fill:#e8f5e9,stroke:#388e3c
```

---

## 6. WebSocket Events

```mermaid
graph LR
    Client["Client"]
    Server["Server"]
    
    subgraph ClientEvents["Client → Server"]
        JOIN["join_execution<br/>{ execution_id }"]
        LEAVE["leave_execution<br/>{ execution_id }"]
    end
    
    subgraph ServerEvents["Server → Client"]
        LOG_UPDATE["log_update<br/>{ execution_id, logs[] }"]
        STATUS_UPDATE["status_update<br/>{ execution_id, status, metrics }"]
    end
    
    Client -->|emit| JOIN
    Client -->|emit| LEAVE
    
    Server -->|emit| LOG_UPDATE
    Server -->|emit| STATUS_UPDATE
    
    LOG_UPDATE -->|received by| Client
    STATUS_UPDATE -->|received by| Client
    
    style ClientEvents fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style ServerEvents fill:#ffccbc,stroke:#d84315,stroke-width:2px
```

---

## 7. Ciclo de Vida de un Proceso

```mermaid
stateDiagram-v2
    [*] --> IDLE
    
    IDLE --> RUNNING: execute_process()
    
    RUNNING --> SUCCESS: process.returncode == 0
    RUNNING --> FAILED: process.returncode != 0
    RUNNING --> STOPPED: user click stop
    RUNNING --> TIMEOUT: duration > timeout
    
    SUCCESS --> IDLE: show_history
    FAILED --> IDLE: show_error
    STOPPED --> IDLE: show_stopped
    TIMEOUT --> IDLE: show_timeout
    
    IDLE --> [*]
    
    note right of RUNNING
        Duración: variable
        Recursos: CPU, Memory
        Logs: streamear cada 2s
    end note
```

---

## 8. Responsabilidades por Capas

```mermaid
graph TB
    subgraph Layer1["🎨 PRESENTATION LAYER"]
        P1["ProcessDashboard: Orquestar UI"]
        P2["ProcessGrid: Renderizar grilla"]
        P3["ProcessCard: Tarjeta individual"]
        P4["LogViewer: Visor logs"]
        P5["ProcessContext: State mgmt"]
    end
    
    subgraph Layer2["🌐 API LAYER"]
        A1["REST Endpoints: CRUD operations"]
        A2["WebSocket: Real-time updates"]
        A3["Error handling: Validación"]
        A4["CORS: Security"]
    end
    
    subgraph Layer3["⚙️ BUSINESS LOGIC LAYER"]
        B1["ProcessEngine: Orquestador"]
        B2["ConfigParser: Validación"]
        B3["ProcessRunner: Ejecución"]
        B4["ResourceMonitor: Monitoreo"]
    end
    
    subgraph Layer4["💾 DATA ACCESS LAYER"]
        D1["ExecutionContext: En memoria"]
        D2["History DB: Persistencia (próximo)"]
        D3["Log Archive: Almacenamiento (próximo)"]
    end
    
    Layer1 -->|REST, WS| Layer2
    Layer2 -->|calls| Layer3
    Layer3 -->|reads/writes| Layer4
    
    style Layer1 fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style Layer2 fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style Layer3 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style Layer4 fill:#fce4ec,stroke:#c2185b,stroke-width:2px
```

---

## 9. Matriz de Responsabilidades

```mermaid
graph LR
    subgraph Frontend["FRONTEND"]
        F1["ProcessCard<br/>─ Render status<br/>─ Handle clicks<br/>─ Show metrics"]
        F2["ProcessContext<br/>─ State mgmt<br/>─ Cache data<br/>─ Sync with API"]
        F3["LogViewer<br/>─ Display logs<br/>─ Scroll/search<br/>─ Format output"]
    end
    
    subgraph Backend["BACKEND"]
        B1["ProcessEngine<br/>─ Validate config<br/>─ Schedule exec<br/>─ Manage contexts"]
        B2["ProcessRunner<br/>─ Execute subprocess<br/>─ Capture output<br/>─ Handle errors"]
        B3["ResourceMonitor<br/>─ Track CPU/Mem<br/>─ Get peak usage<br/>─ Stream metrics"]
    end
    
    subgraph Config["CONFIG"]
        C1["processes.json<br/>─ Define processes<br/>─ Set parameters<br/>─ Enable/disable"]
    end
    
    F1 -->|reads| B1
    F2 -->|calls| B1
    F3 -->|displays| B2
    B1 -->|spawns| B2
    B2 -->|monitors| B3
    B1 -->|loads| C1
    
    style Frontend fill:#e3f2fd
    style Backend fill:#fff3e0
    style Config fill:#e8f5e9
```

---

## 10. Performance & Escalabilidad

```mermaid
graph TB
    subgraph Optimization["⚡ Optimizaciones"]
        O1["Async execution: No bloquea"]
        O2["Log streaming: Chunks pequeños"]
        O3["Context caching: Último 500 logs"]
        O4["WebSocket: Solo deltas"]
        O5["React.memo: Prevenir re-renders"]
    end
    
    subgraph Bottlenecks["🚨 Posibles Bottlenecks"]
        B1["Resource heavy process<br/>→ Limitar CPU/Memory"]
        B2["Many concurrent executions<br/>→ Queue + pool"]
        B3["Large log files<br/>→ Streaming + archive"]
        B4["High cardinality metrics<br/>→ Agregación temporal"]
    end
    
    subgraph Scaling["📈 Escalabilidad"]
        S1["Database: PostgreSQL para persistencia"]
        S2["Message queue: Redis para job dispatch"]
        S3["Horizontal: Multiple backend instances"]
        S4["Caching: Memcached para queries"]
    end
    
    style Optimization fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style Bottlenecks fill:#ffccbc,stroke:#d84315,stroke-width:2px
    style Scaling fill:#bbdefb,stroke:#1565c0,stroke-width:2px
```

---

## 11. Flujo de Configuración

```mermaid
graph LR
    Admin["👨‍💼 Admin"]
    JSON["processes.json"]
    Parser["ConfigParser"]
    Schema["JSON Schema"]
    Validator["Validator"]
    Engine["ProcessEngine"]
    
    Admin -->|edita| JSON
    JSON -->|carga| Parser
    Parser -->|valida contra| Schema
    Validator -->|✓ OK| Engine
    Validator -->|✗ Error| Parser
    
    Engine -->|procesa| Validator
    
    style Admin fill:#e3f2fd
    style JSON fill:#fff3e0
    style Parser fill:#f3e5f5
    style Schema fill:#e8f5e9
    style Validator fill:#fce4ec
    style Engine fill:#c8e6c9
```

---

## 12. Matriz de Tecnologías

```
┌─────────────────────────────────────────────────────────────┐
│                   TECHNOLOGY STACK                           │
├─────────────────────────────────────────────────────────────┤
│ FRONTEND                                                     │
│ ├─ React 19.2.4 (componentes, hooks)                         │
│ ├─ MUI 5.0.6 (componentes, theming)                          │
│ ├─ TypeScript (type safety)                                  │
│ ├─ Context API (state management)                            │
│ ├─ Vite (build tool)                                         │
│ └─ WebSocket (real-time)                                     │
│                                                               │
│ BACKEND                                                      │
│ ├─ Python 3.9+ (runtime)                                     │
│ ├─ Flask (web framework)                                     │
│ ├─ Flask-SocketIO (WebSocket)                                │
│ ├─ psutil (resource monitoring)                              │
│ ├─ subprocess (process execution)                            │
│ └─ threading (async execution)                               │
│                                                               │
│ INFRASTRUCTURE (próximo)                                     │
│ ├─ PostgreSQL (persistence)                                  │
│ ├─ APScheduler (job scheduling)                              │
│ ├─ Redis (message queue)                                     │
│ └─ Docker (containerization)                                 │
│                                                               │
│ TESTING (próximo)                                            │
│ ├─ pytest (unit tests)                                       │
│ ├─ Jest (component tests)                                    │
│ └─ Cypress (e2e tests)                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 13. Propuesta de Migración - Timeline

```mermaid
gantt
    title Migración Titania Monitor → Process Monitor v2
    dateFormat YYYY-MM-DD
    
    section Fase 1
    Preparación :p1, 2024-05-01, 7d
    Extracción Config :p1a, after p1, 3d
    
    section Fase 2
    Migración Datos :p2, after p1a, 2d
    Dev Deployment :p2a, after p2, 3d
    
    section Fase 3
    Testing :p3, after p2a, 7d
    Bug Fixes :p3a, after p3, 3d
    
    section Fase 4
    Staging Setup :p4, after p3a, 3d
    Staging Testing :p4a, after p4, 7d
    
    section Fase 5
    Cutover Plan :p5, after p4a, 1d
    Go Live :p5a, after p5, 1d
    
    section Fase 6
    Post-Live Monitor :p6, after p5a, 7d
    Documentation :p6a, after p6, 3d
```

