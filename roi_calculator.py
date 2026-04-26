import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="ASP Partner ROI Calculator", layout="wide", page_icon="🔶", initial_sidebar_state="expanded")

# ── CSS ──
st.markdown("""<style>
#MainMenu,footer,header{visibility:hidden}
html,body,[class*="css"]{font-family:'Amazon Ember','Segoe UI',Helvetica,Arial,sans-serif}
.hero{background:linear-gradient(135deg,#232F3E,#37475A,#485769);border-radius:14px;padding:30px 40px;margin-bottom:24px;border-bottom:4px solid #FF9900}
.hero h1{color:#FFF;font-size:28px;margin:0 0 4px 0;font-weight:700}.hero .sub{color:#FF9900;font-size:15px;margin:0}.hero .meta{color:#A0AAB4;font-size:11px;margin-top:8px}
.kpi{background:#FFF;border-radius:10px;padding:18px 14px;text-align:center;border:1px solid #E8ECEF;box-shadow:0 2px 6px rgba(0,0,0,.04)}
.kpi .v{color:#232F3E;font-size:26px;font-weight:700;margin:0;line-height:1.2}.kpi .l{color:#6B7785;font-size:11px;margin:4px 0 0;text-transform:uppercase;letter-spacing:.4px}
.kpi.hl{border-left:4px solid #FF9900}.kpi.g .v{color:#067D62}.kpi.r .v{color:#C7511F}.kpi.b .v{color:#0073BB}
.stitle{font-size:18px;font-weight:700;color:#232F3E;border-left:4px solid #FF9900;padding-left:12px;margin:28px 0 12px}
[data-testid="stSidebar"]{background:#232F3E}[data-testid="stSidebar"] *{color:#D5D9DD!important}
</style>""", unsafe_allow_html=True)

def kpi(v, l, c=""):
    return f'<div class="kpi {c}"><p class="v">{v}</p><p class="l">{l}</p></div>'

