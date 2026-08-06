import pandas as pd


def trading_signal(df):
    """
    Nifty/Sensex CE/PE signal strategy

    Required columns:
    Open, High, Low, Close, Volume
    """

    df = df.copy()

    # 20 EMA
    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()

    # VWAP
    typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
    df["VWAP"] = (
        (typical_price * df["Volume"]).cumsum()
        / df["Volume"].cumsum()
    )

    # RSI 14
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Previous candle levels
    df["Previous_High"] = df["High"].shift(1)
    df["Previous_Low"] = df["Low"].shift(1)

    # CE condition
    ce_condition = (
        (df["Close"] > df["VWAP"]) &
        (df["Close"] > df["EMA20"]) &
        (df["Close"] > df["Previous_High"]) &
        (df["RSI"] > 55)
    )

    # PE condition
    pe_condition = (
        (df["Close"] < df["VWAP"]) &
        (df["Close"] < df["EMA20"]) &
        (df["Close"] < df["Previous_Low"]) &
        (df["RSI"] < 45)
    )

    df["Signal"] = "NO TRADE"
    df.loc[ce_condition, "Signal"] = "CE BUY"
    df.loc[pe_condition, "Signal"] = "PE BUY"

    return df


if __name__ == "__main__":
    print("Nifty/Sensex CE-PE Strategy Loaded")
