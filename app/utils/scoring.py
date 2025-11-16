import numpy as np
import pandas as pd

def compute_features(transactions: pd.DataFrame) -> dict:
    """Expect columns: date, amount, type ('inflow'/'outflow'), category (optional)."""
    df = transactions.copy()
    if df.empty:
        return {
            "avg_inflow": 0.0,
            "income_volatility": 1.0,
            "expense_ratio": 1.0,
            "overdraft_count": 0,
            "remittance_count": 0,
            "gig_months_active": 0,
            "mobile_money_signal": False,
        }

    # Ensure required columns & dtypes
    if "category" not in df.columns:
        df["category"] = ""
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["date"]   = pd.to_datetime(df["date"],  errors="coerce")
    df["type"]   = df["type"].astype(str).str.lower()
    cat_lower    = df["category"].astype(str).str.lower()

    # Monthly aggregates
    df["ym"] = df["date"].dt.to_period("M")
    inflows  = df[df["type"] == "inflow"].groupby("ym")["amount"].sum().astype(float)
    outflows = df[df["type"] == "outflow"].groupby("ym")["amount"].sum().astype(float)

    avg_inflow        = float(inflows.mean()) if len(inflows) else 0.0
    income_volatility = float(inflows.std() / inflows.mean()) if len(inflows) and inflows.mean() != 0 else 1.0
    total_in          = float(df.loc[df["type"] == "inflow",  "amount"].sum())
    total_out         = float(df.loc[df["type"] == "outflow", "amount"].sum())
    expense_ratio     = float(total_out / total_in) if total_in > 0 else 1.0

    # Overdraft proxy: months where outflow > inflow by 10%
    overdraft_count = int((outflows.reindex(inflows.index, fill_value=0) > inflows * 1.1).sum())

    # Alternative-data signals
    remittance_mask   = cat_lower.str.contains(r"(remittance|transfer_international)", regex=True, na=False)
    gig_mask          = cat_lower.str.contains(r"(gig|upwork|fiverr|delivery|rappi|grab)", regex=True, na=False)
    mobile_money_mask = cat_lower.str.contains(r"(ecocash|mpesa|m-pesa|momo|zalopay|wallet)", regex=True, na=False)

    remittance_count  = int(remittance_mask.sum())
    gig_months_active = int(df[gig_mask].groupby("ym")["amount"].sum().shape[0])
    mobile_money_signal = bool(mobile_money_mask.any())

    return {
        "avg_inflow": round(avg_inflow, 2),
        "income_volatility": round(float(income_volatility), 2),
        "expense_ratio": round(float(expense_ratio), 2),
        "overdraft_count": int(overdraft_count),
        "remittance_count": int(remittance_count),
        "gig_months_active": int(gig_months_active),
        "mobile_money_signal": mobile_money_signal,
    }

def rule_based_score(feats: dict) -> tuple[int, str]:
    score = 50

    # avg inflow
    if feats["avg_inflow"] >= 800:
        score += 15
    elif feats["avg_inflow"] >= 400:
        score += 5

    # income volatility
    if feats["income_volatility"] > 0.6:
        score -= 10
    elif feats["income_volatility"] > 0.4:
        score -= 5

    # expense ratio
    if feats["expense_ratio"] > 0.95:
        score -= 12
    elif feats["expense_ratio"] > 0.8:
        score -= 6
    elif feats["expense_ratio"] < 0.6:
        score += 4

    # overdrafts
    score -= min(24, 8 * feats["overdraft_count"])

    # remittances
    if feats["remittance_count"] >= 3:
        score += 6

    # gig activity
    if feats["gig_months_active"] >= 3:
        score += 8

    # mobile money
    if feats["mobile_money_signal"]:
        score += 4

    score = max(0, min(100, score))
    band = "Prime" if score >= 86 else "Green" if score >= 70 else "Amber" if score >= 50 else "Red"
    return int(score), band
