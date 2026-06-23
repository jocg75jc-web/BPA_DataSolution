# ONNET Process Monitoring Analysis 🔍

## Executive Summary
El dashboard de monitoreo (`Titania/monitor_app.py`) está configurado para soportar ambos proyectos (Titania + ONNET), pero la información de ONNET no se refleja en el dashboard. Este análisis identifica las causas raíz y proporciona soluciones.

---

## Configuración Actual ✅

### Frontend (Titania/static/monitor.js + index.html)
- **HTML selector**: Tiene ambas opciones (Titania, ONNET) → ✅ **OK**
- **Event listener**: Cambia `clientState.selectedProject` cuando se selecciona proyecto → ✅ **OK**
- **API calls**: Envía `?project=ONNET` cuando se selecciona ONNET → ✅ **OK**
- **Refresh logic**: Sincroniza logs de TODOS los proyectos cada 3 segundos:
  ```javascript
  const allProjects = ['Titania', 'ONNET'];
  await Promise.allSettled(allProjects.map(p => syncLogsFromFile(p)));
  ```
  → ✅ **OK**

### Backend (Titania/monitor_app.py)
- **PROJECT_CONFIG**: Define rutas para Titania y ONNET:
  ```python
  "ONNET": {
      "script": ONNET_DIR / "export_onnet_csv.py",
      "output_dir": ONNET_DIR / "output",
      "log_file": ONNET_DIR / "output" / "scheduled_task.log",
  }
  ```
  → ✅ **OK**

- **PROJECT_QUERIES**: Define queries de ONNET:
  ```python
  "ONNET": {
      "all": {...},
      "modelo3": {...},
      "modelo4": {...},
  }
  ```
  → ✅ **OK**

- **API endpoints** (/api/status, /api/logs, /api/queries, /api/run): Todos reciben `?project` parameter → ✅ **OK**

- **Process execution**: Construye comando para ONNET:
  ```python
  cmd = [python_exe, str(script_path)]
  if query_name and query_name != "all":
      cmd.extend(["--query", query_name])
  ```
  → ✅ **OK**

---

## Potential Issues 🚨

### Issue #1: Directory Structure
**Symptom**: Logs no se guardan o se pierden
**Check Points**:
- [ ] `ONNET/output/` directory exists?
- [ ] `ONNET/output/scheduled_task.log` exists or can be created?
- [ ] Directory has write permissions?

```bash
# Windows check
ls C:\Users\javier.castaneda\botsquad\ONNET\output\
Get-Item C:\Users\javier.castaneda\botsquad\ONNET\output\ -Force
```

### Issue #2: Process State Initialization
**Current State**: PROCESS_STATES initialized at startup:
```python
PROCESS_STATES = {
    project_name: build_process_state()
    for project_name in PROJECT_CONFIG
}
```

**Potential Problem**: If `export_onnet_csv.py` fails on first run, the error is logged but subsequent runs might not clear the error state properly.

**Check**: 
- [ ] Can you manually run `python export_onnet_csv.py` in ONNET directory?
- [ ] Does it produce output files?
- [ ] Does it return exit code 0?

### Issue #3: Log Synchronization (/api/sync-logs)
**Current Flow**:
1. Frontend calls `/api/sync-logs?project=ONNET` every 3 seconds
2. Backend reads `ONNET/output/scheduled_task.log`
3. Parses logs and merges into `PROCESS_STATES["ONNET"]["logs"]`

**Potential Problems**:
- [ ] `scheduled_task.log` file doesn't exist → sync fails silently
- [ ] Log file path in PROJECT_CONFIG is wrong
- [ ] Log file format doesn't match parser expectations

### Issue #4: Python Environment
**Current Code**:
```python
python_exe = get_python_executable(project)
```

**Potential Problem**: Different projects might require different Python environments or virtualenvs.

**Check**:
- [ ] `get_python_executable()` returns correct path for ONNET?
- [ ] ONNET environment has all required dependencies?
- [ ] `ONNET/.venv/` directory properly configured?

### Issue #5: File Paths on Windows
**Current Code**:
```python
cwd=str(script_path.parent)  # Sets working directory
```

**Potential Problem**: Path separator issues, relative imports in `export_onnet_csv.py` might fail.