# ═══════════════════════════════════════════════════════════════
# SIDEBAR — ALL INPUTS
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Model Inputs")
    partner_name = st.text_input("Partner Name", "Holland America Line")

    st.markdown("### 🏨 Property Metrics")
    total_properties = st.number_input("Total Properties/Ships", value=11, min_value=1)
    total_rooms = st.number_input("Total Rooms/Staterooms", value=11394, min_value=1)
    avg_rooms_property = st.number_input("Avg Rooms per Property", value=1036, min_value=1)
    occupancy_pct = st.slider("Occupancy %", 50, 100, 96) / 100
    avg_stay_nights = st.number_input("Avg Guest Stay (nights)", value=7, min_value=1)
    cycles_per_month = st.number_input("Cruises/Cycles per Month", value=4, min_value=1)
    guests_per_room = st.number_input("Guests per Room", value=2.0, step=0.1)

    st.markdown("### 🚀 Alexa Deployment")
    rooms_with_alexa = st.number_input("Rooms with Alexa", value=2500, min_value=1)
    rooms_per_cycle = st.number_input("Rooms per Cruise/Cycle", value=500, min_value=1)

    st.markdown("### 💵 Monthly Revenue per Room")
    monthly_rev_per_room = st.number_input("Total Monthly Revenue/Room ($)", value=5851, min_value=1)
    pre_boarding_pct = st.slider("Pre-boarding/Pre-arrival Revenue %", 0, 100, 60) / 100
    addressable_rev = monthly_rev_per_room * (1 - pre_boarding_pct)
    st.caption(f"Addressable monthly revenue/room: **${addressable_rev:,.0f}**")

    # ── Amenity Categories (12 slots, editable names) ──
    st.markdown("### 🏷️ Amenity Categories")
    st.caption("Edit names & revenue mix. Set % to 0 to disable.")
    NUM_AMENITIES = 12
    default_amenities = [
        ("Beverage Sales", 25, 70), ("Shore Excursions", 18, 70), ("Retail Sales", 10, 30),
        ("Specialty Restaurants", 4, 70), ("Internet & Communication", 7, 70), ("Spa & Wellness", 6, 80),
        ("Photo Sales", 2, 70), ("Art Sales", 1, 70), ("Laundry & Dry-Cleaning", 1, 70),
        ("In-Room Dining", 0, 20), ("Late Checkout", 0, 80), ("Shows & Entertainment", 0, 60),
    ]
    amenities = []
    for i in range(NUM_AMENITIES):
        dn, dp, dm = default_amenities[i] if i < len(default_amenities) else (f"Amenity {i+1}", 0, 50)
        with st.expander(f"Amenity {i+1}: {dn}"):
            name = st.text_input("Name", dn, key=f"an{i}")
            rev_pct = st.slider("% of Revenue", 0, 50, dp, key=f"ap{i}") / 100
            margin = st.slider("Avg Margin %", 0, 100, dm, key=f"am{i}") / 100
            amenities.append({"name": name, "pct": rev_pct, "margin": margin})

    # ── Fixed Fee Revenue Streams (3 slots) ──
    st.markdown("### 🎫 Fixed Fee Revenue Streams")
    st.caption("Casino referral, restaurant reservation, room booking, etc.")
    NUM_FIXED = 3
    default_fixed = [
        ("Casino Referral", 10.0, 10, 20, 50),
        ("Restaurant Reservation", 2.0, 20, 50, 0),
        ("Room Booking Commission", 0.0, 0.5, 5, 0),
    ]
    fixed_fees = []
    for i in range(NUM_FIXED):
        df = default_fixed[i] if i < len(default_fixed) else (f"Fixed Fee {i+1}", 0, 0, 0, 0)
        with st.expander(f"Fixed Fee {i+1}: {df[0]}"):
            fn = st.text_input("Name", df[0], key=f"fn{i}")
            fee = st.number_input("Fee per Transaction ($)", value=df[1], step=1.0, key=f"ff{i}")
            guest_pct = st.slider("% Guests Using via Alexa", 0.0, 50.0, float(df[2]), step=0.1, key=f"fg{i}") / 100
            visit_pct = st.slider("% Guests Visiting/Eligible", 0, 100, df[3], key=f"fv{i}") / 100
            commission_pct = st.slider("Commission % (if applicable)", 0, 100, df[4], key=f"fc{i}") / 100
            fixed_fees.append({"name": fn, "fee": fee, "guest_pct": guest_pct, "visit_pct": visit_pct, "commission_pct": commission_pct})

    # ── Cost Savings ──
    st.markdown("### 📉 Cost Savings")
    call_hours_monthly = st.number_input("Monthly Guest Service Hours", value=336, min_value=0)
    hourly_wage = st.number_input("Hourly Wage ($)", value=40, min_value=1)
    call_reduction_pct = st.slider("Call Volume Reduction %", 0, 100, 25) / 100
    daily_pages = st.number_input("Daily Printed Pages/Room", value=5, min_value=0)
    cost_per_page = st.number_input("Cost per Page ($)", value=0.04, step=0.01, format="%.2f")
    dist_time_min = st.number_input("Distribution Time/Room (min)", value=1, min_value=0)
    print_savings_pct = st.slider("Printing Savings %", 0, 100, 50) / 100

    # ── Deal Terms ──
    st.markdown("### 📋 Deal Terms")
    monthly_sub = st.number_input("Monthly Subscription ($)", value=15.0, step=1.0)
    rev_share_pct = st.slider("Revenue Share %", 0, 50, 10) / 100
    device_msrp = st.number_input("Device MSRP ($)", value=180.0, step=1.0)
    device_discount = st.slider("Device Discount %", 0, 50, 22) / 100
    device_setup = st.number_input("Setup Fee ($)", value=35.0, step=1.0)
    device_life = st.number_input("Device Life (months)", value=60, min_value=1)

# ═══════════════════════════════════════════════════════════════
# CALCULATION ENGINE
# ═══════════════════════════════════════════════════════════════
device_price = device_msrp * (1 - device_discount)
monthly_device_amort = device_price / device_life
guest_days = avg_stay_nights * cycles_per_month
monthly_guests_per_cycle = rooms_per_cycle * guests_per_room * occupancy_pct

# Cost savings
svc_savings_per_cycle = call_hours_monthly * hourly_wage * call_reduction_pct
total_svc_savings = svc_savings_per_cycle * (rooms_with_alexa / rooms_per_cycle) if rooms_per_cycle > 0 else 0
print_cost = rooms_per_cycle * guest_days * daily_pages * cost_per_page
dist_cost = rooms_per_cycle * guest_days * (dist_time_min / 60) * hourly_wage
print_savings_per_cycle = (print_cost + dist_cost) * print_savings_pct
total_print_savings = print_savings_per_cycle * (rooms_with_alexa / rooms_per_cycle) if rooms_per_cycle > 0 else 0
total_cost_savings = total_svc_savings + total_print_savings
cost_savings_per_room = total_cost_savings / rooms_with_alexa if rooms_with_alexa > 0 else 0

