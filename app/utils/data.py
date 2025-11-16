import pandas as pd
from datetime import datetime
import numpy as np

def _month_anchor():
    # First day of the current month as a pandas Timestamp
    return pd.Timestamp.today().normalize().replace(day=1)

def sample_transactions_bank():
    rows = []
    today = _month_anchor()
    for m in range(6):
        month_start = today - pd.DateOffset(months=m)
        # inflow: salary or freelance
        rows.append({"date": month_start + pd.Timedelta(days=1),  "amount": 900.00, "type": "inflow",  "category": "salary"})
        # outflows
        rows.append({"date": month_start + pd.Timedelta(days=3),  "amount": 450.00, "type": "outflow", "category": "rent"})
        rows.append({"date": month_start + pd.Timedelta(days=10), "amount": 120.00, "type": "outflow", "category": "groceries"})
        rows.append({"date": month_start + pd.Timedelta(days=18), "amount": 60.00,  "type": "outflow", "category": "transport"})
    return pd.DataFrame(rows)

def sample_transactions_mobile_money():
    rows = []
    today = _month_anchor()
    for m in range(6):
        month_start = today - pd.DateOffset(months=m)
        rows.append({"date": month_start + pd.Timedelta(days=2),  "amount": 300.00, "type": "inflow",  "category": "ecocash_gig"})
        rows.append({"date": month_start + pd.Timedelta(days=4),  "amount": 200.00, "type": "outflow", "category": "wallet_spend"})
        rows.append({"date": month_start + pd.Timedelta(days=14), "amount": 50.00,  "type": "inflow",  "category": "remittance_in"})
    return pd.DataFrame(rows)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    expected = ["date", "amount", "type", "category"]
    for col in expected:
        if col not in df.columns:
            df[col] = None
    df = df[expected].copy()
    # ensure types are consistent
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["type"] = df["type"].astype(str)
    df["category"] = df["category"].astype(str)
    return df