**Check**:
- [ ] `export_onnet_csv.py` works when called from `ONNET/` directory?
- [ ] All relative imports use `from pathlib import Path` instead of hardcoded paths?

---

## Troubleshooting Steps 🛠️

### Step 1: Verify Backend Configuration
```bash
# In Titania/ directory, start Python shell:
python
>>> from monitor_app import PROJECT_CONFIG, PROJECT_QUERIES
>>> print(PROJECT_CONFIG["ONNET"])
>>> print(PROJECT_QUERIES["ONNET"])
```

### Step 2: Test Direct Script Execution
```bash
# In ONNET/ directory:
python export_onnet_csv.py
python export_onnet_csv.py --query modelo3
python export_onnet_csv.py --query all
```

### Step 3: Check Process States in Memory
```bash
# Start dashboard, select ONNET, try to run a query
# Then check backend logs:
tail -f C:\Users\javier.castaneda\botsquad\Titania\logs\monitor.log
# or
Get-Content C:\Users\javier.castaneda\botsquad\Titania\logs\monitor.log -Tail 50
```

### Step 4: Debug API Responses
```bash
# Check what the API returns for ONNET:
curl "http://localhost:5000/api/queries?project=ONNET"
curl "http://localhost:5000/api/status?project=ONNET"
curl "http://localhost:5000/api/logs?project=ONNET"
```

### Step 5: Monitor Network Traffic
```bash
# Open browser DevTools (F12)
# Go to Network tab
# Select ONNET project
# Observe requests to /api/status, /api/logs, /api/queries
# Check response payloads
```

---

## Data Flow Diagram

```
Frontend (monitor.js)
    ↓ [Select ONNET + Click Ejecutar]
    ↓
POST /api/run?project=ONNET (query_name: "modelo3")
    ↓
Backend (monitor_app.py)
    ↓ [normalize_project("ONNET")]
    ↓ [get_process_state("ONNET")]
    ↓ [python export_onnet_csv.py --query modelo3]
    ↓ [Capture stdout/stderr in real-time]
    ↓ [add_log() → PROCESS_STATES["ONNET"]["logs"]]
    ↓
Frontend (every 3 seconds)
    ↓ [refresh_dashboard_with_sync()]
    ↓ [sync_logs_from_file("ONNET")]
    ↓
GET /api/logs?project=ONNET&start=0&limit=100
    ↓
Response: {logs: [...], total: N}
    ↓
Display in browser console/logs panel
```

---

## Root Cause Hypothesis 🔮

**Most Likely**: `ONNET/output/` directory doesn't exist or `scheduled_task.log` file path is incorrect.

**Evidence**:
- All API endpoints correctly pass `?project=ONNET`
- Frontend correctly sends requests
- Backend correctly handles project parameter
- But logs may not be persisted/synced because log file path is unreachable

**Solution**:
1. Ensure `ONNET/output/` exists
2. Verify `export_onnet_csv.py` writes to the expected log file
3. Check if manual runs are writing output to correct location

---

## Next Steps ✅

1. **Verify ONNET/output directory**:
   ```powershell
   Test-Path "C:\Users\javier.castaneda\botsquad\ONNET\output"
   mkdir "C:\Users\javier.castaneda\botsquad\ONNET\output" -Force
   ```

2. **Test export_onnet_csv.py directly**:
   ```bash
   cd C:\Users\javier.castaneda\botsquad\ONNET
   python export_onnet_csv.py --query modelo3
   ```

3. **Monitor dashboard logs** while running test:
   ```bash
   cd C:\Users\javier.castaneda\botsquad\Titania
   python -m flask run
   # In another terminal:
   Get-Content -Path "logs/monitor.log" -Wait
   ```

4. **Check backend state** via API:
   ```bash
   Invoke-WebRequest http://localhost:5000/api/status?project=ONNET | ConvertFrom-Json | fl
   ```

---

## Success Criteria ✨

When ONNET monitoring is working correctly, you should see:
- ✅ ONNET option selectable in dropdown
- ✅ ONNET queries populate when project changes
- ✅ Clicking "Ejecutar" starts the process (status = "running")
- ✅ Logs stream in real-time to the dashboard
- ✅ Process completes with status = "completed"
- ✅ Output files appear in the files list
- ✅ Process history saved to database

---

**Analysis Date**: 2025-04-29  
**Status**: Investigation pending - awaiting directory/file verification