def calc_roi(txn_pct, inc_pct):
    """Core ROI calculation for given transaction % and incrementality %."""
    pr = rooms_with_alexa if rooms_with_alexa > 0 else 1

    # Amenity revenue (% of transaction model)
    amenity_rev = 0
    amenity_inc = 0
    amenity_rs = 0
    amenity_cost = 0
    details = []
    for a in amenities:
        if a["pct"] <= 0:
            continue
        cat_rev_room = addressable_rev * a["pct"]
        via_alexa = cat_rev_room * txn_pct
        incremental = via_alexa * inc_pct
        rs = via_alexa * rev_share_pct
        cost = incremental * (1 - a["margin"])
        amenity_rev += via_alexa * pr
        amenity_inc += incremental * pr
        amenity_rs += rs * pr
        amenity_cost += cost * pr
        details.append({"name": a["name"], "rev": via_alexa, "inc": incremental, "rs": rs, "cost": cost, "margin": a["margin"]})

    # Fixed fee revenue
    fixed_rev = 0
    fixed_payment = 0
    fixed_details = []
    for ff in fixed_fees:
        if ff["fee"] <= 0 and ff["commission_pct"] <= 0:
            continue
        monthly_eligible = monthly_guests_per_cycle * ff["visit_pct"] * ff["guest_pct"] * (rooms_with_alexa / rooms_per_cycle if rooms_per_cycle > 0 else 0)
        if ff["fee"] > 0:
            rev = monthly_eligible * ff["fee"]
            payment = rev  # fixed fee goes to ASP
        else:
            rev = 0
            payment = 0
        if ff["commission_pct"] > 0:
            # Commission model (like room booking)
            booking_rev = monthly_eligible * avg_stay_nights * monthly_rev_per_room / 30 if ff["name"].lower().find("room") >= 0 else monthly_eligible * 75
            commission = booking_rev * ff["commission_pct"]
            rev += booking_rev
            payment += commission
        fixed_rev += rev
        fixed_payment += payment
        fixed_details.append({"name": ff["name"], "rev": rev / pr, "payment": payment / pr})

    # Totals
    total_rev = amenity_rev + fixed_rev + total_cost_savings
    sub_total = monthly_sub * pr
    device_total = monthly_device_amort * pr
    total_payment = sub_total + amenity_rs + fixed_payment + device_total
    total_inc = amenity_inc + total_cost_savings
    total_amenity_cost_all = amenity_cost
    inc_cp = total_inc - total_payment - total_amenity_cost_all
    investment = total_payment + total_amenity_cost_all
    roi = (inc_cp / investment * 100) if investment > 0 else 0

    return {
        "total_rev": total_rev, "total_rev_room": total_rev / pr,
        "amenity_rev_room": amenity_rev / pr, "amenity_inc_room": amenity_inc / pr,
        "amenity_rs_room": amenity_rs / pr, "amenity_cost_room": amenity_cost / pr,
        "fixed_rev_room": fixed_rev / pr, "fixed_payment_room": fixed_payment / pr,
        "cost_savings_room": cost_savings_per_room,
        "sub_room": monthly_sub, "device_room": monthly_device_amort,
        "total_payment_room": total_payment / pr,
        "total_inc_room": (amenity_inc + total_cost_savings) / pr,
        "inc_cp": inc_cp, "inc_cp_room": inc_cp / pr,
        "roi": roi,
        "cm": ((total_inc - total_payment - total_amenity_cost_all) / total_rev * 100) if total_rev > 0 else 0,
        "details": details, "fixed_details": fixed_details,
        "total_payment": total_payment, "total_amenity_cost": total_amenity_cost_all,
    }

# ═══════════════════════════════════════════════════════════════
# HERO & TABS
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""<div class="hero"><h1>🔶 {partner_name} — Alexa ROI Calculator</h1>
<p class="sub">Deal Financial Model &amp; Sensitivity Analysis</p>
<p class="meta">Confidential | {datetime.now().strftime('%B %d, %Y')} | Expand sidebar (▸) to adjust assumptions</p></div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  📋 Executive Summary  ", "  🎮 Live Scenario Builder  ",
    "  🔢 Calculation Walkthrough  ", "  📊 Sensitivity Analysis  ",
    "  📈 Deployment Scenarios  "
])

