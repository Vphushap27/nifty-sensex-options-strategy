import pandas as pd

from strategy import trading_signal
from risk_management import (
    calculate_risk,
    calculate_position_size,
    calculate_targets
)


def run_strategy(file_path, entry_price, stop_loss):

    # Load market data
    df = pd.read_csv(file_path)

    # Generate trading signal
    df = trading_signal(df)

    latest = df.iloc[-1]

    signal = latest["Signal"]

    print("\n===== TRADING SETUP =====")
    print("Signal:", signal)
    print("Price:", latest["Close"])
    print("RSI:", round(latest["RSI"], 2))
    print("VWAP:", round(latest["VWAP"], 2))
    print("EMA20:", round(latest["EMA20"], 2))

    # Risk calculation
    risk = calculate_risk()

    quantity = calculate_position_size(
        entry_price,
        stop_loss
    )

    targets = calculate_targets(
        entry_price,
        stop_loss
    )

    print("\n===== RISK MANAGEMENT =====")
    print("Maximum Risk: ₹", risk)
    print("Quantity:", quantity)

    print("\n===== TARGETS =====")
    print("Target 1:", round(targets[0], 2))
    print("Target 2:", round(targets[1], 2))
    print("Target 3:", round(targets[2], 2))


if __name__ == "__main__":

    # Example
    run_strategy(
        "market_data.csv",
        entry_price=100,
        stop_loss=90
    )
