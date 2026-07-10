"""
inventory_auditor.py
────────────────────
Inventory & Safety Stock Controller  (Module 2)

Validates that warehouses can fulfill requested products/quantities
while respecting a configurable safety-stock threshold (default 10 %).
"""

from typing import Dict, List, Tuple, Optional


class InventoryAuditor:
    """
    Checks warehouse inventory against an incoming order and filters out
    warehouses that cannot satisfy the request without breaching safety stock.

    Parameters
    ----------
    safety_stock_pct : float
        Fraction of current stock that must remain after allocation.
        For example, 0.10 means 10 % of the *current* on-hand stock
        is reserved as safety buffer.
    """

    def __init__(self, safety_stock_pct: float = 0.10):
        if not 0 <= safety_stock_pct < 1:
            raise ValueError("safety_stock_pct must be in [0, 1)")
        self.safety_stock_pct = safety_stock_pct

    # ── helpers ──────────────────────────────────────────────────────────

    def _available_qty(self, on_hand: int) -> int:
        """Units that can be allocated (above safety stock)."""
        reserved = int(on_hand * self.safety_stock_pct)
        return max(on_hand - reserved, 0)

    def can_fulfill_item(self, warehouse: Dict, sku: str, qty: int) -> bool:
        """True if *warehouse* can fully satisfy *qty* of *sku*."""
        on_hand = warehouse["inventory"].get(sku, 0)
        return self._available_qty(on_hand) >= qty

    def can_fulfill_order(self, warehouse: Dict,
                          order_items: List[Dict]) -> bool:
        """
        True if *warehouse* can satisfy **every** item in the order.

        order_items : list of {"sku": str, "qty": int}
        """
        return all(
            self.can_fulfill_item(warehouse, item["sku"], item["qty"])
            for item in order_items
        )

    # ── main filter ──────────────────────────────────────────────────────

    def filter_eligible(
        self,
        warehouses_ranked: List[Tuple[Dict, float]],
        order_items: List[Dict],
    ) -> List[Tuple[Dict, float]]:
        """
        From a distance-ranked warehouse list, keep only those that can
        fully satisfy the order without breaching safety stock.

        Parameters
        ----------
        warehouses_ranked : list of (warehouse_dict, distance_miles)
        order_items       : list of {"sku": str, "qty": int}

        Returns
        -------
        Filtered list in the same (warehouse, dist) format, preserving
        distance order.
        """
        return [
            (wh, dist) for wh, dist in warehouses_ranked
            if self.can_fulfill_order(wh, order_items)
        ]

    def partial_availability(
        self,
        warehouse: Dict,
        order_items: List[Dict],
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Split an order into (fulfillable, unfulfillable) parts
        for a single warehouse.

        Returns
        -------
        (fulfillable, shortfall)
            Each is a list of {"sku", "qty"} dicts.
        """
        fulfillable, shortfall = [], []
        for item in order_items:
            avail = self._available_qty(
                warehouse["inventory"].get(item["sku"], 0)
            )
            if avail >= item["qty"]:
                fulfillable.append(item)
            elif avail > 0:
                fulfillable.append({"sku": item["sku"], "qty": avail})
                shortfall.append({
                    "sku": item["sku"],
                    "qty": item["qty"] - avail,
                })
            else:
                shortfall.append(item)
        return fulfillable, shortfall

    def deduct_inventory(self, warehouse: Dict,
                         items: List[Dict]) -> Dict[str, int]:
        """
        Subtract allocated quantities from the warehouse's inventory
        and return a ledger of what was deducted.

        Parameters
        ----------
        warehouse  : warehouse dict (mutated in place)
        items      : list of {"sku": str, "qty": int}

        Returns
        -------
        dict  {sku: qty_deducted}
        """
        ledger: Dict[str, int] = {}
        for item in items:
            sku, qty = item["sku"], item["qty"]
            if warehouse["inventory"].get(sku, 0) < qty:
                raise ValueError(
                    f"Cannot deduct {qty} of {sku} from {warehouse['id']}; "
                    f"only {warehouse['inventory'].get(sku, 0)} on hand."
                )
            warehouse["inventory"][sku] -= qty
            ledger[sku] = qty
        return ledger

    # ── diagnostics ──────────────────────────────────────────────────────

    def inventory_snapshot(self, warehouse: Dict,
                           order_items: List[Dict]) -> List[Dict]:
        """Return a readable snapshot of stock vs. request for one warehouse."""
        rows = []
        for item in order_items:
            sku, requested = item["sku"], item["qty"]
            on_hand = warehouse["inventory"].get(sku, 0)
            avail   = self._available_qty(on_hand)
            rows.append({
                "sku": sku,
                "on_hand": on_hand,
                "safety_reserve": on_hand - avail,
                "available": avail,
                "requested": requested,
                "can_fulfill": avail >= requested,
            })
        return rows