# ─── TAB 1: EXECUTIVE SUMMARY (3 pre-set scenarios) ───
with tab1:
    st.markdown(f'<div class="stitle">{partner_name} — ROI Summary</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Scenario 1 — Conservative**")
        s1t = st.slider("Txn via Alexa %", 1, 50, 8, key="e1t") / 100
        s1i = st.slider("Incrementality %", 1, 100, 50, key="e1i") / 100
    with c2:
        st.markdown("**Scenario 2 — Base**")
        s2t = st.slider("Txn via Alexa %", 1, 50, 10, key="e2t") / 100
        s2i = st.slider("Incrementality %", 1, 100, 40, key="e2i") / 100
    with c3:
        st.markdown("**Scenario 3 — Optimistic**")
        s3t = st.slider("Txn via Alexa %", 1, 50, 15, key="e3t") / 100
        s3i = st.slider("Incrementality %", 1, 100, 80, key="e3i") / 100

    r1, r2, r3 = calc_roi(s1t, s1i), calc_roi(s2t, s2i), calc_roi(s3t, s3i)
    st.markdown("---")

    for lbl, r, css in [("Conservative", r1, "b"), ("Base Case", r2, "g"), ("Optimistic", r3, "r")]:
        st.markdown(f"**{lbl}**")
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(kpi(f"{r['roi']:.0f}%", "ROI", f"hl {css}"), unsafe_allow_html=True)
        with k2: st.markdown(kpi(f"${r['inc_cp_room']:,.0f}", "Monthly CP/Room", css), unsafe_allow_html=True)
        with k3: st.markdown(kpi(f"${r['inc_cp_room']*12:,.0f}", "Annual CP/Room", css), unsafe_allow_html=True)
        with k4: st.markdown(kpi(f"${r['inc_cp_room']*12*rooms_per_cycle/1000:,.0f}K", "Annual CP/Property", css), unsafe_allow_html=True)
        st.markdown("")

    st.markdown("---")
    st.markdown(f'<div class="stitle">Side-by-Side (Monthly per Room)</div>', unsafe_allow_html=True)
    def f(v): return f"${v:,.0f}"
    rows = [
        ("Txn via Alexa", f"{s1t*100:.0f}%", f"{s2t*100:.0f}%", f"{s3t*100:.0f}%"),
        ("Incrementality", f"{s1i*100:.0f}%", f"{s2i*100:.0f}%", f"{s3i*100:.0f}%"),
        ("", "", "", ""),
        ("Total Revenue", f(r1["total_rev_room"]), f(r2["total_rev_room"]), f(r3["total_rev_room"])),
        ("Alexa Benefits", f(r1["total_inc_room"]), f(r2["total_inc_room"]), f(r3["total_inc_room"])),
        ("  ↳ Incremental Amenity Rev", f(r1["amenity_inc_room"]), f(r2["amenity_inc_room"]), f(r3["amenity_inc_room"])),
        ("  ↳ Cost Savings", f(r1["cost_savings_room"]), f(r2["cost_savings_room"]), f(r3["cost_savings_room"])),
        ("Total Payment to Alexa", f(-r1["total_payment_room"]), f(-r2["total_payment_room"]), f(-r3["total_payment_room"])),
        ("  ↳ Subscription", f(-r1["sub_room"]), f(-r2["sub_room"]), f(-r3["sub_room"])),
        ("  ↳ Rev-Share", f(-r1["amenity_rs_room"]), f(-r2["amenity_rs_room"]), f(-r3["amenity_rs_room"])),
        ("  ↳ Fixed Fees", f(-r1["fixed_payment_room"]), f(-r2["fixed_payment_room"]), f(-r3["fixed_payment_room"])),
        ("Incremental Amenity Cost", f(-r1["amenity_cost_room"]), f(-r2["amenity_cost_room"]), f(-r3["amenity_cost_room"])),
        ("", "", "", ""),
        ("Incremental CP", f(r1["inc_cp_room"]), f(r2["inc_cp_room"]), f(r3["inc_cp_room"])),
        ("ROI %", f"{r1['roi']:.0f}%", f"{r2['roi']:.0f}%", f"{r3['roi']:.0f}%"),
    ]
    st.dataframe(pd.DataFrame(rows, columns=["Metric", "Scenario 1", "Scenario 2", "Scenario 3"]),
                 use_container_width=True, hide_index=True, height=560)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Conservative","Base","Optimistic"], y=[r1["roi"],r2["roi"],r3["roi"]],
                         marker_color=["#0073BB","#067D62","#C7511F"],
                         text=[f"{v:.0f}%" for v in [r1["roi"],r2["roi"],r3["roi"]]], textposition="outside"))
    fig.update_layout(title="ROI % by Scenario", height=350, plot_bgcolor="#FAFBFC", yaxis=dict(gridcolor="#E8ECEF"))
    st.plotly_chart(fig, use_container_width=True)

