---
title: "📚 ÍNDICE - Process Monitor v2"
date: "2024-04-24"
---

# 📚 Índice Completo - Process Monitor v2

## 🎯 Documentación de Diseño

### 1. **[ARQUITECTURA_MONITOR_v2.md](../ARCHITECTURE_MONITOR_v2.md)**
   - ✅ **Estado**: Completo
   - 📄 **Contenido**:
     - Arquitectura general del sistema
     - Estructura de configuración JSON
     - Flujos de ejecución (manual + scheduled)
     - Componentes React con jerarquía
     - Endpoints API REST
     - Data models (TypeScript)
     - Seguridad y mejores prácticas
     - Escalabilidad y performance
     - Migración desde Titania/ONNET
   - 🎯 **Audiencia**: Arquitectos, leads técnicos
   - ⏱️ **Lectura**: 20-30 minutos

### 2. **[README.md](./README.md)**
   - ✅ **Estado**: Completo
   - 📄 **Contenido**:
     - Descripción y características
     - Estructura de carpetas
     - Guía de inicio rápido
     - Instalación frontend/backend
     - Configuración de procesos
     - Referencia de API
     - WebSocket events
     - Ejemplos de configuración
     - Security guidelines
     - Próximas fases
   - 🎯 **Audiencia**: Desarrolladores, DevOps
   - ⏱️ **Lectura**: 15-20 minutos

### 3. **[MOCKUP.md](./MOCKUP.md)**
   - ✅ **Estado**: Completo
   - 📄 **Contenido**:
     - Mockups ASCII de interfaz
     - Dashboard principal
     - Dialogs y modals
     - LogViewer
     - Historial (DataGrid)
     - Analytics
     - Configuración
     - Responsive design specs
     - Paleta de colores
     - Animaciones y UX
   - 🎯 **Audiencia**: Diseñadores, frontend devs
   - ⏱️ **Lectura**: 15 minutos

### 4. **[MIGRACION.md](./MIGRACION.md)**
   - ✅ **Estado**: Completo
   - 📄 **Contenido**:
     - Plan de migración 7 fases
     - Extracción de configuración
     - Migración de datos históricos
     - Testing strategy
     - Staging paralelo
     - Cutover plan
     - Rollback strategy
     - Timeline estimado
     - Team roles
     - Checklists
   - 🎯 **Audiencia**: Project managers, DevOps, QA
   - ⏱️ **Lectura**: 20 minutos

### 5. **[RESUMEN_EJECUTIVO.md](./RESUMEN_EJECUTIVO.md)**
   - ✅ **Estado**: Completo
   - 📄 **Contenido**:
     - Visión general
     - Problemas actuales vs. soluciones
     - Comparativa (antes/después)
     - Arquitectura de alto nivel
     - Archivos entregables
     - Plan de implementación
     - Configuración ejemplo
     - Comparativa UI
     - Beneficios esperados
     - Riesgos y mitigación
     - Métricas de éxito
   - 🎯 **Audiencia**: Stakeholders, C-level, PMs
   - ⏱️ **Lectura**: 10-15 minutos

---

## 💻 Código Entregable

### Frontend (React 19.2.4 + MUI 5.0.6)

#### **types.ts**
- TypeScript interfaces para todo el sistema
- Enums para estados, tipos, canales
- Completo type safety

#### **App.tsx**
- Componente raíz de React
- Theme MUI setup
- ProcessProvider wrapper
- Mock data para desarrollo

#### **context/ProcessContext.tsx**
- Context API global
- Hooks: useProcessContext
- State management (processes, executions, logs)
- Actions: executeProcess, stopExecution, addLogEntry, etc.

#### **components/**

1. **ProcessDashboard.tsx**
   - Página principal
   - Estadísticas en vivo
   - Tabs: Procesos, Historial, Logs, Analytics
   - Settings drawer
   - ~300 líneas

2. **ProcessGrid.tsx**
   - Grilla responsiva de procesos
   - Búsqueda y filtros
   - Paginación
   - ~200 líneas

3. **ProcessCard.tsx**
   - Tarjeta individual
   - Estado con badge
   - Métricas
   - Botones de acción
   - ~150 líneas

4. **LogViewer.tsx**
   - Visor de logs
   - Búsqueda en vivo
   - Filtro por nivel
   - Auto-scroll
   - Descargar logs
   - ~200 líneas

#### **package.json**
- Dependencias: React 19.2.4, MUI 5.0.6, Vite, TypeScript
- Scripts: dev, build, lint, type-check

---

### Backend (Python + Flask)

#### **backend/process_engine.py**
- ProcessEngine: orquestador principal
- ExecutionContext: contexto de ejecución
- _build_command: interpolación de parámetros
- _run_process: ejecutor de procesos
- _monitor_process: monitoreo de recursos (psutil)
- get_execution, get_statistics
- ~400 líneas

