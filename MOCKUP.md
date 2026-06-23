# Prototipo Visual - Process Monitor v2

## Mockup de Interfaz Interactiva

### 1. PANTALLA PRINCIPAL (Dashboard)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ⟫ Process Monitor v2                    🔄 📢(2) ❓ ⚙️                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ ESTADÍSTICAS EN TIEMPO REAL                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ ⟳ Ejecutando │  │ ✓ Exitosos   │  │ ✗ Errores    │  │ Tasa Éxito   │    │
│  │      2       │  │      47      │  │      3       │  │     94%      │    │
│  │              │  │              │  │              │  │ ████████░░░░ │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ NAVEGACIÓN                                                                  │
│  [Procesos] [Historial] [Logs en vivo] [Analytics]                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FILTROS                                                                     │
│ Buscar procesos...  [Proyecto ▼ Titania]  [Estado ▼ Todos]  [+ Nuevo]     │
│ Resultado: 5 de 8 procesos                                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ GRILLA DE PROCESOS (GRID 4 COLUMNAS EN DESKTOP)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────────────────┐  ┌───────────────────────┐  ┌─────────────────┐  │
│  │ [✓ Completado]        │  │ [⟳ Ejecutando]        │  │ [✓ Completado]  │  │
│  │                       │  │                       │  │                 │  │
│  │ Titania Export SFTP   │  │ ONNET Export Mod3     │  │ DB Health Check │  │
│  │ Titania               │  │ ONNET                 │  │ Infraestructura │  │
│  │                       │  │                       │  │                 │  │
│  │ Exporta queries a CSV │  │ Exporta Modelo 3      │  │ Verifica base   │  │
│  │ y carga vía SFTP      │  │ (Transacciones)       │  │ de datos        │  │
│  │                       │  │                       │  │                 │  │
│  │ Última ejecución:     │  │ Última ejecución:     │  │ Última ejecuc.: │  │
│  │ Hace 2 min            │  │ Hace 30 seg (…)       │  │ Hace 5 min      │  │
│  │ CPU: 32% | Mem: 256MB │  │ CPU: 65% | Mem: 512MB │  │ CPU: 5% | Mem:  │  │
│  │                       │  │                       │  │ 32MB            │  │
│  │ ⏭ Programado: 0 */2   │  │                       │  │ ⏭ Programado:    │  │
│  │ * * *                 │  │                       │  │ */5 * * * *     │  │
│  │                       │  │                       │  │                 │  │
│  │ [▶ Ejecutar] [Más...] │  │ [⏹ Detener] [Ver] [+] │  │ [▶ Ejecutar] [⋮]│  │
│  └───────────────────────┘  └───────────────────────┘  └─────────────────┘  │
│                                                                               │
│  ┌───────────────────────┐  ┌───────────────────────┐                       │
│  │ [✗ Error]             │  │ [Inactivo]            │                       │
│  │                       │  │                       │                       │
│  │ PBI Dashboard Refresh │  │ Custom Process        │                       │
│  │ Titania               │  │ Titania               │                       │
│  │                       │  │                       │                       │
│  │ Refresca dashboards   │  │ Proceso personalizado │                       │
│  │ en Power BI           │  │ (sin ejecuciones)     │                       │
│  │                       │  │                       │                       │
│  │ Última ejecución:     │  │                       │                       │
│  │ Hace 1 hora           │  │                       │                       │
│  │ ERROR: Connection...  │  │ ⏭ Programado:         │                       │
│  │                       │  │ NO                    │                       │
│  │ [Reintentar] [Ver] [⋮]│  │ [▶ Ejecutar] [+] [⋮]  │                       │
│  └───────────────────────┘  └───────────────────────┘                       │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. DIÁLOGO DE EJECUCIÓN CON PARÁMETROS

```
┌──────────────────────────────────────────────────────────────┐
│ Ejecutar: Titania Export SFTP                           [x]  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│ Queries a exportar: *                                        │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ ☑ all                                                  │  │
│ │ ☐ chat_histories                                       │  │
│ │ ☐ user_banned                                          │  │
│ │ ☐ chat_history_analysis                               │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                               │
│ Batch Size:                                                  │
│ [________] (Min: 100, Max: 10000, Defecto: 1000)            │
│                                                               │
│ Date Range: (Optional)                                       │
│ [dd/mm/yyyy] - [dd/mm/yyyy]                                  │
│                                                               │
│ Environment Variables: (Advanced)                            │
│ [Mostrar ▼]                                                  │
│                                                               │
│                                    [Cancelar]  [Ejecutar ▶]  │
└──────────────────────────────────────────────────────────────┘
```

