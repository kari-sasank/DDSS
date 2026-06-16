import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #f4f7fb;
    color: #1e293b;
}

/* Main Content Area */
.main .block-container {
    background-color: #f4f7fb;
    padding-top: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #e9eef5;
    border-right: 1px solid #dbe4ee;
}

section[data-testid="stSidebar"] * {
    color: #1e293b !important;
}

/* Titles */
h1, h2, h3, h4, h5, h6 {
    color: #1e293b !important;
    font-weight: 700;
}

/* Text */
p, span, label, div {
    color: #475569;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #dbe4ee;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Metric Labels */
[data-testid="metric-container"] label {
    color: #64748b !important;
    font-weight: 600;
}

/* Metric Values */
[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-size: 32px !important;
    font-weight: 700 !important;
}

/* Tables */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 12px;
    border: 1px solid #dbe4ee;
}

/* Buttons */
.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
}

.stButton button:hover {
    background-color: #1d4ed8;
}

/* Dividers */
hr {
    border-color: #dbe4ee;
}

/* Plotly Charts */
.js-plotly-plot {
    background: white !important;
    border-radius: 12px;
    padding: 10px;
    border: 1px solid #dbe4ee;
}
            /* Selectbox */
.stSelectbox > div > div {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #dbe4ee !important;
    border-radius: 10px !important;
}

/* Dropdown text */
.stSelectbox label {
    color: #334155 !important;
    font-weight: 600;
}

/* Input fields */
.stTextInput input,
.stNumberInput input {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #dbe4ee !important;
    border-radius: 10px !important;
}
/* Force light selectbox */
div[data-baseweb="select"] > div {
    background: white !important;
    color: #1e293b !important;
    border: 1px solid #dbe4ee !important;
    border-radius: 10px !important;
}

/* Selected value */
div[data-baseweb="select"] span {
    color: #1e293b !important;
}

/* Dropdown menu */
div[role="listbox"] {
    background: white !important;
}

