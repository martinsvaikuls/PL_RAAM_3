from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from routes.orders import bp as orders_bp
from routes.planning import bp as planning_bp
from routes.printers import bp as printers_bp
from routes.clients import bp as clients_bp
from routes.items import bp as items_bp

import json
import os

from sheets_DB import GoogleSheetsDB

current_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(current_dir, "credentials","google_ID.json")
SERVICE_ACCOUNT_FILE = os.path.join(current_dir, "credentials","client_cred.json")

# Try to load config, use placeholder for POC if not available
try:
    if os.path.exists(config_file):
        with open(config_file, 'r') as apiConfigFile:
            config = json.load(apiConfigFile)
            SPREADSHEET_ID = config.get("sheetID", "placeholder-sheet-id")
    else:
        SPREADSHEET_ID = "placeholder-sheet-id"
        print("Warning: google_ID.json not found. Using placeholder. Some features may not work.")
except (json.JSONDecodeError, KeyError) as e:
    SPREADSHEET_ID = "placeholder-sheet-id"
    print(f"Warning: Could not load config. Using placeholder. Error: {e}")


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", static_url_path="")
    CORS(app)  # Enable CORS for frontend

    # Try to initialize Google Sheets DB, fallback to in-memory for POC
    try:
        if os.path.exists(SERVICE_ACCOUNT_FILE) and SPREADSHEET_ID != "placeholder-sheet-id":
            app.db = GoogleSheetsDB(spreadsheet_id=SPREADSHEET_ID, service_account_file=SERVICE_ACCOUNT_FILE)
            print("[OK] Connected to Google Sheets database")
        else:
            raise FileNotFoundError("Credentials not available")
    except Exception as e:
        print(f"[WARNING] Could not connect to Google Sheets: {e}")
        print("[INFO] Using in-memory database for POC (data will be lost on restart)")
        from inmemory_db import InMemoryDB
        app.db = InMemoryDB()
    # Schema definition for Google Sheets (currently commented to reduce API calls)
    # Uncomment to auto-create sheets if they don't exist
    # required_sheets = {
    #     "clients": ["id", "client_name", "email", "hash_password"],
    #     "printers": ["id", "model", "base_speed", "available_from"],
    #     "orders": ["id", "client_id", "shirt_size", "base_color", "attachment", "quantity", "status", "created_at"],
    #     "fulfillment_plan": ["id", "order_id", "printer_id", "start_time", "end_time", "cost", "client_cost"],
    #     "meta": ["key", "value"]
    # }
    # app.db.check_and_create_sheets(required_sheets)

    @app.get("/health")
    def health():
        return jsonify({"ok": True})
    
    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    app.register_blueprint(printers_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(planning_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(items_bp)
    return app

app = create_app()

if __name__ == "__main__":
    # Only for local dev
    app.run(debug=True)