# ─── TAB 2: LIVE SCENARIO BUILDER (partner plays with this) ───
with tab2:
    st.markdown(f'<div class="stitle">🎮 Live Scenario Builder — Build Your Own</div>', unsafe_allow_html=True)
    st.markdown("Adjust the sliders below and see results update instantly. Perfect for live partner calls.")

    lc1, lc2 = st.columns([1, 2])
    with lc1:
        st.markdown("**Your Scenario**")
        live_txn = st.slider("Transactions via Alexa %", 1, 50, 10, key="lt") / 100
        live_inc = st.slider("Incrementality %", 1, 100, 50, key="li") / 100
        st.markdown("---")
        st.markdown("**Override Amenity Txn % individually**")
        override = st.checkbox("Use per-amenity transaction %", value=False)
        per_amenity_txn = {}
        if override:
            for a in amenities:
                if a["pct"] > 0:
                    per_amenity_txn[a["name"]] = st.slider(f"{a['name']} Txn %", 0, 50, int(live_txn*100), key=f"ov_{a['name']}") / 100

    # Calculate with overrides
    if override and per_amenity_txn:
        pr = rooms_with_alexa if rooms_with_alexa > 0 else 1
        tot_rev = 0; tot_inc = 0; tot_rs = 0; tot_cost = 0; det = []
        for a in amenities:
            if a["pct"] <= 0: continue
            t = per_amenity_txn.get(a["name"], live_txn)
            cat_rev = addressable_rev * a["pct"]
            via = cat_rev * t; inc = via * live_inc; rs = via * rev_share_pct; co = inc * (1 - a["margin"])
            tot_rev += via * pr; tot_inc += inc * pr; tot_rs += rs * pr; tot_cost += co * pr
            det.append({"name": a["name"], "txn": f"{t*100:.0f}%", "rev": f"${via:,.0f}", "inc": f"${inc:,.0f}", "rs": f"${rs:,.0f}", "cost": f"${co:,.0f}"})
        # Fixed fees
        fp = 0
        for ff in fixed_fees:
            if ff["fee"] <= 0 and ff["commission_pct"] <= 0: continue
            me = monthly_guests_per_cycle * ff["visit_pct"] * ff["guest_pct"] * (rooms_with_alexa / rooms_per_cycle if rooms_per_cycle > 0 else 0)
            fp += me * ff["fee"] if ff["fee"] > 0 else 0
        sub_t = monthly_sub * pr; dev_t = monthly_device_amort * pr
        total_pay = sub_t + tot_rs + fp + dev_t
        icp = tot_inc + total_cost_savings - total_pay - tot_cost
        inv = total_pay + tot_cost
        live_r = {"inc_cp_room": icp/pr, "roi": (icp/inv*100) if inv > 0 else 0,
                  "total_rev_room": (tot_rev+total_cost_savings)/pr, "total_inc_room": (tot_inc+total_cost_savings)/pr,
                  "total_payment_room": total_pay/pr, "amenity_cost_room": tot_cost/pr, "cost_savings_room": cost_savings_per_room}
    else:
        live_r = calc_roi(live_txn, live_inc)
        det = [{"name": d["name"], "txn": f"{live_txn*100:.0f}%", "rev": f"${d['rev']:,.0f}",
                "inc": f"${d['inc']:,.0f}", "rs": f"${d['rs']:,.0f}", "cost": f"${d['cost']:,.0f}"} for d in live_r.get("details", [])]

    with lc2:
        # KPI row
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(kpi(f"{live_r['roi']:.0f}%", "ROI", "hl g"), unsafe_allow_html=True)
        with k2: st.markdown(kpi(f"${live_r['inc_cp_room']:,.0f}", "Monthly CP/Room", "g"), unsafe_allow_html=True)
        with k3: st.markdown(kpi(f"${live_r['inc_cp_room']*12:,.0f}", "Annual CP/Room"), unsafe_allow_html=True)
        with k4: st.markdown(kpi(f"${live_r['inc_cp_room']*12*rooms_per_cycle/1000:,.0f}K", "Annual CP/Property"), unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Revenue by Amenity (Monthly per Room)**")
        if det:
            st.dataframe(pd.DataFrame(det), use_container_width=True, hide_index=True)

        # Waterfall
        wf_l = ["Benefits", "- Payment", "- Amenity Cost", "= CP"]
        wf_v = [live_r["total_inc_room"], -live_r["total_payment_room"], -live_r["amenity_cost_room"], live_r["inc_cp_room"]]
        fig_wf = go.Figure(go.Waterfall(x=wf_l, y=wf_v, measure=["absolute","relative","relative","total"],
            connector=dict(line=dict(color="#D5D9DD")), increasing=dict(marker=dict(color="#067D62")),
            decreasing=dict(marker=dict(color="#C7511F")), totals=dict(marker=dict(color="#FF9900")),
            text=[f"${v:,.0f}" for v in wf_v], textposition="outside"))
        fig_wf.update_layout(height=380, plot_bgcolor="#FAFBFC", yaxis=dict(gridcolor="#E8ECEF"), margin=dict(t=30))
        st.plotly_chart(fig_wf, use_container_width=True)

# ─── TAB 3: CALCULATION WALKTHROUGH ───
with tab3:
    st.markdown(f'<div class="stitle">🔢 Calculation Walkthrough</div>', unsafe_allow_html=True)
    st.markdown("Step-by-step logic verification with pre-populated scenario.")

    wc1, wc2 = st.columns(2)
    with wc1: wt = st.slider("Transaction %", 1, 30, 8, key="wt") / 100
    with wc2: wi = st.slider("Incrementality %", 10, 100, 50, key="wi") / 100
    wr = calc_roi(wt, wi)

    st.markdown(f'<div class="stitle">Step 1: Amenity Revenue via Alexa</div>', unsafe_allow_html=True)
    st.markdown(f"Addressable Revenue/Room = ${monthly_rev_per_room:,} × (1 - {pre_boarding_pct*100:.0f}%) = **${addressable_rev:,.0f}**")
    step1 = []
    for d in wr["details"]:
        a_match = [a for a in amenities if a["name"] == d["name"]]
        pct = a_match[0]["pct"] if a_match else 0
        step1.append({
            "Amenity": d["name"],
            "Rev Mix %": f"{pct*100:.0f}%",
            "Cat Rev/Room": f"${addressable_rev * pct:,.0f}",
            f"× Txn {wt*100:.0f}%": f"${d['rev']:,.0f}",
            f"× Inc {wi*100:.0f}%": f"${d['inc']:,.0f}",
            f"Rev-Share {rev_share_pct*100:.0f}%": f"${d['rs']:,.0f}",
            f"Cost (1-margin)": f"${d['cost']:,.0f}",
        })
    st.dataframe(pd.DataFrame(step1), use_container_width=True, hide_index=True)

    st.markdown(f'<div class="stitle">Step 2: Fixed Fee Revenue</div>', unsafe_allow_html=True)
    if wr["fixed_details"]:
        st.dataframe(pd.DataFrame([{"Stream": d["name"], "Revenue/Room": f"${d['rev']:,.0f}", "Payment/Room": f"${d['payment']:,.0f}"} for d in wr["fixed_details"]]),
                     use_container_width=True, hide_index=True)
    else:
        st.info("No fixed fee streams configured.")

    st.markdown(f'<div class="stitle">Step 3: Cost Savings</div>', unsafe_allow_html=True)
    cs1, cs2 = st.columns(2)
    with cs1:
        st.metric("Guest Service Savings/Month", f"${total_svc_savings:,.0f}")
        st.caption(f"{call_hours_monthly}hrs × ${hourly_wage} × {call_reduction_pct*100:.0f}% × {rooms_with_alexa/rooms_per_cycle:.0f} cycles")
    with cs2:
        st.metric("Printing Savings/Month", f"${total_print_savings:,.0f}")
        st.caption(f"Print + distribution cost × {print_savings_pct*100:.0f}%")

    st.markdown(f'<div class="stitle">Step 4: Payment to Alexa</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([
        {"Component": "Subscription", "Per Room": f"${monthly_sub:,.0f}"},
        {"Component": "Rev-Share", "Per Room": f"${wr['amenity_rs_room']:,.0f}"},
        {"Component": "Fixed Fees", "Per Room": f"${wr['fixed_payment_room']:,.0f}"},
        {"Component": "Device Amortization", "Per Room": f"${monthly_device_amort:,.2f}"},
        {"Component": "TOTAL", "Per Room": f"${wr['total_payment_room']:,.0f}"},
    ]), use_container_width=True, hide_index=True)

    st.markdown(f'<div class="stitle">Step 5: Incremental CP & ROI</div>', unsafe_allow_html=True)
    st.markdown(f"""
    - **Incremental Benefits/Room** = ${wr['total_inc_room']:,.0f}
    - **Total Payment/Room** = ${wr['total_payment_room']:,.0f}
    - **Amenity Cost/Room** = ${wr['amenity_cost_room']:,.0f}
    - **Incremental CP/Room** = ${wr['total_inc_room']:,.0f} - ${wr['total_payment_room']:,.0f} - ${wr['amenity_cost_room']:,.0f} = **${wr['inc_cp_room']:,.0f}**
    - **ROI** = ${wr['inc_cp_room']:,.0f} / (${wr['total_payment_room']:,.0f} + ${wr['amenity_cost_room']:,.0f}) = **{wr['roi']:.0f}%**
    """)

