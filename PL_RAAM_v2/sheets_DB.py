from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Any, Dict, List
import datetime as dt

# Helper function to get the current time in ISO format
def _now_iso() -> str:
    return dt.datetime.utcnow().isoformat(timespec="seconds")

class GoogleSheetsDB:
    def __init__(self, spreadsheet_id: str, service_account_file: str):
        self.SPREADSHEET_ID = spreadsheet_id
        self.SERVICE_ACCOUNT_FILE = service_account_file
        self.creds = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, 
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        self.service = build('sheets', 'v4', credentials=self.creds)

    def check_and_create_sheets(self, required_sheets):
        ### data table creation
        # clients
        # printers
        # orders
        # fulfillment_plan
        # Check if all required sheets exist, create them if they don't.
        # Get the current sheets in the spreadsheet
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.SPREADSHEET_ID).execute()
        existing_sheets = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
        
        for sheet_name, columns in required_sheets.items():
            if sheet_name not in existing_sheets:
                print(f"Sheet '{sheet_name}' does not exist. Creating it...")
                self.create_sheet(sheet_name, columns)
            else:
                print(f"Sheet '{sheet_name}' already exists.")

    def create_sheet(self, sheet_name, columns):
        #Create a new sheet in the spreadsheet.
        requests = [{
            'addSheet': {
                'properties': {
                    'title': sheet_name,
                    'gridProperties': {
                        'rowCount': 100,  # Default row count
                        'columnCount': len(columns)  # Column count based on headers
                    }
                }
            }
        }]
        
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.SPREADSHEET_ID, body={'requests': requests}).execute()
        print(f"Created sheet '{sheet_name}'")

        self.set_column_headers(sheet_name, columns)

    def set_column_headers(self, sheet_name, columns):
        """Set the column headers for a sheet."""
        range_name = f"{sheet_name}!A1:{chr(65+len(columns)-1)}1"  # A1, B1, C1, etc.
        values = [columns]  # Wrap column headers in a list
        body = {
            'values': values
        }

        self.service.spreadsheets().values().update(
            spreadsheetId=self.SPREADSHEET_ID, range=range_name, valueInputOption="RAW", body=body
        ).execute()
        print(f"Set column headers for sheet '{sheet_name}'")



    def get_sheet_data(self, sheet_name: str) -> List[Dict[str, Any]]:
        #Retrieve data from a specific sheet in the Google Sheet.
        range_name = f"{sheet_name}!A1:Z200"  # Change the range as per your needs
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID, range=range_name).execute()
        rows = result.get('values', [])
        
        # If rows are returned, convert to a list of dictionaries based on headers
        if rows:
            headers = rows[0]
            return [dict(zip(headers, row)) for row in rows[1:]]
        return []

    def get_all_data(self):
        #Get all data from a default range in the spreadsheet
        return self.get_sheet_data("Sheet1")  # Default to Sheet1, you can modify as needed

    def _write_sheet_data(self, sheet_name: str, data: List[Dict[str, Any]]) -> None:
        """Write data to a specific sheet."""
        range_name = f"{sheet_name}!A1"
        headers = list(data[0].keys()) if data else []
        values = [headers] + [list(item.values()) for item in data]

        body = {
            'values': values
        }

        # Write data to Google Sheets
        self.service.spreadsheets().values().update(
            spreadsheetId=self.SPREADSHEET_ID, range=range_name, valueInputOption="RAW", body=body).execute()

    def _append_to_sheet(self, sheet_name: str, data: List[Dict[str, Any]]) -> None:
        """Append new rows to a specific sheet."""
        range_name = f"{sheet_name}!A1"
        values = [list(item.values()) for item in data]

        body = {
            'values': values
        }

        # Append data to Google Sheets
        self.service.spreadsheets().values().append(
            spreadsheetId=self.SPREADSHEET_ID, range=range_name, valueInputOption="RAW", body=body).execute()

    def _next_id(self, table: str) -> int:
        """Get the next ID for a specific table by reading the 'meta' sheet."""
        meta_data = self.get_sheet_data("meta")
        key = f"next_id_{table}"
        meta_entry = next((entry for entry in meta_data if entry['key'] == key), None)
        
        if meta_entry is None:
            # Add the entry if it doesn't exist
            self._append_to_sheet("meta", [{"key": key, "value": 1}])
            return 1
       
        current_id = int(meta_entry["value"])
        # Increment the ID for the next usage
        self._write_sheet_data("meta", [{"key": key, "value": current_id + 1}])
        return current_id

    # PRINTERS
    def list_printers(self) -> List[Dict[str, Any]]:
        return self.get_sheet_data("printers")

    def create_printer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        new_id = self._next_id("printers")
        printer_data = {
            "id": new_id,
            "model": payload["model"],
            "base_speed": float(payload["base_speed"]),
            "available_from": payload.get("available_from") or _now_iso()
        }
        self._append_to_sheet("printers", [printer_data])
        return printer_data

    # ORDERS
    def list_orders(self, status: str | None = None) -> List[Dict[str, Any]]:
        orders = self.get_sheet_data("orders")
        if status:
            orders = [order for order in orders if order["status"] == status]
        return orders

    def create_order(self, payload: Dict[str, Any], client_id: int) -> Dict[str, Any]:
        new_id = self._next_id("orders")
        order_data = {
            "id": new_id,
            "client_id": client_id,
            "shirt_size": payload["shirt_size"],
            "base_color": payload["base_color"],
            "attachment": payload.get("attachment", ""),
            "quantity": int(payload["quantity"]),
            "status": payload.get("status", "NEW"),
            "created_at": _now_iso(),
        }
        self._append_to_sheet("orders", [order_data])
        return order_data

    # FULFILLMENT PLAN
    def save_plan_rows(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not rows:
            return []
        for row in rows:
            row["id"] = self._next_id("fulfillment_plan")
        self._append_to_sheet("fulfillment_plan", rows)
        return rows
