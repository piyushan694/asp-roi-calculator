import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="ASP 2026 OP2 Dashboard", layout="wide")
st.title("ASP 2026 OP2 — Alexa Smart Properties Revenue Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv(Path(__file__).parent / "data.csv")
    df["Start Date"] = pd.to_datetime(df["Start Date"], format="mixed")
    df["Month"] = df["Start Date"].dt.strftime("%b")
    df["MonthNum"] = df["Start Date"].dt.month
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())
verticals = st.sidebar.multiselect("Vertical", df["Vertical"].unique(), default=df["Vertical"].unique())
alexa_type = st.sidebar.multiselect("Classic Alexa / Alexa+", df["Classic Alexa/Alexa+"].unique(), default=df["Classic Alexa/Alexa+"].unique())

filtered = df[
    (df["Region"].isin(regions)) &
    (df["Vertical"].isin(verticals)) &
    (df["Classic Alexa/Alexa+"].isin(alexa_type))
]

# --- KPI Cards ---
rev_df = filtered[filtered["Metrics"] == "Revenue (Subscription + Rev-Share)"]
ib_df = filtered[filtered["Metrics"] == "Install Base"]
nd_df = filtered[filtered["Metrics"] == "New Deployments"]

total_rev = rev_df["Value"].sum()
total_ib_dec = ib_df[ib_df["MonthNum"] == 12]["Value"].sum()
total_nd = nd_df["Value"].sum()

c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue (Sub + Rev-Share)", f"${total_rev:,.0f}")
c2.metric("Install Base (Dec 2026)", f"{total_ib_dec:,.0f}")
c3.metric("New Deployments (Full Year)", f"{total_nd:,.0f}")

st.divider()

# --- Monthly Revenue Trend by Region ---
st.subheader("Monthly Revenue Trend by Region")
rev_monthly = rev_df.groupby(["MonthNum", "Month", "Region"])["Value"].sum().reset_index()
rev_monthly = rev_monthly.sort_values("MonthNum")
fig1 = px.line(rev_monthly, x="Month", y="Value", color="Region",
               labels={"Value": "Revenue ($)", "Month": ""},
               category_orders={"Month": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]})
fig1.update_layout(height=400)
st.plotly_chart(fig1, use_container_width=True)

# --- Revenue by Vertical ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Vertical")
    rev_vert = rev_df.groupby("Vertical")["Value"].sum().reset_index()
    rev_vert = rev_vert[rev_vert["Value"] > 0].sort_values("Value", ascending=False)
    fig2 = px.bar(rev_vert, x="Vertical", y="Value", color="Vertical",
                  labels={"Value": "Revenue ($)"})
    fig2.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Classic Alexa vs Alexa+")
    rev_type = rev_df.groupby("Classic Alexa/Alexa+")["Value"].sum().reset_index()
    fig3 = px.pie(rev_type, values="Value", names="Classic Alexa/Alexa+", hole=0.4)
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

# --- Top Partners by Revenue ---
st.subheader("Top 15 Partners by Total Revenue")
rev_partner = rev_df.groupby("Partner Name")["Value"].sum().reset_index()
rev_partner = rev_partner[rev_partner["Value"] > 0].sort_values("Value", ascending=False).head(15)
fig4 = px.bar(rev_partner, x="Value", y="Partner Name", orientation="h",
              labels={"Value": "Revenue ($)", "Partner Name": ""},
              color="Value", color_continuous_scale="Blues")
fig4.update_layout(yaxis=dict(autorange="reversed"), height=500, showlegend=False)
st.plotly_chart(fig4, use_container_width=True)

# --- Install Base Trend ---
st.subheader("Monthly Install Base Trend")
ib_monthly = ib_df.groupby(["MonthNum", "Month"])["Value"].sum().reset_index().sort_values("MonthNum")
fig5 = px.area(ib_monthly, x="Month", y="Value",
               labels={"Value": "Install Base", "Month": ""},
               category_orders={"Month": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]})
fig5.update_layout(height=350)
st.plotly_chart(fig5, use_container_width=True)

# --- Data Table ---
with st.expander("View Raw Data"):
    st.dataframe(filtered, use_container_width=True, height=400)
