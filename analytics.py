"""
analytics.py
------------
All aggregation, KPI calculation, and business-insight logic.
Every function accepts a clean DataFrame and returns a DataFrame or dict
ready for the Streamlit frontend to display or plot.
"""

import pandas as pd
import numpy as np


# ══════════════════════════════════════════════════════════════════════════════
# KPI SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

def get_kpis(df: pd.DataFrame) -> dict:
    """Top-level KPIs for the headline metric cards."""
    return {
        "Total Revenue":        f"₹{df['Sales'].sum():,.2f}",
        "Total Transactions":   f"{len(df):,}",
        "Avg Order Value":      f"₹{df['Sales'].mean():,.2f}",
        "Avg Rating":           f"{df['Rating'].mean():.2f} / 5",
        "Total Units Sold":     f"{df['Quantity'].sum():,}",
        "Avg Units / Order":    f"{df['Quantity'].mean():.1f}",
        "Unique Products":      f"{df['Product'].nunique()}",
        "Unique Customers":     f"{df['Invoice ID'].nunique():,}",
    }


# ══════════════════════════════════════════════════════════════════════════════
# SALES BREAKDOWNS
# ══════════════════════════════════════════════════════════════════════════════

def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Total revenue, transaction count, avg order value per category."""
    grp = (
        df.groupby("Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order_Value=("Sales", "mean"),
            Total_Units=("Quantity", "sum"),
            Avg_Rating=("Rating", "mean"),
        )
        .round(2)
        .sort_values("Total_Sales", ascending=False)
        .reset_index()
    )
    grp["% Revenue Share"] = (grp["Total_Sales"] / grp["Total_Sales"].sum() * 100).round(1)
    return grp


def sales_by_branch(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue, transactions, avg order value per branch."""
    grp = (
        df.groupby(["Branch", "City"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order_Value=("Sales", "mean"),
            Avg_Rating=("Rating", "mean"),
        )
        .round(2)
        .sort_values("Total_Sales", ascending=False)
        .reset_index()
    )
    grp["% Revenue Share"] = (grp["Total_Sales"] / grp["Total_Sales"].sum() * 100).round(1)
    return grp


def sales_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly revenue trend."""
    grp = (
        df.groupby(["Year", "Month", "Month Name"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order_Value=("Sales", "mean"),
        )
        .round(2)
        .sort_values(["Year", "Month"])
        .reset_index()
    )
    grp["Period"] = grp["Month Name"] + " " + grp["Year"].astype(str)
    return grp


def sales_by_payment(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue and usage by payment method."""
    grp = (
        df.groupby("Payment")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order_Value=("Sales", "mean"),
        )
        .round(2)
        .sort_values("Total_Sales", ascending=False)
        .reset_index()
    )
    grp["% Share"] = (grp["Transactions"] / grp["Transactions"].sum() * 100).round(1)
    return grp


