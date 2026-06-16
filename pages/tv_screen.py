import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import plotly.express as px
st.markdown("""
<style>

.stApp {
    background-color: #f4f7fb;
    color: #1e293b;
}

.main .block-container {
    background-color: #f4f7fb;
}

section[data-testid="stSidebar"] {
    background-color: #e9eef5;
}

section[data-testid="stSidebar"] * {
    color: #1e293b !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #1e293b !important;
}

p, span, label, div {
    color: #475569 !important;
}

[data-testid="metric-container"] {
    background: white;
    border: 1px solid #dbe4ee;
    border-radius: 12px;
    padding: 15px;
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
st.sidebar.header("Filters")

columns_to_show = st.sidebar.multiselect(
    "Select columns to display",
    options=display_df.columns.tolist(),
    default=display_df.columns.tolist()
)
st.dataframe(
    display_df[columns_to_show],
)

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

st.subheader("Supplier Delivery Performance")
st.subheader("Supplier Accuracy Chart")

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
st.bar_chart(chart_df)