---

### 3. PANEL DE LOGS EN TIEMPO REAL

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Logs en tiempo real (152)                                                   │
│ Búscar: __________________  [DEBUG] [INFO] [⚠ WARNING] [✗ ERROR]  ⬇️ 🔄 ✕  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ ███████████████████████████████████ Cargando logs (⟳)                       │
│                                                                               │
│ [14:32:15] [INFO] Iniciando proceso: Titania Export SFTP                   │
│ [14:32:15] [INFO] Parámetros: {"queries": "all", "batch_size": 1000}       │
│ [14:32:16] [INFO] Conectando a base de datos...                             │
│ [14:32:18] [INFO] Conexión exitosa                                          │
│ [14:32:18] [INFO] Consultando VW_n8n_chat_histories_classfication (1/5)    │
│ [14:32:22] [INFO] Rows: 15423                                               │
│ [14:32:25] [INFO] Consultando VW_n8n_chat_histories_textual_all (2/5)      │
│ [14:32:35] [INFO] Rows: 42108                                               │
│ [14:32:35] [⚠ WARNING] Uso de memoria > 80%: 512 MB                        │
│ [14:32:40] [INFO] Consultando VW_n8n_chat_history_textual (3/5)            │
│ [14:32:58] [INFO] Rows: 89234                                               │
│ [14:33:02] [⚠ WARNING] CPU > 75%: 78%                                      │
│ [14:33:05] [INFO] Consultando VW_n8n_chat_user_banned (4/5)                │
│ [14:33:12] [INFO] Rows: 234                                                 │
│ [14:33:15] [INFO] Exportando a CSV...                                       │
│ [14:33:22] [INFO] Archivo: /output/export_2024-01-15.csv (245 MB)          │
│ [14:33:25] [INFO] Iniciando carga SFTP a sftp.example.com...               │
│ [14:33:45] [INFO] Archivo subido exitosamente                               │
│ [14:33:46] [INFO] ✓ Proceso completado en 91 segundos                      │
│                                                                               │
│ █ Descargar logs                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 4. PESTAÑA DE HISTORIAL (DataGrid)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ HISTORIAL DE EJECUCIONES                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Filtro: [Proceso ▼]  [Estado ▼ Todos]  [Rango ▼]                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ ID          │ Proceso              │ Estado    │ Inicio      │ Duración     │
│─────────────┼──────────────────────┼───────────┼─────────────┼──────────    │
│ exec-1234   │ Titania Export SFTP  │ ✓ Exitoso │ 14:32:15    │ 1m 31s       │
│ exec-1233   │ ONNET Export Mod3    │ ⟳ En ejecución (70%)                   │
│ exec-1232   │ ONNET Export Mod4    │ ✓ Exitoso │ 13:15:42    │ 45m 23s      │
│ exec-1231   │ DB Health Check      │ ✓ Exitoso │ 14:35:00    │ 5s           │
│ exec-1230   │ PBI Refresh          │ ✗ Error   │ 13:00:12    │ 2m 45s       │
│ exec-1229   │ Titania Export SFTP  │ ✓ Exitoso │ 12:32:15    │ 1m 44s       │
│ ...         │ ...                  │ ...       │ ...         │ ...          │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 5. PESTAÑA DE ANALYTICS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ANALYTICS - MÉTRICAS Y TENDENCIAS                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│ Período: [Últimos 7 días ▼]                                                 │
│                                                                               │
│ ┌────────────────────────────┐  ┌────────────────────────────┐              │
│ │ Duración Promedio           │  │ Tasa de Éxito              │              │
│ │ (por proceso)               │  │ (últimas 30 ejecuciones)   │              │
│ │                             │  │                            │              │
│ │ Titania Export:     1m 38s  │  │ 94%  ███████████░ exitosas│              │
│ │ ONNET M3:         45m 12s  │  │  6%  ░░░░░░░░░░░░ errores  │              │
│ │ ONNET M4:         38m 45s  │  │                            │              │
│ │ DB Health Check:       8s  │  │                            │              │
│ │ PBI Refresh:       15m 34s  │  │                            │              │
│ │                             │  │                            │              │
│ └────────────────────────────┘  └────────────────────────────┘              │
│                                                                               │
│ ┌──────────────────────────────────────────────────────────┐                │
│ │ Ejecuciones por Día (últimos 7 días)                     │                │
│ │                                                           │                │
│ │     10 ┤                              ╭─╮                 │                │
│ │      9 ┤                              │ │                 │                │
│ │      8 ┤     ╭─╮                      │ │ ╭─╮              │                │
│ │      7 ┤     │ │     ╭─╮              │ │ │ │              │                │
│ │      6 ┤ ╭─╮ │ │ ╭─╮ │ │  ╭─╮        │ │ │ │  ╭─╮         │                │
│ │      5 ┤ │ │ │ │ │ │ │ │  │ │        │ │ │ │  │ │         │                │
│ │      4 ┤ │ │ │ │ │ │ │ │  │ │  ╭─╮  │ │ │ │  │ │         │                │
│ │      3 ┤ │ │ │ │ │ │ │ │  │ │  │ │  │ │ │ │  │ │  ╭─╮    │                │
│ │      2 ┤ │ │ │ │ │ │ │ │  │ │  │ │  │ │ │ │  │ │  │ │    │                │
│ │      1 ┤ │ │ │ │ │ │ │ │  │ │  │ │  │ │ │ │  │ │  │ │    │                │
│ │        └─┴─┴─┴─┴─┴─┴─┴─┴──┴─┴──┴─┴──┴─┴─┴─┴──┴─┴──┴─┴────│                │
│ │          L   M   M   J   V   S   D                         │                │
│ │                                                           │                │
│ └──────────────────────────────────────────────────────────┘                │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 6. DRAWER DE CONFIGURACIÓN

