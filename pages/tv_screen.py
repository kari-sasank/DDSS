import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import plotly.express as px

load_dotenv()

st.set_page_config(
    page_title="DDSS TV Screen",
    layout="wide"
)

st.title("DDSS TV SCREEN")

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
df["Delivery_Accuracy_%"] = df["Delivery_Accuracy_%"].clip(lower=0, upper=100)

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

display_df = df.rename(columns={
    "Supplier_Name": "Supplier",
    "Total_Deliveries": "Total Deliveries",
    "Ordered_Qty": "Ordered Quantity",
    "Received_Qty": "Received Quantity",
    "Delivery_Accuracy_%": "Delivery Accuracy (%)",
    "Status": "Delivery Status"
})

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Supplier Delivery Performance")

chart_df = df[
    ["Supplier_Name", "Delivery_Accuracy_%"]
].set_index("Supplier_Name")

chart_df = (
    df[["Supplier_Name", "Delivery_Accuracy_%"]]
    .sort_values(
        by="Delivery_Accuracy_%",
        ascending=False
    )
)

fig = px.bar(
    chart_df,
    x="Supplier_Name",
    y="Delivery_Accuracy_%",
    color="Delivery_Accuracy_%",
    color_continuous_scale=[
        "#d73027",
        "#fee08b",
        "#1a9850"
    ]
)

fig.update_layout(
    title="Supplier Delivery Performance",
    xaxis_title="Supplier",
    yaxis_title="Accuracy (%)",
    height=550
)

fig.update_xaxes(
    tickangle=-45
)

fig.update_traces(
    texttemplate="%{y:.1f}",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.caption(
    "Higher accuracy percentages indicate better supplier delivery performance."
)