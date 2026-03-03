import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# ── 1. LOAD DATA ──────────────────────────────────────────────────────────────
# Read the CSV we just generated into a DataFrame
df = pd.read_csv("transactions.csv")

# Convert the date column from plain text into real Python date objects
# This lets us do date math later (group by month, sort, etc.)
df["date"] = pd.to_datetime(df["date"])

print(f"✅ Loaded {len(df)} transactions\n")

# ── 2. FEATURE ENGINEERING ───────────────────────────────────────────────────
# "Features" are the numbers we feed into our ML model
# We need to turn our data into a format the algorithm understands

# For each transaction, calculate how much it DEVIATES from the average
# spending in that same category
# Example: A $500 Dining charge is very suspicious. A $500 Rent charge is normal.

# Calculate mean and std (standard deviation) per category
category_stats = df.groupby("category")["amount"].agg(["mean", "std"]).reset_index()
category_stats.columns = ["category", "cat_mean", "cat_std"]

# Merge these stats back into our main dataframe
df = df.merge(category_stats, on="category")

# How many "standard deviations" away from normal is this transaction?
# This is called a Z-score — a classic statistics concept
df["z_score"] = (df["amount"] - df["cat_mean"]) / df["cat_std"]

# Also add the raw amount as a feature
df["amount_feature"] = df["amount"]

print("📊 Category spending averages:")
print(category_stats.to_string(index=False))
print()

# ── 3. ISOLATION FOREST ──────────────────────────────────────────────────────
# Isolation Forest is an ML algorithm designed specifically for anomaly detection
# It works by asking: "How easy is it to isolate this data point from all others?"
# Normal points are hard to isolate (they blend in with others)
# Anomalies are easy to isolate (they stand out)

# contamination=0.02 means we expect ~2% of transactions to be anomalies
model = IsolationForest(contamination=0.02, random_state=42)

# Train the model on our two features
features = df[["amount_feature", "z_score"]]
df["anomaly_score"] = model.fit_predict(features)

# The model returns -1 for anomalies and 1 for normal transactions
# Let's convert that to something more readable
df["is_anomaly"] = df["anomaly_score"].apply(lambda x: "🚨 ANOMALY" if x == -1 else "✅ Normal")

# ── 4. RESULTS ───────────────────────────────────────────────────────────────
anomalies = df[df["anomaly_score"] == -1].sort_values("amount", ascending=False)

print(f"🔍 Found {len(anomalies)} anomalies out of {len(df)} transactions\n")
print("Top anomalies detected:")
print(anomalies[["date", "category", "amount", "note", "z_score"]].to_string(index=False))

# Save the full results to a new CSV
df.to_csv("transactions_analyzed.csv", index=False)
print("\n💾 Full analysis saved to transactions_analyzed.csv")