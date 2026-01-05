import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.modeling import moving_average_forecast
from src.metrics import mape

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
    sorted(df[df["Store_Location"] == store]["Product_Category"].unique())
)

filtered_df = df[
    (df["Store_Location"] == store) &
    (df["Product_Category"] == product)
].sort_values("Date")

# ======================
# Main view
# ======================
st.subheader("📈 Sales over time")
st.line_chart(
    filtered_df.set_index("Date")["Sales_Volume"]
)

st.subheader("ℹ️ Business context")
st.info(
    """
    Sales represent actual units sold.
    Demand may be higher in case of stockouts.
    Forecasting helps reduce inventory risk.
    """
)


st.subheader("📈 Baseline Forecast vs Actual Sales")
st.info(
    """
    The baseline forecast represents expected demand under normal conditions
    without promotional effects. It is used as a reference to evaluate
    more complex machine learning models.
    """
)
baseline_df = moving_average_forecast(filtered_df)
st.line_chart(baseline_df.set_index("Date")["Sales_Volume"])

fig, ax = plt.subplots()

ax.plot(
    filtered_df["Date"],
    filtered_df["Sales"],
    label="Actual Sales"
)

ax.plot(
    filtered_df["Date"],
    filtered_df["Baseline"],
    label="Baseline Forecast"
)

ax.set_xlabel("Date")
ax.set_ylabel("Units Sold")
ax.legend()

st.pyplot(fig)

valid = filtered_df.dropna(subset=["Baseline"])
baseline_mape = mape(valid["Sales_Volume"], valid["Baseline_Forecast"])

st.metric(
    label="Baseline MAPE (%)",
    value=f"{mape_value:.2f}"
)
