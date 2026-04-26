import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="ASP Partner ROI Calculator", layout="wide", page_icon="🔶", initial_sidebar_state="expanded")

# ── Alexa Pitch Deck Theme — Dark BG + High Contrast Interactive ──
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
#MainMenu,footer{visibility:hidden}
html,body,[class*="css"]{font-family:'Inter','Amazon Ember',sans-serif}

/* Dark background matching Alexa deck */
.stApp{background:#0b1120}

/* Hero - Alexa deck gradient with blue glow */
.hero{background:linear-gradient(135deg,#080c18 0%,#0a1128 40%,#0d2847 80%,#1a5276 100%);border-radius:16px;padding:40px 48px;margin-bottom:32px;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;bottom:-40%;right:-10%;width:400px;height:400px;background:radial-gradient(circle,rgba(126,184,218,.12) 0%,transparent 70%);border-radius:50%}
.hero::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#FF9900,#FFB84D,#FF9900)}
.hero h1{color:#FFF;font-size:30px;margin:0 0 6px;font-weight:800;letter-spacing:-.5px;position:relative}
.hero .sub{color:#4ECDC4;font-size:16px;margin:0;font-weight:600;position:relative}
.hero .meta{color:rgba(255,255,255,.35);font-size:10px;margin-top:12px;position:relative;letter-spacing:1.5px;text-transform:uppercase}

/* KPI Cards - elevated dark cards with glow borders */
.kpi-big{background:linear-gradient(145deg,#111d33,#162544);border-radius:14px;padding:26px 20px;text-align:center;border:1px solid rgba(255,255,255,.08);box-shadow:0 4px 24px rgba(0,0,0,.3);transition:all .3s cubic-bezier(.4,0,.2,1)}
.kpi-big:hover{transform:translateY(-4px);box-shadow:0 12px 40px rgba(78,205,196,.08);border-color:rgba(78,205,196,.15)}
.kpi-big .value{font-size:36px;font-weight:800;margin:0;line-height:1.1;letter-spacing:-.5px;color:#fff}
.kpi-big .label{color:#8a9bb0;font-size:11px;margin:8px 0 0;text-transform:uppercase;letter-spacing:.8px;font-weight:600;white-space:nowrap}
.kpi-big .delta{font-size:13px;margin-top:6px;font-weight:600}
.kpi-big.green .value{color:#4ECDC4}.kpi-big.green{border-bottom:3px solid #4ECDC4}
.kpi-big.blue .value{color:#4ECDC4}.kpi-big.blue{border-bottom:3px solid #4ECDC4}
.kpi-big.orange .value{color:#FFB84D}.kpi-big.orange{border-bottom:3px solid #4ECDC4}
.kpi-big.hero-card{background:linear-gradient(135deg,#FF9900,#e68a00);border:none;box-shadow:0 8px 32px rgba(255,153,0,.2)}
.kpi-big.hero-card .value{color:#fff;font-size:42px;text-shadow:0 2px 12px rgba(0,0,0,.3)}.kpi-big.hero-card .label{color:rgba(255,255,255,.85)}

/* Scenario Cards */
.scenario-card{background:rgba(17,29,51,.6);border-radius:14px;padding:20px 24px;border:1px solid rgba(255,255,255,.06)}
.scenario-card .tag{display:inline-block;padding:5px 16px;border-radius:8px;font-size:14px;font-weight:700;letter-spacing:.3px;white-space:nowrap}
.tag-s1{background:rgba(126,184,218,.12);color:#4ECDC4;border:1px solid rgba(126,184,218,.25)}
.tag-s2{background:rgba(0,230,118,.12);color:#4ECDC4;border:1px solid rgba(0,230,118,.25)}
.tag-s3{background:rgba(255,153,0,.12);color:#FF9900;border:1px solid rgba(255,153,0,.25)}

/* Section Headers - cyan accent */
.stitle{font-size:13px;text-transform:uppercase;letter-spacing:2px;font-weight:800;color:#7EB8DA;border-left:4px solid #7EB8DA;padding-left:14px;margin:36px 0 10px}
.stitle-sub{font-size:14px;color:#8a9bb0;margin:0 0 20px 18px;font-weight:400}

/* Insight Box - slightly elevated dark */
.insight{background:linear-gradient(135deg,#111d33,#162544);border-radius:14px;padding:28px 32px;margin:24px 0;position:relative;border:1px solid rgba(126,184,218,.12);box-shadow:0 4px 20px rgba(0,0,0,.2)}
.insight::before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,#4ECDC4,#7EB8DA);border-radius:4px 0 0 4px}
.insight .headline{font-size:18px;font-weight:700;color:#fff;margin:0 0 6px;line-height:1.4}
.insight .body{font-size:13px;color:#8a9bb0;margin:0}

/* Sidebar */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#060a14,#0a1128)}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span{color:#8a9bb0!important}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3{color:#4ECDC4!important}
[data-testid="stSidebar"] label{color:#8a9bb0!important}

/* Tabs - dark with cyan active */
.stTabs [data-baseweb="tab-list"]{gap:0;border-bottom:2px solid rgba(255,255,255,.08);background:transparent}
.stTabs [data-baseweb="tab"]{font-weight:600;font-size:13px;padding:14px 28px;color:#6a7d90;border-bottom:3px solid transparent;margin-bottom:-2px;background:transparent}
.stTabs [aria-selected="true"]{color:#7EB8DA!important;border-bottom:3px solid #7EB8DA!important;background:transparent!important}

/* Tables */
[data-testid="stDataFrame"]{border-radius:10px;overflow:hidden}

/* Sliders */
.stSlider>div>div>div>div{background:#4ECDC4!important}

/* Text colors for dark bg */
[data-testid="stMetricValue"]{color:#fff!important}
[data-testid="stMetricLabel"]{color:#8a9bb0!important}
.stMarkdown p,.stMarkdown li{color:#c8d6e0}
.stMarkdown strong{color:#fff}
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3,.stMarkdown h4{color:#fff}

/* Footer */
.app-footer{background:linear-gradient(135deg,#060a14,#0a1128);border-radius:14px;padding:24px 36px;margin-top:48px;text-align:center;border-top:1px solid rgba(78,205,196,.1)}
.app-footer .brand{color:#7EB8DA;font-size:13px;font-weight:700;margin:0;letter-spacing:2px;text-transform:uppercase}
.app-footer .sub{color:rgba(255,255,255,.3);font-size:11px;margin:6px 0 0}
</style>""", unsafe_allow_html=True)

def kpi(v, l, c="", delta=""):
    d = f'<p class="delta" style="color:{("#0a8f6c" if "+" in str(delta) or delta=="" else "#c7511f")}">{delta}</p>' if delta else ""
    return f'<div class="kpi-big {c}"><p class="value">{v}</p><p class="label">{l}</p>{d}</div>'

# ═══════════════════════════════════════════════════════════════
# SIDEBAR — ALL INPUTS
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Deal Inputs")
    partner_name = st.text_input("Partner Name", "Holland America Line")

    st.markdown("### 🏨 Property Metrics")
    total_properties = st.number_input("Total Properties / Ships", value=11, min_value=1)
    total_rooms = st.number_input("Total Rooms / Staterooms", value=11394, min_value=1)
    avg_rooms_property = st.number_input("Avg Rooms per Property", value=int(total_rooms / total_properties) if total_properties > 0 else 1036, min_value=1)
    occupancy_pct = st.slider("Occupancy %", 50, 100, 96) / 100
    avg_stay_nights = st.number_input("Avg Guest Stay (nights)", value=7, min_value=1)
    cycles_per_month = st.number_input("Cruises / Cycles per Month", value=4, min_value=1)
    guests_per_room = st.number_input("Guests per Room", value=2.0, step=0.1)

    st.markdown("### 📺 Projected Alexa Deployment")
    alexa_properties = st.number_input("Properties / Ships with Alexa", value=5, min_value=1)
    rooms_with_alexa = st.number_input("Total Rooms with Alexa", value=2500, min_value=1)
    rooms_per_cycle = st.number_input("Rooms per Cruise / Cycle", value=500, min_value=1)
    avg_rooms_per_alexa_property = rooms_with_alexa / alexa_properties if alexa_properties > 0 else rooms_with_alexa
    st.caption(f"Avg rooms per Alexa property: **{avg_rooms_per_alexa_property:,.0f}**")

    st.markdown("### 💵 Revenue Inputs")
    rev_method = st.radio("Revenue Input Method", ["Total Annual Revenue", "Average Revenue per Room"], index=0)
    if rev_method == "Total Annual Revenue":
        total_annual_rev = st.number_input("Total Annual Onboard / Ancillary Revenue ($)", value=800_000_000, step=1_000_000, format="%d")
        # Pro-rate: Alexa rooms share of total rooms
        alexa_share = rooms_with_alexa / total_rooms if total_rooms > 0 else 1
        alexa_annual_rev = total_annual_rev * alexa_share
        monthly_rev_per_room = total_annual_rev / total_rooms / 12 if total_rooms > 0 else 0
        st.caption(f"Monthly revenue/room: **${monthly_rev_per_room:,.0f}** | Alexa share: **{alexa_share*100:.1f}%**")
    else:
        total_annual_rev = 0
        monthly_rev_per_room = st.number_input("Avg Monthly Revenue per Room ($)", value=10000, min_value=1)
        st.caption(f"Monthly revenue/room: **${monthly_rev_per_room:,.0f}**")

    pre_boarding_pct = st.slider("Pre-boarding / Pre-arrival Revenue %", 0, 100, 60) / 100
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
st.markdown(f"""<div class="hero">
<div style="display:flex;align-items:center;gap:24px">
<div style="flex:1">
<h1>🔶 Alexa Smart Properties</h1>
<p class="sub">{partner_name} — Return on Investment Analysis</p>
<p class="meta">CONFIDENTIAL — For Partner Discussion Only &nbsp;·&nbsp; {datetime.now().strftime('%B %d, %Y')}</p>
</div>
<div style="flex:0 0 auto">
<img src="https://m.media-amazon.com/images/I/61fBMR-yURL._AC_SL1000_.jpg" style="height:120px;border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,.3)" alt="Echo Show 15">
</div>
</div>
</div>""", unsafe_allow_html=True)

# Sidebar toggle is in the Streamlit header (top-left)

tab1, tab2, tab3, tab4 = st.tabs([
    "  📋 Executive Summary  ", "  🎮 Live Scenario Builder  ",
    "  🔢 Calculation Walkthrough  ", "  📊 Sensitivity Analysis  "
])

# ─── TAB 1: EXECUTIVE SUMMARY ───
with tab1:
    st.markdown(f'<div class="stitle">{partner_name} — ROI Summary</div>', unsafe_allow_html=True)
    st.markdown('<p class="stitle-sub">Three scenarios modeling Alexa deployment impact on incremental revenue and profitability</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="scenario-card"><span class="tag tag-s1">SCENARIO 1</span>', unsafe_allow_html=True)
        s1t = st.slider("Transactions via Alexa %", 1, 50, 8, key="e1t") / 100
        s1i = st.slider("Incrementality via Alexa %", 1, 100, 50, key="e1i") / 100
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="scenario-card"><span class="tag tag-s2">SCENARIO 2</span>', unsafe_allow_html=True)
        s2t = st.slider("Transactions via Alexa %", 1, 50, 10, key="e2t") / 100
        s2i = st.slider("Incrementality via Alexa %", 1, 100, 40, key="e2i") / 100
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="scenario-card"><span class="tag tag-s3">SCENARIO 3</span>', unsafe_allow_html=True)
        s3t = st.slider("Transactions via Alexa %", 1, 50, 15, key="e3t") / 100
        s3i = st.slider("Incrementality via Alexa %", 1, 100, 80, key="e3i") / 100
        st.markdown('</div>', unsafe_allow_html=True)

    r1, r2, r3 = calc_roi(s1t, s1i), calc_roi(s2t, s2i), calc_roi(s3t, s3i)
    ann_prop = lambda r: r["inc_cp_room"] * 12 * avg_rooms_per_alexa_property / 1000

    # Hero ROI cards — the money shot
    st.markdown("---")
    st.markdown(f'<div class="stitle">Incremental Contribution Profit</div>', unsafe_allow_html=True)

    for sn, r, tag, color in [("Scenario 1", r1, "tag-s1", "blue"), ("Scenario 2", r2, "tag-s2", "green"), ("Scenario 3", r3, "tag-s3", "orange")]:
        st.markdown(f'<span class="tag {tag}" style="margin-bottom:8px;display:inline-block">{sn}</span>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(kpi(f"{r['roi']:.0f}%", "Return on Investment", "hero-card" if r['roi'] > 30 else f"{color}"), unsafe_allow_html=True)
        with k2: st.markdown(kpi(f"${r['inc_cp_room']:,.0f}", "Monthly per Room", color), unsafe_allow_html=True)
        with k3: st.markdown(kpi(f"${r['inc_cp_room']*12:,.0f}", "Annual per Room", color), unsafe_allow_html=True)
        with k4: st.markdown(kpi(f"${ann_prop(r):,.0f}K", "Annual per Property (000s)", color), unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Insight callout
    best = max([r1, r2, r3], key=lambda x: x["roi"])
    st.markdown(f"""<div class="insight">
    <p style="font-size:10px;text-transform:uppercase;letter-spacing:2px;color:#7EB8DA;font-weight:700;margin:0 0 8px">💡 Key Takeaway</p>
    <p class="headline">Alexa deployment generates up to ${best['inc_cp_room']*12:,.0f} in annual incremental profit per room — translating to ${ann_prop(best):,.0f}K per property annually.</p>
    <p class="body">Based on {int(avg_rooms_per_alexa_property):,} rooms per property across {alexa_properties} properties with Alexa</p>
    </div>""", unsafe_allow_html=True)

    # Visual: ROI comparison gauge chart
    st.markdown(f'<div class="stitle">ROI Comparison</div>', unsafe_allow_html=True)
    fig_gauge = go.Figure()
    for i, (sn, r, color) in enumerate([("Scenario 1", r1, "#7EB8DA"), ("Scenario 2", r2, "#4ECDC4"), ("Scenario 3", r3, "#FF9900")]):
        fig_gauge.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=r["roi"],
            title={"text": sn, "font": {"size": 16, "color": "#232F3E"}},
            number={"suffix": "%", "font": {"size": 32, "color": "#232F3E"}},
            gauge={
                "axis": {"range": [0, max(150, r["roi"] + 30)], "tickcolor": "rgba(255,255,255,.2)"},
                "bar": {"color": color, "thickness": 0.7},
                "bgcolor": "#111d33",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 20], "color": "#2d1515"},
                    {"range": [20, 50], "color": "#2d2a15"},
                    {"range": [50, 150], "color": "#152d1a"},
                ],
                "threshold": {"line": {"color": "#232F3E", "width": 2}, "thickness": 0.8, "value": r["roi"]},
            },
            domain={"row": 0, "column": i},
        ))
    fig_gauge.update_layout(
        grid={"rows": 1, "columns": 3, "pattern": "independent"},
        height=320, margin=dict(t=60, b=20, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Revenue waterfall — tells the story
    st.markdown(f'<div class="stitle">Value Creation Waterfall — Scenario 2 (Monthly per Room)</div>', unsafe_allow_html=True)
    wf_labels = ["Incremental<br>Revenue", "Cost<br>Savings", "Payment<br>to Alexa", "Amenity<br>Costs", "Net Incremental<br>Profit"]
    wf_vals = [r2["amenity_inc_room"], r2["cost_savings_room"], -r2["total_payment_room"], -r2["amenity_cost_room"], r2["inc_cp_room"]]
    fig_wf = go.Figure(go.Waterfall(
        x=wf_labels, y=wf_vals, measure=["absolute", "relative", "relative", "relative", "total"],
        connector=dict(line=dict(color="rgba(255,255,255,.15)", width=1, dash="dot")),
        increasing=dict(marker=dict(color="#4ECDC4")),
        decreasing=dict(marker=dict(color="#FF5252")),
        totals=dict(marker=dict(color="#4ECDC4")),
        text=[f"${v:,.0f}" for v in wf_vals], textposition="outside",
        textfont=dict(size=14, color="#e0e6ed", family="Inter"),
    ))
    fig_wf.update_layout(height=420, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                         yaxis=dict(gridcolor="#eef0f3", title="$ per Room / Month", title_font=dict(size=12, color="#8896a4")),
                         margin=dict(t=20, b=40), font=dict(family="Inter"))
    st.plotly_chart(fig_wf, use_container_width=True)

    # Detailed Comparison — 3 cards: Monthly/Room, Annual/Room, Annual/Property
    st.markdown(f'<div class="stitle">Detailed Comparison</div>', unsafe_allow_html=True)
    def f(v): return f"${v:,.0f}"
    ap = avg_rooms_per_alexa_property

    detail_metrics = [
        ("Transactions via Alexa", f"{s1t*100:.0f}%", f"{s2t*100:.0f}%", f"{s3t*100:.0f}%", f"{s1t*100:.0f}%", f"{s2t*100:.0f}%", f"{s3t*100:.0f}%", f"{s1t*100:.0f}%", f"{s2t*100:.0f}%", f"{s3t*100:.0f}%"),
        ("Incrementality via Alexa", f"{s1i*100:.0f}%", f"{s2i*100:.0f}%", f"{s3i*100:.0f}%", f"{s1i*100:.0f}%", f"{s2i*100:.0f}%", f"{s3i*100:.0f}%", f"{s1i*100:.0f}%", f"{s2i*100:.0f}%", f"{s3i*100:.0f}%"),
    ]
    fin_metrics = [
        ("Total Revenue", [r1["total_rev_room"], r2["total_rev_room"], r3["total_rev_room"]]),
        ("Alexa Benefits", [r1["total_inc_room"], r2["total_inc_room"], r3["total_inc_room"]]),
        ("  ↳ Incremental Amenities Revenue", [r1["amenity_inc_room"], r2["amenity_inc_room"], r3["amenity_inc_room"]]),
        ("  ↳ Cost Saving", [r1["cost_savings_room"], r2["cost_savings_room"], r3["cost_savings_room"]]),
        ("Total Payment to Alexa", [-r1["total_payment_room"], -r2["total_payment_room"], -r3["total_payment_room"]]),
        ("  ↳ Fixed Subscription Fee", [-r1["sub_room"], -r2["sub_room"], -r3["sub_room"]]),
        ("  ↳ Rev-Share Payments", [-r1["amenity_rs_room"], -r2["amenity_rs_room"], -r3["amenity_rs_room"]]),
        ("Incremental Amenities Cost", [-r1["amenity_cost_room"], -r2["amenity_cost_room"], -r3["amenity_cost_room"]]),
    ]
    bottom_metrics = [
        ("Incremental CP", [r1["inc_cp_room"], r2["inc_cp_room"], r3["inc_cp_room"]]),
    ]
    roi_row = ("ROI %", [f"{r1['roi']:.0f}%", f"{r2['roi']:.0f}%", f"{r3['roi']:.0f}%"])

    def build_card_table(title, multiplier, is_thousands=False):
        """Build an HTML table card for a given time period."""
        div = 1000 if is_thousands else 1
        rows_html = ""
        # Assumption rows
        for label, s1v, s2v, s3v, *_ in detail_metrics:
            rows_html += f'<tr><td style="text-align:left;font-weight:500;padding:6px 12px;border-bottom:1px solid rgba(255,255,255,.06);color:rgba(255,255,255,.65)">{label}</td><td style="text-align:right;padding:6px 12px;border-bottom:1px solid rgba(255,255,255,.06);color:#fff">{s1v}</td><td style="text-align:right;padding:6px 12px;border-bottom:1px solid rgba(255,255,255,.06);color:#fff">{s2v}</td><td style="text-align:right;padding:6px 12px;border-bottom:1px solid rgba(255,255,255,.06);color:#fff">{s3v}</td></tr>'
        # Spacer
        rows_html += '<tr><td colspan="4" style="padding:4px"></td></tr>'
        # Financial rows
        for label, vals in fin_metrics:
            s1 = f"${vals[0]*multiplier/div:,.0f}"
            s2 = f"${vals[1]*multiplier/div:,.0f}"
            s3 = f"${vals[2]*multiplier/div:,.0f}"
            indent = "padding-left:24px;color:#9aacbc" if label.startswith("  ") else "font-weight:500;color:rgba(255,255,255,.65)"
            val_color = "rgba(255,255,255,.7)" if any(v < 0 for v in vals) else "#fff"
            rows_html += f'<tr><td style="text-align:left;{indent};padding:6px 12px;border-bottom:1px solid rgba(255,255,255,.06)">{label}</td><td style="text-align:right;padding:6px 12px;border-bottom:1px solid rgba(255,255,255,.06);color:{val_color}">{s1}</td><td style="text-align:right;padding:6px 12px;border-bottom:1px solid rgba(255,255,255,.06);color:{val_color}">{s2}</td><td style="text-align:right;padding:6px 12px;border-bottom:1px solid rgba(255,255,255,.06);color:{val_color}">{s3}</td></tr>'
        # Spacer
        rows_html += '<tr><td colspan="4" style="padding:4px"></td></tr>'
        # CP row (bold)
        for label, vals in bottom_metrics:
            s1 = f"${vals[0]*multiplier/div:,.0f}"
            s2 = f"${vals[1]*multiplier/div:,.0f}"
            s3 = f"${vals[2]*multiplier/div:,.0f}"
            rows_html += f'<tr style="border-top:2px solid #4ECDC4"><td style="text-align:left;font-weight:800;padding:8px 12px;color:#fff">{label}</td><td style="text-align:right;font-weight:800;padding:8px 12px;color:#4ECDC4">{s1}</td><td style="text-align:right;font-weight:800;padding:8px 12px;color:#4ECDC4">{s2}</td><td style="text-align:right;font-weight:800;padding:8px 12px;color:#4ECDC4">{s3}</td></tr>'
        # ROI row
        rows_html += f'<tr><td style="text-align:left;font-weight:800;padding:8px 12px;color:#fff">{roi_row[0]}</td><td style="text-align:right;font-weight:800;padding:8px 12px;color:#4ECDC4">{roi_row[1][0]}</td><td style="text-align:right;font-weight:800;padding:8px 12px;color:#4ECDC4">{roi_row[1][1]}</td><td style="text-align:right;font-weight:800;padding:8px 12px;color:#4ECDC4">{roi_row[1][2]}</td></tr>'

        return f"""<div style="background:linear-gradient(145deg,#111d33,#162544);border-radius:12px;padding:20px;border:1px solid rgba(255,255,255,.08);box-shadow:0 4px 20px rgba(0,0,0,.2)">
        <p style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:#4ECDC4;margin:0 0 12px;padding-bottom:8px;border-bottom:2px solid #4ECDC4">{title}</p>
        <table style="width:100%;border-collapse:collapse;font-size:13px">
        <tr><th style="text-align:left;padding:6px 12px;font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#8a9bb0;border-bottom:1px solid rgba(255,255,255,.1)">Metric</th><th style="text-align:right;padding:6px 12px;font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#8a9bb0;border-bottom:1px solid rgba(255,255,255,.1)">S1</th><th style="text-align:right;padding:6px 12px;font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#8a9bb0;border-bottom:1px solid rgba(255,255,255,.1)">S2</th><th style="text-align:right;padding:6px 12px;font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#8a9bb0;border-bottom:1px solid rgba(255,255,255,.1)">S3</th></tr>
        {rows_html}
        </table></div>"""

    tc1, tc2, tc3 = st.columns(3)
    with tc1: st.markdown(build_card_table("Monthly per Room", 1), unsafe_allow_html=True)
    with tc2: st.markdown(build_card_table("Annual per Room", 12), unsafe_allow_html=True)
    with tc3: st.markdown(build_card_table("Annual per Property (in 000s)", 12, is_thousands=True), unsafe_allow_html=True)

    # Annual CP bar chart
    fig_cp = go.Figure()
    for sn, r, color in [("Scenario 1", r1, "#7EB8DA"), ("Scenario 2", r2, "#4ECDC4"), ("Scenario 3", r3, "#FF9900")]:
        fig_cp.add_trace(go.Bar(
            name=sn, x=["Annual CP / Room", "Annual CP / Property (000s)"],
            y=[r["inc_cp_room"] * 12, ann_prop(r)],
            marker_color=color, marker_line=dict(color="#e0e6ed", width=0.5),
            text=[f"${r['inc_cp_room']*12:,.0f}", f"${ann_prop(r):,.0f}K"],
            textposition="outside", textfont=dict(size=13, family="Inter", color="#e0e6ed"),
        ))
    fig_cp.update_layout(barmode="group", height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                         yaxis=dict(gridcolor="#eef0f3"), margin=dict(t=40, b=40),
                         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
                         font=dict(family="Inter"))
    st.plotly_chart(fig_cp, use_container_width=True)

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
        with k4: st.markdown(kpi(f"${live_r['inc_cp_room']*12*avg_rooms_per_alexa_property/1000:,.0f}K", "Annual CP/Property"), unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Revenue by Amenity (Monthly per Room)**")
        if det:
            st.dataframe(pd.DataFrame(det), use_container_width=True, hide_index=True)

        # Waterfall
        wf_l = ["Benefits", "- Payment", "- Amenity Cost", "= CP"]
        wf_v = [live_r["total_inc_room"], -live_r["total_payment_room"], -live_r["amenity_cost_room"], live_r["inc_cp_room"]]
        fig_wf = go.Figure(go.Waterfall(x=wf_l, y=wf_v, measure=["absolute","relative","relative","total"],
            connector=dict(line=dict(color="#D5D9DD")), increasing=dict(marker=dict(color="#067D62")),
            decreasing=dict(marker=dict(color="#C7511F")), totals=dict(marker=dict(color="#4ECDC4")),
            text=[f"${v:,.0f}" for v in wf_v], textposition="outside"))
        fig_wf.update_layout(height=380, plot_bgcolor="#FAFBFC", yaxis=dict(gridcolor="rgba(255,255,255,.08)"), margin=dict(t=30))
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
        colorscale=[[0,"#111d33"],[0.5,"#2d2a15"],[1,"#FF5252"]], text=[[f"${v:,.0f}" for v in row] for row in pay_heat],
        texttemplate="%{text}", textfont=dict(size=10), colorbar=dict(title="$/Room"),
    ))
    fig_pay.update_layout(title="Monthly Payment per Room (Sub + Rev Share + Fees)",
        height=450, xaxis_title="Ancillary Transaction %", yaxis_title="ASP Rev Share %",
        plot_bgcolor="#FAFBFC")
    st.plotly_chart(fig_pay, use_container_width=True)

# Footer
st.markdown(f"""<div class="app-footer">
<p class="brand">Alexa Smart Properties</p>
<p class="sub">Confidential</p></div>""", unsafe_allow_html=True)
