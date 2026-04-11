"""
warehouse_manager.py — Order Allocation Logic + Decision Engine

Orchestrates all four sub-systems and returns a structured JSON decision
payload INCLUDING full decision transparency (ranked warehouses, inventory
checks with safety stock details, filtered warehouses, and reasons).
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from warehouse_data import PRODUCTS, generate_warehouse_data
from distance_calculator import DistanceCalculator
from inventory_auditor import InventoryAuditor
from shipping_service import ShippingService


class WarehouseManager:

    def __init__(
        self,
        warehouses: Optional[List[Dict]] = None,
        safety_stock_pct: float = 0.10,
        cost_weight: float = 0.6,
        time_weight: float = 0.4,
    ):
        self.warehouses = warehouses or generate_warehouse_data()
        self.calc     = DistanceCalculator(self.warehouses)
        self.auditor  = InventoryAuditor(safety_stock_pct)
        self.shipping = ShippingService(cost_weight, time_weight)
        self._product_weight = {p["sku"]: p["weight_lbs"] for p in PRODUCTS}

    def _total_weight(self, items: List[Dict]) -> float:
        return sum(
            item["qty"] * self._product_weight.get(item["sku"], 1.0)
            for item in items
        )

    @staticmethod
    def _wh_summary(wh: Dict, dist: float) -> Dict:
        return {
            "warehouse_id": wh["id"],
            "warehouse_name": wh["name"],
            "city": wh["city"],
            "state": wh["state"],
            "lat": wh["lat"],
            "lon": wh["lon"],
            "distance_miles": round(dist, 1),
        }

    def fulfill_order(
        self,
        customer_lat: float,
        customer_lon: float,
        order_items: List[Dict],
        verbose: bool = True,
    ) -> Dict:
        log: List[str] = []

        def _log(msg: str):
            log.append(msg)
            if verbose:
                print(msg)

        # ── Step 1: Geo-rank ─────────────────────────────────────────
        ranked = self.calc.rank_warehouses(customer_lat, customer_lon)

        # Build top-10 nearest warehouses for transparency
        nearest_warehouses = []
        for wh, dist in ranked[:10]:
            nearest_warehouses.append({
                **self._wh_summary(wh, dist),
                "rank": len(nearest_warehouses) + 1,
            })

        # ── Step 2: Inventory & safety stock check ───────────────────
        safety_pct = self.auditor.safety_stock_pct

        # For each of the top-10 nearest, do a detailed inventory check
        inventory_checks = []
        for wh, dist in ranked[:10]:
            snapshot = self.auditor.inventory_snapshot(wh, order_items)
            can_fulfill_all = self.auditor.can_fulfill_order(wh, order_items)

            inventory_checks.append({
                "warehouse_id": wh["id"],
                "warehouse_name": wh["name"],
                "distance_miles": round(dist, 1),
                "can_fulfill": can_fulfill_all,
                "items": snapshot,
            })

        eligible = self.auditor.filter_eligible(ranked, order_items)
        eligible_ids = [wh["id"] for wh, _ in eligible]

        # ── Step 3: Allocation ───────────────────────────────────────
        shipments: List[Dict] = []
        allocation_mode = "single"
        remaining_items: List[Dict] = []  # items we couldn't fulfill

        if eligible:
            best_wh, best_dist = eligible[0]
            ledger = self.auditor.deduct_inventory(best_wh, order_items)
            weight = self._total_weight(order_items)

            shipments.append({
                "warehouse": self._wh_summary(best_wh, best_dist),
                "items_allocated": [
                    {"sku": s, "qty_allocated": q} for s, q in ledger.items()
                ],
                "total_weight_lbs": round(weight, 2),
                "distance_miles": round(best_dist, 1),
            })
        else:
            allocation_mode = "split"
            remaining_items = [dict(i) for i in order_items]
            for wh, dist in ranked:
                if not remaining_items:
                    break

                fulfillable, shortfall = self.auditor.partial_availability(
                    wh, remaining_items,
                )

                if fulfillable:
                    ledger = self.auditor.deduct_inventory(wh, fulfillable)
                    weight = self._total_weight(fulfillable)

                    shipments.append({
                        "warehouse": self._wh_summary(wh, dist),
                        "items_allocated": [
                            {"sku": s, "qty_allocated": q}
                            for s, q in ledger.items()
                        ],
                        "total_weight_lbs": round(weight, 2),
                        "distance_miles": round(dist, 1),
                        "is_distant": dist > 500,
                    })

                    remaining_items = shortfall

        # ── Step 4: Shipping quotes ──────────────────────────────────
        total_cost = 0.0
        max_days   = 0

        for ship in shipments:
            dist   = ship["distance_miles"]
            weight = ship["total_weight_lbs"]
            best   = self.shipping.best_quote(dist, weight)
            all_q  = self.shipping.compare_quotes(dist, weight)

            ship["chosen_carrier"] = best.to_dict()
            ship["all_carrier_quotes"] = all_q
            total_cost += best.cost
            max_days = max(max_days, best.delivery_days)

        est_delivery = (datetime.utcnow() + timedelta(days=max_days)).strftime(
            "%Y-%m-%d"
        )

        # ── Build full decision response ─────────────────────────────
        decision = {
            "order_summary": {
                "customer_location": {"lat": customer_lat, "lon": customer_lon},
                "items_requested": order_items,
                "total_shipments": len(shipments),
            },

            # NEW: Full decision transparency
            "decision_steps": {
                "step1_geo_ranking": {
                    "title": "Geo-Optimization",
                    "description": "Ranked all 50 warehouses by distance to customer",
                    "nearest_warehouses": nearest_warehouses,
                },
                "step2_inventory_check": {
                    "title": "Inventory & Safety Stock Validation",
                    "description": f"Checked stock levels with {safety_pct:.0%} safety reserve threshold",
                    "safety_stock_threshold": f"{safety_pct:.0%}",
                    "total_checked": len(inventory_checks),
                    "total_eligible": len(eligible),
                    "total_filtered_out": len(inventory_checks) - len(eligible_ids),
                    "warehouse_checks": inventory_checks,
                },
                "step3_allocation": {
                    "title": "Order Allocation",
                    "mode": allocation_mode,
                    "description": (
                        f"Fulfilled from single closest eligible warehouse"
                        if allocation_mode == "single"
                        else "No single warehouse had full stock — split across multiple"
                    ),
                },
                "step4_shipping": {
                    "title": "Carrier Optimization",
                    "description": "Compared FedEx & UPS rates for optimal cost/speed",
                },
            },

            "shipments": shipments,
            "metrics": {
                "total_shipping_cost_usd": round(total_cost, 2),
                "estimated_delivery_window": f"{max_days} business day(s)",
                "estimated_arrival_date": est_delivery,
            },
            "unfulfilled_items": remaining_items,
            "partial_fulfillment": len(remaining_items) > 0,
            "inventory_update": [
                {
                    "warehouse_id": s["warehouse"]["warehouse_id"],
                    "items_deducted": s["items_allocated"],
                }
                for s in shipments
            ],
            "decision_log": log,
        }

        return decision
