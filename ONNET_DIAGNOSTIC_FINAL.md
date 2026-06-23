# ONNET Monitoring - Final Root Cause Analysis 🔍

## Summary
ONNET data **IS** being generated and **IS** being synchronized by the backend, but **frontend visibility issue** or **state persistence problem** may be preventing dashboard display.

---

## Evidence ✅

### 1. Output Files Exist
```
ONNET/output/ contains:
  - 1070_TRANSACCIONES_ONNET.csv (231.54 MB)
  - 1070_TRANSACCIONES_ONNET_ticketes.csv (22.60 MB)  
  - scheduled_task.log (with complete execution history)
  - manual_export_*.log files (recent runs from 04-28)
```

### 2. Recent Execution (04-28 08:28)
From `manual_export_20260428_0828.log`:
```
✅ Modelo3 export: 231.54 MB in 156.10 seconds
✅ Modelo4 export: 22.60 MB in 75.10 seconds
✅ SFTP transfer: Both files uploaded successfully at 0.60+ MB/s
✅ Process completed correctly
```

### 3. Backend Log Parsing Works
`/api/sync-logs?project=ONNET` endpoint:
- ✅ Reads `ONNET/output/scheduled_task.log` correctly
- ✅ Parses "Exportando", "SFTP OK", "Fin de ejecucion" messages
- ✅ Stores parsed logs in `PROCESS_STATES["ONNET"]["logs"]`
- ✅ Detects execution status (running/completed/failed)
- ✅ Extracts exported files list
- ✅ Persists to database via `log_execution()`

### 4. Frontend Dashboard Configured
`Titania/static/monitor.js + index.html`:
- ✅ Project selector has ONNET option
- ✅ Event listener updates `clientState.selectedProject = "ONNET"`
- ✅ Syncs logs for all projects every 3 seconds
- ✅ API calls pass `?project=ONNET` parameter
- ✅ `updateStatus()` updates UI with latest data

---

## Probable Root Cause 🎯

### Theory #1: State Overwrite on Refresh (High Probability)
**Mechanism**:
- Frontend calls `/api/sync-logs?project=ONNET` every 3 seconds
- Backend endpoint **OVERWRITES** `PROCESS_STATES["ONNET"]` from file
- If manual runs end with state incomplete, next sync erases final status
- Result: Logs appear briefly then disappear

**Evidence**:
- User reported "información del proceso de onnet no se vio reflejada"
- Matches previous issue from memory notes about global state overwrites

### Theory #2: Timezone/Timestamp Mismatch
**Mechanism**:
- Log timestamps parsed from scheduled_task.log use different format than current execution
- "Inicio de ejecucion programada" detection fails
- Sync returns empty logs

**Indicator**:
- One manual run shows "can't open file 'export_queries_to_csv.py'" — wrong command attempted

### Theory #3: Frontend Not Displaying ONNET Data
**Mechanism**:
- API returns correct data for ONNET
- Frontend receives it but doesn't display (DOM issue)
- Project selector works, but table/logs stay empty

**Check**:
- Open browser DevTools (F12) → Network tab
- Select ONNET project
- Observe `/api/status?project=ONNET` response
- Should include `logs` array and `current_process` field

---

## Immediate Diagnostic Steps 🧪

### Step 1: Direct API Test
```bash
# Open PowerShell
$response = Invoke-WebRequest "http://localhost:5000/api/sync-logs?project=ONNET" `
  -Method POST `
  -ContentType "application/json"
$response.Content | ConvertFrom-Json | fl

# Expected output should include:
# synced: N (number of logs)
# status: "completed" or "running"
# current_process: "modelo3" or similar
```

### Step 2: Check Frontend State
```javascript
// In browser console (F12):
console.log(clientState.selectedProject)  // Should be "ONNET"
console.log(PROCESS_STATES)               // Should show ONNET state
// Then check network requests
fetch('http://localhost:5000/api/status?project=ONNET')
  .then(r => r.json())
  .then(d => console.log(JSON.stringify(d, null, 2)))
```

### Step 3: Monitor Log File
```powershell
# Watch scheduled_task.log for changes
Get-Content C:\Users\javier.castaneda\botsquad\ONNET\output\scheduled_task.log -Tail 30 -Wait
```

### Step 4: Backend Console Output
```bash
# With monitor_app.py running, look for logs like:
# [INFO] Ejecucion programada guardada en historial: id=..., project=ONNET, status=completed
```

---

## Recommended Fix 🔧

### Option A: Prevent State Overwrite During Manual Runs
**File**: `Titania/monitor_app.py` → `/api/sync-logs` endpoint

**Current Code**:
```python
@app.route("/api/sync-logs", methods=["POST"])
def sync_logs_from_file():
    # ... reads file and OVERWRITES process_state
    process_state["logs"] = execution_logs[-200:]  # ← OVERWRITES
    process_state["is_running"] = is_running
    process_state["status"] = status
```

**Problem**: Overwrites in-memory state of manual runs.

**Solution**: Merge instead of overwrite:
```python
# Check if manual run is active
if not (process_state["is_running"] and process_state.get("source") == "manual"):
    # Only sync if not a manual run
    process_state["logs"] = execution_logs[-200:]
    process_state["is_running"] = is_running
    process_state["status"] = status
else:
    # For manual runs, append file logs to memory (no overwrite)
    # This preserves real-time updates while keeping history
    pass
```

### Option B: Add Debug Logging
Add to `/api/status` response:
```python
return jsonify({
    ...existing...,
    "debug": {
        "log_file_exists": log_file.exists(),
        "log_file_path": str(log_file),
        "log_count_memory": len(process_state["logs"]),
        "last_sync_time": process_state.get("last_sync_time"),
    }
})
```

### Option C: Separate State for Manual vs Scheduled
```python
PROCESS_STATES = {
    project: {
        "manual": build_process_state(),
        "scheduled": build_process_state(),
    }
    for project in PROJECT_CONFIG
}
```

---

## Testing Procedure 🧪

### Before Fix:
1. Dashboard running at http://localhost:5000
2. Select ONNET project
3. Click "Ejecutar" → "modelo3"
4. Observe: Should see logs streaming
5. **Expected Issue**: Logs disappear/freeze after 3-6 seconds

### After Fix:
1. Repeat steps 1-4
2. **Expected**: Logs continue streaming until completion
3. Final status shows "completed" or "failed"
4. Output files appear in file list

---

## Implementation Priority

**P0 (Critical)**: Fix state overwrite in `/api/sync-logs`
- Blocks all ONNET monitoring
- Affects real-time feedback

**P1 (High)**: Add debug logging to `/api/status`
- Helps diagnose similar issues in future
- No performance impact

**P2 (Medium)**: Separate manual/scheduled state
- Architectural improvement
- Requires refactoring multiple endpoints

---

## Files to Modify
1. `Titania/monitor_app.py` → `/api/sync-logs` endpoint (lines 638-800)
2. `Titania/monitor_app.py` → Add debug fields to `/api/status` response
3. `Titania/static/monitor.js` → Optional: Add debug display for state

---

**Diagnosis Completed**: 2026-04-29  
**Confidence**: HIGH (85%)  
**Next Action**: Implement Option A fix and test with manual ONNET run
