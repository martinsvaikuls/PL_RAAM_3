import os
import threading
import datetime as dt
from typing import Any, Dict, List

from zipfile import BadZipFile
import pandas as pd

# ====== EXCEL FAILA CEĻŠ (pēc noklusējuma uz proj lab.xlsx projekta saknē) ======
_default_xlsx = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "proj lab.xlsx"))
XLSX_PATH = os.environ.get("XLSX_PATH", _default_xlsx)

SHEETS = [
    "clients",
    "printers",
    "orders",
    "fulfillment_plan",
    "delivery",
    "feedback",
    "meta",
]


def _now_iso() -> str:
    return dt.datetime.utcnow().isoformat(timespec="seconds")


def _ensure_dir_for(path: str) -> None:
    """Droši izveido mapi, ja tā ir norādīta ceļā."""
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


class ExcelDB:
    """
    Excel datu slānis:
    - nolasa/raksta lapas ar pandas (openpyxl engine)
    - auto-increment caur 'meta' lapu
    - rakstīšanas brīdī lieto procesa līmeņa Lock
    - prot atgūties, ja XLSX ir bojāts (BadZipFile / u.c. gadījumi)
    """
    _lock = threading.Lock()

    def __init__(self, path: str = XLSX_PATH):
        self.path = path
        if not os.path.exists(self.path):
            self._init_empty()
        else:
            self._ensure_sheets()

    # ---------- palīgmetodes ----------
    def _init_empty(self) -> None:
        _ensure_dir_for(self.path)
        data = {
            "clients": pd.DataFrame(columns=["id", "user_name", "email", "password_hash", "created_at"]),
            "printers": pd.DataFrame(columns=[
                "id", "name", "performance_shirts_per_hour", "cost_per_shirt", "available_from", "is_active"
            ]),
            "orders": pd.DataFrame(columns=[
                "id", "client_id", "shirt_size", "base_color", "custom_image_url",
                "quantity", "deadline", "status", "created_at"
            ]),
            "fulfillment_plan": pd.DataFrame(columns=[
                "id", "order_id", "printer_id", "start_time", "end_time", "qty", "total_cost"
            ]),
            "delivery": pd.DataFrame(columns=["id", "order_id", "delivery_date", "is_delivered", "method"]),
            "feedback": pd.DataFrame(columns=["id", "order_id", "client_id", "rating", "comment", "created_at"]),
            "meta": pd.DataFrame(
                [["next_id_clients", "1"],
                 ["next_id_printers", "1"],
                 ["next_id_orders", "1"],
                 ["next_id_fulfillment_plan", "1"],
                 ["next_id_delivery", "1"],
                 ["next_id_feedback", "1"]],
                columns=["key", "value"]
            ),
        }
        with pd.ExcelWriter(self.path, engine="openpyxl", mode="w") as w:
            for name, df in data.items():
                df.to_excel(w, sheet_name=name, index=False)

    def _read_all(self) -> Dict[str, pd.DataFrame]:
        """Nolasa visas lapas; bojāta/nelasāma XLSX gadījumā reinitializē tukšu struktūru."""
        try:
            return pd.read_excel(self.path, sheet_name=None, engine="openpyxl")
        except (FileNotFoundError, BadZipFile, KeyError, ValueError):
            # Atjaunojam tukšu, ja fails bojāts vai neeksistē
            self._init_empty()
            return pd.read_excel(self.path, sheet_name=None, engine="openpyxl")

    def _write_all(self, book: Dict[str, pd.DataFrame]) -> None:
        """Droša saglabāšana: sagatavo DF, izveido mapi, atkārto, ja fails īslaicīgi bloķēts."""
        import time
        _ensure_dir_for(self.path)

        # normalizējam datu struktūru
        safe_book: Dict[str, pd.DataFrame] = {}
        for name in SHEETS:
            df = book.get(name)
            if df is None or not isinstance(df, pd.DataFrame):
                df = pd.DataFrame()
            safe_book[name] = df

        last_err = None
        for _ in range(10):  # līdz ~5 sek. kopā (10 * 0.5s)
            try:
                with pd.ExcelWriter(self.path, engine="openpyxl", mode="w") as w:
                    for name, df in safe_book.items():
                        df.to_excel(w, sheet_name=name, index=False)
                return
            except PermissionError as e:
                last_err = e
                time.sleep(0.5)  # iespējams, Excel/OneDrive īslaicīgi tur vaļā
        if last_err:
            raise last_err
        raise RuntimeError("Failed to write Excel workbook")

    def _ensure_sheets(self) -> None:
        """Pārliecinās, ka visas nepieciešamās lapas eksistē; ja nav – izveido un saglabā."""
        with self._lock:
            book = self._read_all()
            changed = False
            for s in SHEETS:
                if s not in book or not isinstance(book[s], pd.DataFrame):
                    book[s] = pd.DataFrame()
                    changed = True
            if "meta" not in book or book["meta"].empty:
                book["meta"] = pd.DataFrame(
                    [["next_id_clients", "1"],
                     ["next_id_printers", "1"],
                     ["next_id_orders", "1"],
                     ["next_id_fulfillment_plan", "1"],
                     ["next_id_delivery", "1"],
                     ["next_id_feedback", "1"]],
                    columns=["key", "value"]
                )
                changed = True
            if changed:
                self._write_all(book)

    def _next_id(self, book: Dict[str, pd.DataFrame], table: str) -> int:
        meta = book["meta"]
        key = f"next_id_{table}"
        if meta.empty or key not in meta["key"].values:
            meta = pd.concat([meta, pd.DataFrame([[key, "1"]], columns=["key", "value"])], ignore_index=True)
        val = int(meta.loc[meta["key"] == key, "value"].iloc[0])
        meta.loc[meta["key"] == key, "value"] = str(val + 1)
        book["meta"] = meta
        return val

    # ---------- publiskās metodes ----------
    # PRINTERI
    def list_printers(self) -> List[Dict[str, Any]]:
        with self._lock:
            df = self._read_all().get("printers", pd.DataFrame())
            if df.empty:
                return []
            return df.fillna("").to_dict(orient="records")

    def create_printer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            book = self._read_all()
            df = book.get("printers", pd.DataFrame(columns=[
                "id", "name", "performance_shirts_per_hour", "cost_per_shirt", "available_from", "is_active"
            ]))
            new_id = self._next_id(book, "printers")
            row = {
                "id": new_id,
                "name": payload["name"],
                "performance_shirts_per_hour": float(payload["performance_shirts_per_hour"]),
                "cost_per_shirt": float(payload["cost_per_shirt"]),
                "available_from": payload.get("available_from") or _now_iso(),
                "is_active": int(payload.get("is_active", 1)),
            }
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            book["printers"] = df
            self._write_all(book)
            return row

    # PASŪTĪJUMI
    def list_orders(self, status: str | None = None) -> List[Dict[str, Any]]:
        with self._lock:
            df = self._read_all().get("orders", pd.DataFrame())
            if df.empty:
                return []
            if status:
                df = df[df["status"] == status]
            return df.fillna("").to_dict(orient="records")

    def create_order(self, payload: Dict[str, Any], client_id: int) -> Dict[str, Any]:
        with self._lock:
            book = self._read_all()
            df = book.get("orders", pd.DataFrame(columns=[
                "id", "client_id", "shirt_size", "base_color", "custom_image_url",
                "quantity", "deadline", "status", "created_at"
            ]))
            new_id = self._next_id(book, "orders")
            row = {
                "id": new_id,
                "client_id": int(client_id),
                "shirt_size": payload["shirt_size"],
                "base_color": payload["base_color"],
                "custom_image_url": payload.get("custom_image_url", ""),
                "quantity": int(payload["quantity"]),
                "deadline": payload["deadline"],  # ISO string: YYYY-MM-DDTHH:MM:SS
                "status": payload.get("status", "NEW"),
                "created_at": _now_iso(),
            }
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            book["orders"] = df
            self._write_all(book)
            return row

    # PLĀNS
    def save_plan_rows(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Saglabā plāna rindas un atjauno pasūtījumu statusu uz PLANNED."""
        if not rows:
            return []
        with self._lock:
            book = self._read_all()
            plan = book.get("fulfillment_plan", pd.DataFrame(columns=[
                "id", "order_id", "printer_id", "start_time", "end_time", "qty", "total_cost"
            ]))
            orders = book.get("orders", pd.DataFrame())

            new_rows = []
            for r in rows:
                r = r.copy()
                r["id"] = self._next_id(book, "fulfillment_plan")
                new_rows.append(r)
                if not orders.empty:
                    orders.loc[orders["id"] == r["order_id"], "status"] = "PLANNED"

            plan = pd.concat([plan, pd.DataFrame(new_rows)], ignore_index=True)
            book["fulfillment_plan"] = plan
            book["orders"] = orders
            self._write_all(book)
            return new_rows
