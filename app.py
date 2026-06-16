import streamlit as st
import pandas as pd
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

</style>
""", unsafe_allow_html=True)

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

    st.dataframe(data, width = "stretch")

elif page == "Portal Screen":

    st.title("PORTAL SCREEN")

    data = pd.DataFrame({
        "Supplier": [
            "ASK AUTOMOTIVE",
            "VARROC ENGINEERING",
            "FIEM"
        ],
        "Accuracy (%)": [50, 0, 100],
        "Risk (%)": [50, 100, 0]
    })

    st.dataframe(data, width = "stretch")