from flask import Flask, jsonify
from excel_db import ExcelDB
from routes.orders import bp as orders_bp
from routes.planning import bp as planning_bp
from routes.printers import bp as printers_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.db = ExcelDB(path=r"..\projlab\proj lab.xlsx")
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
