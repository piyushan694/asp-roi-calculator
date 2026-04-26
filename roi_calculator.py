import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Alexa Smart Properties — Partner ROI", layout="wide", page_icon="🔶", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════════════════════
# INVESTMENT-GRADE CSS — Goldman/McKinsey aesthetic
# ═══════════════════════════════════════════════════════════════
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
#MainMenu,footer,header{visibility:hidden}
html,body,[class*="css"]{font-family:'Inter',sans-serif;color:#1a1a2e}
.block-container{padding:2rem 3rem!important;max-width:1400px}

/* ── Hero ── */
.hero-wrap{margin-bottom:40px}
.hero-top{display:flex;align-items:center;gap:16px;margin-bottom:6px}
.hero-logo{width:40px;height:40px;background:#FF9900;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:22px;color:#fff;font-weight:800}
.hero-title{font-size:13px;text-transform:uppercase;letter-spacing:3px;color:#FF9900;font-weight:700;margin:0}
.hero-partner{font-size:36px;font-weight:800;color:#0d1b2a;margin:8px 0 0;letter-spacing:-1px;line-height:1.1}
.hero-sub{font-size:15px;color:#5c6b7a;margin:8px 0 0;font-weight:400}
.hero-line{height:2px;background:linear-gradient(90deg,#FF9900 0%,#FF9900 30%,#e8ecf1 30%);margin:20px 0 0;border-radius:2px}
.hero-conf{font-size:10px;color:#a0aab4;text-transform:uppercase;letter-spacing:1.5px;margin-top:8px}

/* ── KPI Metric Blocks ── */
.metric-block{padding:28px 24px;border-radius:12px;position:relative;overflow:hidden}
.metric-block.dark{background:#0d1b2a;color:#fff}
.metric-block.light{background:#f7f8fa;border:1px solid #e8ecf1}
.metric-block .eyebrow{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;font-weight:700;margin:0 0 12px;opacity:.6}
.metric-block .big-num{font-size:42px;font-weight:800;margin:0;line-height:1;letter-spacing:-1px}
.metric-block .sub-label{font-size:12px;margin:8px 0 0;opacity:.7;font-weight:500}
.metric-block.dark .eyebrow{color:#FF9900}.metric-block.dark .big-num{color:#fff}.metric-block.dark .sub-label{color:rgba(255,255,255,.5)}
.metric-block.green .big-num{color:#0a8f6c}.metric-block.blue .big-num{color:#0052cc}.metric-block.amber .big-num{color:#c7511f}
.metric-block.accent{border-left:4px solid #FF9900}

/* ── Scenario Columns ── */
.sc-header{font-size:11px;text-transform:uppercase;letter-spacing:2px;font-weight:800;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid}
.sc-header.s1{color:#0052cc;border-color:#0052cc}.sc-header.s2{color:#0a8f6c;border-color:#0a8f6c}.sc-header.s3{color:#c7511f;border-color:#c7511f}

/* ── Section Headers ── */
.sec-title{font-size:11px;text-transform:uppercase;letter-spacing:2.5px;font-weight:800;color:#0d1b2a;margin:48px 0 8px;padding-bottom:8px;border-bottom:1px solid #e8ecf1}
.sec-subtitle{font-size:14px;color:#5c6b7a;margin:0 0 24px;font-weight:400}

/* ── Insight Box ── */
.insight-box{background:#0d1b2a;border-radius:12px;padding:28px 32px;margin:24px 0;position:relative}
.insight-box::before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:#FF9900;border-radius:4px 0 0 4px}
.insight-box .ib-label{font-size:10px;text-transform:uppercase;letter-spacing:2px;color:#FF9900;font-weight:700;margin:0 0 8px}
.insight-box .ib-text{font-size:20px;color:#fff;font-weight:600;margin:0;line-height:1.4}
.insight-box .ib-sub{font-size:13px;color:rgba(255,255,255,.5);margin:10px 0 0}

/* ── Data Table ── */
.clean-table{width:100%;border-collapse:collapse;font-size:13px}
.clean-table th{background:#f7f8fa;padding:10px 14px;text-align:right;font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#5c6b7a;border-bottom:2px solid #0d1b2a}
.clean-table th:first-child{text-align:left}
.clean-table td{padding:8px 14px;text-align:right;border-bottom:1px solid #f0f2f5;color:#1a1a2e}
.clean-table td:first-child{text-align:left;font-weight:500;color:#0d1b2a}
.clean-table tr.highlight td{font-weight:700;background:#f0faf6;border-top:2px solid #0a8f6c;border-bottom:2px solid #0a8f6c}
.clean-table tr.section td{font-weight:700;padding-top:16px;border-bottom:none;color:#5c6b7a;font-size:11px;text-transform:uppercase;letter-spacing:1px}
.clean-table tr.negative td:not(:first-child){color:#c7511f}

/* ── Sidebar ── */
[data-testid="stSidebar"]{background:#0d1b2a;border-right:1px solid #1a2744}
[data-testid="stSidebar"] *{color:#c8d0d8!important}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3{color:#FF9900!important}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{gap:0;border-bottom:2px solid #e8ecf1}
.stTabs [data-baseweb="tab"]{font-weight:600;font-size:13px;padding:12px 28px;color:#5c6b7a;border-bottom:2px solid transparent;margin-bottom:-2px}
.stTabs [aria-selected="true"]{color:#0d1b2a!important;border-bottom:2px solid #FF9900!important}

/* ── Footer ── */
.footer{text-align:center;padding:32px 0;margin-top:60px;border-top:1px solid #e8ecf1}
.footer .f-brand{font-size:11px;text-transform:uppercase;letter-spacing:3px;color:#FF9900;font-weight:700}.footer .f-sub{font-size:11px;color:#a0aab4;margin-top:4px}
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR INPUTS
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## Model Assumptions")
    partner_name = st.text_input("Partner Name", "Holland America Line")

    st.markdown("### Property Metrics")
    total_properties = st.number_input("Total Properties / Ships", value=11, min_value=1)
    total_rooms = st.number_input("Total Rooms / Staterooms", value=11394, min_value=1)
    avg_rooms_property = int(total_rooms / total_properties) if total_properties > 0 else 1036
    occupancy_pct = st.slider("Occupancy %", 50, 100, 96) / 100
    avg_stay_nights = st.number_input("Avg Guest Stay (nights)", value=7, min_value=1)
    cycles_per_month = st.number_input("Cruises / Cycles per Month", value=4, min_value=1)
    guests_per_room = st.number_input("Guests per Room", value=2.0, step=0.1)

    st.markdown("### Alexa Deployment")
    alexa_properties = st.number_input("Properties with Alexa", value=5, min_value=1)
    rooms_with_alexa = st.number_input("Total Rooms with Alexa", value=2500, min_value=1)
    rooms_per_cycle = st.number_input("Rooms per Cruise / Cycle", value=500, min_value=1)
    avg_rooms_per_alexa_property = rooms_with_alexa / alexa_properties if alexa_properties > 0 else rooms_with_alexa

    st.markdown("### Revenue Inputs")
    rev_method = st.radio("Revenue Method", ["Total Annual Revenue", "Average per Room"], index=0)
    if rev_method == "Total Annual Revenue":
        total_annual_rev = st.number_input("Total Annual Revenue ($)", value=800_000_000, step=1_000_000, format="%d")
        monthly_rev_per_room = total_annual_rev / total_rooms / 12 if total_rooms > 0 else 0
    else:
        monthly_rev_per_room = st.number_input("Monthly Revenue / Room ($)", value=10000, min_value=1)
    pre_boarding_pct = st.slider("Pre-boarding Revenue %", 0, 100, 60) / 100
    addressable_rev = monthly_rev_per_room * (1 - pre_boarding_pct)

    st.markdown("### Amenity Categories")
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
        with st.expander(f"{dn}"):
            name = st.text_input("Name", dn, key=f"an{i}")
            rev_pct = st.slider("% of Revenue", 0, 50, dp, key=f"ap{i}") / 100
            margin = st.slider("Margin %", 0, 100, dm, key=f"am{i}") / 100
            amenities.append({"name": name, "pct": rev_pct, "margin": margin})

    st.markdown("### Fixed Fee Streams")
    NUM_FIXED = 3
    default_fixed = [
        ("Casino Referral", 10.0, 10, 20, 50), ("Restaurant Reservation", 2.0, 20, 50, 0), ("Room Booking Commission", 0.0, 0.5, 5, 0),
    ]
    fixed_fees = []
    for i in range(NUM_FIXED):
        df = default_fixed[i] if i < len(default_fixed) else (f"Fixed Fee {i+1}", 0, 0, 0, 0)
        with st.expander(f"{df[0]}"):
            fn = st.text_input("Name", df[0], key=f"fn{i}")
            fee = st.number_input("Fee ($)", value=df[1], step=1.0, key=f"ff{i}")
            guest_pct = st.slider("% Guests via Alexa", 0.0, 50.0, float(df[2]), step=0.1, key=f"fg{i}") / 100
            visit_pct = st.slider("% Eligible", 0, 100, df[3], key=f"fv{i}") / 100
            commission_pct = st.slider("Commission %", 0, 100, df[4], key=f"fc{i}") / 100
            fixed_fees.append({"name": fn, "fee": fee, "guest_pct": guest_pct, "visit_pct": visit_pct, "commission_pct": commission_pct})

    st.markdown("### Cost Savings")
    call_hours_monthly = st.number_input("Monthly Service Hours", value=336, min_value=0)
    hourly_wage = st.number_input("Hourly Wage ($)", value=40, min_value=1)
    call_reduction_pct = st.slider("Call Reduction %", 0, 100, 25) / 100
    daily_pages = st.number_input("Daily Pages / Room", value=5, min_value=0)
    cost_per_page = st.number_input("Cost / Page ($)", value=0.04, step=0.01, format="%.2f")
    dist_time_min = st.number_input("Distribution min / Room", value=1, min_value=0)
    print_savings_pct = st.slider("Print Savings %", 0, 100, 50) / 100

    st.markdown("### Deal Terms")
    monthly_sub = st.number_input("Monthly Subscription ($)", value=15.0, step=1.0)
    rev_share_pct = st.slider("Revenue Share %", 0, 50, 10) / 100
    device_msrp = st.number_input("Device MSRP ($)", value=180.0, step=1.0)
    device_discount = st.slider("Device Discount %", 0, 50, 22) / 100
    device_setup = st.number_input("Setup Fee ($)", value=35.0, step=1.0)
    device_life = st.number_input("Device Life (months)", value=60, min_value=1)

# ═══════════════════════════════════════════════════════════════
# CALCULATION ENGINE (unchanged logic)
# ═══════════════════════════════════════════════════════════════
device_price = device_msrp * (1 - device_discount)
monthly_device_amort = device_price / device_life
guest_days = avg_stay_nights * cycles_per_month
monthly_guests_per_cycle = rooms_per_cycle * guests_per_room * occupancy_pct

svc_savings_per_cycle = call_hours_monthly * hourly_wage * call_reduction_pct
total_svc_savings = svc_savings_per_cycle * (rooms_with_alexa / rooms_per_cycle) if rooms_per_cycle > 0 else 0
print_cost = rooms_per_cycle * guest_days * daily_pages * cost_per_page
dist_cost = rooms_per_cycle * guest_days * (dist_time_min / 60) * hourly_wage
print_savings_per_cycle = (print_cost + dist_cost) * print_savings_pct
total_print_savings = print_savings_per_cycle * (rooms_with_alexa / rooms_per_cycle) if rooms_per_cycle > 0 else 0
total_cost_savings = total_svc_savings + total_print_savings
cost_savings_per_room = total_cost_savings / rooms_with_alexa if rooms_with_alexa > 0 else 0

def calc_roi(txn_pct, inc_pct):
    pr = rooms_with_alexa if rooms_with_alexa > 0 else 1
    amenity_rev = amenity_inc = amenity_rs = amenity_cost = 0
    details = []
    for a in amenities:
        if a["pct"] <= 0: continue
        via = addressable_rev * a["pct"] * txn_pct
        inc = via * inc_pct; rs = via * rev_share_pct; co = inc * (1 - a["margin"])
        amenity_rev += via * pr; amenity_inc += inc * pr; amenity_rs += rs * pr; amenity_cost += co * pr
        details.append({"name": a["name"], "rev": via, "inc": inc, "rs": rs, "cost": co, "margin": a["margin"]})
    fixed_rev = fixed_payment = 0
    fixed_details = []
    for ff in fixed_fees:
        if ff["fee"] <= 0 and ff["commission_pct"] <= 0: continue
        me = monthly_guests_per_cycle * ff["visit_pct"] * ff["guest_pct"] * (rooms_with_alexa / rooms_per_cycle if rooms_per_cycle > 0 else 0)
        rev = me * ff["fee"] if ff["fee"] > 0 else 0; pay = rev
        if ff["commission_pct"] > 0:
            br = me * avg_stay_nights * monthly_rev_per_room / 30 if "room" in ff["name"].lower() else me * 75
            rev += br; pay += br * ff["commission_pct"]
        fixed_rev += rev; fixed_payment += pay
        fixed_details.append({"name": ff["name"], "rev": rev / pr, "payment": pay / pr})
    total_rev = amenity_rev + fixed_rev + total_cost_savings
    sub_total = monthly_sub * pr; dev_total = monthly_device_amort * pr
    total_payment = sub_total + amenity_rs + fixed_payment + dev_total
    total_inc = amenity_inc + total_cost_savings
    inc_cp = total_inc - total_payment - amenity_cost
    inv = total_payment + amenity_cost
    roi = (inc_cp / inv * 100) if inv > 0 else 0
    cm = (inc_cp / total_rev * 100) if total_rev > 0 else 0
    return {
        "total_rev": total_rev, "total_rev_room": total_rev / pr,
        "amenity_inc_room": amenity_inc / pr, "amenity_rs_room": amenity_rs / pr, "amenity_cost_room": amenity_cost / pr,
        "fixed_payment_room": fixed_payment / pr, "cost_savings_room": cost_savings_per_room,
        "sub_room": monthly_sub, "device_room": monthly_device_amort,
        "total_payment_room": total_payment / pr, "total_inc_room": total_inc / pr,
        "inc_cp": inc_cp, "inc_cp_room": inc_cp / pr, "roi": roi, "cm": cm,
        "details": details, "fixed_details": fixed_details,
        "total_payment": total_payment, "total_amenity_cost": amenity_cost,
        "monthly_sub_total": sub_total, "monthly_rev_share_total": amenity_rs,
    }

# ═══════════════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""<div class="hero-wrap">
<div class="hero-top"><div class="hero-logo">A</div><p class="hero-title">Alexa Smart Properties</p></div>
<p class="hero-partner">{partner_name}</p>
<p class="hero-sub">Return on Investment Analysis — Incremental Revenue & Cost Savings from Alexa Deployment</p>
<div class="hero-line"></div>
<p class="hero-conf">Confidential &nbsp;·&nbsp; Prepared {datetime.now().strftime('%B %d, %Y')} &nbsp;·&nbsp; For Discussion Purposes Only</p>
</div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Summary", "Live Scenario Builder", "Calculation Walkthrough", "Sensitivity Analysis"
])

# ═══════════════════════════════════════════════════════════════
# TAB 1: EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════
with tab1:
    # Scenario inputs
    st.markdown('<p class="sec-title">Scenario Assumptions</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<p class="sc-header s1">Scenario 1</p>', unsafe_allow_html=True)
        s1t = st.slider("Transactions via Alexa %", 1, 50, 8, key="e1t") / 100
        s1i = st.slider("Incrementality via Alexa %", 1, 100, 50, key="e1i") / 100
    with c2:
        st.markdown('<p class="sc-header s2">Scenario 2</p>', unsafe_allow_html=True)
        s2t = st.slider("Transactions via Alexa %", 1, 50, 10, key="e2t") / 100
        s2i = st.slider("Incrementality via Alexa %", 1, 100, 40, key="e2i") / 100
    with c3:
        st.markdown('<p class="sc-header s3">Scenario 3</p>', unsafe_allow_html=True)
        s3t = st.slider("Transactions via Alexa %", 1, 50, 15, key="e3t") / 100
        s3i = st.slider("Incrementality via Alexa %", 1, 100, 80, key="e3i") / 100

    r1, r2, r3 = calc_roi(s1t, s1i), calc_roi(s2t, s2i), calc_roi(s3t, s3i)
    ann_prop = lambda r: r["inc_cp_room"] * 12 * avg_rooms_per_alexa_property / 1000

    # Key Metrics — the money shot
    st.markdown('<p class="sec-title">Key Metrics</p>', unsafe_allow_html=True)
    for sn, r, color in [("Scenario 1", r1, "blue"), ("Scenario 2", r2, "green"), ("Scenario 3", r3, "amber")]:
        cols = st.columns([1.2, 1, 1, 1])
        with cols[0]:
            st.markdown(f"""<div class="metric-block dark">
                <p class="eyebrow">{sn} · ROI</p>
                <p class="big-num">{r['roi']:.0f}%</p>
                <p class="sub-label">Return on Investment</p></div>""", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"""<div class="metric-block light {color} accent">
                <p class="eyebrow">Monthly</p>
                <p class="big-num">${r['inc_cp_room']:,.0f}</p>
                <p class="sub-label">Incremental CP per Room</p></div>""", unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f"""<div class="metric-block light {color}">
                <p class="eyebrow">Annual</p>
                <p class="big-num">${r['inc_cp_room']*12:,.0f}</p>
                <p class="sub-label">per Room</p></div>""", unsafe_allow_html=True)
        with cols[3]:
            st.markdown(f"""<div class="metric-block light {color}">
                <p class="eyebrow">Annual</p>
                <p class="big-num">${ann_prop(r):,.0f}K</p>
                <p class="sub-label">per Property (in 000s)</p></div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Insight
    best = max([r1, r2, r3], key=lambda x: x["roi"])
    st.markdown(f"""<div class="insight-box">
        <p class="ib-label">Key Takeaway</p>
        <p class="ib-text">Alexa deployment generates up to ${best['inc_cp_room']*12:,.0f} in annual incremental profit per room — translating to ${ann_prop(best):,.0f}K per property annually.</p>
        <p class="ib-sub">Based on {int(avg_rooms_per_alexa_property):,} rooms per property across {alexa_properties} properties with Alexa</p>
    </div>""", unsafe_allow_html=True)

    # Value Bridge (Waterfall) — Scenario 2
    st.markdown('<p class="sec-title">Value Bridge — Scenario 2 (Monthly per Room)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-subtitle">How Alexa creates incremental value: from revenue generation through to net contribution profit</p>', unsafe_allow_html=True)
    wf = go.Figure(go.Waterfall(
        x=["Incremental<br>Amenity Revenue", "Operational<br>Cost Savings", "Payment<br>to Alexa", "Incremental<br>Amenity Costs", "Net Incremental<br>Contribution Profit"],
        y=[r2["amenity_inc_room"], r2["cost_savings_room"], -r2["total_payment_room"], -r2["amenity_cost_room"], r2["inc_cp_room"]],
        measure=["absolute", "relative", "relative", "relative", "total"],
        connector=dict(line=dict(color="#d0d5dd", width=1, dash="dot")),
        increasing=dict(marker=dict(color="#0a8f6c")), decreasing=dict(marker=dict(color="#c7511f")),
        totals=dict(marker=dict(color="#FF9900")),
        text=[f"${v:,.0f}" for v in [r2["amenity_inc_room"], r2["cost_savings_room"], -r2["total_payment_room"], -r2["amenity_cost_room"], r2["inc_cp_room"]]],
        textposition="outside", textfont=dict(size=14, family="Inter", color="#0d1b2a"),
    ))
    wf.update_layout(height=440, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#f0f2f5", zeroline=True, zerolinecolor="#d0d5dd", title="", showticklabels=True, tickfont=dict(size=11, color="#8896a4")),
        xaxis=dict(tickfont=dict(size=12, family="Inter", color="#0d1b2a")),
        margin=dict(t=20, b=60, l=60, r=20), font=dict(family="Inter"))
    st.plotly_chart(wf, use_container_width=True)

    # Comparison bar chart
    st.markdown('<p class="sec-title">Annual Incremental Contribution Profit</p>', unsafe_allow_html=True)
    fig_bar = go.Figure()
    for sn, r, color in [("Scenario 1", r1, "#0052cc"), ("Scenario 2", r2, "#0a8f6c"), ("Scenario 3", r3, "#FF9900")]:
        fig_bar.add_trace(go.Bar(
            name=sn, x=["Per Room", "Per Property (000s)"],
            y=[r["inc_cp_room"] * 12, ann_prop(r)],
            marker=dict(color=color, line=dict(width=0)),
            text=[f"${r['inc_cp_room']*12:,.0f}", f"${ann_prop(r):,.0f}K"],
            textposition="outside", textfont=dict(size=13, family="Inter"),
        ))
    fig_bar.update_layout(barmode="group", height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#f0f2f5", title="", tickfont=dict(size=11, color="#8896a4")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=12)),
        margin=dict(t=50, b=40), font=dict(family="Inter"))
    st.plotly_chart(fig_bar, use_container_width=True)

    # Detailed table
    st.markdown('<p class="sec-title">Detailed Financial Summary</p>', unsafe_allow_html=True)
    def fv(v): return f"${v:,.0f}"
    def build_cols(r, tp, ip):
        return [
            (f"{tp*100:.0f}%",)*3, (f"{ip*100:.0f}%",)*3, ("",)*3,
            tuple(fv(r["total_rev_room"]*m) for m in [1, 12, 12*avg_rooms_per_alexa_property/1000]),
            tuple(fv(r["total_inc_room"]*m) for m in [1, 12, 12*avg_rooms_per_alexa_property/1000]),
            tuple(fv(r["amenity_inc_room"]*m) for m in [1, 12, 12*avg_rooms_per_alexa_property/1000]),
            tuple(fv(r["cost_savings_room"]*m) for m in [1, 12, 12*avg_rooms_per_alexa_property/1000]),
            tuple(fv(-r["total_payment_room"]*m) for m in [1, 12, 12*avg_rooms_per_alexa_property/1000]),
            tuple(fv(-r["sub_room"]*m) for m in [1, 12, 12*avg_rooms_per_alexa_property/1000]),
            tuple(fv(-r["amenity_rs_room"]*m) for m in [1, 12, 12*avg_rooms_per_alexa_property/1000]),
            tuple(fv(-r["amenity_cost_room"]*m) for m in [1, 12, 12*avg_rooms_per_alexa_property/1000]),
            ("",)*3,
            tuple(fv(r["inc_cp_room"]*m) for m in [1, 12, 12*avg_rooms_per_alexa_property/1000]),
            (f"{r['roi']:.0f}%",)*3,
        ]
    labels = ["Transactions via Alexa", "Incrementality via Alexa", "",
              "Total Revenue", "Alexa Benefits", "  Incremental Amenities Revenue", "  Cost Saving",
              "Total Payment to Alexa", "  Fixed Subscription Fee", "  Rev-Share Payments",
              "Incremental Amenities Cost", "", "Incremental CP", "ROI %"]
    sc1, sc2, sc3 = build_cols(r1,s1t,s1i), build_cols(r2,s2t,s2i), build_cols(r3,s3t,s3i)
    rows = []
    for i, lb in enumerate(labels):
        rows.append({"": lb,
            "S1 Monthly": sc1[i][0], "S1 Annual": sc1[i][1], "S1 Property": sc1[i][2],
            "S2 Monthly": sc2[i][0], "S2 Annual": sc2[i][1], "S2 Property": sc2[i][2],
            "S3 Monthly": sc3[i][0], "S3 Annual": sc3[i][1], "S3 Property": sc3[i][2]})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True, height=560)

# ═══════════════════════════════════════════════════════════════
# TAB 2: LIVE SCENARIO BUILDER
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="sec-title">Live Scenario Builder</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-subtitle">Adjust parameters in real-time during partner discussions</p>', unsafe_allow_html=True)

    lc1, lc2 = st.columns([1, 2.5])
    with lc1:
        live_txn = st.slider("Transactions via Alexa %", 1, 50, 10, key="lt") / 100
        live_inc = st.slider("Incrementality via Alexa %", 1, 100, 50, key="li") / 100
    live_r = calc_roi(live_txn, live_inc)

    with lc2:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""<div class="metric-block dark"><p class="eyebrow">ROI</p>
                <p class="big-num">{live_r['roi']:.0f}%</p></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="metric-block light green accent"><p class="eyebrow">Monthly / Room</p>
                <p class="big-num">${live_r['inc_cp_room']:,.0f}</p></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="metric-block light blue"><p class="eyebrow">Annual / Room</p>
                <p class="big-num">${live_r['inc_cp_room']*12:,.0f}</p></div>""", unsafe_allow_html=True)
        with m4:
            ap = live_r['inc_cp_room'] * 12 * avg_rooms_per_alexa_property / 1000
            st.markdown(f"""<div class="metric-block light amber"><p class="eyebrow">Annual / Property</p>
                <p class="big-num">${ap:,.0f}K</p></div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if live_r["details"]:
            st.markdown("**Revenue by Amenity (Monthly per Room)**")
            st.dataframe(pd.DataFrame([{"Amenity": d["name"], "Revenue": f"${d['rev']:,.0f}", "Incremental": f"${d['inc']:,.0f}",
                "Rev-Share": f"${d['rs']:,.0f}", "Cost": f"${d['cost']:,.0f}"} for d in live_r["details"]]),
                use_container_width=True, hide_index=True)

        wf2 = go.Figure(go.Waterfall(
            x=["Benefits", "Payment", "Costs", "Net CP"],
            y=[live_r["total_inc_room"], -live_r["total_payment_room"], -live_r["amenity_cost_room"], live_r["inc_cp_room"]],
            measure=["absolute","relative","relative","total"],
            connector=dict(line=dict(color="#d0d5dd", dash="dot")),
            increasing=dict(marker=dict(color="#0a8f6c")), decreasing=dict(marker=dict(color="#c7511f")),
            totals=dict(marker=dict(color="#FF9900")),
            text=[f"${v:,.0f}" for v in [live_r["total_inc_room"], -live_r["total_payment_room"], -live_r["amenity_cost_room"], live_r["inc_cp_room"]]],
            textposition="outside", textfont=dict(size=13, family="Inter"),
        ))
        wf2.update_layout(height=360, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="#f0f2f5"), margin=dict(t=20, b=40), font=dict(family="Inter"))
        st.plotly_chart(wf2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# TAB 3: CALCULATION WALKTHROUGH
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="sec-title">Calculation Walkthrough</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-subtitle">Step-by-step verification of the ROI model logic</p>', unsafe_allow_html=True)

    wc1, wc2 = st.columns(2)
    with wc1: wt = st.slider("Transaction %", 1, 30, 8, key="wt") / 100
    with wc2: wi = st.slider("Incrementality %", 10, 100, 50, key="wi") / 100
    wr = calc_roi(wt, wi)

    st.markdown(f"**Step 1** — Addressable Revenue = ${monthly_rev_per_room:,.0f} × (1 − {pre_boarding_pct*100:.0f}%) = **${addressable_rev:,.0f}** / room / month")
    st.markdown("**Step 2** — Amenity Revenue via Alexa")
    st.dataframe(pd.DataFrame([{"Amenity": d["name"], "Mix": f"{[a for a in amenities if a['name']==d['name']][0]['pct']*100:.0f}%" if [a for a in amenities if a['name']==d['name']] else "—",
        "Cat Rev": f"${addressable_rev * ([a for a in amenities if a['name']==d['name']][0]['pct'] if [a for a in amenities if a['name']==d['name']] else 0):,.0f}",
        f"×{wt*100:.0f}% Txn": f"${d['rev']:,.0f}", f"×{wi*100:.0f}% Inc": f"${d['inc']:,.0f}",
        "Rev-Share": f"${d['rs']:,.0f}", "Cost": f"${d['cost']:,.0f}"} for d in wr["details"]]),
        use_container_width=True, hide_index=True)

    st.markdown("**Step 3** — Cost Savings")
    cs1, cs2 = st.columns(2)
    with cs1: st.metric("Guest Service Savings", f"${total_svc_savings:,.0f}/mo")
    with cs2: st.metric("Printing Savings", f"${total_print_savings:,.0f}/mo")

    st.markdown("**Step 4** — Payment to Alexa")
    st.dataframe(pd.DataFrame([
        {"Item": "Subscription", "Per Room": f"${monthly_sub:,.0f}"},
        {"Item": "Rev-Share", "Per Room": f"${wr['amenity_rs_room']:,.0f}"},
        {"Item": "Fixed Fees", "Per Room": f"${wr['fixed_payment_room']:,.0f}"},
        {"Item": "Device", "Per Room": f"${monthly_device_amort:,.2f}"},
        {"Item": "Total", "Per Room": f"${wr['total_payment_room']:,.0f}"},
    ]), use_container_width=True, hide_index=True)

    st.markdown(f"""**Step 5** — ROI Calculation
- Benefits: **${wr['total_inc_room']:,.0f}** / room
- Payment: **${wr['total_payment_room']:,.0f}** / room
- Amenity Cost: **${wr['amenity_cost_room']:,.0f}** / room
- **CP = ${wr['total_inc_room']:,.0f} − ${wr['total_payment_room']:,.0f} − ${wr['amenity_cost_room']:,.0f} = ${wr['inc_cp_room']:,.0f}**
- **ROI = {wr['roi']:.0f}%**""")

# ═══════════════════════════════════════════════════════════════
# TAB 4: SENSITIVITY ANALYSIS
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<p class="sec-title">Sensitivity Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-subtitle">Impact of varying transaction adoption and incrementality on returns</p>', unsafe_allow_html=True)

    sc1, _ = st.columns([1, 3])
    with sc1:
        si = st.slider("Incrementality %", 10, 100, 50, step=5, key="si") / 100
    txns = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.25]
    sr = [calc_roi(t, si) for t in txns]
    st.dataframe(pd.DataFrame({
        "Txn %": [f"{t*100:.0f}%" for t in txns], "Revenue/Room": [f"${r['total_rev_room']:,.0f}" for r in sr],
        "CP/Room": [f"${r['inc_cp_room']:,.0f}" for r in sr], "CM %": [f"{r['cm']:.0f}%" for r in sr],
        "ROI %": [f"{r['roi']:.0f}%" for r in sr],
    }), use_container_width=True, hide_index=True)

    # Heatmaps
    st.markdown('<p class="sec-title">CP per Room Heatmap</p>', unsafe_allow_html=True)
    txn_ax = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28]
    inc_ax = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
    cp_h = [[round(calc_roi(t, i)["inc_cp_room"], 0) for t in txn_ax] for i in inc_ax]
    roi_h = [[round(calc_roi(t, i)["roi"], 0) for t in txn_ax] for i in inc_ax]

    fig_cp = go.Figure(data=go.Heatmap(
        z=cp_h, x=[f"{t*100:.0f}%" for t in txn_ax], y=[f"{i*100:.0f}%" for i in inc_ax],
        colorscale=[[0,"#c7511f"],[0.25,"#fdebd0"],[0.45,"#f5f5f5"],[0.6,"#d5f5e3"],[1,"#0a8f6c"]],
        text=[[f"${v:,.0f}" for v in row] for row in cp_h], texttemplate="%{text}",
        textfont=dict(size=10, family="Inter"), colorbar=dict(title="$/Room", titlefont=dict(size=11)), zmid=0,
    ))
    fig_cp.update_layout(height=480, xaxis_title="Transactions via Alexa %", yaxis_title="Incrementality via Alexa %",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter", size=12),
        margin=dict(t=20, b=60))
    st.plotly_chart(fig_cp, use_container_width=True)

    st.markdown('<p class="sec-title">ROI % Heatmap</p>', unsafe_allow_html=True)
    fig_roi = go.Figure(data=go.Heatmap(
        z=roi_h, x=[f"{t*100:.0f}%" for t in txn_ax], y=[f"{i*100:.0f}%" for i in inc_ax],
        colorscale=[[0,"#c7511f"],[0.25,"#fdebd0"],[0.45,"#f5f5f5"],[0.6,"#d5f5e3"],[1,"#0a8f6c"]],
        text=[[f"{v:.0f}%" for v in row] for row in roi_h], texttemplate="%{text}",
        textfont=dict(size=10, family="Inter"), colorbar=dict(title="ROI %", titlefont=dict(size=11)), zmid=0,
    ))
    fig_roi.update_layout(height=480, xaxis_title="Transactions via Alexa %", yaxis_title="Incrementality via Alexa %",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter", size=12),
        margin=dict(t=20, b=60))
    st.plotly_chart(fig_roi, use_container_width=True)

    # Payment sensitivity
    st.markdown('<p class="sec-title">Monthly Payment per Room Sensitivity</p>', unsafe_allow_html=True)
    rs_ax = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.15]
    pay_h = []
    for rs in rs_ax:
        row = []
        for t in txn_ax:
            ap = addressable_rev * sum(a["pct"] for a in amenities if a["pct"] > 0) * t * rs
            tp = monthly_sub + ap + monthly_device_amort
            for ff in fixed_fees:
                if ff["fee"] > 0:
                    me = monthly_guests_per_cycle * ff["visit_pct"] * ff["guest_pct"] / rooms_per_cycle if rooms_per_cycle > 0 else 0
                    tp += me * ff["fee"]
            row.append(round(tp, 0))
        pay_h.append(row)
    fig_pay = go.Figure(data=go.Heatmap(
        z=pay_h, x=[f"{t*100:.0f}%" for t in txn_ax], y=[f"{r*100:.0f}%" for r in rs_ax],
        colorscale="YlOrRd", text=[[f"${v:,.0f}" for v in row] for row in pay_h],
        texttemplate="%{text}", textfont=dict(size=10, family="Inter"), colorbar=dict(title="$/Room"),
    ))
    fig_pay.update_layout(height=380, xaxis_title="Transaction %", yaxis_title="Rev Share %",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter"),
        margin=dict(t=20, b=60))
    st.plotly_chart(fig_pay, use_container_width=True)

# Footer
st.markdown(f"""<div class="footer">
<p class="f-brand">Alexa Smart Properties</p>
<p class="f-sub">{partner_name} &nbsp;·&nbsp; Confidential &nbsp;·&nbsp; {datetime.now().strftime('%B %d, %Y')}</p></div>""", unsafe_allow_html=True)
