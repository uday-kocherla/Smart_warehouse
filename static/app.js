/* SmartWare — Order UI (v5 — minimal + decision pipeline) */

const API = "";
const GEO_DB = [
  {name:"Birmingham, AL",lat:33.5207,lon:-86.8025},{name:"Montgomery, AL",lat:32.3792,lon:-86.3077},{name:"Huntsville, AL",lat:34.7304,lon:-86.5861},{name:"Mobile, AL",lat:30.6954,lon:-88.0399},
  {name:"Anchorage, AK",lat:61.2181,lon:-149.9003},{name:"Fairbanks, AK",lat:64.8378,lon:-147.7164},{name:"Juneau, AK",lat:58.3005,lon:-134.4197},
  {name:"Phoenix, AZ",lat:33.4484,lon:-112.0740},{name:"Tucson, AZ",lat:32.2226,lon:-110.9747},{name:"Mesa, AZ",lat:33.4152,lon:-111.8315},{name:"Scottsdale, AZ",lat:33.4942,lon:-111.9261},{name:"Flagstaff, AZ",lat:35.1983,lon:-111.6513},
  {name:"Little Rock, AR",lat:34.7465,lon:-92.2896},{name:"Fayetteville, AR",lat:36.0822,lon:-94.1719},
  {name:"Los Angeles, CA",lat:34.0522,lon:-118.2437},{name:"San Francisco, CA",lat:37.7749,lon:-122.4194},{name:"San Diego, CA",lat:32.7157,lon:-117.1611},{name:"San Jose, CA",lat:37.3382,lon:-121.8863},{name:"Sacramento, CA",lat:38.5816,lon:-121.4944},{name:"Fresno, CA",lat:36.7378,lon:-119.7871},{name:"Oakland, CA",lat:37.8044,lon:-122.2712},{name:"Bakersfield, CA",lat:35.3733,lon:-119.0187},{name:"Riverside, CA",lat:33.9534,lon:-117.3962},{name:"Irvine, CA",lat:33.6846,lon:-117.8265},{name:"Santa Barbara, CA",lat:34.4208,lon:-119.6982},{name:"Palm Springs, CA",lat:33.8303,lon:-116.5453},{name:"Pasadena, CA",lat:34.1478,lon:-118.1445},
  {name:"Denver, CO",lat:39.7392,lon:-104.9903},{name:"Colorado Springs, CO",lat:38.8339,lon:-104.8214},{name:"Boulder, CO",lat:40.0150,lon:-105.2705},{name:"Fort Collins, CO",lat:40.5853,lon:-105.0844},
  {name:"Hartford, CT",lat:41.7658,lon:-72.6734},{name:"New Haven, CT",lat:41.3083,lon:-72.9279},{name:"Stamford, CT",lat:41.0534,lon:-73.5387},
  {name:"Wilmington, DE",lat:39.7391,lon:-75.5398},{name:"Dover, DE",lat:39.1582,lon:-75.5244},
  {name:"Miami, FL",lat:25.7617,lon:-80.1918},{name:"Jacksonville, FL",lat:30.3322,lon:-81.6557},{name:"Tampa, FL",lat:27.9506,lon:-82.4572},{name:"Orlando, FL",lat:28.5383,lon:-81.3792},{name:"Fort Lauderdale, FL",lat:26.1224,lon:-80.1373},{name:"Tallahassee, FL",lat:30.4383,lon:-84.2807},{name:"Sarasota, FL",lat:27.3364,lon:-82.5307},{name:"Naples, FL",lat:26.1420,lon:-81.7948},{name:"Pensacola, FL",lat:30.4213,lon:-87.2169},{name:"Daytona Beach, FL",lat:29.2108,lon:-81.0228},{name:"Gainesville, FL",lat:29.6516,lon:-82.3248},
  {name:"Atlanta, GA",lat:33.7490,lon:-84.3880},{name:"Savannah, GA",lat:32.0809,lon:-81.0912},{name:"Augusta, GA",lat:33.4735,lon:-81.9748},{name:"Athens, GA",lat:33.9519,lon:-83.3576},
  {name:"Honolulu, HI",lat:21.3069,lon:-157.8583},
  {name:"Boise, ID",lat:43.6150,lon:-116.2023},
  {name:"Chicago, IL",lat:41.8781,lon:-87.6298},{name:"Springfield, IL",lat:39.7817,lon:-89.6501},{name:"Naperville, IL",lat:41.7508,lon:-88.1535},{name:"Peoria, IL",lat:40.6936,lon:-89.5890},
  {name:"Indianapolis, IN",lat:39.7684,lon:-86.1581},{name:"Fort Wayne, IN",lat:41.0793,lon:-85.1394},{name:"South Bend, IN",lat:41.6764,lon:-86.2520},
  {name:"Des Moines, IA",lat:41.5868,lon:-93.6250},{name:"Cedar Rapids, IA",lat:41.9779,lon:-91.6656},{name:"Iowa City, IA",lat:41.6611,lon:-91.5302},
  {name:"Wichita, KS",lat:37.6872,lon:-97.3301},{name:"Topeka, KS",lat:39.0473,lon:-95.6752},{name:"Kansas City, KS",lat:39.1141,lon:-94.6275},
  {name:"Louisville, KY",lat:38.2527,lon:-85.7585},{name:"Lexington, KY",lat:38.0406,lon:-84.5037},
  {name:"New Orleans, LA",lat:29.9511,lon:-90.0715},{name:"Baton Rouge, LA",lat:30.4515,lon:-91.1871},{name:"Shreveport, LA",lat:32.5252,lon:-93.7502},
  {name:"Portland, ME",lat:43.6591,lon:-70.2568},{name:"Augusta, ME",lat:44.3106,lon:-69.7795},
  {name:"Baltimore, MD",lat:39.2904,lon:-76.6122},{name:"Annapolis, MD",lat:38.9784,lon:-76.4922},
  {name:"Boston, MA",lat:42.3601,lon:-71.0589},{name:"Worcester, MA",lat:42.2626,lon:-71.8023},{name:"Cambridge, MA",lat:42.3736,lon:-71.1097},
  {name:"Detroit, MI",lat:42.3314,lon:-83.0458},{name:"Grand Rapids, MI",lat:42.9634,lon:-85.6681},{name:"Ann Arbor, MI",lat:42.2808,lon:-83.7430},
  {name:"Minneapolis, MN",lat:44.9778,lon:-93.2650},{name:"St. Paul, MN",lat:44.9537,lon:-93.0900},{name:"Rochester, MN",lat:44.0121,lon:-92.4802},
  {name:"Jackson, MS",lat:32.2988,lon:-90.1848},{name:"Gulfport, MS",lat:30.3674,lon:-89.0928},
  {name:"Kansas City, MO",lat:39.0997,lon:-94.5786},{name:"St. Louis, MO",lat:38.6270,lon:-90.1994},{name:"Springfield, MO",lat:37.2090,lon:-93.2923},
  {name:"Billings, MT",lat:45.7833,lon:-108.5007},{name:"Missoula, MT",lat:46.8721,lon:-114.0001},{name:"Helena, MT",lat:46.5958,lon:-112.0270},
  {name:"Omaha, NE",lat:41.2565,lon:-95.9345},{name:"Lincoln, NE",lat:40.8136,lon:-96.7026},
  {name:"Las Vegas, NV",lat:36.1699,lon:-115.1398},{name:"Reno, NV",lat:39.5296,lon:-119.8138},
  {name:"Manchester, NH",lat:42.9956,lon:-71.4548},{name:"Concord, NH",lat:43.2081,lon:-71.5376},
  {name:"Newark, NJ",lat:40.7357,lon:-74.1724},{name:"Jersey City, NJ",lat:40.7178,lon:-74.0431},{name:"Princeton, NJ",lat:40.3573,lon:-74.6672},{name:"Atlantic City, NJ",lat:39.3643,lon:-74.4229},
  {name:"Albuquerque, NM",lat:35.0844,lon:-106.6504},{name:"Santa Fe, NM",lat:35.6870,lon:-105.9378},
  {name:"New York, NY",lat:40.7128,lon:-74.0060},{name:"Buffalo, NY",lat:42.8864,lon:-78.8784},{name:"Albany, NY",lat:42.6526,lon:-73.7562},{name:"Rochester, NY",lat:43.1566,lon:-77.6088},{name:"Syracuse, NY",lat:43.0481,lon:-76.1474},
  {name:"Charlotte, NC",lat:35.2271,lon:-80.8431},{name:"Raleigh, NC",lat:35.7796,lon:-78.6382},{name:"Durham, NC",lat:35.9940,lon:-78.8986},{name:"Asheville, NC",lat:35.5951,lon:-82.5515},{name:"Wilmington, NC",lat:34.2257,lon:-77.9447},
  {name:"Fargo, ND",lat:46.8772,lon:-96.7898},{name:"Bismarck, ND",lat:46.8083,lon:-100.7837},
  {name:"Columbus, OH",lat:39.9612,lon:-82.9988},{name:"Cleveland, OH",lat:41.4993,lon:-81.6944},{name:"Cincinnati, OH",lat:39.1031,lon:-84.5120},{name:"Toledo, OH",lat:41.6528,lon:-83.5379},{name:"Dayton, OH",lat:39.7589,lon:-84.1916},
  {name:"Oklahoma City, OK",lat:35.4676,lon:-97.5164},{name:"Tulsa, OK",lat:36.1540,lon:-95.9928},
  {name:"Portland, OR",lat:45.5152,lon:-122.6784},{name:"Salem, OR",lat:44.9429,lon:-123.0351},{name:"Eugene, OR",lat:44.0521,lon:-123.0868},{name:"Bend, OR",lat:44.0582,lon:-121.3153},
  {name:"Philadelphia, PA",lat:39.9526,lon:-75.1652},{name:"Pittsburgh, PA",lat:40.4406,lon:-79.9959},{name:"Harrisburg, PA",lat:40.2732,lon:-76.8867},{name:"Erie, PA",lat:42.1292,lon:-80.0851},
  {name:"Providence, RI",lat:41.8240,lon:-71.4128},
  {name:"Charleston, SC",lat:32.7765,lon:-79.9311},{name:"Columbia, SC",lat:34.0007,lon:-81.0348},{name:"Greenville, SC",lat:34.8526,lon:-82.3940},{name:"Myrtle Beach, SC",lat:33.6891,lon:-78.8867},
  {name:"Sioux Falls, SD",lat:43.5460,lon:-96.7313},{name:"Rapid City, SD",lat:44.0805,lon:-103.2310},
  {name:"Nashville, TN",lat:36.1627,lon:-86.7816},{name:"Memphis, TN",lat:35.1495,lon:-90.0490},{name:"Knoxville, TN",lat:35.9606,lon:-83.9207},{name:"Chattanooga, TN",lat:35.0456,lon:-85.3097},
  {name:"Houston, TX",lat:29.7604,lon:-95.3698},{name:"Dallas, TX",lat:32.7767,lon:-96.7970},{name:"San Antonio, TX",lat:29.4241,lon:-98.4936},{name:"Austin, TX",lat:30.2672,lon:-97.7431},{name:"Fort Worth, TX",lat:32.7555,lon:-97.3308},{name:"El Paso, TX",lat:31.7619,lon:-106.4850},{name:"Corpus Christi, TX",lat:27.8006,lon:-97.3964},{name:"Lubbock, TX",lat:33.5779,lon:-101.8552},{name:"Amarillo, TX",lat:35.2220,lon:-101.8313},{name:"Laredo, TX",lat:27.5036,lon:-99.5076},{name:"Brownsville, TX",lat:25.9017,lon:-97.4975},{name:"McAllen, TX",lat:26.2034,lon:-98.2300},
  {name:"Salt Lake City, UT",lat:40.7608,lon:-111.8910},{name:"Provo, UT",lat:40.2338,lon:-111.6585},{name:"Park City, UT",lat:40.6461,lon:-111.4980},
  {name:"Burlington, VT",lat:44.4759,lon:-73.2121},
  {name:"Richmond, VA",lat:37.5407,lon:-77.4360},{name:"Virginia Beach, VA",lat:36.8529,lon:-75.9780},{name:"Arlington, VA",lat:38.8799,lon:-77.1068},{name:"Charlottesville, VA",lat:38.0293,lon:-78.4767},{name:"Roanoke, VA",lat:37.2710,lon:-79.9414},
  {name:"Seattle, WA",lat:47.6062,lon:-122.3321},{name:"Spokane, WA",lat:47.6588,lon:-117.4260},{name:"Tacoma, WA",lat:47.2529,lon:-122.4443},{name:"Bellevue, WA",lat:47.6101,lon:-122.2015},
  {name:"Charleston, WV",lat:38.3498,lon:-81.6326},{name:"Morgantown, WV",lat:39.6295,lon:-79.9559},
  {name:"Milwaukee, WI",lat:43.0389,lon:-87.9065},{name:"Madison, WI",lat:43.0731,lon:-89.4012},{name:"Green Bay, WI",lat:44.5133,lon:-88.0133},
  {name:"Cheyenne, WY",lat:41.1400,lon:-104.8202},{name:"Jackson, WY",lat:43.4799,lon:-110.7624},
  {name:"Washington, DC",lat:38.9072,lon:-77.0369},
];

