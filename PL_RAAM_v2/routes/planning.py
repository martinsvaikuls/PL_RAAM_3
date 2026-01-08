from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

bp = Blueprint("planning", __name__, url_prefix="/planning")

@bp.get("")
def list_plans():
    order = request.args.get("order")
    
    items = current_app.db.list_plans(order=order)
    return jsonify(items)



SPEC_WAGE_HR = 4
TAX = 1.21
MARKUP = 1.5

@bp.post("/run")
def run_planning():
    printers = current_app.db.list_printers()
    orders = current_app.db.list_orders(status="NEW")
    itemPrices = current_app.db.list_items()

    if not printers or not orders:
        return jsonify({"rows": [], "note": "No printers or no NEW orders"})

    rows = plan_edd(orders, printers, itemPrices)

    # Save the planning result to Google Sheets
    saved_rows = current_app.db.save_plan_rows(rows)
    return jsonify({"rows": saved_rows})

time_format = "%Y-%m-%dT%H:%M:%S"
def plan_edd(orders, printers, itemPrices):
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
                startTime = now
                finishTime = now + timedelta(hours=printerSpeed_hours)
            

                if finishTime.hour >= 18 or startTime.hour >= 18:
                    printerFinishDate = (now + timedelta(days=1)).replace(hour=8, minute=0, second=0) + timedelta(hours=printerSpeed_hours)                    
                    printer["available_form"] = (now + timedelta(days=1)).replace(hour=8, minute=0, second=0)
                elif finishTime.hour < 8 or startTime.hour < 8:
                    printerFinishDate = (now).replace(hour=8, minute=0, second=0) + timedelta(hours=printerSpeed_hours)
                    printer["available_form"] = now.replace(hour=8, minute=0, second=0)
                else:
                    printerFinishDate = finishTime
                    printer["available_form"] = now
                
                

                print("time", startTime)
                print("NextDay_time", printerFinishDate)

            else: 
                startTime = datetime.strptime(printer["available_from"],time_format)
                finishTime = datetime.strptime(printer["available_from"],time_format) + timedelta(hours=printerSpeed_hours)

                if finishTime.hour >= 18 or startTime.hour >= 18:
                    printerFinishDate = (datetime.strptime(printer["available_from"],time_format)+ timedelta(days=1)).replace(hour=8, minute=0, second=0) + timedelta(hours=printerSpeed_hours)
                    printer["available_form"] = (now + timedelta(days=1)).replace(hour=8, minute=0, second=0)
                elif finishTime.hour < 8 or startTime.hour < 8:
                    printerFinishDate = (datetime.strptime(printer["available_from"],time_format)).replace(hour=8, minute=0, second=0) + timedelta(hours=printerSpeed_hours)
                    printer["available_form"] = now.replace(hour=8, minute=0, second=0)

                else:
                    printerFinishDate = finishTime 
                
                print("time", startTime)
                print("NextDay_time", printerFinishDate)


            if fastestDelivery > printerFinishDate:
                fastestDelivery = printerFinishDate

                if isinstance(printer["available_from"], datetime):
                # If it's already a datetime object, no need to parse it again, just compare it
                    printer["available_from"] = printer["available_from"].isoformat(timespec="seconds")
                
                start_time = datetime.strptime(printer["available_from"], time_format)
                if start_time.hour >= 18 or start_time.hour >= 18:
                    start_time = (start_time+ timedelta(days=1)).replace(hour=8, minute=0, second=0)
                elif start_time.hour < 8 or start_time.hour < 8:
                    start_time = (start_time).replace(hour=8, minute=0, second=0)
                best_printer = printer
                
            
            #print(printerFinishDate)
            #print(printer)
        
        #print()
        for printer in printers:
            if printer["id"] == best_printer["id"]:
                printer["available_from"] = fastestDelivery.isoformat(timespec="seconds")
                best_printer = printer
                break
        

        for item in itemPrices:
            if item["product"] == order["product"] and item["size"] == order["shirt_size"]:
                product = item
                break

        averagePrinterSpeed = averagePrinterSpeed / printerCount
        hoursWorked = qty / averagePrinterSpeed
        materialCost = qty * float(product["cost_material"])
        materialCost = materialDiscount(materialCost)

        cost = round(hoursWorked * SPEC_WAGE_HR + materialCost,2)

        materialCost = qty * float(product["cost"]) 
        client_cost = round((hoursWorked * SPEC_WAGE_HR + materialCost) * TAX,2)
        
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

def materialDiscount(materialCost: float):
    if materialCost < 150:
        return materialCost
    elif materialCost < 300:
        return materialCost * 0.992
    elif materialCost < 500:
        return materialCost * 0.988
    elif materialCost < 1000:
        return materialCost * 0.984
    elif materialCost < 5000:
        return materialCost * 0.980
    elif materialCost >= 5000:
        return materialCost * 0.976
