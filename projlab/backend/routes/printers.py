from flask import Blueprint, request, jsonify, current_app

bp = Blueprint("printers", __name__, url_prefix="/printers")

@bp.get("")
def list_printers():
    return jsonify(current_app.db.list_printers())

@bp.post("")
def create_printer():
    payload = request.get_json() or {}
    need = ["name", "performance_shirts_per_hour", "cost_per_shirt"]
    missing = [k for k in need if k not in payload]
    if missing:
        return jsonify({"error": f"Missing: {', '.join(missing)}"}), 400
    row = current_app.db.create_printer(payload)
    return jsonify(row), 201