let PRODUCTS = [], loc = null;

document.addEventListener("DOMContentLoaded", async () => {
  const r = await fetch(`${API}/api/products`).catch(()=>null);
  PRODUCTS = r ? await r.json() : [];
  renderProducts();
  wireSearch();
  document.getElementById("btnRun").addEventListener("click", run);
});

// ── Products ──────────────────────────────────────
function renderProducts() {
  const list = document.getElementById("prodList");
  PRODUCTS.forEach(p => {
    const row = document.createElement("div");
    row.className = "prod-row"; row.dataset.sku = p.sku; row.dataset.on = "0";
    row.innerHTML = `
      <div class="check"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg></div>
      <div class="info"><div class="sku">${p.sku}</div><div class="name">${p.name}</div><div class="wt">${p.weight_lbs} lbs/unit</div></div>
      <div class="qty-area"><button class="qb" type="button">−</button><input type="number" class="qi" value="10" min="1"/><button class="qb" type="button">+</button></div>`;
    const qi = row.querySelector(".qi");
    row.addEventListener("click", e => {
      if (e.target.closest(".qty-area")) return;
      const on = row.dataset.on === "1";
      row.dataset.on = on ? "0" : "1"; row.classList.toggle("on");
      if (!on) qi.focus();
      updateBtn();
    });
    row.querySelector(".qb").addEventListener("click", () => { qi.value = Math.max(1, (parseInt(qi.value)||1)-1); });
    row.querySelectorAll(".qb")[1].addEventListener("click", () => { qi.value = (parseInt(qi.value)||0)+1; });
    qi.addEventListener("change", () => { if (parseInt(qi.value)<1||isNaN(parseInt(qi.value))) qi.value = 1; });
    qi.addEventListener("click", e => e.stopPropagation());
    list.appendChild(row);
  });
}