# ─── TAB 4: SENSITIVITY ANALYSIS (matching your Excel screenshots) ───
with tab4:
    st.markdown(f'<div class="stitle">📊 Sensitivity Analysis</div>', unsafe_allow_html=True)

    # 1D sweep
    st.markdown("**ROI across Transaction % (fixed incrementality)**")
    sc1, sc2 = st.columns([1, 3])
    with sc1:
        si = st.slider("Incrementality %", 10, 100, 50, step=5, key="si") / 100
    txns = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.25]
    sr = [calc_roi(t, si) for t in txns]
    st.dataframe(pd.DataFrame({
        "Txn %": [f"{t*100:.0f}%" for t in txns],
        "Rev/Room": [f"${r['total_rev_room']:,.0f}" for r in sr],
        "CP/Room": [f"${r['inc_cp_room']:,.0f}" for r in sr],
        "CM %": [f"{r['cm']:.0f}%" for r in sr],
        "ROI %": [f"{r['roi']:.0f}%" for r in sr],
    }), use_container_width=True, hide_index=True)

    # 2D Heatmaps (CP per room + ROI %)
    st.markdown(f'<div class="stitle">CP per Room — Txn % × Revenue Growth (Incrementality)</div>', unsafe_allow_html=True)
    txn_ax = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28]
    inc_ax = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15]
    # Map inc_ax to incrementality (inc_ax represents revenue growth %, we scale to incrementality)
    inc_map = [i * 10 for i in inc_ax]  # 1%→10%, 15%→150% — use directly as incrementality

    cp_heat = []
    roi_heat = []
    for inc_val in inc_ax:
        cp_row = []
        roi_row = []
        for txn_val in txn_ax:
            r = calc_roi(txn_val, inc_val * 10)  # scale: 1% growth → 10% incrementality
            cp_row.append(round(r["inc_cp_room"], 2))
            roi_row.append(round(r["roi"]))
        cp_heat.append(cp_row)
        roi_heat.append(roi_row)

    fig_cp = go.Figure(data=go.Heatmap(
        z=cp_heat, x=[f"{t*100:.0f}%" for t in txn_ax], y=[f"{i*100:.1f}%" for i in inc_ax],
        colorscale=[[0,"#C7511F"],[0.3,"#FDEBD0"],[0.5,"#F5F5F5"],[0.7,"#D5F5E3"],[1,"#067D62"]],
        text=[[f"${v:,.0f}" for v in row] for row in cp_heat], texttemplate="%{text}",
        textfont=dict(size=10), colorbar=dict(title="CP/Room"), zmid=0,
    ))
    fig_cp.update_layout(title=f"{partner_name} CP per Room", height=520,
        xaxis_title="Ancillary Transaction % through Alexa", yaxis_title="Revenue Growth % due to Alexa",
        plot_bgcolor="#FAFBFC")
    st.plotly_chart(fig_cp, use_container_width=True)

    st.markdown(f'<div class="stitle">ROI % — Txn % × Revenue Growth</div>', unsafe_allow_html=True)
    fig_roi = go.Figure(data=go.Heatmap(
        z=roi_heat, x=[f"{t*100:.0f}%" for t in txn_ax], y=[f"{i*100:.1f}%" for i in inc_ax],
        colorscale=[[0,"#C7511F"],[0.3,"#FDEBD0"],[0.5,"#F5F5F5"],[0.7,"#D5F5E3"],[1,"#067D62"]],
        text=[[f"{v}%" for v in row] for row in roi_heat], texttemplate="%{text}",
        textfont=dict(size=10), colorbar=dict(title="ROI %"), zmid=0,
    ))
    fig_roi.update_layout(title=f"{partner_name} ROI %", height=520,
        xaxis_title="Ancillary Transaction % through Alexa", yaxis_title="Revenue Growth % due to Alexa",
        plot_bgcolor="#FAFBFC")
    st.plotly_chart(fig_roi, use_container_width=True)

    # Payment sensitivity
    st.markdown(f'<div class="stitle">Monthly Rev Share & Referral Fee Payout per Room</div>', unsafe_allow_html=True)
    rs_ax = [0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.09, 0.10, 0.11, 0.13, 0.15]
    pay_heat = []
    for rs in rs_ax:
        row = []
        for txn_val in txn_ax:
            # Payment = sub + rev_share on amenity + fixed fees + device
            amenity_payment = addressable_rev * sum(a["pct"] for a in amenities if a["pct"] > 0) * txn_val * rs
            total_pay = monthly_sub + amenity_payment + monthly_device_amort
            # Add fixed fee estimates
            for ff in fixed_fees:
                if ff["fee"] > 0:
                    me = monthly_guests_per_cycle * ff["visit_pct"] * ff["guest_pct"] / rooms_per_cycle if rooms_per_cycle > 0 else 0
                    total_pay += me * ff["fee"]
            row.append(round(total_pay, 2))
        pay_heat.append(row)

    fig_pay = go.Figure(data=go.Heatmap(
        z=pay_heat, x=[f"{t*100:.0f}%" for t in txn_ax], y=[f"{r*100:.0f}%" for r in rs_ax],
        colorscale="YlOrRd", text=[[f"${v:,.0f}" for v in row] for row in pay_heat],
        texttemplate="%{text}", textfont=dict(size=10), colorbar=dict(title="$/Room"),
    ))
    fig_pay.update_layout(title="Monthly Payment per Room (Sub + Rev Share + Fees)",
        height=450, xaxis_title="Ancillary Transaction %", yaxis_title="ASP Rev Share %",
        plot_bgcolor="#FAFBFC")
    st.plotly_chart(fig_pay, use_container_width=True)

