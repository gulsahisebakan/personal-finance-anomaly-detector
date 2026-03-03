import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set a random seed so we get the same data every time we run this
random.seed(42)
np.random.seed(42)

# Define spending categories like a real bank would
categories = [
    "Groceries", "Dining", "Transport", "Utilities",
    "Shopping", "Entertainment", "Healthcare", "Rent"
]

# Define typical monthly spending amounts per category
# This is what "normal" looks like for our fake person
typical_amounts = {
    "Groceries":     (40, 120),
    "Dining":        (15, 60),
    "Transport":     (10, 50),
    "Utilities":     (60, 150),
    "Shopping":      (20, 200),
    "Entertainment": (10, 80),
    "Healthcare":    (20, 100),
    "Rent":          (800, 1200),
}

# Generate 12 months of daily transactions
transactions = []
start_date = datetime(2024, 1, 1)

for day in range(365):
    current_date = start_date + timedelta(days=day)
    
    # Generate 1 to 4 transactions per day
    num_transactions = random.randint(1, 4)
    
    for _ in range(num_transactions):
        category = random.choice(categories)
        low, high = typical_amounts[category]
        amount = round(random.uniform(low, high), 2)
        
        transactions.append({
            "date":     current_date.strftime("%Y-%m-%d"),
            "category": category,
            "amount":   amount,
            "note":     f"{category} purchase"
        })

# Now inject 10 anomalies — unusually large transactions
# This simulates fraud or unexpected big expenses
anomalies = [
    {"date": "2024-02-14", "category": "Dining",        "amount": 480.00, "note": "Valentine's Day dinner"},
    {"date": "2024-03-22", "category": "Shopping",      "amount": 1200.00, "note": "Laptop purchase"},
    {"date": "2024-05-10", "category": "Entertainment", "amount": 650.00, "note": "Concert tickets"},
    {"date": "2024-06-01", "category": "Transport",     "amount": 900.00, "note": "Flight booking"},
    {"date": "2024-07-04", "category": "Dining",        "amount": 520.00, "note": "Holiday party"},
    {"date": "2024-08-15", "category": "Healthcare",    "amount": 750.00, "note": "Emergency visit"},
    {"date": "2024-09-09", "category": "Groceries",     "amount": 430.00, "note": "Bulk shopping"},
    {"date": "2024-10-31", "category": "Shopping",      "amount": 980.00, "note": "Halloween costumes"},
    {"date": "2024-11-29", "category": "Shopping",      "amount": 1500.00, "note": "Black Friday"},
    {"date": "2024-12-25", "category": "Shopping",      "amount": 2000.00, "note": "Christmas gifts"},
]

# Add the anomalies to our transactions list
transactions.extend(anomalies)

# Convert the list into a Pandas DataFrame
# A DataFrame is like an Excel spreadsheet inside Python
df = pd.DataFrame(transactions)

# Sort everything by date so it looks like a real bank statement
df = df.sort_values("date").reset_index(drop=True)

# Save it as a CSV file
df.to_csv("transactions.csv", index=False)

print(f"✅ Generated {len(df)} transactions")
print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
print(f"💰 Total spent: ${df['amount'].sum():,.2f}")
print(f"\nFirst 5 rows:")
print(df.head())