function getItems() {
  return Array.from(document.querySelectorAll('.prod-row[data-on="1"]')).map(r => ({
    sku: r.dataset.sku, qty: parseInt(r.querySelector(".qi").value)||1
  }));
}
function updateBtn() { document.getElementById("btnRun").disabled = !loc || !getItems().length; }

// ── Search ──────────────────────────────────────
function wireSearch() {
  const inp = document.getElementById("locInput"), dd = document.getElementById("dropdown");
  inp.addEventListener("input", () => {
    const q = inp.value.trim().toLowerCase();
    if (!q) { dd.classList.remove("open"); return; }
    const m = GEO_DB.filter(c => c.name.toLowerCase().includes(q)).slice(0,7);
    dd.innerHTML = m.map(c => `<div class="dd-row" data-lat="${c.lat}" data-lon="${c.lon}" data-name="${c.name}"><span class="city">${c.name}</span><span class="coords">${c.lat.toFixed(4)}, ${c.lon.toFixed(4)}</span></div>`).join("")
      + `<div class="dd-row manual">⊕ Enter coordinates manually</div>`;
    dd.classList.add("open");
    dd.querySelectorAll(".dd-row:not(.manual)").forEach(r => r.addEventListener("click", () => { pick(r.dataset.name, +r.dataset.lat, +r.dataset.lon); dd.classList.remove("open"); }));
    dd.querySelector(".manual").addEventListener("click", () => { dd.classList.remove("open"); showManual(); });
  });
  document.addEventListener("click", e => { if (!e.target.closest("#searchWrap")) dd.classList.remove("open"); });
}

