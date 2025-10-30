from flask import Blueprint, request, jsonify, current_app

bp = Blueprint("planning", __name__, url_prefix="/planning")

@bp.post("/run")
def run_planning():
    body = request.get_json() or {}
    method = (body.get("method") or "HEURISTIC").upper()
    penalty = float(body.get("penaltyPerHour", 5.0))
    printers = current_app.db.list_printers()
    orders = current_app.db.list_orders(status="NEW")
    if not printers or not orders:
        return jsonify({"rows": [], "note": "no printers or no NEW orders"})
    rows = plan_milp(orders, printers, penalty) if method == "MILP" else plan_edd(orders, printers)
    saved = current_app.db.save_plan_rows(rows)
    return jsonify({"rows": saved})

from datetime import datetime, timedelta

def plan_edd(orders, printers):
    rows = []
    now = datetime.now()
    orders = sorted(orders, key=lambda o: o["deadline"])
    for o in orders:
        qty = int(o["quantity"])
        best = min(printers, key=lambda p: float(p["cost_per_shirt"]))
        perf = float(best["performance_shirts_per_hour"]) or 1.0
        dur_h = qty / perf
        start = now
        end = start + timedelta(hours=dur_h)
        rows.append({
            "order_id": int(o["id"]),
            "printer_id": int(best["id"]),
            "start_time": start.isoformat(timespec="seconds"),
            "end_time": end.isoformat(timespec="seconds"),
            "qty": qty,
            "total_cost": round(qty * float(best["cost_per_shirt"]), 2),
        })
        now = end
    return rows

def plan_milp(orders, printers, penalty_per_hour=5.0):
    return plan_edd(orders, printers)