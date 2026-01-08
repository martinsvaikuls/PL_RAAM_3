import pytest
import time
from unittest.mock import MagicMock
from datetime import datetime, timedelta

# Importējam funkciju no jūsu faila
# Pieņemot, ka fails atrodas tajā pašā direktorijā vai ir pieejams ceļā
from PL_RAAM_v2.routes.planning import plan_edd

@pytest.fixture
def test_mock_flask_app(monkeypatch):
    """Izveido mākslīgu Flask kontekstu un DB, lai algoritms neizsauktu reālu API."""
    mock_app = MagicMock()
    mock_db = MagicMock()
    mock_app.db = mock_db
    
    # Aizstājam current_app ar mūsu mock objektu
    monkeypatch.setattr("PL_RAAM_v2.routes.planning.current_app", mock_app)
    return mock_app

def generate_test_data(num_orders, num_printers):
    """Ģenerē sintētiskus datus veiktspējas testam."""
    printers = []
    for i in range(num_printers):
        printers.append({
            "id": i + 1,
            "model": f"Printer {i+1}",
            "base_speed": 10.0 + i, # Dažādi ātrumi
            "available_from": datetime.now().isoformat(timespec="seconds")
        })

    orders = []
    for i in range(num_orders):
        orders.append({
            "id": i + 1,
            "quantity": 50,
            "shirt_size": "m",
            "base_color": "white",
            "created_at": (datetime.now() + timedelta(minutes=i)).isoformat()
        })
    
    return orders, printers

@pytest.mark.parametrize("order_count, printer_count", [
    (10, 2),    # Mazs apjoms
    (100, 5),   # Vidējs apjoms
    (1000, 10)  # Liels apjoms (veiktspējas pārbaude)
])
def test_plan_edd_performance(test_mock_flask_app, order_count, printer_count):
    orders, printers = generate_test_data(order_count, printer_count)
    
    start_bench = time.time()
    results = plan_edd(orders, printers)
    duration = time.time() - start_bench

    # 1. Aprēķinām vidējo gaidīšanas laiku (W)
    waiting_times = []
    for order, res in zip(orders, results):
        created = datetime.fromisoformat(order["created_at"])
        started = datetime.fromisoformat(res["start_time"])
        waiting_times.append((started - created).total_seconds() / 60) # minūtēs
    
    avg_waiting = sum(waiting_times) / len(waiting_times)

    # 2. Aprēķinām noslodzi (rho)
    # Summējam visu printeru darba laiku sekundēs
    total_work_time = 0
    first_start = datetime.max
    last_end = datetime.min
    
    for res in results:
        start = datetime.fromisoformat(res["start_time"])
        end = datetime.fromisoformat(res["end_time"])
        total_work_time += (end - start).total_seconds()
        first_start = min(first_start, start)
        last_end = max(last_end, end)
    
    total_available_time = (last_end - first_start).total_seconds() * printer_count
    utilization = (total_work_time / total_available_time) * 100 if total_available_time > 0 else 0

    print(f"\n[Novērtējums] N:{order_count}, M:{printer_count}")
    print(f" -> Algoritma ātrums (Tr): {duration:.4f}s")
    print(f" -> Vid. gaidīšanas laiks (W): {avg_waiting:.2f} min")
    print(f" -> Iekārtu noslodze (rho): {utilization:.2f}%")
    