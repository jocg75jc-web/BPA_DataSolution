---
title: "✅ QUICK START - Process Monitor v2"
date: "2024-04-24"
---

# ✅ Quick Start - Process Monitor v2

## 📌 Resumen de 2 Minutos

**Objetivo**: Reemplazar `monitor_app.py` con un sistema modular, parametrizable y en tiempo real.

**Solución**: 
- Frontend React 19 + MUI v5 (componentes modernos)
- Backend Python Flask (engine de ejecución)
- Configuración JSON (sin código)
- WebSocket para logs en vivo
- Extensible para nuevos procesos

**Estado**: ✅ Prototipo funcional completo

---

## 🎯 Punto de Partida - Qué Revisar Primero

### 1. **Para PM/Stakeholders** (5 min)
   📄 Leer: [RESUMEN_EJECUTIVO.md](./RESUMEN_EJECUTIVO.md)
   - Problemas que resuelve
   - Beneficios esperados
   - Timeline

### 2. **Para Arquitectos/Leads Técnicos** (20 min)
   📄 Leer: [ARCHITECTURE_MONITOR_v2.md](../ARCHITECTURE_MONITOR_v2.md)
   - Diseño completo
   - Componentes y flujos
   - Escalabilidad

### 3. **Para Frontend Developers** (15 min)
   📄 Leer: [README.md](./README.md) + [MOCKUP.md](./MOCKUP.md)
   - Estructura componentes
   - Guía de inicio
   - Mockups UI
   - Ver: `App.tsx`, `ProcessDashboard.tsx`, `ProcessContext.tsx`

### 4. **Para Backend Developers** (15 min)
   📄 Leer: [README.md](./README.md)
   - API endpoints
   - Process Engine
   - Ver: `process_engine.py`, `api.py`

### 5. **Para DevOps/QA** (15 min)
   📄 Leer: [MIGRACION.md](./MIGRACION.md)
   - Plan de migración
   - Testing strategy
   - Deployment steps

---

## 🚀 Pasos Iniciales (Hoy)

### Paso 1: Setup Dev Environment (30 min)

**Frontend**:
```bash
cd ProcessMonitor
npm install
npm run dev
# Acceder: http://localhost:5173
```

**Backend**:
```bash
cd ProcessMonitor/backend
pip install -r requirements.txt
python api.py
# API: http://localhost:5000
```

**Verificación**:
- [ ] Dashboard visible en navegador
- [ ] API responde en /api/processes
- [ ] Logs en tiempo real (WebSocket)
- [ ] Procesos de ejemplo funcionan

### Paso 2: Revisar Código Clave (1 hora)

**Frontend**:
- `types.ts` - Entender estructuras
- `ProcessContext.tsx` - Entender state management
- `ProcessDashboard.tsx` - Entender UI main
- `components/` - Componentes reutilizables

**Backend**:
- `process_engine.py` - Entender execution engine
- `api.py` - Entender REST + WebSocket
- `config/processes.json` - Entender configuración

### Paso 3: Crear Primer Proceso Personalizado (1 hora)

Editar `config/processes.json`:
```json
{
  "id": "mi-primer-proceso",
  "name": "Mi Primer Proceso",
  "project": "Mi Proyecto",
  "type": "python_script",
  "command": {
    "script": "mi_script.py",
    "workdir": "/path/to/workdir",
    "timeout_seconds": 600
  }
}
```

Verificar:
- [ ] Aparece en dashboard
- [ ] Puede ejecutarse
- [ ] Logs fluyen en tiempo real

---

## 📚 Estructura de Archivos - Dónde Encontrar Qué

```
ProcessMonitor/
├── 📄 README.md                 ← Guía técnica
├── 📄 MOCKUP.md                 ← Mockups UI
├── 📄 MIGRACION.md              ← Plan de migración
├── 📄 RESUMEN_EJECUTIVO.md      ← Overview ejecutivo
├── 📄 DIAGRAMAS.md              ← Arquitectura visual
├── 📄 INDEX.md                  ← Índice completo
├── 🎨 ARQUITECTURA_v2.md        ← Diseño completo
│
├── ⚛️ Frontend
│   ├── App.tsx                  ← App raíz + theme
│   ├── types.ts                 ← TypeScript defs
│   ├── package.json             ← npm dependencies
│   ├── context/
│   │   └── ProcessContext.tsx   ← State global
│   └── components/
│       ├── ProcessDashboard.tsx ← Página principal
│       ├── ProcessGrid.tsx      ← Grilla
│       ├── ProcessCard.tsx      ← Tarjeta
│       └── LogViewer.tsx        ← Visor logs
│
├── 🐍 Backend
│   ├── process_engine.py        ← Engine ejecución
│   ├── api.py                   ← API Flask
│   └── requirements.txt         ← pip dependencies
│
└── ⚙️ Config
    └── processes.json           ← Configuración
```

