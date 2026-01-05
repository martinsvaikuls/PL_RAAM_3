from flask import Flask, jsonify
from routes.orders import bp as orders_bp
from routes.planning import bp as planning_bp
from routes.printers import bp as printers_bp

from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
import os

from sheets_DB import GoogleSheetsDB

current_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(current_dir, r'credentials\google_ID.json'), 'r') as apiConfigFile:
    config = json.load(apiConfigFile)

SPREADSHEET_ID = config["sheetID"]
apiConfigFile.close()


SERVICE_ACCOUNT_FILE = os.path.join(current_dir, r'credentials\client_cred.json')


def create_app() -> Flask:
    app = Flask(__name__)

    app.db = GoogleSheetsDB(spreadsheet_id=SPREADSHEET_ID, service_account_file=SERVICE_ACCOUNT_FILE)
    required_sheets = {
        "clients": ["id", "client_name", "email", "hash_password"],
        "printers": ["id", "model", "base_speed", "available_from"],
        "orders": ["id", "client_id", "shirt_size", "base_color", "attachment", "quantity", "status", "created_at"],
        "fulfillment_plan": ["id", "order_id", "printer_id", "start_time", "end_time", "cost", "client_cost"],
        "meta": ["key", "value"]
    }
    ####################### so less requests are made
    #app.db.check_and_create_sheets(required_sheets)

    @app.get("/health")
    def health():
        return jsonify({"ok": True})
    


    app.register_blueprint(printers_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(planning_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