function pick(name, lat, lon) {
  loc = { name, lat, lon };
  document.getElementById("locInput").value = name;
  document.getElementById("locChip").innerHTML = `<div class="chip">${name} <span class="c">${lat.toFixed(4)}, ${lon.toFixed(4)}</span></div>`;
  document.getElementById("stepProducts").classList.remove("hidden");
  document.getElementById("runWrap").classList.remove("hidden");
  updateBtn();
}

function showManual() {
  const el = document.createElement("div"); el.className = "modal-bg"; el.id = "manModal";
  el.innerHTML = `<div class="modal"><h3>Custom coordinates</h3><p>Enter any latitude & longitude.</p>
    <div class="modal-fields"><div class="mf"><label>Latitude</label><input id="mLat" type="number" step="any" placeholder="e.g. 40.7128"/></div>
    <div class="mf"><label>Longitude</label><input id="mLon" type="number" step="any" placeholder="e.g. -74.0060"/></div>
    <div class="mf"><label>Label</label><input id="mLbl" type="text" placeholder="e.g. My Office"/></div></div>
    <div class="modal-btns"><button class="m-cancel" id="mC">Cancel</button><button class="m-ok" id="mOk">Use</button></div></div>`;
  document.body.appendChild(el);
  document.getElementById("mC").onclick = () => el.remove();
  document.getElementById("mOk").onclick = () => {
    const lat = parseFloat(document.getElementById("mLat").value), lon = parseFloat(document.getElementById("mLon").value);
    if (isNaN(lat)||isNaN(lon)) { alert("Enter valid numbers"); return; }
    pick(document.getElementById("mLbl").value.trim() || `Custom (${lat.toFixed(2)}, ${lon.toFixed(2)})`, lat, lon);
    el.remove();
  };
}

