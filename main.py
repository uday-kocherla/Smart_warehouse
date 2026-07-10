"""
main.py
───────
Test-case runner for the Smart Warehouse Allocation System.

Simulates a customer order from New York City (40.7128, -74.0060) for
3 products and prints the full step-by-step decision-making process,
then exports the final JSON payload.
"""

import json

from warehouse_data import generate_warehouse_data, export_warehouses_csv, PRODUCTS
from warehouse_manager import WarehouseManager


def main():
    # ── 1. Generate & export warehouse data ──────────────────────────────
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║     SMART WAREHOUSE ALLOCATION & SHIPPING OPTIMIZATION         ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")

    warehouses = generate_warehouse_data(seed=42)
    export_warehouses_csv(warehouses, "warehouses.csv")

    print(f"\nProduct catalogue ({len(PRODUCTS)} items):")
    for p in PRODUCTS:
        print(f"  • {p['sku']}  {p['name']:<38s}  {p['weight_lbs']:.1f} lbs")

    # ── 2. Customer order ────────────────────────────────────────────────
    customer_lat = 40.7128     # New York City
    customer_lon = -74.0060

    order_items = [
        {"sku": "SKU-A100", "qty": 15},   # Wireless Bluetooth Headphones
        {"sku": "SKU-C300", "qty": 8},     # Smart Home Security Camera
        {"sku": "SKU-E500", "qty": 5},     # USB-C Docking Station
    ]

    print(f"\n{'─' * 60}")
    print(f"Customer location  : New York City ({customer_lat}, {customer_lon})")
    print(f"Order line items   : {len(order_items)}")
    for item in order_items:
        print(f"  → {item['sku']}  ×{item['qty']}")
    print(f"{'─' * 60}\n")

    # ── 3. Run the decision engine ───────────────────────────────────────
    manager = WarehouseManager(warehouses=warehouses)
    decision = manager.fulfill_order(
        customer_lat=customer_lat,
        customer_lon=customer_lon,
        order_items=order_items,
        verbose=True,
    )

    # ── 4. Export JSON ───────────────────────────────────────────────────
    # Remove the verbose log from the JSON file for cleanliness
    export_payload = {k: v for k, v in decision.items() if k != "decision_log"}

    output_path = "decision_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_payload, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Full decision JSON exported → {output_path}")


    # ── 5. Bonus: run a second scenario — split-order ────────────────────
    print("\n\n")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║     SCENARIO 2 — High-demand order to trigger SPLIT logic      ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")

    large_order = [
        {"sku": "SKU-A100", "qty": 400},  # very large quantity
        {"sku": "SKU-B200", "qty": 350},
        {"sku": "SKU-D400", "qty": 300},
    ]
    customer_lat_2 = 34.0522   # Los Angeles
    customer_lon_2 = -118.2437

    print(f"Customer location  : Los Angeles ({customer_lat_2}, {customer_lon_2})")
    print(f"Order line items   : {len(large_order)}")
    for item in large_order:
        print(f"  → {item['sku']}  ×{item['qty']}")
    print(f"{'─' * 60}\n")

    decision2 = manager.fulfill_order(
        customer_lat=customer_lat_2,
        customer_lon=customer_lon_2,
        order_items=large_order,
        verbose=True,
    )

    output_path2 = "decision_output_split.json"
    export_payload2 = {k: v for k, v in decision2.items() if k != "decision_log"}
    with open(output_path2, "w", encoding="utf-8") as f:
        json.dump(export_payload2, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Split-order decision JSON → {output_path2}")


if __name__ == "__main__":
    main()
