from flask import Blueprint, request, jsonify, current_app
from auth import require_auth

bp = Blueprint("orders", __name__, url_prefix="/orders")

@bp.get("")
@require_auth
def list_orders():
    status = request.args.get("status")
    orders = current_app.db.list_orders(status=status)
    # Filter orders to only show current user's orders
    user_orders = [o for o in orders if o.get("client_id") == request.current_user["client_id"]]
    return jsonify(user_orders)

@bp.post("")
@require_auth
def create_order():
    payload = request.get_json() or {}
    if isinstance(payload, list):
        listPayload = payload
    else:
        listPayload = [payload]
    
    rows = []
    for order_payload in listPayload:
        need = ["product","shirt_size", "base_color", "quantity"]
        missing = [k for k in need if k not in order_payload]
        if missing:
            return jsonify({"error": f"Missing: {', '.join(missing)}"}), 400
        
        # Use authenticated user's client_id
        order_payload["client_id"] = request.current_user["client_id"]
        
        # Create the order using your database function
        row = current_app.db.create_order(order_payload)
        rows.append(row)

    return jsonify(rows), 201