// ── Run ──────────────────────────────────────────
async function run(isConfirm = false) {
  if (isConfirm instanceof Event) isConfirm = false; // protect against event object
  const btn = isConfirm ? document.getElementById("btnConfirm") : document.getElementById("btnRun");
  if (btn.disabled) return;
  btn.classList.add("loading");
  
  try {
    const res = await fetch(`${API}/api/fulfill`, {
      method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ customer_lat: loc.lat, customer_lon: loc.lon, order_items: getItems(), confirm: isConfirm })
    });
    const d = await res.json();
    
    if (isConfirm) {
      document.getElementById("results").innerHTML = `
        <div class="note-card" style="border-color:rgba(74,222,128,.3);background:rgba(74,222,128,.05);text-align:center;padding:40px 20px">
          <div style="font-size:3rem;margin-bottom:16px">📦</div>
          <h2 style="color:var(--green);margin-bottom:8px">Order Placed Successfully</h2>
          <p style="color:var(--t2);margin-bottom:24px">Warehouse inventory has been physically deducted and your shipments are being processed.</p>
          <div style="display:flex;gap:12px;justify-content:center">
            <a href="/orders" class="btn-run" style="display:inline-block;text-decoration:none;width:auto;padding:12px 24px">Track Placed Orders</a>
            <a href="/inventory" class="btn-run" style="display:inline-block;text-decoration:none;width:auto;padding:12px 24px;background:var(--surface);color:var(--t1);border-color:var(--border)">View Live Inventory</a>
          </div>
        </div>
      `;
    } else {
      render(d);
      document.getElementById("orderActions").classList.remove("hidden");
    }
  } catch { alert("Engine error"); }
  
  btn.classList.remove("loading");
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("btnConfirm").addEventListener("click", () => run(true));
});

