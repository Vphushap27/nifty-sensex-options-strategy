import pandas as pd

# CSV file
FILE = "NIFTY 50-06-08-2025-to-06-08-2026.csv"

# Load data
df = pd.read_csv(FILE)

# Remove spaces from column names
df.columns = df.columns.str.strip()

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# Sort oldest to newest
df = df.sort_values("Date").reset_index(drop=True)

# Moving averages
df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
df["EMA21"] = df["Close"].ewm(span=21, adjust=False).mean()

# Signals
df["Signal"] = ""

for i in range(1, len(df)):

    # Bullish = CE
    if df.loc[i, "EMA9"] > df.loc[i, "EMA21"] and \
       df.loc[i-1, "EMA9"] <= df.loc[i-1, "EMA21"]:

        df.loc[i, "Signal"] = "BUY CE"

    # Bearish = PE
    elif df.loc[i, "EMA9"] < df.loc[i, "EMA21"] and \
         df.loc[i-1, "EMA9"] >= df.loc[i-1, "EMA21"]:

        df.loc[i, "Signal"] = "BUY PE"

# Show signals
signals = df[df["Signal"] != ""]

print("\n===== NIFTY SIGNALS =====\n")
print(
    signals[
        ["Date", "Close", "EMA9", "EMA21", "Signal"]
    ].to_string(index=False)
)

# Save results
signals.to_csv("signals.csv", index=False)

print("\nSignals saved to signals.csv")
