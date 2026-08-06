import pandas as pd
from strategy import trading_signal


def run_backtest(file_path):
    # Load historical data
    df = pd.read_csv(file_path)

    # Generate signals
    df = trading_signal(df)

    # Show signals
    signals = df[df["Signal"] != "NO TRADE"]

    print("\n===== BACKTEST SIGNALS =====")

    if signals.empty:
        print("No trading signals found.")
    else:
        print(
            signals[
                ["Close", "EMA20", "VWAP", "RSI", "Signal"]
            ].tail(20)
        )

    return df


if __name__ == "__main__":
    print("Nifty/Sensex Backtest Engine")