// ── Render Decision Pipeline ────────────────────
function render(d) {
  const wrap = document.getElementById("results");
  wrap.classList.remove("hidden");

  const steps = d.decision_steps;
  const s1 = steps.step1_geo_ranking;
  const s2 = steps.step2_inventory_check;
  const s3 = steps.step3_allocation;
  const m = d.metrics;

  // ── Metrics bar ──
  const pipe = document.getElementById("pipeline");
  pipe.innerHTML = `
    <div class="metrics">
      <div class="mc"><div class="ml">Total cost</div><div class="mv gr">$${m.total_shipping_cost_usd.toFixed(2)}</div></div>
      <div class="mc"><div class="ml">Delivery</div><div class="mv bl">${m.estimated_delivery_window}</div></div>
      <div class="mc"><div class="ml">Shipments</div><div class="mv pu">${d.order_summary.total_shipments}</div></div>
      <div class="mc"><div class="ml">ETA</div><div class="mv am">${m.estimated_arrival_date}</div></div>
    </div>

    <!-- Step 1: Geo -->
    <div class="pipe-step open" data-step="1">
      <div class="pipe-head">
        <div class="pipe-left"><div class="pipe-icon geo">1</div><span class="pipe-title">${s1.title}</span></div>
        <span class="pipe-badge badge-info">${s1.nearest_warehouses.length} nearest</span>
      </div>
      <div class="pipe-body">
        <p class="pipe-desc">${s1.description}</p>
        <table class="ptable">
          <thead><tr><th>#</th><th>Warehouse</th><th>City</th><th>Distance</th></tr></thead>
          <tbody>${s1.nearest_warehouses.map(w => `<tr><td class="td-mono">${w.rank}</td><td>${w.warehouse_name}</td><td>${w.city}, ${w.state}</td><td class="td-mono" style="color:var(--cyan)">${w.distance_miles} mi</td></tr>`).join("")}</tbody>
        </table>
      </div>
    </div>

    <!-- Step 2: Inventory -->
    <div class="pipe-step open" data-step="2">
      <div class="pipe-head">
        <div class="pipe-left"><div class="pipe-icon inv">2</div><span class="pipe-title">${s2.title}</span></div>
        <span class="pipe-badge ${s2.total_eligible > 0 ? 'badge-ok' : 'badge-warn'}">${s2.total_eligible} eligible / ${s2.total_checked} checked</span>
      </div>
      <div class="pipe-body">
        <p class="pipe-desc">${s2.description}</p>
        <table class="ptable">
          <thead><tr><th>Warehouse</th><th>Dist</th>${d.order_summary.items_requested.map(i => `<th>${i.sku}</th>`).join("")}<th>Result</th></tr></thead>
          <tbody>${s2.warehouse_checks.map(wc => {
            const itemCells = wc.items.map(it => {
              const pct = it.on_hand > 0 ? Math.min(100, Math.round((it.available / Math.max(it.requested, 1)) * 100)) : 0;
              const cls = pct >= 100 ? 'ok' : pct > 50 ? 'low' : 'crit';
              return `<td class="td-mono"><div class="bar-wrap"><span style="min-width:36px">${it.available}</span><div class="bar"><div class="bar-fill ${cls}" style="width:${Math.min(pct,100)}%"></div></div></div></td>`;
            }).join("");
            return `<tr><td>${wc.warehouse_name}</td><td class="td-mono">${wc.distance_miles} mi</td>${itemCells}<td class="${wc.can_fulfill ? 'td-pass' : 'td-fail'}">${wc.can_fulfill ? '✓ Pass' : '✗ Fail'}</td></tr>`;
          }).join("")}</tbody>
        </table>
      </div>
    </div>

    <!-- Step 3: Allocation -->
    <div class="pipe-step open" data-step="3">
      <div class="pipe-head">
        <div class="pipe-left"><div class="pipe-icon alloc">3</div><span class="pipe-title">${s3.title}</span></div>
        <span class="pipe-badge ${s3.mode === 'single' ? 'badge-ok' : 'badge-warn'}">${s3.mode === 'single' ? 'Single warehouse' : 'Split order'}</span>
      </div>
      <div class="pipe-body"><p class="pipe-desc">${s3.description}</p></div>
    </div>

    <!-- Step 4: Shipping -->
    <div class="pipe-step open" data-step="4">
      <div class="pipe-head">
        <div class="pipe-left"><div class="pipe-icon ship">4</div><span class="pipe-title">${steps.step4_shipping.title}</span></div>
        <span class="pipe-badge badge-ok">$${m.total_shipping_cost_usd.toFixed(2)}</span>
      </div>
      <div class="pipe-body"><p class="pipe-desc">${steps.step4_shipping.description}</p></div>
    </div>
  `;

  // Toggle accordion
  pipe.querySelectorAll(".pipe-head").forEach(h => h.addEventListener("click", () => h.closest(".pipe-step").classList.toggle("open")));

  // ── Shipment cards ──
  const cards = document.getElementById("shipmentCards");
  const split = d.shipments.length > 1;
  cards.innerHTML = d.shipments.map((s, i) => {
    const wh = s.warehouse, ch = s.chosen_carrier;
    return `<div class="ship" style="animation-delay:${i*.06}s">
      <div class="ship-hd"><div class="ship-hd-l"><div class="ship-idx">${i+1}</div><div><div class="ship-name">${wh.warehouse_name}</div><div class="ship-sub">${wh.city}, ${wh.state}</div></div></div>
      <span class="ship-tag ${split?'tag-split':'tag-full'}">${split?'Split':'Full order'}</span></div>
      <div class="ship-grid"><div class="ship-col"><div class="col-lbl">Warehouse</div>
        <div class="det-row"><span class="lbl">ID</span><span class="val">${wh.warehouse_id}</span></div>
        <div class="det-row"><span class="lbl">Dist</span><span class="val dist">${wh.distance_miles} mi</span></div>
        <div class="det-row"><span class="lbl">Weight</span><span class="val">${s.total_weight_lbs} lbs</span></div></div>
      <div class="ship-col"><div class="col-lbl">Carriers</div>
        ${s.all_carrier_quotes.map(q => {
          const w = q.carrier === ch.carrier && q.service_level === ch.service_level;
          return `<div class="cq${w?' win':''}"><span class="cn">${q.service_level}${w?'<span class="best">★ best</span>':''}</span><span class="cc">$${q.cost_usd.toFixed(2)}</span><span class="cd">${q.estimated_delivery_days}d</span></div>`;
        }).join("")}</div></div>
      <div class="ship-items">${s.items_allocated.map(it => {
        const p = PRODUCTS.find(x=>x.sku===it.sku);
        return `<div class="si-row"><span class="si-sku">${it.sku}</span><span class="si-nm">${p?p.name:''}</span><span class="si-qt">×${it.qty_allocated}</span></div>`;
      }).join("")}</div></div>`;
  }).join("");

  // ── Partial fulfillment / unfulfilled items note ──
  if (d.partial_fulfillment && d.unfulfilled_items && d.unfulfilled_items.length > 0) {
    // Build a summary of what was delivered vs what was requested
    const requested = d.order_summary.items_requested;
    const allocatedMap = {};
    d.shipments.forEach(s => {
      s.items_allocated.forEach(it => {
        allocatedMap[it.sku] = (allocatedMap[it.sku] || 0) + it.qty_allocated;
      });
    });

    const rows = requested.map(req => {
      const delivered = allocatedMap[req.sku] || 0;
      const short = req.qty - delivered;
      const p = PRODUCTS.find(x => x.sku === req.sku);
      const name = p ? p.name : req.sku;
      return { sku: req.sku, name, requested: req.qty, delivered, short };
    });

    const unfulfilledRows = rows.filter(r => r.short > 0);

    cards.innerHTML += `
      <div class="note-card note-warn" style="animation: fadeIn .5s ease both; animation-delay: .2s">
        <div class="note-hd">
          <span class="note-icon">⚠</span>
          <span class="note-title">Partial Fulfillment Notice</span>
        </div>
        <p class="note-desc">We were unable to fulfill your complete order. Below is a breakdown of what we can deliver vs. what remains out of stock across all warehouses.</p>
        <table class="ptable" style="margin-top:12px">
          <thead><tr><th>Product</th><th>Requested</th><th>Delivering</th><th>Shortfall</th><th>Status</th></tr></thead>
          <tbody>
            ${rows.map(r => `
              <tr>
                <td><span style="font-weight:600">${r.name}</span><br><span class="td-mono" style="font-size:.68rem;color:var(--t3)">${r.sku}</span></td>
                <td class="td-mono">${r.requested}</td>
                <td class="td-mono ${r.short > 0 ? '' : 'td-pass'}">${r.delivered}</td>
                <td class="td-mono ${r.short > 0 ? 'td-fail' : ''}">${r.short > 0 ? '-' + r.short : '—'}</td>
                <td>${r.short === 0
                  ? '<span class="td-pass">✓ Fulfilled</span>'
                  : r.delivered > 0
                    ? '<span style="color:var(--amber);font-weight:600">◐ Partial</span>'
                    : '<span class="td-fail">✗ Out of stock</span>'
                }</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
        <p class="note-footer">The remaining ${unfulfilledRows.map(r => `${r.short}× ${r.sku}`).join(", ")} could not be sourced from any warehouse while maintaining the 10% safety stock reserve.</p>
      </div>
    `;
  }

  wrap.scrollIntoView({ behavior:"smooth", block:"start" });
}
