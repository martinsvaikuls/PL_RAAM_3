from flask import Blueprint, request, jsonify, current_app

bp = Blueprint("orders", __name__, url_prefix="/orders")

@bp.get("")
def list_orders():
    status = request.args.get("status")
    orders = current_app.db.list_orders(status=status)
    return jsonify(orders)

@bp.post("")
def create_order():
    payload = request.get_json() or {}
    if isinstance(payload, list):
        listPayload = payload
    else:
        listPayload = [payload]
    
    rows = []
    for order_payload in listPayload:
        need = ["client_id", "shirt_size", "base_color", "quantity"]
        missing = [k for k in need if k not in order_payload]
        if missing:
            return jsonify({"error": f"Missing: {', '.join(missing)}"}), 400
        
        # Create the order using your database function
        row = current_app.db.create_order(order_payload)
        rows.append(row)

    return jsonify(rows), 201

