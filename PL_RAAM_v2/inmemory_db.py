"""
In-memory database fallback for POC when Google Sheets credentials are not available.
Data is stored in memory and will be lost on server restart.
"""
from typing import Any, Dict, List, Optional
import datetime as dt

def _now_iso() -> str:
    return dt.datetime.utcnow().isoformat(timespec="seconds")

class InMemoryDB:
    """Simple in-memory database that mimics GoogleSheetsDB interface"""
    
    def __init__(self):
        self.data = {
            "clients": [],
            "printers": [],
            "orders": [],
            "fulfillment_plan": [],
            "meta": [
                {"key": "next_id_clients", "value": "1"},
                {"key": "next_id_printers", "value": "1"},
                {"key": "next_id_orders", "value": "1"},
                {"key": "next_id_fulfillment_plan", "value": "1"},
            ]
        }
        print("[INFO] In-memory database initialized")
    
    def _next_id(self, table: str) -> int:
        """Get the next ID for a specific table"""
        key = f"next_id_{table}"
        meta_entry = next((entry for entry in self.data["meta"] if entry['key'] == key), None)
        
        if meta_entry is None:
            self.data["meta"].append({"key": key, "value": "1"})
            return 1
        
        current_id = int(meta_entry["value"])
        meta_entry["value"] = str(current_id + 1)
        return current_id
    
    def get_sheet_data(self, sheet_name: str) -> List[Dict[str, Any]]:
        """Get all data from a sheet"""
        return self.data.get(sheet_name, [])
    
    # CLIENTS
    def list_clients(self) -> List[Dict[str, Any]]:
        return self.data["clients"]
    
    def get_client_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        clients = self.list_clients()
        return next((client for client in clients if client.get("email") == email), None)
    
    def create_client(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        new_id = self._next_id("clients")
        client_data = {
            "id": new_id,
            "client_name": payload["client_name"],
            "email": payload["email"],
            "hash_password": payload["hash_password"]
        }
        self.data["clients"].append(client_data)
        return client_data
    
    # PRINTERS
    def list_printers(self) -> List[Dict[str, Any]]:
        return self.data["printers"]
    
    def create_printer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        new_id = self._next_id("printers")
        printer_data = {
            "id": new_id,
            "model": payload["model"],
            "base_speed": float(payload["base_speed"]),
            "available_from": payload.get("available_from") or _now_iso()
        }
        self.data["printers"].append(printer_data)
        return printer_data
    
    # ORDERS
    def list_orders(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        orders = self.data["orders"]
        if status:
            orders = [order for order in orders if order["status"] == status]
        return orders
    
    def create_order(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        new_id = self._next_id("orders")
        order_data = {
            "id": new_id,
            "client_id": payload["client_id"],
            "shirt_size": payload["shirt_size"],
            "base_color": payload["base_color"],
            "attachment": payload.get("attachment", ""),
            "quantity": int(payload["quantity"]),
            "status": payload.get("status", "NEW"),
            "created_at": _now_iso(),
        }
        self.data["orders"].append(order_data)
        return order_data
    
    def update_objects(self, sheet_name: str, updates: List[Dict[str, Any]]) -> bool:
        """Update multiple objects by their IDs"""
        if sheet_name not in self.data:
            return False
        
        id_dict = {item['id']: item for item in self.data[sheet_name]}
        
        for update in updates:
            obj_id = update.get("id")
            if obj_id in id_dict:
                obj = id_dict[obj_id]
                for key, value in update.items():
                    if key != "id" and key in obj:
                        obj[key] = value
                id_dict[obj_id] = obj
        
        self.data[sheet_name] = list(id_dict.values())
        return True
    
    # FULFILLMENT PLAN
    def save_plan_rows(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not rows:
            return []
        for row in rows:
            row["id"] = self._next_id("fulfillment_plan")
        self.data["fulfillment_plan"].extend(rows)
        return rows

