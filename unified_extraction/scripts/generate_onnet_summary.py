"""
generate_onnet_summary.py
-------------------------
Genera onnet_summary.json a partir de los CSV operativos ONNET.

Salidas:
  - BPA_DataCentric/Dashboards/onnet/DB_React/public/data/onnet_summary.json
  - BPA_DataCentric/Dashboards/onnet/DB_Tailwind/public/data/onnet_summary.json
  - BPA_DataCentric/Dashboards/onnet/DB_SvelteKit/static/data/onnet_summary.json

Uso:
  python unified_extraction/scripts/generate_onnet_summary.py
  python unified_extraction/scripts/generate_onnet_summary.py --no-copy   # solo imprime JSON
"""

import csv
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent          # BPA_DataSolution/
DATACENTRIC_ROOT = os.environ.get(
    "DATACENTRIC_ROOT",
    str(REPO_ROOT.parent / "BPA_DataCentric"),
)
ONNET_OUTPUTS = Path(DATACENTRIC_ROOT) / "Outputs" / "Onnet"
TRANSACTIONS_CSV = ONNET_OUTPUTS / "1070_TRANSACCIONES_ONNET.csv"
TICKETS_CSV      = ONNET_OUTPUTS / "1070_TRANSACCIONES_ONNET_ticketes.csv"

DASHBOARD_BASE = Path(DATACENTRIC_ROOT) / "Dashboards" / "onnet"
OUTPUT_PATHS = [
    DASHBOARD_BASE / "DB_React"    / "public" / "data" / "onnet_summary.json",
    DASHBOARD_BASE / "DB_Tailwind" / "public" / "data" / "onnet_summary.json",
    DASHBOARD_BASE / "DB_SvelteKit"/ "static"  / "data" / "onnet_summary.json",
]

HOURS_24_S = 24 * 3600

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def _to_number(value) -> float:
    try:
        n = float(value)
        return n if math.isfinite(n) else 0.0
    except (ValueError, TypeError):
        return 0.0


def _round(value: float, decimals: int = 2) -> float:
    factor = 10 ** decimals
    return round(value * factor) / factor


def _to_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value.strip()[:26], fmt)
        except ValueError:
            continue
    return None


def _compact_key(value: Optional[str]) -> str:
    import unicodedata
    s = (value or "").strip()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = "".join(c for c in s if c.isalnum()).upper()
    return s or "UNKNOWN"


def _is_meaningful(value: Optional[str]) -> bool:
    key = _compact_key(value)
    return key not in ("UNKNOWN", "NO", "NA", "N/A", "")


def _normalize_category(value: Optional[str]) -> str:
    key = _compact_key(value)
    if not _is_meaningful(key):
        return "UNKNOWN"
    if key in ("DATOS", "DATA", "DATAISSUE", "CALIDADDATOS"):
        return "DATOS"
    if key in ("RED", "NETWORK", "NETWORKFAIL", "CONECTIVIDAD"):
        return "RED"
    if key in ("APROVISIONAMIENTO", "PROVISIONING", "ACTIVACION", "ACTIVACIONSERVICIO"):
        return "APROVISIONAMIENTO"
    if key in ("CONFIGURACION", "CONFIG", "PARAMETRIZACION", "PARAMETRIZACIONRED"):
        return "CONFIGURACION"
    if key in ("INCIDENTE", "INCIDENT", "FALLA", "ERROROPERATIVO"):
        return "INCIDENTE"
    if key in ("NOAPLICA", "NA"):
        return "NO APLICA"
    return (value or "").strip().upper() or "UNKNOWN"


