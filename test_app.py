"""
test_app.py
───────────
Smoke tests for the Smart Warehouse Flask API.

pytest auto-discovers this file because its name starts with "test_".
Each function starting with "test_" is one test case.
We use Flask's built-in test_client() so we can call the API
*without* actually starting a real server.
"""

from app import app, warehouses
from warehouse_data import PRODUCTS


def make_client():
    """A Flask test client lets us send fake HTTP requests in-process."""
    return app.test_client()


def test_warehouses_endpoint_returns_all_50():
    client = make_client()
    resp = client.get("/api/warehouses")

    assert resp.status_code == 200          # request succeeded
    data = resp.get_json()
    assert len(data) == 50                  # we seed exactly 50 warehouses
    assert "inventory" in data[0]           # each one carries its stock


def test_products_endpoint_returns_catalogue():
    client = make_client()
    resp = client.get("/api/products")

    assert resp.status_code == 200
    assert resp.get_json() == PRODUCTS      # same catalogue the app loaded


def test_inventory_endpoint_has_status_fields():
    client = make_client()
    resp = client.get("/api/inventory")

    assert resp.status_code == 200
    body = resp.get_json()
    first_wh = body["warehouses"][0]
    # every SKU line should carry a computed availability status
    for sku_info in first_wh["products"].values():
        assert sku_info["status"] in {"ok", "low", "critical", "out"}


def test_fulfill_order_quote_does_not_mutate_stock():
    """A quote (confirm=False) must not change real inventory."""
    client = make_client()
    before = warehouses[0]["inventory"].copy()

    resp = client.post("/api/fulfill", json={
        "customer_lat": 40.7128,
        "customer_lon": -74.0060,
        "order_items": [{"sku": "SKU-A100", "qty": 5}],
        "confirm": False,
    })

    assert resp.status_code == 200
    assert warehouses[0]["inventory"] == before   # unchanged
