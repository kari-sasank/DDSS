import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(
    page_title="DDSS Supplier Dashboard",
    layout="wide"
)

st.title("DDSS SUPPLIER DASHBOARD")

# SQL CONNECTION
connection_string = (
    "mssql+pyodbc://@SAMEERA\\SQLEXPRESS/sam"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
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

col1, col2, col3, col4 = st.columns(4)

col1.metric("Suppliers", total_suppliers)
col2.metric("Ordered Qty", total_orders)
col3.metric("Received Qty", total_received)
col4.metric("Avg Accuracy %", avg_accuracy)

st.divider()

# TABLE
st.subheader("Supplier Performance")

st.dataframe(
    df[
        [
            "Supplier_Name",
            "Total_Deliveries",
            "Ordered_Qty",
            "Received_Qty",
            "Pending_Qty",
            "Delivery_Accuracy_%",
            "Status"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# TOP SUPPLIERS
st.subheader("🏆 Top 5 Suppliers")

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