div[role="option"] {
    color: #1e293b !important;
    background: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("DDSS - Supplier Delivery Performance Dashboard")
st.caption("Real-time supplier delivery monitoring and performance tracking")

# SQL CONNECTION
db_server = os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")

connection_string = (
    f"mssql+pyodbc://@{db_server}/{db_name}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(connection_string)

query = """
SELECT
    [Supplier Name] AS Supplier_Name,
    COUNT(*) AS Total_Deliveries,
    SUM([DLV ODR QTY]) AS Ordered_Qty,
    SUM([Shipment QTY]) AS Shipped_Qty,
    SUM([Received QTY]) AS Received_Qty
FROM SupplierDelivery
GROUP BY [Supplier Name]
ORDER BY COUNT(*) DESC
"""

df = pd.read_sql(query, engine)

df = df.fillna(0)

# CALCULATIONS
df["Pending_Qty"] = (
    df["Ordered_Qty"] - df["Received_Qty"]
)
df["Negative_Qty"] = -df["Pending_Qty"]

df["Delivery_Accuracy_%"] = (
    df["Received_Qty"] /
    df["Ordered_Qty"].replace(0, 1)
) * 100

# STATUS
df["Status"] = df["Delivery_Accuracy_%"].apply(
    lambda x:
    "🟢 GREEN" if x >= 95
    else "🟡 YELLOW" if x >= 80
    else "🔴 RED"
)

from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="DDSS Supplier Dashboard",
    layout="wide"
)

st.title("DDSS SUPPLIER DASHBOARD")

# SQL CONNECTION
db_server = os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")

connection_string = (
    f"mssql+pyodbc://@{db_server}/{db_name}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(connection_string)

query = """
SELECT
    [Supplier Name] AS Supplier_Name,
    COUNT(*) AS Total_Deliveries,
    SUM([DLV ODR QTY]) AS Ordered_Qty,
    SUM([Shipment QTY]) AS Shipped_Qty,
    SUM([Received QTY]) AS Received_Qty
FROM SupplierDelivery
GROUP BY [Supplier Name]
ORDER BY COUNT(*) DESC
"""

df = pd.read_sql(query, engine)

df = df.fillna(0)

# CALCULATIONS
df["Pending_Qty"] = (
    df["Ordered_Qty"] - df["Received_Qty"]
)

df["Delivery_Accuracy_%"] = (
    df["Received_Qty"] /
    df["Ordered_Qty"].replace(0, 1)
) * 100

# STATUS
df["Status"] = df["Delivery_Accuracy_%"].apply(
    lambda x:
    "🟢 GREEN" if x >= 95
    else "🟡 YELLOW" if x >= 80
    else "🔴 RED"
)

# KPI CARDS
total_suppliers = len(df)
total_orders = int(df["Ordered_Qty"].sum())
total_received = int(df["Received_Qty"].sum())
avg_accuracy = round(df["Delivery_Accuracy_%"].mean(), 2)

st.markdown("""
<style>
[data-testid="metric-container"] {
    background-color: #1e293b;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

[data-testid="metric-container"] label {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
}

[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-size: 30px !important;
    color: #60a5fa !important;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Active Suppliers", total_suppliers)
col2.metric("Total Ordered Quantity", total_orders)
col3.metric("Total Received Quantity", total_received)
col4.metric("Average Delivery Accuracy", f"{avg_accuracy}%")
st.divider()

# TABLE
st.subheader("Supplier Delivery Performance Overview")

display_df = df.rename(columns={
    "Supplier_Name": "Supplier",
    "Total_Deliveries": "Total Deliveries",
    "Ordered_Qty": "Ordered Quantity",
    "Received_Qty": "Received Quantity",
    "Pending_Qty": "Pending Quantity",
    "Delivery_Accuracy_%": "Delivery Accuracy (%)",
    "Status": "Delivery Status"
})
st.sidebar.header("Filters")

selected_metrics = st.sidebar.multiselect(
    "Select Metrics",
    [
        "Total Deliveries",
        "Ordered Quantity",
        "Received Quantity",
        "Pending Quantity",
        "Delivery Accuracy"
    ],
    default=[
        "Total Deliveries",
        "Ordered Quantity",
        "Received Quantity",
        "Pending Quantity",
        "Delivery Accuracy"
    ]
)

columns_to_show = ["Supplier"]

if "Total Deliveries" in selected_metrics:
    columns_to_show.append("Total Deliveries")

if "Ordered Quantity" in selected_metrics:
    columns_to_show.append("Ordered Quantity")

if "Received Quantity" in selected_metrics:
    columns_to_show.append("Received Quantity")

if "Pending Quantity" in selected_metrics:
    columns_to_show.append("Pending Quantity")

if "Delivery Accuracy" in selected_metrics:
    columns_to_show.append("Delivery Accuracy (%)")
st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)
st.divider()

# TOP SUPPLIERS
st.subheader("Top 5 Performing Suppliers")

top5 = df.sort_values(
    by="Delivery_Accuracy_%",
    ascending=False
).head(5)

st.table(
    top5[
        [
            "Supplier_Name",
            "Total_Deliveries",
            "Delivery_Accuracy_%"
        ]
    ]
)

st.divider()

# CHART
st.subheader("📊 Supplier Accuracy")

chart_df = df[
    ["Supplier_Name", "Delivery_Accuracy_%"]
].set_index("Supplier_Name")

import plotly.express as px

chart_df = df[
    ["Supplier_Name", "Received_Qty", "Negative_Qty"]
]

fig = px.bar(
    chart_df,
    x="Supplier_Name",
    y=["Received_Qty", "Negative_Qty"],
    barmode="group",
    title="Supplier Delivery Performance",
    color_discrete_sequence=["#2E8B57", "#DC143C"]
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("""
### Graph Explanation

🟢 Green Bars = Quantity Successfully Received

🔴 Red Bars = Pending / Negative Quantity

Higher green bars indicate better supplier performance.

Higher red bars indicate delivery risk and pending shipments.
""")
st.bar_chart(chart_df)

st.divider()

# STATUS SUMMARY
green = len(df[df["Status"].str.contains("GREEN")])
yellow = len(df[df["Status"].str.contains("YELLOW")])
red = len(df[df["Status"].str.contains("RED")])

st.subheader("Traffic Status Summary")

c1, c2, c3 = st.columns(3)

c1.success(f"GREEN : {green}")
c2.warning(f"YELLOW : {yellow}")
c3.error(f"RED : {red}")