import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(
    page_title="DDSS TV Screen",
    layout="wide"
)

st.title("DDSS TV SCREEN")

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
    SUM([Received QTY]) AS Received_Qty
FROM SupplierDelivery
GROUP BY [Supplier Name]
"""

df = pd.read_sql(query, engine)

df = df.fillna(0)

# Accuracy Calculation
df["Delivery_Accuracy_%"] = (
    df["Received_Qty"]
    / df["Ordered_Qty"].replace(0, 1)
) * 100

# Status Logic
def get_status(acc):
    if acc >= 95:
        return "🟢 GREEN"
    elif acc >= 80:
        return "🟡 YELLOW"
    else:
        return "🔴 RED"

df["Status"] = df["Delivery_Accuracy_%"].apply(get_status)

# Sort best to worst
df = df.sort_values(
    by="Delivery_Accuracy_%",
    ascending=False
)

# KPI Cards
green = len(df[df["Status"].str.contains("GREEN")])
yellow = len(df[df["Status"].str.contains("YELLOW")])
red = len(df[df["Status"].str.contains("RED")])

c1, c2, c3 = st.columns(3)

c1.success(f"🟢 GREEN : {green}")
c2.warning(f"🟡 YELLOW : {yellow}")
c3.error(f"🔴 RED : {red}")

st.divider()

st.subheader("Live Supplier Status")

st.dataframe(
    df[
        [
            "Supplier_Name",
            "Total_Deliveries",
            "Ordered_Qty",
            "Received_Qty",
            "Delivery_Accuracy_%",
            "Status"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Supplier Accuracy Chart")

chart_df = df[
    ["Supplier_Name", "Delivery_Accuracy_%"]
].set_index("Supplier_Name")

st.bar_chart(chart_df)