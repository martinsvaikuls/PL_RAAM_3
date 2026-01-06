from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

bp = Blueprint("planning", __name__, url_prefix="/planning")

tShirt_sizesCostAndTimeMult = {
    "s": 1,
    "m": 1.2,
    "l": 1.3
}

attachmentColour_on_tshirtColour_TimeMult = {
    "darkOnLight": 1,
    "lightOnDark": 1.75,
}

SPEC_WAGE_HR = 4
TAX = 1.21
MARKUP = 1.5

@bp.post("/run")
def run_planning():
    printers = current_app.db.list_printers()
    orders = current_app.db.list_orders(status="NEW")

    if not printers or not orders:
        return jsonify({"rows": [], "note": "No printers or no NEW orders"})

    rows = plan_edd(orders, printers)


    # Save the planning result to Google Sheets
    saved_rows = current_app.db.save_plan_rows(rows)
    return jsonify({"rows": saved_rows})

time_format = "%Y-%m-%dT%H:%M:%S"
def plan_edd(orders, printers):
    rows = []
    printersToUpdate = []
    completedOrders = []
    now = datetime.now()
    orders = sorted(orders, key=lambda o: o["created_at"])

    

    for order in orders:
        qty = int(order["quantity"])
        #best_printer = max(printers, key=lambda p: float(p["base_speed"]))
        fastestDelivery =  datetime.max
        averagePrinterSpeed = 0
        printerCount = 0
        start_time = datetime.now()
        for printer in printers:
            averagePrinterSpeed = float(printer["base_speed"])
            printerCount = printerCount + 1
            printerFinishDate = datetime.now()
            printerSpeed_hours = qty / float(printer["base_speed"])
            if isinstance(printer["available_from"], datetime):
                # If it's already a datetime object, no need to parse it again, just compare it
                printer["available_from"] = printer["available_from"].isoformat(timespec="seconds")
            

            if datetime.strptime(printer["available_from"],time_format) < datetime.now():
                printerFinishDate = now + timedelta(hours=printerSpeed_hours)
                printer["available_from"] = now
            else: 
                printerFinishDate = datetime.strptime(printer["available_from"],time_format) + timedelta(hours=printerSpeed_hours)

            if fastestDelivery > printerFinishDate:
                fastestDelivery = printerFinishDate
                if isinstance(printer["available_from"], datetime):
                # If it's already a datetime object, no need to parse it again, just compare it
                    printer["available_from"] = printer["available_from"].isoformat(timespec="seconds")
                start_time = datetime.strptime(printer["available_from"],time_format)
                best_printer = printer
                
            
            #print(printerFinishDate)
            #print(printer)
        
        #print()
        for printer in printers:
            if printer["id"] == best_printer["id"]:
                printer["available_from"] = fastestDelivery.isoformat(timespec="seconds")
                best_printer = printer
                break
        
        averagePrinterSpeed = averagePrinterSpeed / printerCount
        hoursWorked = qty / averagePrinterSpeed
        materialCost = qty * tShirt_sizesCostAndTimeMult[str(order["shirt_size"])]
        cost = round(hoursWorked * SPEC_WAGE_HR + materialCost,2)
        client_cost = round(cost * MARKUP * TAX,2)
        
        rows.append({
            "id": "",
            "order_id": int(order["id"]),
            "printer_id": int(best_printer["id"]),
            "start_time": start_time.isoformat(timespec="seconds"),
            "end_time": fastestDelivery.isoformat(timespec="seconds"),
            "cost":  cost,
            "client_cost": client_cost,
        })
        
        appended = False
        for printerToUpdate in printersToUpdate:
            if printerToUpdate["id"] == best_printer["id"]:
                printersToUpdate.remove(printerToUpdate)
                printersToUpdate.append(best_printer)
                appended = True
                break
        #print(best_printer)
        if not appended:
            printersToUpdate.append(best_printer)

        order["status"] = "PLANNED"
        completedOrders.append(order)

    
    #print(printersToUpdate)
    current_app.db.update_objects("printers", printersToUpdate)
    current_app.db.update_objects("orders", orders)

    return rows
