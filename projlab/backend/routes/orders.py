from flask import Blueprint, request, jsonify, current_app

bp = Blueprint("orders", __name__, url_prefix="/orders")

@bp.get("")
def list_orders():
    status = request.args.get("status")
    return jsonify(current_app.db.list_orders(status=status))

@bp.post("")
def create_order():
    payload = request.get_json() or {}
    need = ["shirt_size", "base_color", "quantity", "deadline"]
    missing = [k for k in need if k not in payload]
    if missing:
        return jsonify({"error": f"Missing: {', '.join(missing)}"}), 400
    # demo: klienta ID fiksēts uz 1
    row = current_app.db.create_order(payload, client_id=1)
    return jsonify(row), 201