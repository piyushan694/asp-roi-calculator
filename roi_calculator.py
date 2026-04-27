import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import base64

st.set_page_config(page_title="ASP Partner ROI Calculator", layout="wide", page_icon="🔶", initial_sidebar_state="expanded")

# ══════════════════════════════════════════════════════════════════════
# Alexa+ Pitch Deck Theme — Institutional Finance (Goldman / McKinsey)
# Palette: Deep navy → Electric Alexa blue → Subtle glow
#   Background:   #05070C (near-black) → #0A1628 (deep navy)
#   Hero glow:    #1E90FF → #4AA8FF → #7DBFFF (Alexa brand blue spectrum)
#   Accent:       #00A8E8 (Alexa cyan-blue) + #4AA8FF (electric blue)
#   Text:         #FFFFFF / #B8C5D6 / #6B7A8F
# ══════════════════════════════════════════════════════════════════════
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
#MainMenu,footer{visibility:hidden}
/* Hide ONLY the Deploy button — keep stToolbar so sidebar collapse arrow stays visible */
.stDeployButton,[data-testid="stDeployButton"]{display:none!important}
[data-testid="stToolbarActions"]{display:none!important}
html,body,[class*="css"]{font-family:'Inter','Amazon Ember',-apple-system,sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}

/* ── Page background: Alexa deck vertical gradient ── */
.stApp{background:radial-gradient(ellipse at top right,#0F2847 0%,#071020 40%,#05070C 100%);background-attachment:fixed}
.block-container{padding-top:1.5rem;padding-bottom:3rem;max-width:1400px}

/* ── HERO: The Alexa+ title slide aesthetic ── */
.hero{background:linear-gradient(125deg,#05070C 0%,#0A1628 35%,#0F2847 65%,#1E4A7C 100%);border-radius:18px;padding:48px 56px;margin-bottom:36px;position:relative;overflow:hidden;box-shadow:0 8px 48px rgba(0,0,0,.4),0 0 0 1px rgba(74,168,255,.08) inset}
.hero::before{content:'';position:absolute;top:-30%;right:-15%;width:600px;height:600px;background:radial-gradient(circle,rgba(74,168,255,.22) 0%,rgba(30,144,255,.10) 40%,transparent 70%);border-radius:50%;filter:blur(20px)}
.hero::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#4AA8FF 30%,#7DBFFF 50%,#4AA8FF 70%,transparent)}
.hero h1{color:#FFFFFF;font-size:34px;margin:0 0 8px;font-weight:800;letter-spacing:-0.8px;position:relative;line-height:1.15}
.hero .sub{color:#7DBFFF;font-size:17px;margin:0;font-weight:500;position:relative;letter-spacing:0.2px}
.hero .meta{color:rgba(255,255,255,.4);font-size:10px;margin-top:14px;position:relative;letter-spacing:2px;text-transform:uppercase;font-weight:600}
.hero .meta-divider{color:rgba(125,191,255,.5);margin:0 10px}

/* ── KPI Cards: Premium elevated dark cards ── */
.kpi-big{background:linear-gradient(160deg,rgba(15,40,71,.6) 0%,rgba(10,22,40,.8) 100%);border-radius:14px;padding:28px 22px;text-align:center;border:1px solid rgba(125,191,255,.10);backdrop-filter:blur(12px);box-shadow:0 4px 24px rgba(0,0,0,.35);transition:all .35s cubic-bezier(.4,0,.2,1);position:relative;overflow:hidden}
.kpi-big::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(125,191,255,.3),transparent)}
.kpi-big:hover{transform:translateY(-3px);box-shadow:0 12px 40px rgba(30,144,255,.15);border-color:rgba(125,191,255,.25)}
.kpi-big .value{font-size:38px;font-weight:800;margin:0;line-height:1.05;letter-spacing:-0.8px;color:#FFFFFF;font-variant-numeric:tabular-nums}
.kpi-big .label{color:#8FA3BC;font-size:10.5px;margin:10px 0 0;text-transform:uppercase;letter-spacing:1.4px;font-weight:700;white-space:nowrap}
.kpi-big .delta{font-size:13px;margin-top:6px;font-weight:600}
.kpi-big.green .value{color:#FFFFFF}.kpi-big.green{border-bottom:2px solid #FFFFFF;box-shadow:0 4px 24px rgba(255,255,255,.05)}
.kpi-big.blue .value{color:#B8B8B8}.kpi-big.blue{border-bottom:2px solid #B8B8B8;box-shadow:0 4px 24px rgba(184,184,184,.06)}
.kpi-big.orange .value{color:#C9C9C9}.kpi-big.orange{border-bottom:2px solid #C9C9C9;box-shadow:0 4px 24px rgba(201,201,201,.06)}
.kpi-big.hero-card{background:linear-gradient(135deg,#1E90FF 0%,#0062CC 100%);border:none;box-shadow:0 8px 40px rgba(30,144,255,.35),0 0 0 1px rgba(255,255,255,.1) inset}
.kpi-big.hero-card .value{color:#FFFFFF;font-size:44px;text-shadow:0 2px 20px rgba(0,0,0,.3)}
.kpi-big.hero-card .label{color:rgba(255,255,255,.9);font-weight:700}

/* ── Scenario Cards: Clean glass panels ── */
.scenario-card{background:linear-gradient(160deg,rgba(15,40,71,.4) 0%,rgba(10,22,40,.6) 100%);border-radius:14px;padding:22px 26px;border:1px solid rgba(125,191,255,.08);backdrop-filter:blur(8px)}
.scenario-card .tag{display:inline-block;padding:6px 18px;border-radius:6px;font-size:11px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px}
.tag-s1{background:rgba(255,255,255,.12);color:#FFFFFF;border:1px solid rgba(255,255,255,.3)}
.tag-s2{background:rgba(184,184,184,.15);color:#B8B8B8;border:1px solid rgba(184,184,184,.35)}
.tag-s3{background:rgba(201,201,201,.12);color:#C9C9C9;border:1px solid rgba(201,201,201,.3)}

/* ── Section Headers: Institutional finance style ── */
.stitle{font-size:11.5px;text-transform:uppercase;letter-spacing:2.5px;font-weight:800;color:#7DBFFF;padding:0 0 8px 0;margin:40px 0 6px;border-bottom:1px solid rgba(125,191,255,.15);display:flex;align-items:center;gap:10px}
.stitle::before{content:'';width:3px;height:14px;background:linear-gradient(180deg,#4AA8FF,#1E90FF);border-radius:2px}
.stitle-sub{font-size:14px;color:#8FA3BC;margin:0 0 24px 0;font-weight:400;line-height:1.5}

/* ── Insight Box: Premium callout ── */
.insight{background:linear-gradient(135deg,rgba(15,40,71,.7) 0%,rgba(30,74,124,.4) 100%);border-radius:16px;padding:32px 36px;margin:28px 0;position:relative;border:1px solid rgba(125,191,255,.15);backdrop-filter:blur(10px);box-shadow:0 6px 30px rgba(0,0,0,.25)}
.insight::before{content:'';position:absolute;left:0;top:20%;bottom:20%;width:3px;background:linear-gradient(180deg,#4AA8FF,#1E90FF);border-radius:0 3px 3px 0}
.insight .eyebrow{font-size:10px;text-transform:uppercase;letter-spacing:2.5px;color:#4AA8FF;font-weight:800;margin:0 0 10px}
.insight .headline{font-size:19px;font-weight:700;color:#FFFFFF;margin:0 0 8px;line-height:1.45;letter-spacing:-0.2px}
.insight .body{font-size:13px;color:#8FA3BC;margin:0;line-height:1.5}

/* ── Sidebar: Dark navy command panel ── */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#05070C 0%,#0A1628 100%);border-right:1px solid rgba(125,191,255,.08)}
[data-testid="stSidebar"] .stMarkdown h2{color:#FFFFFF!important;font-size:16px;font-weight:800;letter-spacing:-0.3px;padding-bottom:10px;border-bottom:1px solid rgba(125,191,255,.12);margin-bottom:16px}
[data-testid="stSidebar"] .stMarkdown h3{color:#7DBFFF!important;font-size:11.5px;font-weight:800;text-transform:uppercase;letter-spacing:1.8px;margin-top:20px}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span{color:#8FA3BC!important}
[data-testid="stSidebar"] label{color:#B8C5D6!important;font-size:12.5px;font-weight:500}
[data-testid="stSidebar"] .stNumberInput input,[data-testid="stSidebar"] .stTextInput input{background:rgba(15,40,71,.4);color:#FFFFFF;border:1px solid rgba(125,191,255,.15);border-radius:6px}
[data-testid="stSidebar"] .stNumberInput input:focus,[data-testid="stSidebar"] .stTextInput input:focus{border-color:#4AA8FF;box-shadow:0 0 0 1px #4AA8FF}
[data-testid="stSidebar"] .stExpander{background:rgba(15,40,71,.3);border:1px solid rgba(125,191,255,.08);border-radius:8px}
[data-testid="stSidebar"] details summary{color:#B8C5D6!important;font-size:12.5px;font-weight:500}

/* ── Tabs: Clean institutional ── */
.stTabs [data-baseweb="tab-list"]{gap:4px;border-bottom:1px solid rgba(125,191,255,.12);background:transparent;padding-bottom:0}
.stTabs [data-baseweb="tab"]{font-weight:600;font-size:13px;padding:14px 24px;color:#6B7A8F;border-bottom:2px solid transparent;margin-bottom:-1px;background:transparent;transition:all .2s ease}
.stTabs [data-baseweb="tab"]:hover{color:#B8C5D6}
.stTabs [aria-selected="true"]{color:#FFFFFF!important;border-bottom:2px solid #C9C9C9!important;background:transparent!important;font-weight:700}
/* Tab highlight/underline bar (BaseWeb injects its own) — force silver */
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{background:#C9C9C9!important;background-color:#C9C9C9!important}

/* ── Tables & DataFrames ── */
[data-testid="stDataFrame"]{border-radius:10px;overflow:hidden;border:1px solid rgba(125,191,255,.08)}
[data-testid="stDataFrame"] [role="gridcell"]{background:rgba(15,40,71,.3)!important;color:#E0E8F2!important}
[data-testid="stDataFrame"] [role="columnheader"]{background:rgba(30,74,124,.6)!important;color:#7DBFFF!important;font-weight:700!important;text-transform:uppercase;letter-spacing:1px;font-size:10.5px!important}

/* ── Form controls — Sliders (ALL silver/white, catch ALL Streamlit injected colors) ── */
/* Thumb (draggable circle) */
.stSlider [data-baseweb="slider"] [role="slider"]{background:#FFFFFF!important;border:2px solid #C9C9C9!important;box-shadow:0 0 10px rgba(201,201,201,.5)!important}
/* Value bubble (number label above thumb) — WHITE on every child layer */
.stSlider [data-testid="stThumbValue"],
.stSlider [data-testid="stThumbValue"] *,
.stSlider [data-testid="stThumbValue"] div,
.stSlider [data-testid="stThumbValue"] span{color:#FFFFFF!important;background:transparent!important;font-weight:700!important;fill:#FFFFFF!important}
/* FILLED track (left of thumb, SELECTED range) — WHITE */
.stSlider [data-baseweb="slider"] > div > div > div:first-child,
.stSlider [data-baseweb="slider"] > div > div > div:first-child > div{background:#FFFFFF!important;background-color:#FFFFFF!important;background-image:none!important}
/* UNFILLED track (right of thumb, REMAINING range) — dim silver (unchanged) */
.stSlider [data-baseweb="slider"] > div > div > div:last-child,
.stSlider [data-baseweb="slider"] > div > div > div:last-child > div{background:rgba(201,201,201,.35)!important;background-color:rgba(201,201,201,.35)!important}
/* Streamlit's newer progress-bar-style slider (v1.30+) */
.stSlider progress{accent-color:#FFFFFF!important}
.stSlider progress::-webkit-progress-value{background:#FFFFFF!important}
.stSlider progress::-webkit-progress-bar{background:rgba(201,201,201,.35)!important}
.stSlider progress::-moz-progress-bar{background:#FFFFFF!important}
/* Tick labels */
.stSlider [data-testid="stTickBarMin"],.stSlider [data-testid="stTickBarMax"]{color:#8FA3BC!important}
/* Kill every known Streamlit accent color (green/teal/red/blue) on slider children */
div[data-baseweb="slider"] div[style*="rgb(0, 204"],
div[data-baseweb="slider"] div[style*="rgb(0, 191"],
div[data-baseweb="slider"] div[style*="rgb(0, 171"],
div[data-baseweb="slider"] div[style*="rgb(255, 75"],
div[data-baseweb="slider"] div[style*="rgb(255, 43"],
div[data-baseweb="slider"] div[style*="rgb(0, 104"],
div[data-baseweb="slider"] div[style*="rgb(246, 51"],
div[data-baseweb="slider"] div[style*="rgb(14, 17"]{background:#FFFFFF!important;background-color:#FFFFFF!important}
/* Every text node in/near slider → white */
.stSlider span,.stSlider div[role="slider"] + div,.stSlider label + div span{color:#FFFFFF!important}
.stRadio label,.stCheckbox label{color:#B8C5D6!important}

/* ── Text colors ── */
[data-testid="stMetricValue"]{color:#FFFFFF!important;font-weight:800;letter-spacing:-0.5px}
[data-testid="stMetricLabel"]{color:#8FA3BC!important;text-transform:uppercase;letter-spacing:1px;font-size:11px!important;font-weight:600!important}
.stMarkdown p,.stMarkdown li{color:#B8C5D6}
.stMarkdown strong{color:#FFFFFF;font-weight:700}
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3,.stMarkdown h4{color:#FFFFFF;letter-spacing:-0.3px}
.stCaption,[data-testid="stCaptionContainer"]{color:#6B7A8F!important;font-size:11.5px!important}
hr{border-color:rgba(125,191,255,.08)!important}

/* ── Footer: Pitch deck style ── */
.app-footer{background:linear-gradient(135deg,#05070C 0%,#0A1628 100%);border-radius:14px;padding:28px 40px;margin-top:56px;text-align:center;border-top:1px solid rgba(74,168,255,.15);position:relative;overflow:hidden}
.app-footer::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:200px;height:2px;background:linear-gradient(90deg,transparent,#4AA8FF,transparent)}
.app-footer .brand{color:#7DBFFF;font-size:11px;font-weight:800;margin:0;letter-spacing:3px;text-transform:uppercase}
.app-footer .sub{color:rgba(255,255,255,.35);font-size:10px;margin:8px 0 0;letter-spacing:1.5px;text-transform:uppercase}

/* ── Streamlit plotly container ── */
.stPlotlyChart{background:transparent!important;border-radius:12px;overflow:hidden}
</style>""", unsafe_allow_html=True)

# ── Unified chart theme for all Plotly figures ──
PLOT_BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(125,191,255,.08)"
AXIS_COLOR = "#8FA3BC"
TEXT_COLOR = "#E0E8F2"
ALEXA_BLUE = "#4AA8FF"
ALEXA_CYAN = "#FFFFFF"       # Scenario 1 - White (per reference)
ALEXA_PURPLE = "#C9C9C9"     # Scenario 3 - Light gray (per reference)
ALEXA_DEEP = "#1E90FF"
ALEXA_NEG = "#B8B8B8"        # bumped from #909090 for readability on navy
ALEXA_GRAY = "#B8B8B8"       # Scenario 2 - brightened gray (ref #909090 too dark)

def apply_plot_theme(fig, height=400):
    fig.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(family="Inter, sans-serif", color=TEXT_COLOR, size=12),
        height=height, margin=dict(t=40, b=40, l=40, r=40),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, tickfont=dict(color=AXIS_COLOR), title_font=dict(color=AXIS_COLOR, size=12)),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, tickfont=dict(color=AXIS_COLOR), title_font=dict(color=AXIS_COLOR, size=12)),
        legend=dict(font=dict(color=TEXT_COLOR), bgcolor="rgba(0,0,0,0)"),
    )
    return fig

def kpi(v, l, c="", delta=""):
    d = f'<p class="delta" style="color:{("#0a8f6c" if "+" in str(delta) or delta=="" else "#5C7A99")}">{delta}</p>' if delta else ""
    return f'<div class="kpi-big {c}"><p class="value">{v}</p><p class="label">{l}</p>{d}</div>'

# ═══════════════════════════════════════════════════════════════
# SIDEBAR — ALL INPUTS
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Deal Assumptions")
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
        # Sync expander header with current name (or placeholder if empty)
        current_name = st.session_state.get(f"an{i}", dn)
        display_name = current_name.strip() if current_name and current_name.strip() else f"— empty slot {i+1} —"
        with st.expander(f"Amenity {i+1}: {display_name}"):
            name = st.text_input("Name", dn, key=f"an{i}", placeholder=f"e.g. {dn}")
            rev_pct = st.slider("% of Revenue", 0, 50, dp, key=f"ap{i}") / 100
            margin = st.slider("Avg Margin %", 0, 100, dm, key=f"am{i}") / 100
            amenities.append({"name": name.strip() if name else dn, "pct": rev_pct, "margin": margin})

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
        current_fn = st.session_state.get(f"fn{i}", df[0])
        display_fn = current_fn.strip() if current_fn and current_fn.strip() else f"— empty slot {i+1} —"
        with st.expander(f"Fixed Fee {i+1}: {display_fn}"):
            fn = st.text_input("Name", df[0], key=f"fn{i}", placeholder=f"e.g. {df[0]}")
            fee = st.number_input("Fee per Transaction ($)", value=df[1], step=1.0, key=f"ff{i}")
            guest_pct = st.slider("% Guests Using via Alexa", 0.0, 50.0, float(df[2]), step=0.1, key=f"fg{i}") / 100
            visit_pct = st.slider("% Guests Visiting/Eligible", 0, 100, df[3], key=f"fv{i}") / 100
            commission_pct = st.slider("Commission % (if applicable)", 0, 100, df[4], key=f"fc{i}") / 100
            fixed_fees.append({"name": fn.strip() if fn else df[0], "fee": fee, "guest_pct": guest_pct, "visit_pct": visit_pct, "commission_pct": commission_pct})

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

def _load_logo_html():
    """Load alexa+ logo from dashboard/assets/ if present; return empty if no file."""
    assets = Path(__file__).parent / "assets"
    for name in ("alexa-plus-logo.png", "alexa-plus-logo.jpg", "alexa-plus-logo.svg", "alexa+.png"):
        p = assets / name
        if p.exists():
            mime = "image/svg+xml" if p.suffix == ".svg" else f"image/{p.suffix.lstrip('.')}"
            b64 = base64.b64encode(p.read_bytes()).decode()
            return f'<img src="data:{mime};base64,{b64}" style="height:110px;max-width:280px;object-fit:contain;filter:drop-shadow(0 4px 20px rgba(74,168,255,.35))" alt="Alexa+">'
    # No logo file — render nothing (keep hero clean)
    return ""

st.markdown(f"""<div class="hero">
<div style="display:flex;align-items:center;gap:32px">
<div style="flex:1">
<h1>Alexa+ ROI Analysis</h1>
<p class="sub">{partner_name}</p>
<p class="meta">Confidential<span class="meta-divider">|</span>For Partner Discussion Only</p>
</div>
<div style="flex:0 0 auto;text-align:center">
{_load_logo_html()}
</div>
</div>
</div>""", unsafe_allow_html=True)

# Sidebar toggle is in the Streamlit header (top-left)

tab1, tab2, tab3, tab4 = st.tabs([
    "  Executive Summary  ", "  Live Scenario Builder  ",
    "  Calculation Walkthrough  ", "  Sensitivity Analysis  "
])

# ─── TAB 1: EXECUTIVE SUMMARY ───
with tab1:
    st.markdown(f'<div class="stitle">{partner_name} — ROI Summary</div>', unsafe_allow_html=True)
    st.markdown('<p class="stitle-sub">Three scenarios modeling Alexa deployment impact on incremental revenue and profitability</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="scenario-card"><p style="font-size:11px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:#7DBFFF;margin:0 0 12px">SCENARIO 1</p>', unsafe_allow_html=True)
        s1t = st.slider("Transactions via Alexa %", 1, 50, 8, key="e1t") / 100
        s1i = st.slider("Incrementality via Alexa %", 1, 100, 50, key="e1i") / 100
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="scenario-card"><p style="font-size:11px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:#7DBFFF;margin:0 0 12px">SCENARIO 2</p>', unsafe_allow_html=True)
        s2t = st.slider("Transactions via Alexa %", 1, 50, 10, key="e2t") / 100
        s2i = st.slider("Incrementality via Alexa %", 1, 100, 40, key="e2i") / 100
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="scenario-card"><p style="font-size:11px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:#7DBFFF;margin:0 0 12px">SCENARIO 3</p>', unsafe_allow_html=True)
        s3t = st.slider("Transactions via Alexa %", 1, 50, 15, key="e3t") / 100
        s3i = st.slider("Incrementality via Alexa %", 1, 100, 80, key="e3i") / 100
        st.markdown('</div>', unsafe_allow_html=True)

    r1, r2, r3 = calc_roi(s1t, s1i), calc_roi(s2t, s2i), calc_roi(s3t, s3i)
    ann_prop = lambda r: r["inc_cp_room"] * 12 * avg_rooms_per_alexa_property / 1000

    # Hero ROI cards — the money shot
    st.markdown("---")
    st.markdown(f'<div class="stitle">Incremental Contribution Profit</div>', unsafe_allow_html=True)

    for sn, r, tag, color in [("Scenario 1", r1, "tag-s1", "blue"), ("Scenario 2", r2, "tag-s2", "green"), ("Scenario 3", r3, "tag-s3", "orange")]:
        st.markdown(f'<p style="font-size:11px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:#7DBFFF;margin:0 0 8px">{sn}</p>', unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.markdown(kpi(f"{r['roi']:.0f}%", "Return on Investment", "hero-card" if r['roi'] > 30 else f"{color}"), unsafe_allow_html=True)
        with k2: st.markdown(kpi(f"${r['inc_cp_room']:,.0f}", "Monthly per Room", color), unsafe_allow_html=True)
        with k3: st.markdown(kpi(f"${r['inc_cp_room']*12:,.0f}", "Annual per Room", color), unsafe_allow_html=True)
        with k4: st.markdown(kpi(f"${ann_prop(r):,.0f}K", "Annual per Property (000s)", color), unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Insight callout
    best = max([r1, r2, r3], key=lambda x: x["roi"])
    st.markdown(f"""<div class="insight">
    <p class="eyebrow">Key Takeaway</p>
    <p class="headline">Alexa+ deployment generates up to ${best['inc_cp_room']*12:,.0f} in annual incremental profit per room — translating to ${ann_prop(best):,.0f}K per property annually.</p>
    <p class="body">Based on {int(avg_rooms_per_alexa_property):,} rooms per property across {alexa_properties} properties with Alexa</p>
    </div>""", unsafe_allow_html=True)

    # Visual: ROI comparison gauge chart
    st.markdown(f'<div class="stitle">ROI Comparison</div>', unsafe_allow_html=True)
    fig_gauge = go.Figure()
    for i, (sn, r, color) in enumerate([("Scenario 1", r1, "#FFFFFF"), ("Scenario 2", r2, "#B8B8B8"), ("Scenario 3", r3, "#C9C9C9")]):
        fig_gauge.add_trace(go.Indicator(
            mode="gauge+number",
            value=r["roi"],
            title={"text": sn, "font": {"size": 14, "color": "#C9C9C9", "family": "Inter"}},
            number={"suffix": "%", "font": {"size": 36, "color": "#FFFFFF", "family": "Inter"}},
            gauge={
                "axis": {"range": [0, max(150, r["roi"] + 30)], "tickcolor": "rgba(201,201,201,.3)", "tickfont": {"color": "#B8B8B8", "size": 10}},
                "bar": {"color": color, "thickness": 0.75},
                "bgcolor": "rgba(15,40,71,.4)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 20], "color": "rgba(74,168,255,.06)"},
                    {"range": [20, 50], "color": "rgba(74,168,255,.10)"},
                    {"range": [50, 150], "color": "rgba(74,168,255,.16)"},
                ],
                "threshold": {"line": {"color": "#4AA8FF", "width": 2}, "thickness": 0.8, "value": r["roi"]},
            },
            domain={"row": 0, "column": i},
        ))
    fig_gauge.update_layout(
        grid={"rows": 1, "columns": 3, "pattern": "independent"},
        height=340, margin=dict(t=60, b=30, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter"),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    # Revenue waterfall — tells the story
    st.markdown(f'<div class="stitle">Value Creation Waterfall — Scenario 2 (Monthly per Room)</div>', unsafe_allow_html=True)
    wf_labels = ["Incremental<br>Revenue", "Cost<br>Savings", "Payment<br>to Alexa", "Amenity<br>Costs", "Net Incremental<br>Profit"]
    wf_vals = [r2["amenity_inc_room"], r2["cost_savings_room"], -r2["total_payment_room"], -r2["amenity_cost_room"], r2["inc_cp_room"]]
    fig_wf = go.Figure(go.Waterfall(
        x=wf_labels, y=wf_vals, measure=["absolute", "relative", "relative", "relative", "total"],
        connector=dict(line=dict(color="rgba(201,201,201,.2)", width=1, dash="dot")),
        increasing=dict(marker=dict(color="#4AA8FF", line=dict(color="#4AA8FF", width=0))),
        decreasing=dict(marker=dict(color="#B8B8B8", line=dict(color="#B8B8B8", width=0))),
        totals=dict(marker=dict(color="#1E90FF", line=dict(color="#1E90FF", width=0))),
        text=[f"${v:,.0f}" for v in wf_vals], textposition="outside",
        textfont=dict(size=13, color="#FFFFFF", family="Inter"),
    ))
    apply_plot_theme(fig_wf, height=440)
    fig_wf.update_layout(yaxis=dict(title="$ per Room / Month", gridcolor=GRID_COLOR, title_font=dict(color=AXIS_COLOR, size=11)))
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

    def fmt_money(v, div=1):
        """Accounting format: negatives as ($455), positives as $455."""
        amount = v / div
        if amount < 0:
            return f"(${abs(amount):,.0f})"
        return f"${amount:,.0f}"

    def build_card_table(title, multiplier, is_thousands=False):
        """Build an HTML table card for a given time period."""
        div = 1000 if is_thousands else 1
        rows_html = ""
        # Assumption rows (%)
        for label, s1v, s2v, s3v, *_ in detail_metrics:
            rows_html += f'<tr><td style="text-align:left;font-weight:500;padding:10px 14px;border-bottom:1px solid rgba(125,191,255,.06);color:#8FA3BC;font-size:12.5px;line-height:1.35">{label}</td><td style="text-align:right;padding:10px 14px;border-bottom:1px solid rgba(125,191,255,.06);color:#FFFFFF;font-weight:600;font-variant-numeric:tabular-nums">{s1v}</td><td style="text-align:right;padding:10px 14px;border-bottom:1px solid rgba(125,191,255,.06);color:#D8D8D8;font-weight:600;font-variant-numeric:tabular-nums">{s2v}</td><td style="text-align:right;padding:10px 14px;border-bottom:1px solid rgba(125,191,255,.06);color:#C9C9C9;font-weight:600;font-variant-numeric:tabular-nums">{s3v}</td></tr>'
        # Spacer row
        rows_html += '<tr><td colspan="4" style="padding:6px 0;border-bottom:1px solid rgba(74,168,255,.15)"></td></tr>'
        # Financial rows
        for label, vals in fin_metrics:
            s1 = fmt_money(vals[0]*multiplier, div)
            s2 = fmt_money(vals[1]*multiplier, div)
            s3 = fmt_money(vals[2]*multiplier, div)
            indent = "padding-left:28px;color:#6B7A8F;font-size:12px" if label.startswith("  ") else "font-weight:600;color:#C9C9C9;font-size:12.5px"
            val_muted = any(v < 0 for v in vals)
            v1_color = "#B8C5D6" if val_muted else "#FFFFFF"
            v2_color = "#98A5B8" if val_muted else "#D8D8D8"
            v3_color = "#98A5B8" if val_muted else "#C9C9C9"
            rows_html += f'<tr><td style="text-align:left;{indent};padding:10px 14px;border-bottom:1px solid rgba(125,191,255,.06);line-height:1.35">{label}</td><td style="text-align:right;padding:10px 14px;border-bottom:1px solid rgba(125,191,255,.06);color:{v1_color};font-weight:600;font-variant-numeric:tabular-nums">{s1}</td><td style="text-align:right;padding:10px 14px;border-bottom:1px solid rgba(125,191,255,.06);color:{v2_color};font-weight:600;font-variant-numeric:tabular-nums">{s2}</td><td style="text-align:right;padding:10px 14px;border-bottom:1px solid rgba(125,191,255,.06);color:{v3_color};font-weight:600;font-variant-numeric:tabular-nums">{s3}</td></tr>'
        # Spacer
        rows_html += '<tr><td colspan="4" style="padding:6px 0"></td></tr>'
        # Incremental CP row (bold, emphasized)
        for label, vals in bottom_metrics:
            s1 = fmt_money(vals[0]*multiplier, div)
            s2 = fmt_money(vals[1]*multiplier, div)
            s3 = fmt_money(vals[2]*multiplier, div)
            rows_html += f'<tr style="border-top:2px solid #4AA8FF;background:rgba(74,168,255,.05)"><td style="text-align:left;font-weight:800;padding:12px 14px;color:#FFFFFF;font-size:13px">{label}</td><td style="text-align:right;font-weight:800;padding:12px 14px;color:#4AA8FF;font-size:14px;font-variant-numeric:tabular-nums">{s1}</td><td style="text-align:right;font-weight:800;padding:12px 14px;color:#4AA8FF;font-size:14px;font-variant-numeric:tabular-nums">{s2}</td><td style="text-align:right;font-weight:800;padding:12px 14px;color:#4AA8FF;font-size:14px;font-variant-numeric:tabular-nums">{s3}</td></tr>'
        # ROI row
        rows_html += f'<tr style="background:rgba(74,168,255,.03)"><td style="text-align:left;font-weight:800;padding:10px 14px;color:#FFFFFF;font-size:13px">{roi_row[0]}</td><td style="text-align:right;font-weight:800;padding:10px 14px;color:#4AA8FF;font-size:13px">{roi_row[1][0]}</td><td style="text-align:right;font-weight:800;padding:10px 14px;color:#4AA8FF;font-size:13px">{roi_row[1][1]}</td><td style="text-align:right;font-weight:800;padding:10px 14px;color:#4AA8FF;font-size:13px">{roi_row[1][2]}</td></tr>'

        return f"""<div style="background:linear-gradient(160deg,rgba(15,40,71,.5) 0%,rgba(10,22,40,.7) 100%);border-radius:14px;padding:22px;border:1px solid rgba(125,191,255,.12);backdrop-filter:blur(10px);box-shadow:0 4px 24px rgba(0,0,0,.25)">
        <p style="font-size:10.5px;font-weight:800;text-transform:uppercase;letter-spacing:2px;color:#4AA8FF;margin:0 0 14px;padding-bottom:10px;border-bottom:1px solid rgba(74,168,255,.25)">{title}</p>
        <table style="width:100%;border-collapse:collapse;font-size:12.5px;table-layout:fixed">
        <colgroup><col style="width:37%"><col style="width:21%"><col style="width:21%"><col style="width:21%"></colgroup>
        <tr><th style="text-align:left;padding:8px 14px;font-size:9.5px;text-transform:uppercase;letter-spacing:1.2px;color:#6B7A8F;border-bottom:1px solid rgba(125,191,255,.15);font-weight:700">Metric</th><th style="text-align:right;padding:8px 14px;font-size:9.5px;text-transform:uppercase;letter-spacing:1.2px;color:#FFFFFF;border-bottom:1px solid rgba(125,191,255,.15);font-weight:700">S1</th><th style="text-align:right;padding:8px 14px;font-size:9.5px;text-transform:uppercase;letter-spacing:1.2px;color:#D8D8D8;border-bottom:1px solid rgba(125,191,255,.15);font-weight:700">S2</th><th style="text-align:right;padding:8px 14px;font-size:9.5px;text-transform:uppercase;letter-spacing:1.2px;color:#C9C9C9;border-bottom:1px solid rgba(125,191,255,.15);font-weight:700">S3</th></tr>
        {rows_html}
        </table></div>"""

    tc1, tc2, tc3 = st.columns(3)
    with tc1: st.markdown(build_card_table("Monthly per Room", 1), unsafe_allow_html=True)
    with tc2: st.markdown(build_card_table("Annual per Room", 12), unsafe_allow_html=True)
    with tc3: st.markdown(build_card_table("Annual per Property (in 000s)", 12, is_thousands=True), unsafe_allow_html=True)

    st.markdown('<p style="font-size:10px;color:#6B7A8F;margin:12px 0 0;letter-spacing:0.5px">S1: Scenario 1 &nbsp;&nbsp;|&nbsp;&nbsp; S2: Scenario 2 &nbsp;&nbsp;|&nbsp;&nbsp; S3: Scenario 3</p>', unsafe_allow_html=True)

    # Annual CP bar chart
    fig_cp = go.Figure()
    for sn, r, color in [("Scenario 1", r1, "#FFFFFF"), ("Scenario 2", r2, "#B8B8B8"), ("Scenario 3", r3, "#C9C9C9")]:
        fig_cp.add_trace(go.Bar(
            name=sn, x=["Annual CP / Room", "Annual CP / Property (000s)"],
            y=[r["inc_cp_room"] * 12, ann_prop(r)],
            marker=dict(color=color, line=dict(color="#3C4B5E", width=1)),
            text=[f"${r['inc_cp_room']*12:,.0f}", f"${ann_prop(r):,.0f}K"],
            textposition="outside", textfont=dict(size=13, family="Inter", color="#FFFFFF"),
        ))
    apply_plot_theme(fig_cp, height=400)
    fig_cp.update_layout(barmode="group",
                         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(color=TEXT_COLOR)))
    st.plotly_chart(fig_cp, use_container_width=True)

    # ─── APPENDIX: ASSUMPTIONS ───
    st.markdown('<div class="stitle">Appendix: Assumptions</div>', unsafe_allow_html=True)
    st.markdown('<p class="stitle-sub">Full input parameters driving this analysis · <span style="color:#7DBFFF">All values are configurable in the sidebar</span></p>', unsafe_allow_html=True)

    # Executive narrative callout — McKinsey-style plain-English summary
    active_amenities = [a for a in amenities if a["pct"] > 0]
    active_fixed = [ff for ff in fixed_fees if ff["fee"] > 0 or ff["commission_pct"] > 0]
    total_mix_pct = sum(a["pct"] for a in active_amenities) * 100
    avg_margin = sum(a["margin"] for a in active_amenities) / len(active_amenities) * 100 if active_amenities else 0

    st.markdown(f"""<div style="background:linear-gradient(135deg,rgba(15,40,71,.5) 0%,rgba(30,74,124,.3) 100%);border-radius:12px;padding:20px 26px;margin:0 0 20px;border-left:3px solid #4AA8FF">
    <p style="font-size:10px;text-transform:uppercase;letter-spacing:2px;color:#4AA8FF;font-weight:700;margin:0 0 8px">How to read this</p>
    <p style="font-size:14px;color:#E0E8F2;margin:0;line-height:1.6">
    We modeled <strong style="color:#FFFFFF">{len(active_amenities)} revenue categories</strong> representing <strong style="color:#4AA8FF">{total_mix_pct:.0f}% of ancillary spend per room</strong>, at an average margin of <strong style="color:#4AA8FF">{avg_margin:.0f}%</strong>.
    Partner pays a <strong style="color:#FFFFFF">${monthly_sub:.0f}/room monthly subscription</strong> plus <strong style="color:#FFFFFF">{rev_share_pct*100:.0f}% revenue share</strong> on Alexa-attributed sales.
    One-time device cost is <strong style="color:#FFFFFF">${device_price:.0f}/unit</strong> (amortized over {device_life} months).
    </p></div>""", unsafe_allow_html=True)

    ac1, ac2 = st.columns([1.1, 1])

    # Table 1: Amenity Mix & Margins — shows ALL 12 slots, dims empty ones, ends with Total row
    with ac1:
        st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.8px;color:#4AA8FF;margin:8px 0 12px;padding-bottom:6px;border-bottom:1px solid rgba(74,168,255,.2)">Revenue Mix & Margins</p>', unsafe_allow_html=True)
        max_pct = max((a["pct"] for a in amenities if a["pct"] > 0), default=1)
        total_pct = sum(a["pct"] for a in amenities if a["pct"] > 0)
        # Weighted avg margin across active amenities (weighted by revenue mix %)
        weighted_margin = (sum(a["margin"] * a["pct"] for a in amenities if a["pct"] > 0) / total_pct) if total_pct > 0 else 0
        rows = ""
        for idx, a in enumerate(amenities):
            is_active = a["pct"] > 0
            if is_active:
                # Active row — full color, show name
                display_name = (a["name"] or "").strip() or f"Amenity {idx+1}"
                bar_width = (a["pct"] / max_pct * 100) if max_pct > 0 else 0
                name_color = "#FFFFFF"
                pct_color = "#C9C9C9"
                margin_color = "#C9C9C9"
                pct_display = f"{a['pct']*100:.0f}%"
                margin_display = f"{a['margin']*100:.0f}%"
                bar_html = f'<div style="flex:1;background:rgba(201,201,201,.1);border-radius:3px;height:6px;overflow:hidden"><div style="width:{bar_width}%;height:100%;background:linear-gradient(90deg,#8A96A8,#C9C9C9);border-radius:3px"></div></div>'
                row_bg = ""
            else:
                # Empty/disabled row — blank cells, near-invisible dim, clean presentation
                display_name = "&nbsp;"
                name_color = "#1A2330"
                pct_color = "#1A2330"
                margin_color = "#1A2330"
                pct_display = "&nbsp;"
                margin_display = "&nbsp;"
                bar_html = '<div style="flex:1;background:rgba(26,35,48,.6);border-radius:3px;height:4px"></div>'
                row_bg = "background:rgba(8,14,24,.6);"
            rows += f"""<tr style="{row_bg}">
                <td style="padding:10px 14px;color:{name_color};font-weight:500;border-bottom:1px solid rgba(125,191,255,.06);width:38%">{display_name}</td>
                <td style="padding:10px 14px;border-bottom:1px solid rgba(125,191,255,.06);width:42%">
                  <div style="display:flex;align-items:center;gap:10px">
                    {bar_html}
                    <span style="color:{pct_color};font-weight:700;min-width:38px;text-align:right;font-size:12.5px">{pct_display}</span>
                  </div>
                </td>
                <td style="padding:10px 14px;text-align:right;color:{margin_color};font-weight:600;border-bottom:1px solid rgba(125,191,255,.06);width:20%">{margin_display}</td>
                </tr>"""
        # TOTAL row at the end — all white for clean presentation
        total_bar_html = f'<div style="flex:1;background:rgba(201,201,201,.15);border-radius:3px;height:8px;overflow:hidden"><div style="width:100%;height:100%;background:linear-gradient(90deg,#8A96A8,#FFFFFF);border-radius:3px"></div></div>'
        rows += f"""<tr style="border-top:2px solid #FFFFFF;background:rgba(255,255,255,.05)">
            <td style="padding:12px 14px;color:#FFFFFF;font-weight:800;font-size:13px;text-transform:uppercase;letter-spacing:0.5px">Total</td>
            <td style="padding:12px 14px">
              <div style="display:flex;align-items:center;gap:10px">
                {total_bar_html}
                <span style="color:#FFFFFF;font-weight:800;min-width:38px;text-align:right;font-size:13.5px">{total_pct*100:.0f}%</span>
              </div>
            </td>
            <td style="padding:12px 14px;text-align:right;color:#FFFFFF;font-weight:800;font-size:13.5px">{weighted_margin*100:.0f}%</td>
            </tr>"""
        st.markdown(f"""<div style="background:linear-gradient(160deg,rgba(15,40,71,.4) 0%,rgba(10,22,40,.6) 100%);border-radius:12px;padding:8px;border:1px solid rgba(125,191,255,.1)">
        <table style="width:100%;border-collapse:collapse;font-size:13px;table-layout:fixed">
        <colgroup><col style="width:38%"><col style="width:42%"><col style="width:20%"></colgroup>
        <thead><tr>
        <th style="text-align:left;padding:10px 14px;font-size:10px;text-transform:uppercase;letter-spacing:1.2px;color:#6B7A8F;font-weight:700;border-bottom:1px solid rgba(125,191,255,.15)">Amenity</th>
        <th style="text-align:left;padding:10px 14px;font-size:10px;text-transform:uppercase;letter-spacing:1.2px;color:#6B7A8F;font-weight:700;border-bottom:1px solid rgba(125,191,255,.15)">% of Revenue Mix</th>
        <th style="text-align:right;padding:10px 14px;font-size:10px;text-transform:uppercase;letter-spacing:1.2px;color:#6B7A8F;font-weight:700;border-bottom:1px solid rgba(125,191,255,.15)">Margin</th>
        </tr></thead>
        <tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)

    # Table 2: Deal Terms — grouped into Recurring / One-time / Fixed Fees
    with ac2:
        st.markdown('<p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.8px;color:#4AA8FF;margin:8px 0 12px;padding-bottom:6px;border-bottom:1px solid rgba(74,168,255,.2)">Deal Terms & Charges</p>', unsafe_allow_html=True)

        def section(title, items, accent_color="#7DBFFF"):
            """Build a grouped charges section with fixed column widths."""
            rows = ""
            for label, value in items:
                rows += f"""<tr>
                <td style="padding:9px 14px;color:#C9C9C9;font-size:13px;border-bottom:1px solid rgba(125,191,255,.06);width:65%">{label}</td>
                <td style="padding:9px 14px;text-align:right;color:#FFFFFF;font-weight:600;font-size:13px;border-bottom:1px solid rgba(125,191,255,.06);width:35%;font-variant-numeric:tabular-nums">{value}</td>
                </tr>"""
            return f"""<div style="margin-bottom:16px">
            <p style="font-size:10px;text-transform:uppercase;letter-spacing:1.8px;color:{accent_color};font-weight:700;margin:0 0 6px;padding-left:10px;border-left:2px solid {accent_color}">{title}</p>
            <table style="width:100%;border-collapse:collapse;table-layout:fixed">
            <colgroup><col style="width:65%"><col style="width:35%"></colgroup>
            {rows}</table>
            </div>"""

        # Group 1: Recurring (monthly)
        recurring = [
            ("Revenue Share %", f"{rev_share_pct*100:.0f}%"),
            ("Monthly Subscription", f"${monthly_sub:.2f} / room"),
            ("Monthly Device Amortization", f"${monthly_device_amort:.2f} / room"),
        ]

        # Group 2: One-time device costs
        one_time = [
            ("Device MSRP", f"${device_msrp:,.2f}"),
            ("Device Discount", f"{device_discount*100:.0f}%"),
            ("Device Net Price", f"${device_price:,.2f}"),
            ("Setup Fee", f"${device_setup:,.2f} / unit"),
            ("Device Life", f"{device_life} months"),
        ]

        # Group 3: Fixed Fees (dynamic — only active)
        fixed_rows = []
        for ff in fixed_fees:
            if ff["fee"] > 0:
                fixed_rows.append((f"{ff['name']} — fee/txn", f"${ff['fee']:.2f}"))
            if ff["commission_pct"] > 0:
                fixed_rows.append((f"{ff['name']} — commission", f"{ff['commission_pct']*100:.0f}%"))

        html = f"""<div style="background:linear-gradient(160deg,rgba(15,40,71,.4) 0%,rgba(10,22,40,.6) 100%);border-radius:12px;padding:16px 18px;border:1px solid rgba(125,191,255,.1)">
        {section("Recurring / Monthly", recurring, "#4AA8FF")}
        {section("One-Time Device Cost", one_time, "#7DBFFF")}"""
        if fixed_rows:
            html += section("Fixed Fee Amenities", fixed_rows, "#C9C9C9")
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

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
            connector=dict(line=dict(color="rgba(201,201,201,.2)", dash="dot")),
            increasing=dict(marker=dict(color="#4AA8FF")),
            decreasing=dict(marker=dict(color="#B8B8B8")),
            totals=dict(marker=dict(color="#1E90FF")),
            text=[f"${v:,.0f}" for v in wf_v], textposition="outside",
            textfont=dict(color="#FFFFFF", family="Inter", size=12)))
        apply_plot_theme(fig_wf, height=400)
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
        colorscale=[[0,"#3C4B5E"],[0.3,"#5A6B82"],[0.5,"#909090"],[0.7,"#7DBFFF"],[1,"#4AA8FF"]],
        text=[[f"${v:,.0f}" for v in row] for row in cp_heat], texttemplate="%{text}",
        textfont=dict(size=10, color="#FFFFFF"), colorbar=dict(title=dict(text="CP/Room", font=dict(color=AXIS_COLOR)), tickfont=dict(color=AXIS_COLOR)), zmid=0,
    ))
    apply_plot_theme(fig_cp, height=540)
    fig_cp.update_layout(title=dict(text=f"{partner_name} — CP per Room", font=dict(color="#FFFFFF", size=14)),
        xaxis_title="Ancillary Transaction % through Alexa", yaxis_title="Revenue Growth % due to Alexa")
    st.plotly_chart(fig_cp, use_container_width=True)

    st.markdown(f'<div class="stitle">ROI % — Txn % × Revenue Growth</div>', unsafe_allow_html=True)
    fig_roi = go.Figure(data=go.Heatmap(
        z=roi_heat, x=[f"{t*100:.0f}%" for t in txn_ax], y=[f"{i*100:.1f}%" for i in inc_ax],
        colorscale=[[0,"#3C4B5E"],[0.3,"#5A6B82"],[0.5,"#909090"],[0.7,"#7DBFFF"],[1,"#4AA8FF"]],
        text=[[f"{v}%" for v in row] for row in roi_heat], texttemplate="%{text}",
        textfont=dict(size=10, color="#FFFFFF"), colorbar=dict(title=dict(text="ROI %", font=dict(color=AXIS_COLOR)), tickfont=dict(color=AXIS_COLOR)), zmid=0,
    ))
    apply_plot_theme(fig_roi, height=540)
    fig_roi.update_layout(title=dict(text=f"{partner_name} — ROI %", font=dict(color="#FFFFFF", size=14)),
        xaxis_title="Ancillary Transaction % through Alexa", yaxis_title="Revenue Growth % due to Alexa")
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
        colorscale=[[0,"#0A1628"],[0.5,"#1E4A7C"],[1,"#4AA8FF"]], text=[[f"${v:,.0f}" for v in row] for row in pay_heat],
        texttemplate="%{text}", textfont=dict(size=10, color="#FFFFFF"),
        colorbar=dict(title=dict(text="$/Room", font=dict(color=AXIS_COLOR)), tickfont=dict(color=AXIS_COLOR)),
    ))
    apply_plot_theme(fig_pay, height=460)
    fig_pay.update_layout(title=dict(text="Monthly Payment per Room (Sub + Rev Share + Fees)", font=dict(color="#FFFFFF", size=14)),
        xaxis_title="Ancillary Transaction %", yaxis_title="ASP Rev Share %")
    st.plotly_chart(fig_pay, use_container_width=True)

# Footer
st.markdown(f"""<div class="app-footer">
<p class="brand">Alexa+ for Hospitality</p>
<p class="sub">Amazon Confidential · ©{datetime.now().year} Amazon.com or its affiliates</p></div>""", unsafe_allow_html=True)