def _normalize_severity(value: Optional[str]) -> str:
    key = _compact_key(value)
    if not _is_meaningful(key):
        return "UNKNOWN"
    if key in ("CRITICO", "CRITICAL", "SEV1", "P1", "ALTOCRITICO"):
        return "CRITICA"
    if key in ("ALTA", "HIGH", "SEV2", "P2", "ALTO"):
        return "ALTA"
    if key in ("MEDIA", "MEDIUM", "SEV3", "P3"):
        return "MEDIA"
    if key in ("BAJA", "LOW", "SEV4", "P4"):
        return "BAJA"
    if key in ("NOAPLICA", "NA"):
        return "NO APLICA"
    return (value or "").strip().upper() or "UNKNOWN"


def _normalize_owner(value: Optional[str]) -> str:
    key = _compact_key(value)
    if not _is_meaningful(key):
        return "UNKNOWN"
    if key in ("ONNET", "NOCONNET", "EQUIPOONNET"):
        return "ONNET"
    if key in ("PROVEEDOR", "VENDOR", "TERCERO", "OUTSOURCING"):
        return "PROVEEDOR"
    if key in ("BACKOFFICE", "BACKOFFICEONNET", "BO"):
        return "BACKOFFICE"
    if key in ("OPERACIONES", "OPS", "NOC", "NOCOPS"):
        return "OPERACIONES"
    return (value or "").strip().upper() or "UNKNOWN"


def _normalize_error(value: Optional[str]) -> str:
    key = _compact_key(value)
    if not _is_meaningful(key):
        return "UNKNOWN"
    if key in ("TIMEOUT", "TIMEOUTERROR", "CONNECTIONTIMEOUT", "REQUESTTIMEOUT"):
        return "TIMEOUT"
    if key in ("AUTH", "AUTHERROR", "UNAUTHORIZED", "CREDENCIALESINVALIDAS"):
        return "AUTH"
    if key in ("VALIDATION", "VALIDACION", "DATAVALIDATION", "PARAMINVALID"):
        return "VALIDACION"
    if key in ("UNAVAILABLE", "SERVICEUNAVAILABLE", "SERVICIONODISPONIBLE", "HTTP503"):
        return "SERVICIO NO DISPONIBLE"
    return (value or "").strip().upper() or "UNKNOWN"


