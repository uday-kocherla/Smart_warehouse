# SmartWarehouse: 3-Minute Technical Video Showcase Script

**Target Length:** ~3:00  
**Pacing:** Confident, professional, and dense with technical architecture references.

---

### [0:00 - 0:30] Introduction & Technical Stack
**[Visuals]** 
*Start with a wide shot of the clean "SmartWarehouse" dashboard. Briefly jump to your IDE or the "Warehouses" tab to show the raw data scale.*

**[Voiceover]**
"Welcome to SmartWarehouse. This is a high-performance Allocation and Shipping Optimization system engineered entirely via a modular Python backend and a lightweight Vanilla JavaScript Single Page Application.

The framework runs on a Flask REST API server. It currently maintains an in-memory data store of 50 seeded warehouse dictionaries spanning the entire US coordinate grid, tracking unique capacities and real-time product arrays without the overhead of an external relational database during this prototype phase."

---

### [0:30 - 1:00] Step 1: Geo-Optimization Engine (Module 1)
**[Visuals]** 
*Select 'Chicago' or punch in custom coordinates. Select products, and hit 'Get Delivery Quote'. Smoothly pause at Step 1 of the pipeline interface.*

**[Voiceover]**
"Let's trace a live POST request to the `/api/fulfill` endpoint. The controller immediately delegates to the first agent: the **Distance Calculator Module**. 

Instead of relying on heavy third-party mapping SDKs, this engine mathematically parses the incoming Latitude and Longitude payload and natively processes it through the Haversine trigonometric formula. It calculates the exact spherical distance to all 50 warehouses and returns a cleanly sorted, distance-ranked dictionary in milliseconds."

---

### [1:00 - 1:30] Step 2 & 3: Inventory Auditor & Allocation Orchestrator
**[Visuals]** 
*Scroll down to highlight Step 2 (Inventory Pass/Fail checks) and Step 3 (Single vs Split mode).*

**[Voiceover]**
"Next, the engine pipes that sorted list into the **Inventory Auditor**. This agent validates current on-hand units against the requested order volume, but injects a strict business-logic constraint: a 10% safety stock reserve. If fulfilling an item drops physical inventory below 10%, the auditor legally throws a 'Fail' status and strips that warehouse from the eligible pool.

Surviving locations are handed to the **Allocation Orchestrator**. This module strongly prefers single-origin fulfillment. Prioritizing the closest surviving node, it attempts to pack the whole box. If the order is too massive, emergency failover logic shards the payload—recursively iterating outward to physically split the order across multiple origin nodes."

---

### [1:30 - 2:00] Step 4: Mock API Carrier Integration (Module 4)
**[Visuals]** 
*Scroll to Step 4 and specifically point out the "Shipment Cards", hovering over FedEx Ground vs UPS Next Day Air.*

**[Voiceover]**
"To solve the final mile, the system delegates to the **Shipping Service Controller**, which queries simulated third-party APIs for standard integrations like FedEx and UPS. 

These mock API classes dynamically react to payload weight and physical distance variables. For instance, the FedEx mocked node leverages a $4.99 baseline with dynamic weight multipliers, calculating ~600 ground-miles per day. The engine generates all theoretical JSON quotes, evaluates them against a configured Time-vs-Cost mathematical weight matrix, and dynamically flags the absolute optimal carrier."

---

### [2:00 - 2:30] Persistence & State Mutation
**[Visuals]** 
*Click the "Place Order & Deduct Inventory" button. Watch the success screen pop, then click over to the "Placed Orders" dashboard.*

**[Voiceover]**
"All of this runs dynamically as a 'quote' initially simulating memory. But the moment you click 'Place Order', a secondary boolean is pushed back to the `/api/fulfill` route. 

Triggering this boolean commands the Python state manager to permanently mutate the global dictionary. A unique 'ORD' sequence token is generated, the item array is permanently deducted, and the full JSON receipt is persisted into the active state, accessible instantly via a `/api/orders` fetch from this monitoring dashboard."

---

### [2:30 - 3:00] Admin Overrides & Conclusion 
**[Visuals]** 
*Navigate to the 'Inventory' tab. Hover over a cell to show the "✎ Edit" tooltip, click it, type a fresh number into the prompt, and watch the colors shift.*

**[Voiceover]**
"And to ensure system parity for admins, the Live Inventory matrix acts as both a dashboard and a control hook. Clicking any numeric cell directly triggers a localized `/api/inventory/update` POST payload. 

By injecting a forced quantity override, administrators can manually simulate warehouse shrinkage or immediate pallet restocking, forcing the frontend to aggressively re-compute safety margins and status tags. 

SmartWarehouse proves complex supply chain mathematics can be fast, completely transparent, and deeply interactive."
