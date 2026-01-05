import pandas as pd

def moving_average_forecast(df, window=7):
    """
    Baseline demand forecast using moving average.
    Forecast is shifted by 1 to avoid data leakage.
    """
    df = df.sort_values("Date").copy()

    df["Baseline_Forecast"] = (
        df["Sales_Volume"]
        .rolling(window=window)
        .mean()
        .shift(1)
    )

    return df