#### **backend/api.py**
- Flask app con CORS y SocketIO
- REST endpoints:
  - GET /api/processes
  - GET /api/processes/:id
  - POST /api/execute/:process-id
  - GET /api/status/:execution-id
  - GET /api/logs/:execution-id
  - GET /api/history/:process-id
  - GET /api/config
  - POST /api/config/reload
- WebSocket events:
  - join_execution
  - leave_execution
  - log_update (callback)
  - status_update (callback)
- ~250 líneas

#### **backend/requirements.txt**
- Flask, Flask-CORS, Flask-SocketIO
- SQLAlchemy, psycopg2 (para BD)
- APScheduler (para scheduler)
- psutil (monitoreo)
- pydantic (validación)
- pytest (testing)

---

### Configuration

#### **config/processes.json** (Template)
- Estructura JSON con todos los procesos
- Ejemplos: Titania, ONNET M3, ONNET M4, DB Health Check
- Cada proceso con:
  - id, name, description, project
  - command (script, workdir, timeout, env_vars)
  - parameters (nombre, tipo, valores, requerido)
  - schedule (cron, enabled, timezone)
  - notifications (on_success, on_failure)
  - monitoring (track_duration, track_resources, alert_threshold)

---

## 📊 Diagrama de Arquitectura

```
┌────────────────────────────────────────────────────────────┐
│                   FRONTEND LAYER                           │
├────────────────────────────────────────────────────────────┤
│  React 19.2.4 + MUI 5.0.6 + TypeScript                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ ProcessDashboard                                    │  │
│  │ ├─ Stats (running, success, failed, success_rate)  │  │
│  │ ├─ Tabs: [Procesos] [Historial] [Logs] [Analytics] │  │
│  │ └─ Settings Drawer                                  │  │
│  └─────────────────────────────────────────────────────┘  │
│       ↓ Grid, Cards, Logs         │                       │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ ProcessContext (React Hooks + Context API)         │  │
│  │ - processes: Map<id, definition>                   │  │
│  │ - executions: Map<id, execution>                   │  │
│  │ - currentLogs: LogEntry[]                          │  │
│  │ - actions: executeProcess, stopExecution, etc.    │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
└────────────────────────────────────────────────────────────┘
              ↓ REST API + WebSocket ↑

┌────────────────────────────────────────────────────────────┐
│                    API LAYER (Flask)                       │
├────────────────────────────────────────────────────────────┤
│  ├─ REST: /api/processes, /api/execute, /api/status       │
│  ├─ WebSocket: logs en vivo, status updates               │
│  └─ Error handling + CORS                                  │
└────────────────────────────────────────────────────────────┘
              ↓ Instantiate + Execute ↑

┌────────────────────────────────────────────────────────────┐
│               EXECUTION LAYER (ProcessEngine)              │
├────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐ │
│  │ ExecutionContext                                     │ │
│  │ - execution_id, process_id, status                  │ │
│  │ - parameters, logs, resources                       │ │
│  │ - start_time, end_time, exit_code                  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Process Runner (subprocess)                          │ │
│  │ - Build command con interpolación de parámetros    │ │
│  │ - Ejecutar en thread (no-blocking)                  │ │
│  │ - Capturar stdout/stderr                            │ │
│  │ - Monitor resources (CPU, memory)                   │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Callbacks                                            │ │
│  │ - on_log_update → WebSocket emit                     │ │
│  │ - on_status_update → WebSocket emit                  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                             │
└────────────────────────────────────────────────────────────┘
              ↓ Load/Validate ↑

┌────────────────────────────────────────────────────────────┐
│             CONFIG ENGINE (JSON Validator)                 │
├────────────────────────────────────────────────────────────┤
│  - Cargar processes.json                                   │
│  - Validar estructura vs. schema                           │
│  - Interpolar variables (${PROJECT_ROOT}, ${VAR})         │
│  - Resolver dependencies                                   │
└────────────────────────────────────────────────────────────┘
              ↓ Persist ↑

┌────────────────────────────────────────────────────────────┐
│                  STORAGE LAYER (próximo)                   │
├────────────────────────────────────────────────────────────┤
│  - Execution history (PostgreSQL)                          │
│  - Log archive                                             │
│  - Metrics & analytics                                     │
│  - Configuration versioning                                │
└────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos - Ejecución Manual

```
1. User clicks "Ejecutar" en ProcessCard
                 ↓
2. Abre diálogo con parámetros requeridos
                 ↓
3. User selecciona/ingresa valores y click "Ejecutar"
                 ↓
4. POST /api/execute/:process-id { parameters }
                 ↓
5. Backend valida parámetros vs. schema
                 ↓
