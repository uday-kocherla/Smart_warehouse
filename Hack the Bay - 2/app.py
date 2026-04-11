"""
app.py
──────
Flask API server for the Smart Warehouse Allocation Dashboard.
Serves the static frontend and exposes REST endpoints.
"""

import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from warehouse_data import generate_warehouse_data, PRODUCTS
from warehouse_manager import WarehouseManager

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

# ── Initialise warehouse data once ───────────────────────────────────────
warehouses = generate_warehouse_data(seed=42)
manager = WarehouseManager(warehouses=warehouses)


# ── Serve frontend pages ─────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/warehouses")
def warehouses_page():
    return send_from_directory("static", "warehouses.html")

@app.route("/inventory")
def inventory_page():
    return send_from_directory("static", "inventory.html")


# ── API routes ───────────────────────────────────────────────────────────

@app.route("/api/warehouses", methods=["GET"])
def get_warehouses():
    """Return all 50 warehouses with their inventory."""
    data = []
    for wh in warehouses:
        data.append({
            "id": wh["id"],
            "name": wh["name"],
            "city": wh["city"],
            "state": wh["state"],
            "lat": wh["lat"],
            "lon": wh["lon"],
            "max_capacity": wh["max_capacity"],
            "inventory": wh["inventory"],
        })
    return jsonify(data)


@app.route("/api/products", methods=["GET"])
def get_products():
    """Return the product catalogue."""
    return jsonify(PRODUCTS)


@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    """Return inventory matrix: each warehouse with stock levels + status."""
    data = []
    for wh in warehouses:
        wh_data = {
            "id": wh["id"],
            "name": wh["name"],
            "city": wh["city"],
            "state": wh["state"],
            "max_capacity": wh["max_capacity"],
            "products": {},
            "total_stock": 0,
        }
        for sku, qty in wh["inventory"].items():
            safety = int(qty * 0.10)
            available = max(qty - safety, 0)
            status = "ok"
            if qty == 0:
                status = "out"
            elif available < 20:
                status = "critical"
            elif available < 50:
                status = "low"

            wh_data["products"][sku] = {
                "on_hand": qty,
                "safety_reserve": safety,
                "available": available,
                "status": status,
            }
            wh_data["total_stock"] += qty
        data.append(wh_data)
    return jsonify({"warehouses": data, "products": PRODUCTS})

@app.route("/api/inventory/update", methods=["POST"])
def update_inventory():
    """Manually update physical stock level for a given warehouse and SKU."""
    global warehouses
    body = request.get_json(force=True)
    wh_id = body.get("warehouse_id")
    sku = body.get("sku")
    qty = int(body.get("qty", 0))

    for wh in warehouses:
        if wh["id"] == wh_id:
            if sku in wh["inventory"]:
                wh["inventory"][sku] = qty
            break

    return jsonify({"success": True})

import copy
from datetime import datetime

placed_orders = []

@app.route("/orders")
def orders_page():
    return send_from_directory("static", "orders.html")

@app.route("/api/orders", methods=["GET"])
def get_orders():
    return jsonify(placed_orders)

@app.route("/api/fulfill", methods=["POST"])
def fulfill_order():
    """Run the decision engine."""
    global warehouses, placed_orders
    body = request.get_json(force=True)
    customer_lat = float(body["customer_lat"])
    customer_lon = float(body["customer_lon"])
    order_items = body["order_items"]
    is_confirm = body.get("confirm", False)

    # Use deepcopy for a quote, otherwise mutate real memory state
    target_warehouses = warehouses if is_confirm else copy.deepcopy(warehouses)
    mgr = WarehouseManager(warehouses=target_warehouses)

    result = mgr.fulfill_order(
        customer_lat=customer_lat,
        customer_lon=customer_lon,
        order_items=order_items,
        verbose=False,
    )

    result.pop("decision_log", None)

    if is_confirm:
        # Save the placed order
        order_id = f"ORD-{len(placed_orders) + 1000}"
        record = {
            "order_id": order_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Processing",
            "details": result
        }
        placed_orders.append(record)
        return jsonify({"success": True, "order_id": order_id})

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