def _to_rate(count: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return _round((count / total) * 100)


def _percentile(values: list[float], p: int) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = math.ceil((p / 100) * len(sorted_vals)) - 1
    return sorted_vals[max(0, min(idx, len(sorted_vals) - 1))]


def _top_distribution(counter: dict, total: int, limit: int = 5) -> list:
    return [
        {"name": name, "count": count, "ratePct": _to_rate(count, max(total, 1))}
        for name, count in sorted(counter.items(), key=lambda x: -x[1])[:limit]
    ]

# ---------------------------------------------------------------------------
# CSV readers
# ---------------------------------------------------------------------------

def _read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        return [
            {k.strip().lower(): (v or "").strip() for k, v in row.items()}
            for row in reader
        ]


def _pick(row: dict, aliases: list[str]) -> str:
    for alias in aliases:
        if alias in row and row[alias]:
            return row[alias]
    return ""

# ---------------------------------------------------------------------------
# KPI computation
# ---------------------------------------------------------------------------

def aggregate_retry_by_order(rows: list[dict]) -> list[dict]:
    by_order: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        cfs = _pick(row, ["cfs_id", "cfsid", "order_id"])
        if cfs:
            by_order[cfs].append(row)

    aggregates = []
    for cfs_id, order_rows in by_order.items():
        def resp_ts(r):
            dt = _to_dt(_pick(r, ["fecha_response", "response_date"]))
            return dt.timestamp() if dt else 0

        sorted_rows = sorted(order_rows, key=resp_ts)
        last = sorted_rows[-1]
        reintentos_vals = [_to_number(_pick(r, ["reintentos", "retry_count"])) for r in sorted_rows]
        max_r = max(reintentos_vals) if reintentos_vals else 0
        unique_r = len(set(reintentos_vals))

        aggregates.append({
            "cfs_id": cfs_id,
            "tmf": _pick(last, ["tmf", "api"]) or "UNKNOWN",
            "operation": _pick(last, ["operation", "operacion"]) or "UNKNOWN",
            "maxReintentos": max_r,
            "uniqueReintentos": unique_r,
            "singleAttempt": max_r == 1,
            "retryOvereffort": max_r > 1,
            "multivalueOvereffort": unique_r > 1,
            # Use earliest reception_date for the order
            "receptionMonth": _reception_month(order_rows),
        })

    return aggregates


def _reception_month(order_rows: list[dict]) -> str:
    """Return YYYY-MM string from the earliest reception_date in the group, or ''."""
    months = []
    for r in order_rows:
        raw = _pick(r, ["reception_date", "fecha_recepcion", "fecha_creacion"])
        dt = _to_dt(raw)
        if dt:
            months.append(dt.strftime("%Y-%m"))
    return min(months) if months else ""


def calculate_retry_by_tmf_by_month(agg: list[dict]) -> list[dict]:
    """Group orders by TMF and reception month, returning monthly bar+line data."""
    # buckets[tmf][month] = {sinReintento, conReintento, total}
    buckets: dict[str, dict[str, dict]] = defaultdict(lambda: defaultdict(lambda: {"sinReintento": 0, "conReintento": 0, "total": 0}))

    for row in agg:
        tmf = row["tmf"]
        month = row["receptionMonth"]
        if not month:
            continue
        buckets[tmf][month]["total"] += 1
        if row["singleAttempt"]:
            buckets[tmf][month]["sinReintento"] += 1
        else:
            buckets[tmf][month]["conReintento"] += 1

    result = []
    for tmf, months_data in buckets.items():
        months_list = []
        for month in sorted(months_data):
            d = months_data[month]
            total = d["total"]
            single = d["sinReintento"]
            months_list.append({
                "month": month,
                "sinReintento": single,
                "conReintento": d["conReintento"],
                "total": total,
                "singleAttemptRatePct": _to_rate(single, total),
            })
        result.append({"group": tmf, "months": months_list})

    # Order same as retryByTmf (by retryOvereffortRatePct desc)
    tmf_order = {}
    for row in agg:
        tmf = row["tmf"]
        if tmf not in tmf_order:
            tmf_order[tmf] = {"retry": 0, "total": 0}
        tmf_order[tmf]["total"] += 1
        if row["retryOvereffort"]:
            tmf_order[tmf]["retry"] += 1

    def _sort_key(entry):
        t = tmf_order.get(entry["group"], {"retry": 0, "total": 1})
        return -(t["retry"] / max(t["total"], 1))

    return sorted(result, key=_sort_key)


def calculate_retry_summary(agg: list[dict]) -> dict:
    total = len(agg)
    single = sum(1 for r in agg if r["singleAttempt"])
    retry_oe = sum(1 for r in agg if r["retryOvereffort"])
    multi_oe = sum(1 for r in agg if r["multivalueOvereffort"])
    max_vals = [r["maxReintentos"] for r in agg]
    avg_max = (sum(max_vals) / total) if total > 0 else 0.0

    return {
        "totalOrders": total,
        "singleAttemptOrders": single,
        "singleAttemptRatePct": _to_rate(single, total),
        "retryOvereffortOrders": retry_oe,
        "retryOvereffortRatePct": _to_rate(retry_oe, total),
        "multivalueOvereffortOrders": multi_oe,
        "multivalueOvereffortRatePct": _to_rate(multi_oe, total),
        "avgMaxReintentos": _round(avg_max, 4),
        "p95MaxReintentos": _round(_percentile(max_vals, 95), 4),
    }


def calculate_retry_by_group(agg: list[dict], group_by: str) -> list[dict]:
    buckets: dict[str, list[dict]] = defaultdict(list)
    for row in agg:
        key = row["tmf"] if group_by == "tmf" else row["operation"]
        buckets[key].append(row)

    result = []
    for group, items in buckets.items():
        orders = len(items)
        single = sum(1 for r in items if r["singleAttempt"])
        retry = sum(1 for r in items if r["retryOvereffort"])
        multi = sum(1 for r in items if r["multivalueOvereffort"])
        avg_max = sum(r["maxReintentos"] for r in items) / max(orders, 1)
        result.append({
            "group": group,
            "orders": orders,
            "singleAttemptRatePct": _round((single / max(orders, 1)) * 100),
            "retryOvereffortRatePct": _round((retry / max(orders, 1)) * 100),
            "multivalueOvereffortRatePct": _round((multi / max(orders, 1)) * 100),
            "avgMaxReintentos": _round(avg_max, 3),
        })

    return sorted(result, key=lambda x: (-x["retryOvereffortRatePct"], -x["orders"]))


def calculate_sla_general_24h(rows: list[dict], target_rate_pct: float = 97.0) -> dict:
    # Última fila por cfs_id (último response_date)
    by_order: dict[str, dict] = {}
    for row in rows:
        cfs = _pick(row, ["cfs_id"])
        if not cfs:
            continue
        prev = by_order.get(cfs)
        if prev is None:
            by_order[cfs] = row
        else:
            prev_dt = _to_dt(_pick(prev, ["fecha_response", "response_date"]))
            curr_dt = _to_dt(_pick(row, ["fecha_response", "response_date"]))
            if curr_dt and (not prev_dt or curr_dt >= prev_dt):
                by_order[cfs] = row

    total = 0
    in_24h = 0
    for row in by_order.values():
        created = _to_dt(_pick(row, ["fecha_creacion", "reception_date", "creation_date"]))
        response = _to_dt(_pick(row, ["fecha_response", "response_date"]))
        if not created or not response:
            continue
        total += 1
        diff = (response - created).total_seconds()
        if diff <= HOURS_24_S:
            in_24h += 1

    rate = (in_24h / total * 100) if total > 0 else 0.0
    return {
        "totalAttendedCases": total,
        "attendedIn24hCases": in_24h,
        "attendedIn24hRatePct": _round(rate),
        "targetRatePct": target_rate_pct,
        "isCompliant": rate >= target_rate_pct,
    }


def calculate_operational_summary(tx_rows: list[dict], ticket_rows: list[dict]) -> dict:
    agg = aggregate_retry_by_order(tx_rows)
    total_operations = len(agg)

    # Errores desde transacciones: error=SI (flag), agrupados por response_code no-200
    # Tomamos el último response_code por cfs_id (orden de response_date)
    last_response: dict[str, dict] = {}
    for row in tx_rows:
        cfs = _pick(row, ["cfs_id"])
        if not cfs:
            continue
        prev = last_response.get(cfs)
        if prev is None:
            last_response[cfs] = row
        else:
            prev_dt = _to_dt(_pick(prev, ["response_date"]))
            curr_dt = _to_dt(_pick(row, ["response_date"]))
            if curr_dt and (not prev_dt or curr_dt >= prev_dt):
                last_response[cfs] = row

    error_by_name: dict[str, int] = defaultdict(int)
    error_orders: set[str] = set()
    for cfs, row in last_response.items():
        # error='SI' indica operación con error
        err_flag = _pick(row, ["error"]).strip().upper()
        if err_flag == "SI":
            error_orders.add(cfs)
            # Agrupar por response_code para top errors (excluir códigos 2xx)
            resp_code = _pick(row, ["response_code"]).strip() or "UNKNOWN"
            if resp_code.startswith("2"):
                continue
            resp_desc = _pick(row, ["response_description"]).strip()
            # Label = "CODE - descripción corta (max 40 chars)"
            if resp_desc and resp_code != resp_desc:
                label = f"{resp_code} - {resp_desc[:40]}"
            else:
                label = resp_code
            error_by_name[label] += 1

    operations_with_error = len(error_orders)

    # Tickets
    ticket_by_category: dict[str, int] = defaultdict(int)
    ticket_by_severity: dict[str, int] = defaultdict(int)
    ticket_by_owner: dict[str, int] = defaultdict(int)
    ticket_orders: set[str] = set()
    sla_raw: dict[str, dict] = defaultdict(lambda: {"total": 0, "in24h": 0})

    for row in ticket_rows:
        cfs = _pick(row, ["cfs_id"]) or "UNKNOWN"
        ticket_num = _pick(row, ["ticket_number", "ticket", "tiquete"])
        if not _is_meaningful(ticket_num):
            continue

        category = _normalize_category(_pick(row, ["category", "categoria"]))
        severity = _normalize_severity(_pick(row, ["severity", "severidad"]))
        owner = _normalize_owner(_pick(row, ["owner", "dueno", "json_name"]))

        ticket_orders.add(cfs)
        ticket_by_category[category] += 1
        ticket_by_severity[severity] += 1
        ticket_by_owner[owner] += 1

        created = _to_dt(_pick(row, ["fecha_creacion", "reception_date"]))
        response = _to_dt(_pick(row, ["fecha_response"]))
        if created and response:
            diff = (response - created).total_seconds()
            sla_raw[category]["total"] += 1
            if diff <= HOURS_24_S:
                sla_raw[category]["in24h"] += 1

    operations_with_ticket = len(ticket_orders)

    sla_by_category = sorted(
        [
            {
                "category": cat,
                "total": vals["total"],
                "in24h": vals["in24h"],
                "in24hRatePct": _to_rate(vals["in24h"], vals["total"]),
            }
            for cat, vals in sla_raw.items()
        ],
        key=lambda x: -x["total"],
    )[:5]

    return {
        "totalOperations": total_operations,
        "operationsWithError": operations_with_error,
        "errorRatePct": _to_rate(operations_with_error, total_operations),
        "operationsWithTicket": operations_with_ticket,
        "ticketOpenRatePct": _to_rate(operations_with_ticket, total_operations),
        "topErrors": _top_distribution(error_by_name, max(operations_with_error, 1)),
        "topTicketCategories": _top_distribution(ticket_by_category, max(operations_with_ticket, 1)),
        "topSeverities": _top_distribution(ticket_by_severity, max(operations_with_ticket, 1)),
        "topOwners": _top_distribution(ticket_by_owner, max(operations_with_ticket, 1)),
        "slaByCategory": sla_by_category,
    }

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate_summary(no_copy: bool = False) -> dict:
    print(f"[onnet_summary] Leyendo transacciones: {TRANSACTIONS_CSV}")
    tx_rows = _read_csv(TRANSACTIONS_CSV)
    print(f"  → {len(tx_rows):,} filas")

    print(f"[onnet_summary] Leyendo tickets:        {TICKETS_CSV}")
    ticket_rows = _read_csv(TICKETS_CSV)
    print(f"  → {len(ticket_rows):,} filas")

    print("[onnet_summary] Calculando KPIs...")
    agg = aggregate_retry_by_order(tx_rows)

    summary = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "retrySummary":         calculate_retry_summary(agg),
        "retryByTmf":           calculate_retry_by_group(agg, "tmf"),
        "retryByTmfByMonth":    calculate_retry_by_tmf_by_month(agg),
        "retryByOperation":     calculate_retry_by_group(agg, "operation"),
        "slaGeneral24h":        calculate_sla_general_24h(tx_rows),
        "operationalSummary":   calculate_operational_summary(tx_rows, ticket_rows),
    }

    if no_copy:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return summary

    for path in OUTPUT_PATHS:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"  [OK] {path}")

    print("[onnet_summary] Completado.")
    return summary


if __name__ == "__main__":
    no_copy = "--no-copy" in sys.argv
    generate_summary(no_copy=no_copy)
