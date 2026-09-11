"""
data_loader.py
--------------
Handles loading, validation, cleaning, and feature engineering
for the supermarket sales CSV dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path


# ── Column definitions ──────────────────────────────────────────────────────
REQUIRED_COLUMNS = [
    "Invoice ID", "Date", "Branch", "City", "Customer Type",
    "Gender", "Product", "Category", "Quantity", "Unit Price",
    "Payment", "Rating", "Sales",
]

NUMERIC_COLUMNS = ["Quantity", "Unit Price", "Sales", "Rating"]
CATEGORICAL_COLUMNS = ["Branch", "City", "Customer Type", "Gender",
                       "Product", "Category", "Payment"]


def load_data(filepath: str | Path) -> pd.DataFrame:
    """Load CSV and return a cleaned, enriched DataFrame."""
    df = _read_csv(filepath)
    df = _validate_columns(df)
    df = _clean_data(df)
    df = _engineer_features(df)
    return df


# ── Private helpers ──────────────────────────────────────────────────────────

def _read_csv(filepath: str | Path) -> pd.DataFrame:
    """Read the CSV file into a DataFrame."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path.resolve()}")
    return pd.read_csv(path)


def _validate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Check that all expected columns are present."""
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")
    return df[REQUIRED_COLUMNS]          # keep only known columns, in order


def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    1. Parse dates.
    2. Coerce numeric columns to float; replace non-parseable with NaN.
    3. Drop fully-duplicate rows.
    4. Flag & drop rows where critical numeric fields are null/non-positive.
    5. Strip whitespace from string columns.
    """
    df = df.copy()

    # --- Date parsing ---
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # --- Numeric coercion ---
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- Strip whitespace ---
    for col in CATEGORICAL_COLUMNS:
        df[col] = df[col].astype(str).str.strip()

    # --- Remove full duplicates ---
    df = df.drop_duplicates()

    # --- Drop rows with critical nulls ---
    critical = ["Date", "Quantity", "Unit Price", "Sales", "Category", "Branch"]
    before = len(df)
    df = df.dropna(subset=critical)
    dropped = before - len(df)
    if dropped:
        print(f"[data_loader] Dropped {dropped} rows with missing critical values.")

    # --- Ensure positivity of sales-related columns ---
    df = df[(df["Quantity"] > 0) & (df["Unit Price"] > 0)]

    return df.reset_index(drop=True)


def _engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns useful for analysis."""
    df = df.copy()

    # Recalculate Sales to verify / correct any rounding issues
    df["Calculated Sales"] = (df["Quantity"] * df["Unit Price"]).round(2)

    # Flag rows where provided Sales deviates from calculated by > 1 %
    df["Sales Mismatch"] = ~np.isclose(df["Sales"], df["Calculated Sales"],
                                       rtol=0.01, atol=0.01)

    # Use recalculated sales as the authoritative figure
    df["Sales"] = df["Calculated Sales"]
    df.drop(columns=["Calculated Sales"], inplace=True)

    # Date parts
    df["Year"]  = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month Name"] = df["Date"].dt.strftime("%b")
    df["Day of Week"] = df["Date"].dt.strftime("%A")
    df["Week"] = df["Date"].dt.isocalendar().week.astype(int)

    # Revenue bucket
    df["Revenue Tier"] = pd.cut(
        df["Sales"],
        bins=[0, 200, 500, 1000, np.inf],
        labels=["Low (<₹200)", "Mid (₹200–500)", "High (₹500–1000)", "Premium (>₹1000)"],
    )

    return df


def get_data_quality_report(df_raw: pd.DataFrame, df_clean: pd.DataFrame) -> dict:
    """Return a structured quality-check summary for display in the UI."""
    total_raw   = len(df_raw)
    total_clean = len(df_clean)

    report = {
        "Total Records (Raw)":     total_raw,
        "Total Records (Clean)":   total_clean,
        "Rows Removed":            total_raw - total_clean,
        "Missing Values (Raw)":    int(df_raw.isnull().sum().sum()),
        "Duplicate Rows (Raw)":    int(df_raw.duplicated().sum()),
        "Sales Mismatches Fixed":  int(df_clean["Sales Mismatch"].sum()),
        "Date Range":              f"{df_clean['Date'].min().date()}  →  {df_clean['Date'].max().date()}",
        "Branches":                ", ".join(sorted(df_clean["Branch"].unique())),
        "Cities":                  ", ".join(sorted(df_clean["City"].unique())),
        "Categories":              ", ".join(sorted(df_clean["Category"].unique())),
        "Payment Methods":         ", ".join(sorted(df_clean["Payment"].unique())),
    }
    return report