6. ProcessEngine.execute_process():
   - Crear ExecutionContext
   - Agregar a contexts map
   - Iniciar thread _run_process()
                 ↓
7. Retornar execution_id al frontend
                 ↓
8. Frontend se conecta WebSocket: ws://...?execution_id=...
                 ↓
9. Backend _run_process():
   - Construir comando con parámetros
   - Ejecutar subprocess
   - Monitorear recursos (psutil)
   - Capturar logs
   - Emit WebSocket updates
                 ↓
10. Frontend recibe actualizaciones en tiempo real:
    - log_update: nuevos logs
    - status_update: cambio de estado
                 ↓
11. Completar/Error:
    - Actualizar estado en ExecutionContext
    - Guardar duración y recursos
    - Emit notificaciones (si configurado)
                 ↓
12. Frontend actualiza Dashboard:
    - ProcessCard status badge
    - Stats cards
    - LogViewer logs
    - Charts si aplica
```

---

## 📦 Archivos Entregables - Resumen

```
c:\Users\javier.castaneda\botsquad\
├── ARCHITECTURE_MONITOR_v2.md         ← Diseño completo
├── ProcessMonitor/
│   ├── README.md                       ← Guía de inicio
│   ├── MOCKUP.md                       ← Mockups UI
│   ├── MIGRACION.md                    ← Plan de migración
│   ├── RESUMEN_EJECUTIVO.md            ← Overview
│   │
│   ├── App.tsx                         ← App raíz
│   ├── types.ts                        ← TypeScript definitions
│   ├── package.json                    ← Dependencias npm
│   │
│   ├── context/
│   │   └── ProcessContext.tsx          ← Context + Hooks
│   │
│   ├── components/
│   │   ├── ProcessDashboard.tsx        ← Dashboard principal
│   │   ├── ProcessGrid.tsx             ← Grilla responsive
│   │   ├── ProcessCard.tsx             ← Tarjeta proceso
│   │   └── LogViewer.tsx               ← Visor logs
│   │
│   ├── backend/
│   │   ├── process_engine.py           ← Engine ejecución
│   │   ├── api.py                      ← API Flask
│   │   └── requirements.txt            ← Dependencias pip
│   │
│   └── config/
│       └── processes.json              ← Configuración
│
└── ... (datos y otros)
```

---

## 🚀 Pasos para Empezar

### 1. **Leer Documentación** (1 hora)
   - [ ] RESUMEN_EJECUTIVO.md (overview)
   - [ ] ARCHITECTURE_MONITOR_v2.md (diseño)
   - [ ] README.md (guía técnica)

### 2. **Explorar Código** (2 horas)
   - [ ] types.ts (entiende data structures)
   - [ ] ProcessContext.tsx (entiende state mgmt)
   - [ ] ProcessDashboard.tsx (entiende componentes)
   - [ ] process_engine.py (entiende backend)

### 3. **Revisar Mockups** (30 min)
   - [ ] MOCKUP.md (visualiza interfaz)

### 4. **Planificar Migración** (2 horas)
   - [ ] MIGRACION.md (plan de implementación)
   - [ ] Identificar procesos a migrar
   - [ ] Crear processes.json

### 5. **Setup Dev Environment** (1 hora)
   - [ ] npm install
   - [ ] pip install -r requirements.txt
   - [ ] npm run dev + python api.py

### 6. **Testing** (2-3 horas)
   - [ ] Ejecutar procesos de ejemplo
   - [ ] Validar logs en tiempo real
   - [ ] Verificar WebSocket

**TOTAL**: 8-10 horas para entender sistema completo

---

## 🎯 Próximos Pasos Inmediatos

1. **Fase 1**: Prototiping & Validation
   - Revisar código con team
   - Identificar ajustes necesarios
   - Create GitHub repo

2. **Fase 2**: Backend Enhancement
   - Agregar scheduler (APScheduler)
   - Agregar alerting engine
   - Conectar a PostgreSQL

3. **Fase 3**: Frontend Polish
   - DataGrid MUI X para historial
   - Charts MUI X para analytics
   - Dark mode support

4. **Fase 4**: Migración
   - Extraer procesos actuales
   - Setup staging
   - Testing exhaustivo

---

## 📞 Referencias & Links

- **React 19**: https://react.dev/
- **MUI v5**: https://mui.com/material-ui/getting-started/
- **Flask**: https://flask.palletsprojects.com/
- **WebSocket**: https://socket.io/

---

## 📝 Notas Importantes

⚠️ **Este es un prototipo** funcional que sirve como base. Requiere:
- Testing exhaustivo en staging
- Enhancements basados en feedback del team
- Documentation actualizada después de cada fase

✅ **Está listo para**: 
- Code review
- Architecture validation
- Development setup

🚀 **Next**: Implementar Fase 1 (backend enhancement) → Fase 2 (migración)

