import pandas as pd

# ==========================================
# NIFTY 50 TRADING SIGNAL STRATEGY
# ==========================================

FILE = "market_data.csv"

# Load CSV
try:
    df = pd.read_csv(FILE)
except FileNotFoundError:
    print(f"ERROR: {FILE} not found.")
    print("Make sure market_data.csv is in the same GitHub folder.")
    raise

# Clean column names
df.columns = df.columns.str.strip()

# Show columns for checking
print("CSV Columns:")
print(df.columns.tolist())

# Convert Date
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert OHLC columns to numbers
for col in ["Open", "High", "Low", "Close"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove invalid rows
df = df.dropna(subset=["Date", "Close"])

# Sort by date
df = df.sort_values("Date").reset_index(drop=True)

# ==========================================
# INDICATORS
# ==========================================

# 9 EMA
df["EMA9"] = df["Close"].ewm(
    span=9,
    adjust=False
).mean()

# 21 EMA
df["EMA21"] = df["Close"].ewm(
    span=21,
    adjust=False
).mean()

# ==========================================
# SIGNALS
# ==========================================

df["Signal"] = ""

for i in range(1, len(df)):

    # BUY CE
    if (
        df.loc[i, "EMA9"] > df.loc[i, "EMA21"]
        and
        df.loc[i - 1, "EMA9"] <= df.loc[i - 1, "EMA21"]
    ):
        df.loc[i, "Signal"] = "BUY CE"

    # BUY PE
    elif (
        df.loc[i, "EMA9"] < df.loc[i, "EMA21"]
        and
        df.loc[i - 1, "EMA9"] >= df.loc[i - 1, "EMA21"]
    ):
        df.loc[i, "Signal"] = "BUY PE"

# ==========================================
# DISPLAY SIGNALS
# ==========================================

signals = df[df["Signal"] != ""].copy()

print("\n================================")
print("       NIFTY 50 SIGNALS")
print("================================\n")

if signals.empty:
    print("No trading signals found.")
else:
    print(
        signals[
            [
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "EMA9",
                "EMA21",
                "Signal"
            ]
        ].to_string(index=False)
    )

# ==========================================
# SAVE SIGNALS
# ==========================================

signals.to_csv(
    "signals.csv",
    index=False
)

print("\n================================")
print("Signals saved to signals.csv")
print("================================")
