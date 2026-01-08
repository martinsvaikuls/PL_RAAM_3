from flask import Blueprint, request, jsonify, current_app
from auth import require_auth

bp = Blueprint("items", __name__, url_prefix="/items")

@bp.get("")
def list_items():
    
    items = current_app.db.list_items()
    return jsonify(items)
"""
@bp.get("/specific")
def get_items():
    #payload = request.get_json() or {}
    #if isinstance(payload, list):
    #    listPayload = payload
    #else:
    #    listPayload = [payload]

   
    #rows =[]
    #for item_payload in listPayload:
    #    product = item_payload.get("prodcut")
    #    size = item_payload.get("size")
    #    
    #    item = current_app.db.get_item(product=product,size=size)
    #
    #    rows.append(item)
    items = c
    return jsonify(rows)
"""
@bp.post("")
def create_item():
    payload = request.get_json() or {}
    if isinstance(payload, list):
        listPayload = payload
    else:
        listPayload = [payload]
    
    rows = []
    for item_payload in listPayload:
        need = ["product", "size", "cost", "cost_material"]
        missing = [k for k in need if k not in item_payload]
        if missing:
            return jsonify({"error": f"Missing: {', '.join(missing)}"}), 400
        
        # Create the order using your database function
        row = current_app.db.create_item(item_payload)
        rows.append(row)

    return jsonify(rows), 201