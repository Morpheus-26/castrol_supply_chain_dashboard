import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import plotly.express as px
# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Castrol Supply Chain Command Center",
    page_icon="📦",
    layout="wide"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.main{
    background-color:#f7f9fb;
}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

[data-testid="metric-container"]{
    background:white;
    border-radius:12px;
    padding:15px;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUTS = PROJECT_ROOT / "outputs"

ASSETS = PROJECT_ROOT / "assets"

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    planning = pd.read_csv(
        OUTPUTS / "planning_table.csv"
    )

    plants = pd.read_csv(
        OUTPUTS / "plants.csv"
    )

    forecast = pd.read_csv(
        OUTPUTS / "jan_forecast.csv"
    )

    inventory = pd.read_csv(
        OUTPUTS / "inventory.csv"
    )

    return planning, plants, forecast, inventory


try:

    planning, plants, forecast, inventory = load_data()

except Exception as e:

    st.error("Unable to load processed CSV files.")

    st.exception(e)

    st.stop()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Filters")

# Region

regions = sorted(
    planning["CFA region"].unique()
)

selected_region = st.sidebar.selectbox(

    "Region",

    ["All"] + list(regions)

)

# CFA

cfas = sorted(
    planning["CFA"].unique()
)

selected_cfa = st.sidebar.selectbox(

    "CFA",

    ["All"] + list(cfas)

)

# Product

products = sorted(
    planning["Product Name"].unique()
)

selected_product = st.sidebar.selectbox(

    "Product",

    ["All"] + list(products)

)

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered = planning.copy()

if selected_region != "All":

    filtered = filtered[
        filtered["CFA region"] == selected_region
    ]

if selected_cfa != "All":

    filtered = filtered[
        filtered["CFA"] == selected_cfa
    ]

if selected_product != "All":

    filtered = filtered[
        filtered["Product Name"] == selected_product
    ]

# ==========================================================
# HEADER
# ==========================================================

left,right = st.columns([1,6])

logo = ASSETS / "castrol_logo.png"

if logo.exists():

    left.image(str(logo), width=120)

with right:

    st.title("Castrol Supply Chain Command Center")

    st.caption(
        "Supply Chain Decision Support Dashboard"
    )

st.markdown("---")

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

capacity_columns = [

    "Line Capacity \n<=1.5 LT (kl / month)",

    "Line Capacity \n3- 5 LT (kl / month)",

    "Line Capacity \n7- 20 LT (kl / month)",

    "Line Capacity \n50 LT (kl / month)",

    "Line Capacity \n180- 210LT (kl / month)"

]

plants[capacity_columns] = plants[
    capacity_columns
].apply(
    pd.to_numeric,
    errors="coerce"
)

total_capacity = plants[
    capacity_columns
].sum().sum()

forecast_total = filtered[
    "Forecast"
].sum()

inventory_total = filtered[
    "Opening Inventory"
].sum()

net_requirement = filtered[
    "Net Requirement"
].sum()

utilization = (
    net_requirement /
    total_capacity
) * 100

inventory_cover = (
    inventory_total /
    forecast_total
) * 100

# ==========================================================
# KPI CARDS
# ==========================================================

# -------------------------
# First Row
# -------------------------

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Forecast", f"{forecast_total:,.0f} KL")
k2.metric("Inventory", f"{inventory_total:,.0f} KL")
k3.metric("Net Requirement", f"{net_requirement:,.0f} KL")
k4.metric("Capacity", f"{total_capacity:,.0f} KL")
k5.metric("Utilization", f"{utilization:.1f}%")

# -------------------------
# Second Row
# -------------------------

k6, k7 = st.columns(2)

k6.metric("Plants", plants["Plant Code"].nunique())
k7.metric("CFAs", filtered["CFA"].nunique())


st.markdown("---")

# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

left,right = st.columns([3,1])

with left:

    st.subheader("Executive Summary")

    st.write("""
This dashboard provides an integrated view of production,
inventory, demand and supply chain performance across the
Castrol distribution network.
""")

with right:

    st.info(

f"""
**Generated**

{datetime.now().strftime("%d-%m-%Y")}

{datetime.now().strftime("%H:%M")}
"""

    )

st.markdown("---")

# ==========================================================
# DEMAND ANALYTICS
# ==========================================================

st.header("📊 Demand Analytics")

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# Demand by Region
# ----------------------------------------------------------

with col1:

    region_data = (
        filtered
        .groupby("CFA region", as_index=False)["Forecast"]
        .sum()
        .sort_values("Forecast", ascending=False)
    )

    fig = px.bar(
        region_data,
        x="CFA region",
        y="Forecast",
        color="Forecast",
        color_continuous_scale="Greens",
        text_auto=".1f",
        title="Demand by Region"
    )

    fig.update_layout(
        height=420,
        xaxis_title="Region",
        yaxis_title="Forecast (KL)",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------------------------
# Demand by CFA
# ----------------------------------------------------------

with col2:

    cfa_data = (
        filtered
        .groupby("CFA", as_index=False)["Forecast"]
        .sum()
        .sort_values("Forecast", ascending=False)
    )

    fig = px.bar(
        cfa_data,
        x="Forecast",
        y="CFA",
        orientation="h",
        color="Forecast",
        color_continuous_scale="Blues",
        text_auto=".0f",
        title="Demand by CFA"
    )

    fig.update_layout(
        height=420,
        coloraxis_showscale=False,
        xaxis_title="Forecast (KL)",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# ==========================================================
# PRODUCT ANALYTICS
# ==========================================================

st.header("📦 Product Analytics")

product_data = (
    filtered
    .groupby("Product Name", as_index=False)["Forecast"]
    .sum()
    .sort_values("Forecast", ascending=False)
    .head(10)
)

fig = px.bar(
    product_data,
    x="Forecast",
    y="Product Name",
    orientation="h",
    color="Forecast",
    color_continuous_scale="Viridis",
    text_auto=".0f",
    title="Top 10 Products by Demand"
)

fig.update_layout(
    height=500,
    coloraxis_showscale=False,
    xaxis_title="Forecast (KL)",
    yaxis_title=""
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# ==========================================================
# PLANT ANALYTICS
# ==========================================================

st.header("🏭 Plant Analytics")

plants["Total Capacity"] = plants[
    capacity_columns
].sum(axis=1)

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# Plant Capacity
# ----------------------------------------------------------

with col1:

    fig = px.bar(
        plants,
        x="Location",
        y="Total Capacity",
        color="Total Capacity",
        color_continuous_scale="Oranges",
        text_auto=".0f",
        title="Plant Capacity"
    )

    fig.update_layout(
        height=420,
        coloraxis_showscale=False,
        xaxis_title="Plant",
        yaxis_title="Capacity (KL)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------------------------
# Production Cost
# ----------------------------------------------------------

with col2:

    fig = px.bar(
        plants,
        x="Location",
        y="Production Cost (₹/kl)",
        color="Production Cost (₹/kl)",
        color_continuous_scale="Reds",
        text_auto=".0f",
        title="Production Cost per KL"
    )

    fig.update_layout(
        height=420,
        coloraxis_showscale=False,
        xaxis_title="Plant",
        yaxis_title="₹ / KL"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# ==========================================================
# INVENTORY ANALYTICS
# ==========================================================

st.header("📦 Inventory Analytics")

comparison = pd.DataFrame({

    "Category": [
        "Forecast",
        "Inventory",
        "Net Requirement"
    ],

    "Volume": [
        forecast_total,
        inventory_total,
        net_requirement
    ]

})

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# Forecast vs Inventory
# ----------------------------------------------------------

with col1:

    fig = px.bar(
        comparison,
        x="Category",
        y="Volume",
        color="Category",
        text_auto=".0f",
        title="Forecast vs Inventory"
    )

    fig.update_layout(
        height=420,
        showlegend=False,
        yaxis_title="KL"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------------------------
# Demand Distribution
# ----------------------------------------------------------

with col2:

    fig = px.pie(
        region_data,
        names="CFA region",
        values="Forecast",
        hole=0.45,
        title="Demand Distribution"
    )

    fig.update_layout(
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

st.header("💡 Executive Insights")

col1, col2 = st.columns(2)

# Highest Demand Region
highest_region = (
    region_data.sort_values(
        "Forecast",
        ascending=False
    ).iloc[0]
)

highest_cfa = (
    cfa_data.sort_values(
        "Forecast",
        ascending=False
    ).iloc[0]
)

highest_capacity = (
    plants.sort_values(
        "Total Capacity",
        ascending=False
    ).iloc[0]
)

lowest_cost = (
    plants.sort_values(
        "Production Cost (₹/kl)"
    ).iloc[0]
)

with col1:

    st.success(
        f"""
### 📈 Demand Insights

• Highest Demand Region : **{highest_region['CFA region']}**

• Highest Demand CFA : **{highest_cfa['CFA']}**

• Total Forecast : **{forecast_total:,.0f} KL**

• Net Requirement : **{net_requirement:,.0f} KL**
"""
    )

with col2:

    if utilization < 80:

        status = "🟢 Capacity is sufficient."

    elif utilization < 95:

        status = "🟡 Capacity is nearing full utilization."

    else:

        status = "🔴 Capacity expansion recommended."

    st.info(
        f"""
### 🏭 Production Insights

• Largest Plant : **{highest_capacity['Location']}**

• Lowest Cost Plant : **{lowest_cost['Location']}**

• Utilization : **{utilization:.1f}%**

• {status}
"""
    )

st.markdown("---")

# ==========================================================
# SUPPLY CHAIN SUMMARY
# ==========================================================

st.header("📋 Supply Chain Summary")

summary = pd.DataFrame({

    "Metric":[

        "Forecast",

        "Opening Inventory",

        "Net Requirement",

        "Plant Capacity",

        "Inventory Coverage",

        "Capacity Utilization"

    ],

    "Value":[

        f"{forecast_total:,.0f} KL",

        f"{inventory_total:,.0f} KL",

        f"{net_requirement:,.0f} KL",

        f"{total_capacity:,.0f} KL",

        f"{inventory_cover:.1f}%",

        f"{utilization:.1f}%"

    ]

})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================================================
# DOWNLOAD FILTERED DATA
# ==========================================================

st.header("📥 Export Data")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(

    label="⬇ Download Planning Table",

    data=csv,

    file_name="planning_table.csv",

    mime="text/csv"

)

st.markdown("---")

# ==========================================================
# DATA EXPLORER
# ==========================================================

st.header("🗂 Data Explorer")

with st.expander("Planning Table"):

    st.dataframe(
        filtered,
        use_container_width=True,
        height=400
    )

with st.expander("Plant Information"):

    st.dataframe(
        plants,
        use_container_width=True
    )

with st.expander("Forecast Data"):

    st.dataframe(
        forecast,
        use_container_width=True
    )

with st.expander("Inventory Data"):

    st.dataframe(
        inventory,
        use_container_width=True
    )

st.markdown("---")

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
"""
Developed as part of the Castrol Supply Chain Case Competition.

Built using Python • Pandas • Plotly • Streamlit
"""
)