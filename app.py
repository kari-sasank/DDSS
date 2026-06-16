import streamlit as st
import pandas as pd

st.title("DDSS Dashboard")

page = st.sidebar.selectbox(
    "Choose Screen",
    ["TV Screen", "Portal Screen"]
)

if page == "TV Screen":

    st.title("DDSS TV SCREEN")

    data = pd.DataFrame({
        "Lot": ["5HG1139", "5HG1140", "5HG1141", "5HG1142"],
        "Status": ["GREEN", "GREEN", "RED", "YELLOW"]
    })

    st.dataframe(data, use_container_width=True)

elif page == "Portal Screen":

    st.title("🏭 PORTAL SCREEN")

    data = pd.DataFrame({
        "Supplier": [
            "ASK AUTOMOTIVE",
            "VARROC ENGINEERING",
            "FIEM"
        ],
        "Accuracy (%)": [50, 0, 100],
        "Risk (%)": [50, 100, 0]
    })

    st.dataframe(data, use_container_width=True)