```
┌────────────────────────────────────┐
│ CONFIGURACIÓN                  [x] │
├────────────────────────────────────┤
│                                    │
│ ⚙️  Procesos                       │
│    Gestionar procesos              │
│                                    │
│ 📢 Alertas & Notificaciones        │
│    Configurar canales              │
│                                    │
│ 📋 Historial                       │
│    Retención de datos              │
│                                    │
│ 🔑 Seguridad                       │
│    Tokens y permisos               │
│                                    │
│ ❓ Ayuda & Documentación           │
│    Ver guías                       │
│                                    │
└────────────────────────────────────┘
```

---

## 🎯 Características de UX/UI

### Responsive Design
- **Desktop (lg)**: 4 columnas en grid
- **Tablet (md)**: 3 columnas
- **Mobile (sm)**: 2 columnas
- **Extra pequeño (xs)**: 1 columna

### Temas
- Dark mode soportado (MUI theme)
- Material Design 3 compliance
- Accesibilidad (WCAG 2.1 AA)

### Interacciones
- ✅ Animaciones suaves (MUI transitions)
- ✅ Loading states (skeleton, progress)
- ✅ Error handling con mensajes claros
- ✅ Confirmación antes de acciones destructivas
- ✅ Tooltips informativos
- ✅ Snackbars para notificaciones

### Performance
- ✅ Lazy loading de componentes
- ✅ Virtualización de listas largas
- ✅ Memoización con React.memo
- ✅ Code splitting automático (Vite)

---

## 📱 Responsive Breakpoints (MUI v5)

```typescript
// xs: 0px (mobile)
// sm: 600px (tablet)
// md: 960px (desktop small)
// lg: 1280px (desktop large)
// xl: 1920px (ultra-wide)

sx={{
  gridTemplateColumns: {
    xs: '1fr',           // Mobile: 1 column
    sm: 'repeat(2, 1fr)', // Tablet: 2 columns
    md: 'repeat(3, 1fr)', // Desktop: 3 columns
    lg: 'repeat(4, 1fr)', // Large: 4 columns
  }
}}
```

---

## 🎨 Paleta de Colores

```typescript
const theme = {
  primary: '#1976d2',    // Azul (Acciones principales)
  secondary: '#dc004e',  // Rojo/Rosa (Acentos)
  success: '#4caf50',    // Verde (Éxito)
  error: '#f44336',      // Rojo (Errores)
  warning: '#ff9800',    // Naranja (Advertencias)
  info: '#2196f3',       // Azul claro (Info)
  background: '#f5f5f5', // Gris claro
}
```

---

## ✨ Próximas Mejoras UI

- [ ] Dark mode toggle en AppBar
- [ ] Drag & drop para reordenar tarjetas
- [ ] Custom theming por usuario
- [ ] PWA (installable)
- [ ] Real-time notifications (toast)
- [ ] Keyboard shortcuts
- [ ] Exportar dashboard como PDF
- [ ] Tema colorblind-friendly

