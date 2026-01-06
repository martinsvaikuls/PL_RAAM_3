from flask import Blueprint, request, jsonify, current_app

bp = Blueprint("clients", __name__, url_prefix="/clients")

@bp.get("")
def list_clients():
  pass
  return jsonify(orders)

@bp.post("")
def create_clients():
  pass
  return jsonify(rows), 201

