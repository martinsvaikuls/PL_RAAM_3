from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

bp = Blueprint("planning", __name__, url_prefix="/planning")

@bp.post("/run")
def run_planning():
    """Run the planning algorithm (either HEURISTIC or MILP)."""
    body = request.get_json() or {}
    method = (body.get("method") or "HEURISTIC").upper()
    #penalty = float(body.get("penaltyPerHour", 5.0))

    # Fetch printers and orders from Google Sheets
    printers = current_app.db.list_printers()
    orders = current_app.db.list_orders(status="NEW")

    if not printers or not orders:
        return jsonify({"rows": [], "note": "No printers or no NEW orders"})

    # Choose the planning method
    #rows = plan_milp(orders, printers, penalty) if method == "MILP" else plan_edd(orders, printers)
    rows = plan_edd(orders, printers)


    # Save the planning result to Google Sheets
    saved_rows = current_app.db.save_plan_rows(rows)
    return jsonify({"rows": saved_rows})

def plan_edd(orders, printers):
    """Plan using the EDD (Earliest Due Date) method."""
    rows = []
    now = datetime.now()
    orders = sorted(orders, key=lambda o: o["created_at"])

    for order in orders:
        qty = int(order["quantity"])
        best_printer = max(printers, key=lambda p: float(p["base_speed"]))
        performance = float(best_printer["base_speed"]) or 1.0
        duration_hours = qty / performance
        start_time = now
        end_time = start_time + timedelta(hours=duration_hours)

        rows.append({
            "order_id": int(order["id"]),
            "printer_id": int(best_printer["id"]),
            "start_time": start_time.isoformat(timespec="seconds"),
            "end_time": end_time.isoformat(timespec="seconds"),
            "cost":  round(qty * float(best_printer["base_speed"]), 2),
            "client_cost": round(1.2* qty * float(best_printer["base_speed"]), 2),
        })

        now = end_time
    return rows

#def plan_milp(orders, printers, penalty_per_hour=5.0):
    """Plan using the MILP method. In this example, it falls back to EDD."""
    #    return plan_edd(orders, printers)