# ─── TAB 5: DEPLOYMENT SCENARIOS ───
with tab5:
    st.markdown(f'<div class="stitle">📈 Multi-Year Deployment Scenarios</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("**Low Case**")
        l_rs = st.number_input("Rev Share/Room ($)", value=10.0, key="lrs")
        l_cv = st.text_input("Conversion % (Yr1-5)", "23.5,52.1,100,100,100", key="lcv")
    with d2:
        st.markdown("**Mid Case**")
        m_rs = st.number_input("Rev Share/Room ($)", value=20.0, key="mrs")
        m_cv = st.text_input("Conversion % (Yr1-5)", "23.5,60.5,100,100,100", key="mcv")
    with d3:
        st.markdown("**High Case**")
        h_rs = st.number_input("Rev Share/Room ($)", value=35.0, key="hrs")
        h_cv = st.text_input("Conversion % (Yr1-5)", "23.5,100,100,100,100", key="hcv")

    def pconv(s):
        try: return [float(x.strip())/100 for x in s.split(",")]
        except: return [.235,.521,1,1,1]

    def deploy(convs, mrs):
        rows, prev = [], 0
        for i, c in enumerate(convs):
            tgt = int(total_rooms * c); nd = max(0, tgt - prev); avg = (prev + tgt) / 2
            sc = avg * monthly_sub * 12; rc = avg * mrs * 12
            rows.append({"Year": 2026+i+1, "New": nd, "IB(YE)": tgt, "IB(Avg)": int(avg),
                         "Sub": sc, "RevShare": rc, "Setup": nd*device_setup, "Device": nd*device_price,
                         "Total": sc+rc+nd*device_setup+nd*device_price, "Recurring": sc+rc})
            prev = tgt
        return pd.DataFrame(rows)

    ldf, mdf, hdf = deploy(pconv(l_cv), l_rs), deploy(pconv(m_cv), m_rs), deploy(pconv(h_cv), h_rs)
    st.markdown("---")
    for lbl, df in [("Low", ldf), ("Mid", mdf), ("High", hdf)]:
        st.markdown(f"**{lbl} Case**")
        show = df.copy()
        for c in show.columns:
            if c != "Year":
                show[c] = show[c].apply(lambda x: f"${x:,.0f}" if any(k in c for k in ["Sub","Rev","Setup","Device","Total","Recurring"]) else f"{x:,.0f}")
        st.dataframe(show, use_container_width=True, hide_index=True)

    fig_d = go.Figure()
    for n, df, co in [("Low",ldf,"#0073BB"),("Mid",mdf,"#067D62"),("High",hdf,"#C7511F")]:
        fig_d.add_trace(go.Bar(name=n, x=df["Year"], y=df["Recurring"], marker_color=co))
    fig_d.update_layout(barmode="group", height=380, yaxis_title="Annual Recurring ($)", plot_bgcolor="#FAFBFC")
    st.plotly_chart(fig_d, use_container_width=True)

    # 5yr totals
    st.dataframe(pd.DataFrame({
        "": ["Total Cost (5yr)", "Recurring (5yr)", "Device+Setup (5yr)"],
        "Low": [f"${ldf['Total'].sum():,.0f}", f"${ldf['Recurring'].sum():,.0f}", f"${(ldf['Setup'].sum()+ldf['Device'].sum()):,.0f}"],
        "Mid": [f"${mdf['Total'].sum():,.0f}", f"${mdf['Recurring'].sum():,.0f}", f"${(mdf['Setup'].sum()+mdf['Device'].sum()):,.0f}"],
        "High": [f"${hdf['Total'].sum():,.0f}", f"${hdf['Recurring'].sum():,.0f}", f"${(hdf['Setup'].sum()+hdf['Device'].sum()):,.0f}"],
    }), use_container_width=True, hide_index=True)

# Footer
st.markdown(f"""<div style="background:#232F3E;border-radius:10px;padding:16px 28px;margin-top:36px;text-align:center">
<p style="color:#FF9900;font-weight:600;margin:0">Alexa Smart Properties</p>
<p style="color:#A0AAB4;font-size:11px;margin:4px 0 0">{partner_name} | Confidential | {datetime.now().strftime('%B %d, %Y')}</p></div>""", unsafe_allow_html=True)