---

## 🔥 10 Tareas Inmediatas (Prioridad)

### CRÍTICAS (hoy)
1. ✅ Setup dev environment (frontend + backend)
2. ✅ Revisar documentación arquitectónica
3. ✅ Verificar que procesos de ejemplo funcionan
4. ✅ Crear primer proceso personalizado

### IMPORTANTES (esta semana)
5. Extraer procesos de Titania a processes.json
6. Extraer procesos de ONNET a processes.json
7. Testing de procesos actuales en v2
8. Validar outputs vs. versión anterior

### MEDIA PRIORIDAD (próximas 2 semanas)
9. Agregar scheduler (APScheduler)
10. Agregar alerting + notificaciones

---

## 🎨 Mockup Visual - Lo Que Verás

```
┌───────────────────────────────────────────────────────────┐
│ Process Monitor v2                    🔄 🔔 ⚙️            │
├───────────────────────────────────────────────────────────┤
│                                                             │
│ ESTADÍSTICAS                                               │
│ ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐               │
│ │ 2     │  │ 47    │  │ 3     │  │ 94%   │               │
│ │Ejecut │  │Exitos │  │Errores│  │Tasa   │               │
│ └───────┘  └───────┘  └───────┘  └───────┘               │
│                                                             │
│ [Procesos] [Historial] [Logs] [Analytics]                │
│                                                             │
│ Buscar... [Proyecto▼] [Estado▼] [+Nuevo]                │
│                                                             │
│ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ │
│ │ Titania Export │ │ ONNET M3       │ │ ONNET M4       │ │
│ │ ✓ Completado   │ │ ⟳ Ejecutando   │ │ ✗ Error        │ │
│ │ CPU:32% Mem:   │ │ CPU:65% Mem:   │ │ hace 5 min     │ │
│ │ 256MB          │ │ 512MB          │ │                │ │
│ │ [▶] [+]        │ │ [⏹] [+]        │ │ [Reintentar]   │ │
│ └────────────────┘ └────────────────┘ └────────────────┘ │
│                                                             │
└───────────────────────────────────────────────────────────┘
```

---

## 💡 Conceptos Clave

### 1. **Configuración JSON** (sin código)
Todos los procesos se definen en `processes.json`:
```json
{
  "id": "proceso-id",
  "name": "Nombre legible",
  "command": { "script": "script.py", "timeout_seconds": 1800 },
  "schedule": { "expression": "0 */2 * * *" },
  "notifications": { "on_failure": { "channels": ["email"] } }
}
```

### 2. **Ejecución Asincrónica**
Procesos se ejecutan en threads, nunca bloquean el frontend.
Dashboard actualiza en tiempo real vía WebSocket.

### 3. **Monitoreo de Recursos**
Cada proceso captura: CPU%, Memory MB, peak memory, duración.

### 4. **Logs en Vivo**
Visor de logs con búsqueda, filtro por nivel, descarga automática.

### 5. **Estado Global (React Context)**
No Redux/Zustand. Simple Context API con hooks.
Escalable para futuro si se necesita.

---

## 🔧 Configuración 101

### Crear nuevo proceso

1. Abrir `config/processes.json`
2. Agregar entrada en array `processes`:
   ```json
   {
     "id": "mi-proceso",
     "name": "Mi Proceso",
     "project": "Mi Proyecto",
     "type": "python_script",
     "command": {
       "script": "script.py",
       "workdir": "/path/to/workdir",
       "timeout_seconds": 600
     }
   }
   ```
3. Guardar archivo
4. POST /api/config/reload (o reiniciar backend)
5. Proceso aparece en dashboard

---

## 📊 API Rápida (Cheat Sheet)