def sales_by_gender(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue split by gender."""
    grp = (
        df.groupby("Gender")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Rating=("Rating", "mean"),
        )
        .round(2)
        .reset_index()
    )
    return grp


def sales_by_customer_type(df: pd.DataFrame) -> pd.DataFrame:
    """Member vs Normal customer comparison."""
    grp = (
        df.groupby("Customer Type")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order_Value=("Sales", "mean"),
            Avg_Rating=("Rating", "mean"),
        )
        .round(2)
        .reset_index()
    )
    return grp


def sales_by_product(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Top-N products by revenue."""
    grp = (
        df.groupby(["Product", "Category"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Total_Units=("Quantity", "sum"),
            Avg_Unit_Price=("Unit Price", "mean"),
        )
        .round(2)
        .sort_values("Total_Sales", ascending=False)
        .head(top_n)
        .reset_index()
    )
    return grp


def sales_by_day_of_week(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue by day of week, ordered Mon → Sun."""
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    grp = (
        df.groupby("Day of Week")
        .agg(
            Total_Sales=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order_Value=("Sales", "mean"),
        )
        .round(2)
        .reindex(order)
        .dropna()
        .reset_index()
    )
    return grp


def revenue_tier_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Count of orders falling into each revenue tier."""
    grp = (
        df["Revenue Tier"]
        .value_counts()
        .reset_index()
        .rename(columns={"Revenue Tier": "Tier", "count": "Count"})
    )
    return grp


# ══════════════════════════════════════════════════════════════════════════════
# CROSS-DIMENSIONAL HEATMAP
# ══════════════════════════════════════════════════════════════════════════════

def category_branch_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot: Category × Branch total sales — for heatmap."""
    pivot = df.pivot_table(
        values="Sales", index="Category", columns="Branch",
        aggfunc="sum", fill_value=0
    ).round(2)
    return pivot


def category_gender_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot: Category × Gender total sales."""
    pivot = df.pivot_table(
        values="Sales", index="Category", columns="Gender",
        aggfunc="sum", fill_value=0
    ).round(2)
    return pivot


# ══════════════════════════════════════════════════════════════════════════════
# RATING ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def rating_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Average rating per category."""
    return (
        df.groupby("Category")["Rating"]
        .agg(Avg_Rating="mean", Count="count")
        .round(2)
        .sort_values("Avg_Rating", ascending=False)
        .reset_index()
    )


def rating_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Histogram bins for customer ratings."""
    bins = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5.01]
    labels = ["1–1.5", "1.5–2", "2–2.5", "2.5–3", "3–3.5", "3.5–4", "4–4.5", "4.5–5"]
    df2 = df.copy()
    df2["Rating Bin"] = pd.cut(df2["Rating"], bins=bins, labels=labels, right=False)
    return df2["Rating Bin"].value_counts().sort_index().reset_index().rename(
        columns={"Rating Bin": "Range", "count": "Count"}
    )


# ══════════════════════════════════════════════════════════════════════════════
# BUSINESS INSIGHTS (text)
# ══════════════════════════════════════════════════════════════════════════════

def generate_insights(df: pd.DataFrame) -> list[dict]:
    """
    Derive data-driven textual recommendations.
    Returns a list of dicts: {icon, title, detail}
    """
    insights = []

    # 1. Best-performing category
    cat = sales_by_category(df).iloc[0]
    insights.append({
        "icon": "🏆",
        "title": f"Top Category: {cat['Category']}",
        "detail": (
            f"{cat['Category']} leads with ₹{cat['Total_Sales']:,.2f} in total revenue "
            f"({cat['% Revenue Share']}% of all sales) across {cat['Transactions']} transactions. "
            "Consider expanding product range or offering loyalty discounts in this category."
        ),
    })

    # 2. Underperforming category
    cat_low = sales_by_category(df).iloc[-1]
    insights.append({
        "icon": "⚠️",
        "title": f"Underperforming Category: {cat_low['Category']}",
        "detail": (
            f"{cat_low['Category']} contributes only {cat_low['% Revenue Share']}% of revenue. "
            "Review pricing, shelf placement, or run targeted promotions to boost sales."
        ),
    })

    # 3. Best branch
    branch = sales_by_branch(df).iloc[0]
    insights.append({
        "icon": "📍",
        "title": f"Highest Revenue Branch: {branch['Branch']} — {branch['City']}",
        "detail": (
            f"Branch {branch['Branch']} ({branch['City']}) generated ₹{branch['Total_Sales']:,.2f} "
            f"with an average order of ₹{branch['Avg_Order_Value']:,.2f}. "
            "Replicate its stock mix and staff practices at lower-performing branches."
        ),
    })

    # 4. Preferred payment method
    pay = sales_by_payment(df).iloc[0]
    insights.append({
        "icon": "💳",
        "title": f"Dominant Payment: {pay['Payment']}",
        "detail": (
            f"{pay['Payment']} accounts for {pay['% Share']}% of all transactions. "
            "Ensure seamless checkout experience and consider cashback offers for this method."
        ),
    })

    # 5. Member vs Normal
    ct = sales_by_customer_type(df)
    member = ct[ct["Customer Type"] == "Member"]
    if not member.empty:
        m = member.iloc[0]
        insights.append({
            "icon": "👤",
            "title": "Member Customers Are More Valuable",
            "detail": (
                f"Members average ₹{m['Avg_Order_Value']:,.2f} per order "
                f"vs. Normal customers. Invest in membership acquisition campaigns and "
                "reward programmes to convert regular shoppers."
            ),
        })

    # 6. Peak day
    dow = sales_by_day_of_week(df)
    if not dow.empty:
        peak_day = dow.sort_values("Total_Sales", ascending=False).iloc[0]
        insights.append({
            "icon": "📅",
            "title": f"Busiest Day: {peak_day['Day of Week']}",
            "detail": (
                f"{peak_day['Day of Week']} drives ₹{peak_day['Total_Sales']:,.2f} in revenue. "
                "Schedule additional staff, ensure full inventory, and run flash deals on this day."
            ),
        })

    # 7. Rating alert
    low_rated = rating_by_category(df).sort_values("Avg_Rating").iloc[0]
    insights.append({
        "icon": "⭐",
        "title": f"Lowest-Rated Category: {low_rated['Category']}",
        "detail": (
            f"{low_rated['Category']} has an average rating of {low_rated['Avg_Rating']:.2f}. "
            "Investigate product quality, freshness, or pricing. Customer surveys may help identify root cause."
        ),
    })

    # 8. High-value orders
    premium = (df["Revenue Tier"] == "Premium (>₹1000)").sum()
    pct = premium / len(df) * 100
    insights.append({
        "icon": "💰",
        "title": "Premium Order Opportunity",
        "detail": (
            f"Only {premium} orders ({pct:.1f}%) exceed ₹1,000. "
            "Bundle deals and up-sell strategies (e.g. buy 5 get 1 free) could push more orders "
            "into the premium tier and significantly raise average basket size."
        ),
    })

    return insights
