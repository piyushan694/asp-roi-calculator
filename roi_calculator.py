import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG & BRANDING
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Alexa Smart Properties — Partner ROI Calculator",
    layout="wide",
    page_icon="�",
    initial_sidebar_state="collapsed",
)

# Professional CSS
st.markdown("""
<style>
    /* Hide Streamlit branding for clean presentation */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Global font */
    html, body, [class*="css"] { font-family: 'Amazon Ember', 'Segoe UI', Helvetica, Arial, sans-serif; }

    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, #232F3E 0%, #37475A 50%, #485769 100%);
        border-radius: 16px; padding: 36px 48px; margin-bottom: 28px;
        border-bottom: 4px solid #FF9900;
    }
    .hero-banner h1 { color: #FFFFFF; font-size: 32px; margin: 0 0 6px 0; font-weight: 700; letter-spacing: -0.5px; }
    .hero-banner .subtitle { color: #FF9900; font-size: 16px; margin: 0; font-weight: 500; }
    .hero-banner .meta { color: #A0AAB4; font-size: 12px; margin-top: 10px; }

    /* KPI cards */
    .kpi-card {
        background: #FFFFFF; border-radius: 12px; padding: 24px 20px;
        text-align: center; border: 1px solid #E8ECEF;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
    .kpi-card .value { color: #232F3E; font-size: 30px; font-weight: 700; margin: 0; line-height: 1.2; }
    .kpi-card .label { color: #6B7785; font-size: 12px; margin: 6px 0 0 0; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-card.highlight { border-left: 4px solid #FF9900; }
    .kpi-card.green .value { color: #067D62; }
    .kpi-card.orange .value { color: #C7511F; }
    .kpi-card.blue .value { color: #0073BB; }

    /* Scenario headers */
    .scenario-tag {
        display: inline-block; padding: 4px 14px; border-radius: 20px;
        font-size: 12px; font-weight: 600; letter-spacing: 0.3px; margin-bottom: 8px;
    }
    .tag-conservative { background: #E3F2FD; color: #0D47A1; }
    .tag-base { background: #E8F5E9; color: #1B5E20; }
    .tag-optimistic { background: #FFF3E0; color: #E65100; }

    /* Section dividers */
    .section-title {
        font-size: 20px; font-weight: 700; color: #232F3E;
        border-left: 4px solid #FF9900; padding-left: 14px; margin: 32px 0 16px 0;
    }

    /* Table styling */
    .dataframe { font-size: 13px !important; }

    /* Sidebar */
    [data-testid="stSidebar"] { background: #232F3E; }
    [data-testid="stSidebar"] * { color: #D5D9DD !important; }
    [data-testid="stSidebar"] .stSlider label { color: #FF9900 !important; }

    /* Footer */
    .app-footer {
        background: #232F3E; border-radius: 12px; padding: 20px 32px;
        margin-top: 40px; text-align: center;
    }
    .app-footer p { color: #A0AAB4; font-size: 12px; margin: 0; }
    .app-footer .brand { color: #FF9900; font-weight: 600; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 24px; font-weight: 600; font-size: 14px;
        border-radius: 8px 8px 0 0;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HERO BANNER
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero-banner">
    <h1>🔶 Alexa Smart Properties — Partner ROI Calculator</h1>
    <p class="subtitle">Deal Financial Model &amp; Sensitivity Analysis</p>
    <p class="meta">Confidential — For Partner & BD Team Use Only &nbsp;|&nbsp; Generated {datetime.now().strftime('%B %d, %Y')}</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR — INPUT ASSUMPTIONS (collapsed by default for presentation)
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Model Assumptions")
    st.caption("Adjust inputs below — all tabs update in real-time")
    st.divider()

    # --- Property & Operating Metrics ---
    st.markdown("### 🏨 Property & Operating Metrics")
    partner_name = st.text_input("Partner Name", "Holland America Line")
    total_ships = st.number_input("Total Ships / Properties", value=11, min_value=1)
    total_staterooms = st.number_input("Total Staterooms / Rooms", value=11394, min_value=1)
    avg_rooms_per_property = st.number_input("Avg Rooms per Property", value=1036, min_value=1)
    annual_obr = st.number_input("Annual Onboard Revenue ($)", value=800_000_000, step=1_000_000, format="%d")
    pre_boarding_pct = st.slider("Pre-boarding Revenue %", 0, 100, 60) / 100
    avg_passenger_days = st.number_input("Avg Passenger Days per Cruise", value=7, min_value=1)
    avg_cruises_per_month = st.number_input("Avg Cruises per Month", value=4, min_value=1)
    avg_passengers_per_room = st.number_input("Avg Passengers per Room", value=2.0, step=0.1)
    avg_occupancy = st.slider("Avg Occupancy Rate %", 50, 100, 96) / 100

    st.divider()
    st.markdown("### 🚀 Alexa Deployment")
    projected_cruises_alexa = st.number_input("Projected Cruises with Alexa", value=5, min_value=1)
    projected_rooms_alexa = st.number_input("Projected Rooms with Alexa", value=2500, min_value=1)
    avg_rooms_per_cruise_alexa = st.number_input("Avg Rooms per Cruise (Alexa)", value=500, min_value=1)

    st.divider()
    st.markdown("### 💰 Revenue Mix")
    rev_categories = {}
    default_mix = {
        "Beverage Sales": {"pct": 25, "margin": 70},
        "Shore Excursions": {"pct": 18, "margin": 70},
        "Casino Gaming": {"pct": 26, "margin": 70},
        "Retail Sales": {"pct": 10, "margin": 70},
        "Specialty Restaurants": {"pct": 4, "margin": 70},
        "Internet & Communication": {"pct": 7, "margin": 70},
        "Spa & Wellness": {"pct": 6, "margin": 70},
        "Photo Sales": {"pct": 2, "margin": 70},
        "Art Sales": {"pct": 1, "margin": 70},
        "Laundry & Dry-Cleaning": {"pct": 1, "margin": 70},
    }
    for cat, vals in default_mix.items():
        with st.expander(cat):
            pct = st.slider(f"% of Revenue", 0, 50, vals["pct"], key=f"rev_{cat}") / 100
            margin = st.slider(f"Avg Margin %", 0, 100, vals["margin"], key=f"margin_{cat}") / 100
            rev_categories[cat] = {"pct": pct, "margin": margin}

    st.divider()
    st.markdown("### 📉 Cost Savings")
    avg_call_duration_min = st.number_input("Avg Call Duration (min)", value=2, min_value=1)
    hourly_wage = st.number_input("Hourly Wage — Guest Relations ($)", value=40, min_value=1)
    call_volume_reduction_pct = st.slider("Call Volume Reduction via Alexa %", 0, 100, 25) / 100
    monthly_guest_service_hours = st.number_input("Monthly Guest Service Call Hours", value=336, min_value=1)

    st.divider()
    st.markdown("### 🖨️ Printing Savings")
    daily_pages_per_room = st.number_input("Daily Printed Pages / Room", value=5, min_value=0)
    daily_print_freq = st.number_input("Daily Print Frequency / Room", value=2, min_value=0)
    cost_per_page = st.number_input("Cost per Page ($)", value=0.04, step=0.01, format="%.2f")
    distribution_time_min = st.number_input("Distribution Time / Room (min)", value=1, min_value=0)
    staff_hourly_wage = st.number_input("Staff Hourly Wage ($)", value=40, min_value=1)
    printing_savings_pct = st.slider("Printing Savings via Alexa %", 0, 100, 50) / 100

    st.divider()
    st.markdown("### 🎰 Casino & Cruise")
    casino_guest_pct = st.slider("% Guests Visiting Casino", 0, 100, 20) / 100
    casino_alexa_scan_pct = st.slider("% Casino Guests via Alexa", 0, 100, 10) / 100
    casino_referral_fee = st.number_input("Referral Fee / Casino Guest ($)", value=10, min_value=0)
    cruise_booking_pct = st.slider("% Guests Booking Next Cruise", 0.0, 5.0, 0.5, step=0.1) / 100
    avg_ticket_revenue = st.number_input("Avg Ticket Revenue / Passenger ($)", value=1500, min_value=0)
    cruise_booking_commission_pct = st.slider("Commission % on Cruise Bookings", 0, 50, 0) / 100

    st.divider()
    st.markdown("### 📋 Deal Terms")
    monthly_sub_fee = st.number_input("Monthly Subscription Fee ($)", value=15.0, step=1.0)
    rev_share_pct = st.slider("Revenue Share %", 0, 50, 10) / 100
    device_msrp = st.number_input("Device MSRP ($)", value=180.0, step=1.0)
    device_discount_pct = st.slider("Device Discount %", 0, 50, 22) / 100
    device_setup_fee = st.number_input("Device Setup Fee ($)", value=35.0, step=1.0)
    device_usage_months = st.number_input("Device Usage Life (months)", value=60, min_value=1)

# ═══════════════════════════════════════════════════════════════
# DERIVED CALCULATIONS
# ═══════════════════════════════════════════════════════════════
monthly_obr_per_room = annual_obr / total_staterooms / 12
onboard_monthly_obr = monthly_obr_per_room * (1 - pre_boarding_pct)
device_price = device_msrp * (1 - device_discount_pct)
monthly_device_amortization = device_price / device_usage_months
avg_monthly_passenger_days = avg_passenger_days * avg_cruises_per_month

# Cost savings
monthly_service_cost = monthly_guest_service_hours * hourly_wage
monthly_service_savings_per_cruise = monthly_service_cost * call_volume_reduction_pct
total_monthly_service_savings = monthly_service_savings_per_cruise * projected_cruises_alexa

monthly_print_cost_per_cruise = avg_rooms_per_cruise_alexa * avg_monthly_passenger_days * daily_pages_per_room * cost_per_page
distribution_cost_per_cruise = avg_rooms_per_cruise_alexa * avg_monthly_passenger_days * (distribution_time_min / 60) * staff_hourly_wage
monthly_printing_savings_per_cruise = (monthly_print_cost_per_cruise + distribution_cost_per_cruise) * printing_savings_pct
total_monthly_printing_savings = monthly_printing_savings_per_cruise * projected_cruises_alexa

total_monthly_cost_savings = total_monthly_service_savings + total_monthly_printing_savings
cost_savings_per_room = total_monthly_cost_savings / projected_rooms_alexa

# Casino
monthly_casino_guests_per_cruise = avg_rooms_per_cruise_alexa * avg_monthly_passenger_days * casino_guest_pct * casino_alexa_scan_pct
total_monthly_casino_fee = monthly_casino_guests_per_cruise * casino_referral_fee * projected_cruises_alexa

# Cruise booking
monthly_passengers_volume = projected_rooms_alexa * avg_passengers_per_room * avg_cruises_per_month
monthly_cruise_bookings = monthly_passengers_volume * cruise_booking_pct
monthly_cruise_booking_revenue = monthly_cruise_bookings * avg_ticket_revenue
monthly_cruise_commission = monthly_cruise_booking_revenue * cruise_booking_commission_pct


# ═══════════════════════════════════════════════════════════════
# ROI CALCULATION ENGINE
# ═══════════════════════════════════════════════════════════════
def calculate_roi(txn_pct, inc_pct):
    total_amenity_revenue = 0
    total_rev_share_payment = 0
    total_amenity_cost = 0
    category_details = {}

    for cat, vals in rev_categories.items():
        cat_monthly = (annual_obr * vals["pct"] / total_staterooms / 12) * projected_rooms_alexa * (1 - pre_boarding_pct)
        if cat == "Casino Gaming":
            category_details[cat] = {
                "revenue": total_monthly_casino_fee,
                "incremental": total_monthly_casino_fee * inc_pct,
                "rev_share": 0,
                "cost": total_monthly_casino_fee * (1 - vals["margin"]),
            }
        else:
            rev = cat_monthly * txn_pct
            category_details[cat] = {
                "revenue": rev,
                "incremental": rev * inc_pct,
                "rev_share": rev * rev_share_pct,
                "cost": rev * inc_pct * (1 - vals["margin"]),
            }
        total_amenity_revenue += category_details[cat]["revenue"]
        total_rev_share_payment += category_details[cat]["rev_share"]
        total_amenity_cost += category_details[cat]["cost"]

    cruise_rev = monthly_cruise_booking_revenue
    total_revenue = total_amenity_revenue + total_monthly_casino_fee + cruise_rev + total_monthly_cost_savings
    total_incremental = sum(d["incremental"] for d in category_details.values()) + cruise_rev * inc_pct
    alexa_benefits = total_incremental + total_monthly_cost_savings

    monthly_sub_total = monthly_sub_fee * projected_rooms_alexa
    total_payment = monthly_sub_total + total_rev_share_payment + total_monthly_casino_fee + monthly_cruise_commission + monthly_device_amortization * projected_rooms_alexa

    incremental_cp = total_incremental + total_monthly_cost_savings - total_payment - total_amenity_cost
    total_investment = total_payment + total_amenity_cost
    roi = (incremental_cp / total_investment * 100) if total_investment > 0 else 0
    cm = (alexa_benefits - total_payment - total_amenity_cost) / total_revenue * 100 if total_revenue > 0 else 0
    pr = projected_rooms_alexa if projected_rooms_alexa > 0 else 1

    return {
        "total_revenue": total_revenue, "total_revenue_per_room": total_revenue / pr,
        "alexa_benefits": alexa_benefits, "alexa_benefits_per_room": alexa_benefits / pr,
        "incremental_rev": total_incremental, "incremental_rev_per_room": total_incremental / pr,
        "cost_savings_per_room": cost_savings_per_room,
        "total_payment": total_payment, "total_payment_per_room": total_payment / pr,
        "sub_per_room": monthly_sub_fee,
        "rev_share_per_room": total_rev_share_payment / pr,
        "amenity_cost": total_amenity_cost, "amenity_cost_per_room": total_amenity_cost / pr,
        "incremental_cp": incremental_cp, "incremental_cp_per_room": incremental_cp / pr,
        "roi_pct": roi, "cm_pct": cm,
        "category_details": category_details,
        "monthly_sub_total": monthly_sub_total,
        "monthly_rev_share_total": total_rev_share_payment,
    }


# Helper: KPI card HTML
def kpi_card(value, label, css_class=""):
    return f"""<div class="kpi-card {css_class}">
        <p class="value">{value}</p>
        <p class="label">{label}</p>
    </div>"""

# ═══════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "  📋  Executive Summary  ", "  📊  Sensitivity Analysis  ",
    "  🔍  Detailed Breakdown  ", "  📈  Deployment Scenarios  "
])

# ─────────────────────────────────────────────────────────────
# TAB 1: EXECUTIVE SUMMARY
# ─────────────────────────────────────────────────────────────
with tab1:
    st.markdown(f'<div class="section-title">{partner_name} — ROI Summary</div>', unsafe_allow_html=True)
    st.markdown("Adjust scenario assumptions below to model different adoption outcomes.")

    # Scenario inputs in clean columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<span class="scenario-tag tag-conservative">SCENARIO 1 — CONSERVATIVE</span>', unsafe_allow_html=True)
        s1_txn = st.slider("Transactions via Alexa %", 1, 50, 8, key="s1t") / 100
        s1_inc = st.slider("Incrementality %", 1, 100, 50, key="s1i") / 100
    with col2:
        st.markdown('<span class="scenario-tag tag-base">SCENARIO 2 — BASE CASE</span>', unsafe_allow_html=True)
        s2_txn = st.slider("Transactions via Alexa %", 1, 50, 10, key="s2t") / 100
        s2_inc = st.slider("Incrementality %", 1, 100, 40, key="s2i") / 100
    with col3:
        st.markdown('<span class="scenario-tag tag-optimistic">SCENARIO 3 — OPTIMISTIC</span>', unsafe_allow_html=True)
        s3_txn = st.slider("Transactions via Alexa %", 1, 50, 15, key="s3t") / 100
        s3_inc = st.slider("Incrementality %", 1, 100, 80, key="s3i") / 100

    r1, r2, r3 = calculate_roi(s1_txn, s1_inc), calculate_roi(s2_txn, s2_inc), calculate_roi(s3_txn, s3_inc)

    st.markdown("---")

    # KPI Cards Row
    for tag, label, r, css in [
        ("tag-conservative", "Conservative", r1, "blue"),
        ("tag-base", "Base Case", r2, "green"),
        ("tag-optimistic", "Optimistic", r3, "orange"),
    ]:
        st.markdown(f'<span class="scenario-tag {tag}">{label.upper()}</span>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(kpi_card(f"{r['roi_pct']:.0f}%", "ROI", f"highlight {css}"), unsafe_allow_html=True)
        with k2:
            st.markdown(kpi_card(f"${r['incremental_cp_per_room']:,.0f}", "Monthly CP / Room", css), unsafe_allow_html=True)
        with k3:
            st.markdown(kpi_card(f"${r['incremental_cp_per_room']*12:,.0f}", "Annual CP / Room", css), unsafe_allow_html=True)
        with k4:
            st.markdown(kpi_card(f"${r['incremental_cp_per_room']*12*avg_rooms_per_cruise_alexa/1000:,.0f}K", "Annual CP / Property", css), unsafe_allow_html=True)
        st.markdown("")

    st.markdown("---")

    # Summary comparison table
    st.markdown('<div class="section-title">Side-by-Side Comparison (Monthly per Room)</div>', unsafe_allow_html=True)

    def f(v):
        return f"${v:,.0f}"

    rows = [
        ("Transactions via Alexa", f"{s1_txn*100:.0f}%", f"{s2_txn*100:.0f}%", f"{s3_txn*100:.0f}%"),
        ("Incrementality via Alexa", f"{s1_inc*100:.0f}%", f"{s2_inc*100:.0f}%", f"{s3_inc*100:.0f}%"),
        ("", "", "", ""),
        ("Total Revenue", f(r1["total_revenue_per_room"]), f(r2["total_revenue_per_room"]), f(r3["total_revenue_per_room"])),
        ("Alexa Benefits", f(r1["alexa_benefits_per_room"]), f(r2["alexa_benefits_per_room"]), f(r3["alexa_benefits_per_room"])),
        ("  ↳ Incremental Amenities Revenue", f(r1["incremental_rev_per_room"]), f(r2["incremental_rev_per_room"]), f(r3["incremental_rev_per_room"])),
        ("  ↳ Cost Savings", f(r1["cost_savings_per_room"]), f(r2["cost_savings_per_room"]), f(r3["cost_savings_per_room"])),
        ("Total Payment to Alexa", f(-r1["total_payment_per_room"]), f(-r2["total_payment_per_room"]), f(-r3["total_payment_per_room"])),
        ("  ↳ Subscription Fee", f(-r1["sub_per_room"]), f(-r2["sub_per_room"]), f(-r3["sub_per_room"])),
        ("  ↳ Rev-Share Payments", f(-r1["rev_share_per_room"]), f(-r2["rev_share_per_room"]), f(-r3["rev_share_per_room"])),
        ("Incremental Amenities Cost", f(-r1["amenity_cost_per_room"]), f(-r2["amenity_cost_per_room"]), f(-r3["amenity_cost_per_room"])),
        ("", "", "", ""),
        ("Incremental CP", f(r1["incremental_cp_per_room"]), f(r2["incremental_cp_per_room"]), f(r3["incremental_cp_per_room"])),
        ("ROI %", f"{r1['roi_pct']:.0f}%", f"{r2['roi_pct']:.0f}%", f"{r3['roi_pct']:.0f}%"),
    ]
    df_summary = pd.DataFrame(rows, columns=["Metric", "Scenario 1", "Scenario 2", "Scenario 3"])
    st.dataframe(df_summary, use_container_width=True, hide_index=True, height=530)

    # ROI comparison chart
    fig_cmp = go.Figure()
    fig_cmp.add_trace(go.Bar(
        x=["Conservative", "Base Case", "Optimistic"],
        y=[r1["roi_pct"], r2["roi_pct"], r3["roi_pct"]],
        marker_color=["#0073BB", "#067D62", "#C7511F"],
        text=[f"{v:.0f}%" for v in [r1["roi_pct"], r2["roi_pct"], r3["roi_pct"]]],
        textposition="outside", textfont=dict(size=16, color="#232F3E"),
    ))
    fig_cmp.update_layout(
        title=dict(text="ROI % by Scenario", font=dict(size=18, color="#232F3E")),
        height=380, yaxis_title="ROI %", plot_bgcolor="#FAFBFC",
        yaxis=dict(gridcolor="#E8ECEF"), margin=dict(t=60, b=40),
    )
    st.plotly_chart(fig_cmp, use_container_width=True)

    # Annual CP comparison
    fig_cp = go.Figure()
    for name, r, color in [("Conservative", r1, "#0073BB"), ("Base", r2, "#067D62"), ("Optimistic", r3, "#C7511F")]:
        fig_cp.add_trace(go.Bar(
            name=name, x=["Annual CP / Room", "Annual CP / Property (000s)"],
            y=[r["incremental_cp_per_room"] * 12, r["incremental_cp_per_room"] * 12 * avg_rooms_per_cruise_alexa / 1000],
            marker_color=color,
            text=[f"${r['incremental_cp_per_room']*12:,.0f}", f"${r['incremental_cp_per_room']*12*avg_rooms_per_cruise_alexa/1000:,.0f}K"],
            textposition="outside",
        ))
    fig_cp.update_layout(
        barmode="group", height=380,
        title=dict(text="Annual Contribution Profit Comparison", font=dict(size=18, color="#232F3E")),
        plot_bgcolor="#FAFBFC", yaxis=dict(gridcolor="#E8ECEF"), margin=dict(t=60, b=40),
    )
    st.plotly_chart(fig_cp, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# TAB 2: SENSITIVITY ANALYSIS
# ─────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">Sensitivity Analysis</div>', unsafe_allow_html=True)
    st.markdown("How does ROI change as transaction adoption and incrementality vary?")

    col_a, col_b = st.columns([1, 2])
    with col_a:
        sens_inc = st.slider("Incrementality % (fixed)", 10, 100, 50, step=5, key="si") / 100

    txn_range = [0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20]
    sens = [calculate_roi(t, sens_inc) for t in txn_range]

    # Table
    st.dataframe(pd.DataFrame({
        "Txn %": [f"{t*100:.0f}%" for t in txn_range],
        "Revenue/Room": [f"${r['total_revenue_per_room']:,.0f}" for r in sens],
        "Benefits/Room": [f"${r['alexa_benefits_per_room']:,.0f}" for r in sens],
        "Payment/Room": [f"${r['total_payment_per_room']:,.0f}" for r in sens],
        "CP/Room": [f"${r['incremental_cp_per_room']:,.0f}" for r in sens],
        "CM %": [f"{r['cm_pct']:.0f}%" for r in sens],
        "ROI %": [f"{r['roi_pct']:.0f}%" for r in sens],
    }), use_container_width=True, hide_index=True)

    # Charts side by side
    c1, c2 = st.columns(2)
    with c1:
        fig_sr = go.Figure()
        fig_sr.add_trace(go.Scatter(
            x=[f"{t*100:.0f}%" for t in txn_range], y=[r["roi_pct"] for r in sens],
            mode="lines+markers+text", line=dict(color="#FF9900", width=3),
            marker=dict(size=10, color="#FF9900"),
            text=[f"{r['roi_pct']:.0f}%" for r in sens], textposition="top center",
            textfont=dict(size=11),
        ))
        fig_sr.update_layout(
            title="ROI % vs Transaction Rate", height=400,
            xaxis_title="Transactions via Alexa %", yaxis_title="ROI %",
            plot_bgcolor="#FAFBFC", yaxis=dict(gridcolor="#E8ECEF"),
        )
        st.plotly_chart(fig_sr, use_container_width=True)

    with c2:
        fig_sc = go.Figure()
        fig_sc.add_trace(go.Bar(
            x=[f"{t*100:.0f}%" for t in txn_range],
            y=[r["incremental_cp_per_room"] for r in sens],
            marker_color="#067D62",
            text=[f"${r['incremental_cp_per_room']:,.0f}" for r in sens],
            textposition="outside", textfont=dict(size=10),
        ))
        fig_sc.update_layout(
            title="Monthly Incremental CP / Room", height=400,
            xaxis_title="Transactions via Alexa %", yaxis_title="$ per Room",
            plot_bgcolor="#FAFBFC", yaxis=dict(gridcolor="#E8ECEF"),
        )
        st.plotly_chart(fig_sc, use_container_width=True)

    # 2D Heatmap
    st.markdown('<div class="section-title">2D Sensitivity — ROI % Heatmap</div>', unsafe_allow_html=True)
    txn_ax = [0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20]
    inc_ax = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
    heat = [[round(calculate_roi(t, i)["roi_pct"]) for t in txn_ax] for i in inc_ax]

    fig_h = go.Figure(data=go.Heatmap(
        z=heat, x=[f"{t*100:.0f}%" for t in txn_ax], y=[f"{i*100:.0f}%" for i in inc_ax],
        colorscale=[[0, "#FDEBD0"], [0.5, "#F5B041"], [1, "#067D62"]],
        text=[[f"{v}%" for v in row] for row in heat],
        texttemplate="%{text}", textfont=dict(size=13, color="#232F3E"),
        colorbar=dict(title="ROI %"),
    ))
    fig_h.update_layout(
        title="ROI % — Transaction Rate × Incrementality",
        xaxis_title="Transactions via Alexa %", yaxis_title="Incrementality %",
        height=500, plot_bgcolor="#FAFBFC",
    )
    st.plotly_chart(fig_h, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# TAB 3: DETAILED BREAKDOWN
# ─────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">Detailed Revenue & Cost Breakdown</div>', unsafe_allow_html=True)

    dc1, dc2 = st.columns(2)
    with dc1:
        dt = st.slider("Transaction via Alexa %", 1, 30, 8, key="dt") / 100
    with dc2:
        di = st.slider("Incrementality %", 10, 100, 50, key="di") / 100

    rd = calculate_roi(dt, di)

    # Revenue by category
    st.markdown('<div class="section-title">Revenue via Alexa by Category</div>', unsafe_allow_html=True)
    rev_rows = []
    for cat, d in rd["category_details"].items():
        rev_rows.append({"Category": cat, "Revenue": f"${d['revenue']:,.0f}",
                         "Incremental": f"${d['incremental']:,.0f}",
                         "Rev-Share": f"${d['rev_share']:,.0f}", "Cost": f"${d['cost']:,.0f}"})
    rev_rows.append({"Category": "🚢 Future Cruise Bookings", "Revenue": f"${monthly_cruise_booking_revenue:,.0f}",
                     "Incremental": f"${monthly_cruise_booking_revenue*di:,.0f}",
                     "Rev-Share": f"${monthly_cruise_commission:,.0f}", "Cost": f"${monthly_cruise_booking_revenue*0.30:,.0f}"})
    rev_rows.append({"Category": "💰 Cost Savings", "Revenue": f"${total_monthly_cost_savings:,.0f}",
                     "Incremental": f"${total_monthly_cost_savings:,.0f}", "Rev-Share": "—", "Cost": "—"})
    st.dataframe(pd.DataFrame(rev_rows), use_container_width=True, hide_index=True)

    st.markdown("---")

    # Cost savings detail
    cs1, cs2 = st.columns(2)
    with cs1:
        st.markdown('<div class="section-title">Guest Service Savings</div>', unsafe_allow_html=True)
        st.markdown(kpi_card(f"${total_monthly_service_savings:,.0f}", "Total Monthly Savings", "highlight green"), unsafe_allow_html=True)
        st.caption(f"Based on {call_volume_reduction_pct*100:.0f}% call volume reduction across {projected_cruises_alexa} cruises")
    with cs2:
        st.markdown('<div class="section-title">Printing Savings</div>', unsafe_allow_html=True)
        st.markdown(kpi_card(f"${total_monthly_printing_savings:,.0f}", "Total Monthly Savings", "highlight green"), unsafe_allow_html=True)
        st.caption(f"Based on {printing_savings_pct*100:.0f}% print reduction across {projected_cruises_alexa} cruises")

    st.markdown("---")

    # Payment breakdown
    st.markdown('<div class="section-title">Payment to Alexa (Monthly)</div>', unsafe_allow_html=True)
    pr = projected_rooms_alexa if projected_rooms_alexa > 0 else 1
    pay_rows = [
        ("Subscription Fee", rd["monthly_sub_total"], monthly_sub_fee),
        ("Revenue Share", rd["monthly_rev_share_total"], rd["monthly_rev_share_total"] / pr),
        ("Casino Referral Fee", total_monthly_casino_fee, total_monthly_casino_fee / pr),
        ("Cruise Commission", monthly_cruise_commission, monthly_cruise_commission / pr),
        ("Amortized Device Cost", monthly_device_amortization * projected_rooms_alexa, monthly_device_amortization),
    ]
    total_all = sum(r[1] for r in pay_rows)
    pay_rows.append(("TOTAL", total_all, total_all / pr))
    st.dataframe(pd.DataFrame([
        {"Component": r[0], "All Rooms": f"${r[1]:,.0f}", "Per Room": f"${r[2]:,.0f}"} for r in pay_rows
    ]), use_container_width=True, hide_index=True)

    # Waterfall
    st.markdown('<div class="section-title">Revenue → CP Waterfall (Monthly / Room)</div>', unsafe_allow_html=True)
    wf_labels = ["Alexa Benefits", "Payment to Alexa", "Amenity Costs", "Incremental CP"]
    wf_vals = [rd["alexa_benefits_per_room"], -rd["total_payment_per_room"], -rd["amenity_cost_per_room"], rd["incremental_cp_per_room"]]
    fig_wf = go.Figure(go.Waterfall(
        x=wf_labels, y=wf_vals, measure=["absolute", "relative", "relative", "total"],
        connector=dict(line=dict(color="#D5D9DD")),
        increasing=dict(marker=dict(color="#067D62")),
        decreasing=dict(marker=dict(color="#C7511F")),
        totals=dict(marker=dict(color="#FF9900")),
        text=[f"${v:,.0f}" for v in wf_vals], textposition="outside",
        textfont=dict(size=13, color="#232F3E"),
    ))
    fig_wf.update_layout(height=420, plot_bgcolor="#FAFBFC", yaxis=dict(gridcolor="#E8ECEF"),
                         margin=dict(t=40, b=40))
    st.plotly_chart(fig_wf, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# TAB 4: DEPLOYMENT SCENARIOS
# ─────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title">Multi-Year Deployment & Revenue Scenarios</div>', unsafe_allow_html=True)
    st.markdown("Models Low / Mid / High deployment ramp-up over 5 years (2027–2031)")

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown('<span class="scenario-tag tag-conservative">LOW CASE</span>', unsafe_allow_html=True)
        low_rs = st.number_input("Monthly Rev Share ($)", value=10.0, key="lrs")
        low_cv = st.text_input("Conversion % (Yr1–Yr5)", "23.5, 52.1, 100, 100, 100", key="lcv")
    with d2:
        st.markdown('<span class="scenario-tag tag-base">MID CASE</span>', unsafe_allow_html=True)
        mid_rs = st.number_input("Monthly Rev Share ($)", value=20.0, key="mrs")
        mid_cv = st.text_input("Conversion % (Yr1–Yr5)", "23.5, 60.5, 100, 100, 100", key="mcv")
    with d3:
        st.markdown('<span class="scenario-tag tag-optimistic">HIGH CASE</span>', unsafe_allow_html=True)
        high_rs = st.number_input("Monthly Rev Share ($)", value=35.0, key="hrs")
        high_cv = st.text_input("Conversion % (Yr1–Yr5)", "23.5, 100, 100, 100, 100", key="hcv")

    def parse_conv(s):
        try:
            return [float(x.strip()) / 100 for x in s.split(",")]
        except Exception:
            return [0.235, 0.521, 1.0, 1.0, 1.0]

    def calc_deploy(convs, mrs, sub, setup, dev, tam):
        rows, prev = [], 0
        for i, c in enumerate(convs):
            tgt = int(tam * c)
            nd = max(0, tgt - prev)
            avg_ib = (prev + tgt) / 2
            sc = avg_ib * sub * 12
            rc = avg_ib * mrs * 12
            rows.append({
                "Year": 2026 + i + 1, "New Deployments": nd,
                "Install Base (YE)": tgt, "Install Base (Avg)": int(avg_ib),
                "Subscription": sc, "Rev Share": rc,
                "Setup Cost": nd * setup, "Device Cost": nd * dev,
                "Total Cost": sc + rc + nd * setup + nd * dev,
                "Recurring (excl Device)": sc + rc,
            })
            prev = tgt
        return pd.DataFrame(rows)

    low_df = calc_deploy(parse_conv(low_cv), low_rs, monthly_sub_fee, device_setup_fee, device_price, total_staterooms)
    mid_df = calc_deploy(parse_conv(mid_cv), mid_rs, monthly_sub_fee, device_setup_fee, device_price, total_staterooms)
    high_df = calc_deploy(parse_conv(high_cv), high_rs, monthly_sub_fee, device_setup_fee, device_price, total_staterooms)

    st.markdown("---")

    for label, df, tag in [("Low Case", low_df, "tag-conservative"), ("Mid Case", mid_df, "tag-base"), ("High Case", high_df, "tag-optimistic")]:
        st.markdown(f'<span class="scenario-tag {tag}">{label.upper()}</span>', unsafe_allow_html=True)
        show_df = df.copy()
        for col in show_df.columns:
            if col != "Year":
                if any(k in col for k in ["Cost", "Share", "Subscription", "Rev", "Total", "Recurring"]):
                    show_df[col] = show_df[col].apply(lambda x: f"${x:,.0f}")
                else:
                    show_df[col] = show_df[col].apply(lambda x: f"{x:,.0f}")
        st.dataframe(show_df, use_container_width=True, hide_index=True)

    # Charts
    st.markdown('<div class="section-title">Annual Recurring Cost Comparison</div>', unsafe_allow_html=True)
    fig_dc = go.Figure()
    for name, df, color in [("Low", low_df, "#0073BB"), ("Mid", mid_df, "#067D62"), ("High", high_df, "#C7511F")]:
        fig_dc.add_trace(go.Bar(name=name, x=df["Year"], y=df["Recurring (excl Device)"], marker_color=color))
    fig_dc.update_layout(barmode="group", height=400, yaxis_title="Annual Cost ($)",
                         plot_bgcolor="#FAFBFC", yaxis=dict(gridcolor="#E8ECEF"))
    st.plotly_chart(fig_dc, use_container_width=True)

    st.markdown('<div class="section-title">Install Base Ramp-Up</div>', unsafe_allow_html=True)
    fig_ib = go.Figure()
    for name, df, color in [("Low", low_df, "#0073BB"), ("Mid", mid_df, "#067D62"), ("High", high_df, "#C7511F")]:
        fig_ib.add_trace(go.Scatter(name=name, x=df["Year"], y=df["Install Base (YE)"],
                                    mode="lines+markers", line=dict(color=color, width=3), marker=dict(size=10)))
    fig_ib.update_layout(height=400, yaxis_title="Install Base (Year-End)",
                         plot_bgcolor="#FAFBFC", yaxis=dict(gridcolor="#E8ECEF"))
    st.plotly_chart(fig_ib, use_container_width=True)

    # 5-year totals
    st.markdown('<div class="section-title">5-Year Total Cost Summary</div>', unsafe_allow_html=True)
    totals = pd.DataFrame({
        "Metric": ["Total Cost (5yr)", "Recurring Only (5yr)", "Device + Setup (5yr)"],
        "Low": [f"${low_df['Total Cost'].sum():,.0f}", f"${low_df['Recurring (excl Device)'].sum():,.0f}",
                f"${(low_df['Setup Cost'].sum()+low_df['Device Cost'].sum()):,.0f}"],
        "Mid": [f"${mid_df['Total Cost'].sum():,.0f}", f"${mid_df['Recurring (excl Device)'].sum():,.0f}",
                f"${(mid_df['Setup Cost'].sum()+mid_df['Device Cost'].sum()):,.0f}"],
        "High": [f"${high_df['Total Cost'].sum():,.0f}", f"${high_df['Recurring (excl Device)'].sum():,.0f}",
                 f"${(high_df['Setup Cost'].sum()+high_df['Device Cost'].sum()):,.0f}"],
    })
    st.dataframe(totals, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="app-footer">
    <p><span class="brand">Alexa Smart Properties</span> — Partner ROI Calculator</p>
    <p>{partner_name} &nbsp;|&nbsp; Confidential &nbsp;|&nbsp; {datetime.now().strftime('%B %d, %Y')} &nbsp;|&nbsp; Expand sidebar (▸) to adjust assumptions</p>
</div>
""", unsafe_allow_html=True)
