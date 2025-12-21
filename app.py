import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FMCG Demand Forecasting",
    layout="wide"
)

st.title("📦 FMCG Sales Demand Forecasting")
st.markdown(
    """
    This application demonstrates demand forecasting and promotion impact analysis
    in an FMCG retail environment.
    """
)

# ======================
# Data loading
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("data/extended_fmcg_demand_forecasting.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ======================
# Sidebar - filters
# ======================
st.sidebar.header("Filters")

store = st.sidebar.selectbox(
    "Select Store",
    sorted(df["Store_Location"].unique())
)

product = st.sidebar.selectbox(
    "Select Product (SKU)",
    sorted(df["Product_Category"].unique())
)

filtered_df = df[
    (df["Store_Location"] == store) &
    (df["Product_Category"] == product)
]

# ======================
# Main view
# ======================
st.subheader("📈 Sales over time")
st.line_chart(
    filtered_df.set_index("Date")["Sales"]
)

st.subheader("ℹ️ Business context")
st.info(
    """
    Sales represent actual units sold.
    Demand may be higher in case of stockouts.
    Forecasting helps reduce inventory risk.
    """
)