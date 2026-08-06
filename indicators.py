import pandas as pd


def calculate_indicators(df):
    df = df.copy()

    # 20 EMA
    df["EMA20"] = df["Close"].ewm(
        span=20,
        adjust=False
    ).mean()

    # RSI 14
    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = 100 - (100 / (1 + rs))

    # VWAP
    typical_price = (
        df["High"] + df["Low"] + df["Close"]
    ) / 3

    df["VWAP"] = (
        (typical_price * df["Volume"]).cumsum()
        / df["Volume"].cumsum()
    )

    return df