```bash
# Listar procesos
curl http://localhost:5000/api/processes

# Ejecutar proceso
curl -X POST http://localhost:5000/api/execute/titania-export-sftp \
  -H "Content-Type: application/json" \
  -d '{"queries": "all"}'

# Obtener estado
curl http://localhost:5000/api/status/exec-123456789

# Obtener logs
curl http://localhost:5000/api/logs/exec-123456789

# Health check
curl http://localhost:5000/api/health
```

---

## 🐛 Debugging

### Frontend no carga
```bash
cd ProcessMonitor
npm run dev
# Verificar: http://localhost:5173
# Si error: npm install nuevamente
```

### Backend no responde
```bash
cd ProcessMonitor/backend
pip install -r requirements.txt
python api.py
# Verificar: http://localhost:5000/api/health
```

### Logs no se actualizan
```bash
# Verificar WebSocket en DevTools (Network → WS)
# Verificar que execution_id es correcto
# Verificar logs en backend console
```

### Proceso no aparece en dashboard
```bash
# Recargar página (Ctrl+R)
# Verificar processes.json es válido JSON
# POST /api/config/reload
# Reiniciar backend
```

---

## ⚡ Performance Tips

- Dashboard: Responde en <100ms
- Logs: Streaming en tiempo real (2s de latencia)
- Procesos: 10+ simultáneos (en máquina normal)
- Memory: Caché últimos 500 logs, no más

---

## 🛠️ Tech Stack Quick Ref

| Aspecto | Tecnología | Versión |
|--------|-----------|---------|
| **Frontend** | React | 19.2.4 |
| **UI Library** | MUI | 5.0.6 |
| **Language** | TypeScript | 5.3+ |
| **Build** | Vite | 5.0+ |
| **Backend** | Python | 3.9+ |
| **Framework** | Flask | 2.3+ |
| **Real-time** | SocketIO | 5.9+ |
| **Monitoring** | psutil | 5.9+ |

---

## 📞 Soporte Rápido

### "No funciona X"
1. Revisar console (frontend F12 / backend terminal)
2. Verificar archivo de config JSON
3. Reiniciar backend
4. Limpiar cache browser

### "Quiero agregar Y"
1. Si es nuevo proceso: editar processes.json
2. Si es nueva funcionalidad: ver architecture doc
3. Contactar lead técnico para approval

### "Necesito Z"
Crear issue / contactar PM

---

## ✅ Checklist Pre-Production

Antes de ir a producción, verificar:

- [ ] Todos los procesos de Titania migrados
- [ ] Todos los procesos de ONNET migrados
- [ ] Outputs validados vs. versión anterior
- [ ] Testing en staging completado
- [ ] Performance dentro de SLA
- [ ] Logs persisten correctamente
- [ ] Alertas configuradas
- [ ] Backup de monitor_app.py
- [ ] Rollback plan documentado
- [ ] Team capacitado

---

## 🎓 Material de Aprendizaje

**React Hooks**:
- https://react.dev/reference/react/hooks

**MUI v5**:
- https://mui.com/material-ui/getting-started/

**Flask**:
- https://flask.palletsprojects.com/

**Socket.IO**:
- https://socket.io/

---

## 🚀 Próxima Sesión

Después de revisar esto, próxima sesión debe cubrir:
1. ✅ Setup dev environment
2. ✅ Revisar código
3. ✅ Crear primer proceso
4. ✅ Testing manual
5. ✅ Plan de integración con monitor_app.py

---

## 📝 Resumen

| Qué | Dónde | Tiempo |
|-----|-------|--------|
| **Entender concepto** | RESUMEN_EJECUTIVO.md | 15 min |
| **Revisar arquitectura** | ARCHITECTURE_MONITOR_v2.md | 30 min |
| **Setup dev** | README.md | 30 min |
| **Ver mockups** | MOCKUP.md | 15 min |
| **Entender código** | Código fuente | 60 min |
| **Crear 1er proceso** | processes.json | 60 min |
| **Total** | | 3.5 horas |

---

## 🎉 ¡Listo!

Ya tienes todo para empezar. 

**Próximo paso**: Abre `ProcessMonitor/README.md` y sigue "Quick Start".

**Preguntas?** Ver INDEX.md para documentación completa.

¡Vamos a modernizar el monitoreo! 🚀

