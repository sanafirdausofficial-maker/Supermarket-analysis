"""
app.py
------
Streamlit frontend for Supermarket Sales Analysis.
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import sys, os

# ── Allow imports from the project root ─────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from data_loader import load_data, get_data_quality_report
import analytics as an

# ════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Main background */
    .main { background-color: #f8f9fb; }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e0e4ea;
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    div[data-testid="metric-container"] label {
        font-size: 0.78rem;
        color: #6b7280;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 1.55rem;
        font-weight: 700;
        color: #1f2937;
    }

    /* Section headers */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1e293b;
        border-left: 4px solid #3b82f6;
        padding-left: 10px;
        margin: 24px 0 12px 0;
    }

    /* Insight card */
    .insight-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .insight-title {
        font-size: 0.97rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 4px;
    }
    .insight-detail {
        font-size: 0.88rem;
        color: #475569;
        line-height: 1.6;
    }

    /* Quality badge */
    .badge-green { color:#15803d; background:#dcfce7; border-radius:6px; padding:2px 8px; font-size:0.8rem; font-weight:600; }
    .badge-red   { color:#b91c1c; background:#fee2e2; border-radius:6px; padding:2px 8px; font-size:0.8rem; font-weight:600; }

    /* Sidebar */
    section[data-testid="stSidebar"] { background: #1e293b; }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label { color: #94a3b8 !important; font-size:0.8rem; }

    /* Divider */
    hr { border-color: #e2e8f0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ════════════════════════════════════════════════════════════════════════════

DATA_PATHS = [
    Path(__file__).parent.parent / "SUPER MARKET DATA - supermarket_sales_500_rows.csv",
    Path(__file__).parent / "supermarket_sales_500_rows.csv",
    Path("SUPER MARKET DATA - supermarket_sales_500_rows.csv"),
]


@st.cache_data(show_spinner=False)
def load_dataset(path_str: str):
    import pandas as pd
    from data_loader import load_data, get_data_quality_report
    df_raw = pd.read_csv(path_str)
    df = load_data(path_str)
    quality = get_data_quality_report(df_raw, df)
    return df, quality


def find_data_file(uploaded=None) -> str | None:
    if uploaded:
        tmp = Path(__file__).parent / "_uploaded_data.csv"
        tmp.write_bytes(uploaded.getbuffer())
        return str(tmp)
    for p in DATA_PATHS:
        if p.exists():
            return str(p)
    return None


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🛒 Supermarket\nSales Analytics")
    st.markdown("---")

    uploaded = st.file_uploader(
        "📂 Upload CSV (optional)", type=["csv"],
        help="Leave blank to use the default dataset",
    )

    data_path = find_data_file(uploaded)
    if data_path is None:
        st.error("Dataset not found. Please upload a CSV file.")
        st.stop()

    with st.spinner("Loading data…"):
        df, quality = load_dataset(data_path)

    st.success(f"✅ {quality['Total Records (Clean)']} records loaded")
    st.markdown("---")

    # ── Filters ──────────────────────────────────────────────────────────────
    st.markdown("### 🔍 Filters")

    all_branches  = sorted(df["Branch"].unique())
    all_cities    = sorted(df["City"].unique())
    all_cats      = sorted(df["Category"].unique())
    all_payments  = sorted(df["Payment"].unique())

    sel_branches  = st.multiselect("Branch",       all_branches,  default=all_branches)
    sel_cities    = st.multiselect("City",          all_cities,    default=all_cities)
    sel_cats      = st.multiselect("Category",      all_cats,      default=all_cats)
    sel_payments  = st.multiselect("Payment",       all_payments,  default=all_payments)

    date_min = df["Date"].min().date()
    date_max = df["Date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
    )

    st.markdown("---")
    st.markdown(
        "<small style='color:#94a3b8'>Built with Streamlit · Plotly · Pandas</small>",
        unsafe_allow_html=True,
    )


# ── Apply filters ─────────────────────────────────────────────────────────
mask = (
    df["Branch"].isin(sel_branches) &
    df["City"].isin(sel_cities) &
    df["Category"].isin(sel_cats) &
    df["Payment"].isin(sel_payments)
)
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    d0, d1 = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    mask &= (df["Date"] >= d0) & (df["Date"] <= d1)

dff = df[mask].copy()

if dff.empty:
    st.warning("No data matches the current filters. Please broaden your selection.")
    st.stop()


# ════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════

PALETTE = px.colors.qualitative.Bold
BLUE    = "#3b82f6"
GREEN   = "#10b981"
ORANGE  = "#f59e0b"
RED     = "#ef4444"
PURPLE  = "#8b5cf6"

def chart_layout(fig, height=380):
    fig.update_layout(
        height=height,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Segoe UI, system-ui, sans-serif", size=12, color="#374151"),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11),
        xaxis=dict(showgrid=False, tickfont_size=11),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0", tickfont_size=11),
    )
    return fig


def fmt_inr(val):
    return f"₹{val:,.2f}"


# ════════════════════════════════════════════════════════════════════════════
# PAGE TITLE
# ════════════════════════════════════════════════════════════════════════════

st.markdown(
    """
    <div style='background:linear-gradient(135deg,#1e293b 0%,#334155 100%);
                padding:28px 32px;border-radius:14px;margin-bottom:24px'>
      <h1 style='color:#f1f5f9;margin:0;font-size:1.9rem'>🛒 Supermarket Sales Analytics</h1>
      <p style='color:#94a3b8;margin:6px 0 0 0;font-size:0.95rem'>
        End-to-end data analysis · KPIs · Charts · Business Insights
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ════════════════════════════════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════════════════════════════════

tabs = st.tabs([
    "📊 Overview",
    "🔍 Data Quality",
    "📦 Category Analysis",
    "🏪 Branch & City",
    "📅 Time Trends",
    "💳 Payment & Customer",
    "⭐ Ratings",
    "💡 Business Insights",
])

TAB_OVERVIEW, TAB_QUALITY, TAB_CATEGORY, TAB_BRANCH, TAB_TIME, TAB_PAYMENT, TAB_RATING, TAB_INSIGHTS = tabs


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════

with TAB_OVERVIEW:
    # ── KPI Cards ────────────────────────────────────────────────────────────
    kpis = an.get_kpis(dff)
    cols = st.columns(4)
    for i, (k, v) in enumerate(kpis.items()):
        cols[i % 4].metric(k, v)

    st.markdown("---")

    # ── Revenue by Category (bar) + Revenue Share (pie) ────────────────────
    st.markdown('<div class="section-header">Revenue by Category</div>', unsafe_allow_html=True)
    cat_df = an.sales_by_category(dff)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = px.bar(
            cat_df, x="Category", y="Total_Sales",
            color="Category", color_discrete_sequence=PALETTE,
            text=cat_df["Total_Sales"].apply(lambda v: f"₹{v:,.0f}"),
            title="Total Revenue by Category",
        )
        fig.update_traces(textposition="outside", textfont_size=11)
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Revenue (₹)")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with col2:
        fig2 = px.pie(
            cat_df, names="Category", values="Total_Sales",
            color_discrete_sequence=PALETTE,
            title="Revenue Share by Category",
            hole=0.4,
        )
        fig2.update_traces(textposition="inside", textinfo="percent+label", textfont_size=11)
        st.plotly_chart(chart_layout(fig2), use_container_width=True)

    # ── Monthly Trend ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)
    mon_df = an.sales_by_month(dff)
    fig3 = px.line(
        mon_df, x="Period", y="Total_Sales",
        markers=True, title="Monthly Revenue",
        color_discrete_sequence=[BLUE],
    )
    fig3.update_traces(line_width=2.5, marker_size=7)
    fig3.update_layout(xaxis_title="", yaxis_title="Revenue (₹)")
    st.plotly_chart(chart_layout(fig3, 340), use_container_width=True)

    # ── Raw data preview ─────────────────────────────────────────────────
    with st.expander("📄 View Raw Data (first 100 rows)"):
        show_cols = [c for c in dff.columns if c != "Sales Mismatch"]
        st.dataframe(
            dff[show_cols].head(100).style.format(
                {"Sales": "₹{:,.2f}", "Unit Price": "₹{:,.2f}", "Rating": "{:.1f}"}
            ),
            use_container_width=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — DATA QUALITY
# ════════════════════════════════════════════════════════════════════════════

with TAB_QUALITY:
    st.markdown('<div class="section-header">Data Quality Report</div>', unsafe_allow_html=True)

    q = quality          # uses full dataset (unfiltered)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Raw Records",   q["Total Records (Raw)"])
    c2.metric("Clean Records", q["Total Records (Clean)"])
    c3.metric("Rows Removed",  q["Rows Removed"])
    c4.metric("Missing Values (Raw)", q["Missing Values (Raw)"])

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 📋 Quality Checks")
        rows = [
            ("Duplicate Rows (Raw)",   q["Duplicate Rows (Raw)"],   0),
            ("Sales Mismatches Fixed", q["Sales Mismatches Fixed"],  0),
            ("Missing Values (Raw)",   q["Missing Values (Raw)"],    0),
            ("Rows Removed",           q["Rows Removed"],            0),
        ]
        for label, val, threshold in rows:
            badge = f'<span class="badge-green">✓ {val}</span>' if val <= threshold else f'<span class="badge-red">⚠ {val}</span>'
            st.markdown(f"**{label}:** {badge}", unsafe_allow_html=True)

        st.markdown("#### 📅 Dataset Scope")
        st.info(f"**Date Range:** {q['Date Range']}")
        st.info(f"**Branches:** {q['Branches']}")
        st.info(f"**Cities:** {q['Cities']}")

    with col_b:
        st.markdown("#### 🗂 Column Summary")
        dtypes_df = pd.DataFrame({
            "Column":    df.columns.tolist(),
            "Data Type": df.dtypes.astype(str).tolist(),
            "Non-Null":  df.notnull().sum().tolist(),
            "Null Count": df.isnull().sum().tolist(),
            "Unique Values": [df[c].nunique() for c in df.columns],
        })
        st.dataframe(dtypes_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 📐 Descriptive Statistics (Numeric Columns)")
    desc = dff[["Quantity", "Unit Price", "Sales", "Rating"]].describe().round(2)
    desc.index.name = "Statistic"
    desc = desc.rename(columns={
        "Sales": "Sales (₹)", "Unit Price": "Unit Price (₹)"
    })
    st.dataframe(desc.style.format("{:.2f}"), use_container_width=True)

    # Sales Mismatch flag
    mismatches = dff[dff["Sales Mismatch"] == True][["Invoice ID", "Date", "Product",
                                                       "Quantity", "Unit Price", "Sales"]]
    if mismatches.empty:
        st.success("✅ No Sales vs (Quantity × Unit Price) mismatches found after cleaning.")
    else:
        st.warning(f"⚠️ {len(mismatches)} mismatch rows — shown below (Sales was recalculated).")
        st.dataframe(mismatches.head(20), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — CATEGORY ANALYSIS
# ════════════════════════════════════════════════════════════════════════════

with TAB_CATEGORY:
    cat_df = an.sales_by_category(dff)
    prod_df = an.sales_by_product(dff, top_n=10)

    st.markdown('<div class="section-header">Category Performance</div>', unsafe_allow_html=True)

    # ── Summary table ───────────────────────────────────────────────────────
    display_cat = cat_df.rename(columns={
        "Total_Sales": "Revenue (₹)",
        "Transactions": "Transactions",
        "Avg_Order_Value": "Avg Order (₹)",
        "Total_Units": "Units Sold",
        "Avg_Rating": "Avg Rating",
        "% Revenue Share": "Revenue Share (%)",
    })
    st.dataframe(
        display_cat.style.format({
            "Revenue (₹)": "₹{:,.2f}",
            "Avg Order (₹)": "₹{:,.2f}",
            "Avg Rating": "{:.2f}",
        }).background_gradient(subset=["Revenue (₹)"], cmap="Blues"),
        use_container_width=True,
        hide_index=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            cat_df.sort_values("Avg_Order_Value", ascending=True),
            x="Avg_Order_Value", y="Category", orientation="h",
            color="Avg_Order_Value", color_continuous_scale="Blues",
            title="Average Order Value by Category",
            text=cat_df.sort_values("Avg_Order_Value")["Avg_Order_Value"]
                       .apply(lambda v: f"₹{v:,.0f}"),
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, xaxis_title="Avg Order (₹)", yaxis_title="",
                          coloraxis_showscale=False)
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with col2:
        fig2 = px.bar(
            cat_df.sort_values("Total_Units", ascending=True),
            x="Total_Units", y="Category", orientation="h",
            color="Total_Units", color_continuous_scale="Greens",
            title="Total Units Sold by Category",
            text="Total_Units",
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(showlegend=False, xaxis_title="Units", yaxis_title="",
                           coloraxis_showscale=False)
        st.plotly_chart(chart_layout(fig2), use_container_width=True)

    # ── Heatmap: Category × Branch ──────────────────────────────────────────
    st.markdown('<div class="section-header">Revenue Heatmap: Category × Branch</div>',
                unsafe_allow_html=True)
    heat = an.category_branch_heatmap(dff)
    fig_heat = go.Figure(go.Heatmap(
        z=heat.values.tolist(),
        x=heat.columns.tolist(),
        y=heat.index.tolist(),
        colorscale="Blues",
        text=[[f"₹{v:,.0f}" for v in row] for row in heat.values],
        texttemplate="%{text}",
        textfont_size=11,
        showscale=True,
    ))
    fig_heat.update_layout(
        title="Total Sales: Category × Branch",
        height=380,
        plot_bgcolor="#fff", paper_bgcolor="#fff",
        font=dict(family="Segoe UI, sans-serif", size=12),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── Top 10 products ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Top 10 Products by Revenue</div>',
                unsafe_allow_html=True)
    fig_prod = px.bar(
        prod_df.sort_values("Total_Sales"),
        x="Total_Sales", y="Product", orientation="h",
        color="Category", color_discrete_sequence=PALETTE,
        title="Top 10 Products",
        text=prod_df.sort_values("Total_Sales")["Total_Sales"].apply(lambda v: f"₹{v:,.0f}"),
    )
    fig_prod.update_traces(textposition="outside")
    fig_prod.update_layout(xaxis_title="Revenue (₹)", yaxis_title="")
    st.plotly_chart(chart_layout(fig_prod, 420), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — BRANCH & CITY
# ════════════════════════════════════════════════════════════════════════════

with TAB_BRANCH:
    branch_df = an.sales_by_branch(dff)

    st.markdown('<div class="section-header">Branch Performance</div>', unsafe_allow_html=True)

    display_br = branch_df.rename(columns={
        "Total_Sales": "Revenue (₹)",
        "Transactions": "Transactions",
        "Avg_Order_Value": "Avg Order (₹)",
        "Avg_Rating": "Avg Rating",
        "% Revenue Share": "Revenue Share (%)",
    })
    st.dataframe(
        display_br.style.format({
            "Revenue (₹)": "₹{:,.2f}",
            "Avg Order (₹)": "₹{:,.2f}",
            "Avg Rating": "{:.2f}",
        }).background_gradient(subset=["Revenue (₹)"], cmap="Purples"),
        use_container_width=True,
        hide_index=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            branch_df, x="Branch", y="Total_Sales",
            color="City", color_discrete_sequence=PALETTE,
            barmode="group",
            title="Total Revenue by Branch",
            text=branch_df["Total_Sales"].apply(lambda v: f"₹{v:,.0f}"),
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(xaxis_title="Branch", yaxis_title="Revenue (₹)")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with col2:
        fig2 = px.funnel(
            branch_df.sort_values("Total_Sales", ascending=False),
            x="Total_Sales", y="City",
            title="Revenue Funnel by City",
            color_discrete_sequence=PALETTE,
        )
        fig2.update_layout(yaxis_title="", xaxis_title="Revenue (₹)")
        st.plotly_chart(chart_layout(fig2), use_container_width=True)

    # ── Category mix per branch ──────────────────────────────────────────────
    st.markdown('<div class="section-header">Category Mix per Branch</div>',
                unsafe_allow_html=True)
    branch_cat = (
        dff.groupby(["Branch", "Category"])["Sales"]
        .sum().reset_index()
    )
    fig_bc = px.bar(
        branch_cat, x="Branch", y="Sales", color="Category",
        barmode="stack",
        color_discrete_sequence=PALETTE,
        title="Sales Breakdown by Branch and Category",
        text_auto=False,
    )
    fig_bc.update_layout(xaxis_title="Branch", yaxis_title="Revenue (₹)")
    st.plotly_chart(chart_layout(fig_bc, 400), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — TIME TRENDS
# ════════════════════════════════════════════════════════════════════════════

with TAB_TIME:
    mon_df = an.sales_by_month(dff)
    dow_df = an.sales_by_day_of_week(dff)

    st.markdown('<div class="section-header">Monthly Revenue Trend</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=mon_df["Period"], y=mon_df["Total_Sales"],
                   name="Revenue", marker_color=BLUE, opacity=0.85),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=mon_df["Period"], y=mon_df["Transactions"],
                       name="Transactions", mode="lines+markers",
                       line=dict(color=ORANGE, width=2.5), marker_size=6),
            secondary_y=True,
        )
        fig.update_yaxes(title_text="Revenue (₹)", secondary_y=False, showgrid=True, gridcolor="#f0f0f0")
        fig.update_yaxes(title_text="Transactions", secondary_y=True, showgrid=False)
        fig.update_layout(
            title="Monthly Revenue & Transactions",
            height=360, plot_bgcolor="#fff", paper_bgcolor="#fff",
            font=dict(family="Segoe UI, sans-serif", size=12),
            margin=dict(l=10, r=10, t=45, b=10),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.dataframe(
            mon_df[["Period", "Total_Sales", "Transactions", "Avg_Order_Value"]]
            .rename(columns={
                "Total_Sales": "Revenue (₹)",
                "Avg_Order_Value": "Avg Order (₹)"
            })
            .style.format({
                "Revenue (₹)": "₹{:,.2f}",
                "Avg Order (₹)": "₹{:,.2f}",
            }),
            use_container_width=True,
            hide_index=True,
            height=360,
        )

    # ── Day-of-week ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Sales by Day of Week</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        fig2 = px.bar(
            dow_df, x="Day of Week", y="Total_Sales",
            color="Total_Sales", color_continuous_scale="Blues",
            title="Revenue by Day of Week",
            text=dow_df["Total_Sales"].apply(lambda v: f"₹{v:,.0f}"),
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(showlegend=False, coloraxis_showscale=False,
                           xaxis_title="", yaxis_title="Revenue (₹)")
        st.plotly_chart(chart_layout(fig2), use_container_width=True)

    with col4:
        fig3 = px.bar(
            dow_df, x="Day of Week", y="Avg_Order_Value",
            color="Avg_Order_Value", color_continuous_scale="Greens",
            title="Avg Order Value by Day of Week",
            text=dow_df["Avg_Order_Value"].apply(lambda v: f"₹{v:,.0f}"),
        )
        fig3.update_traces(textposition="outside")
        fig3.update_layout(showlegend=False, coloraxis_showscale=False,
                           xaxis_title="", yaxis_title="Avg Order (₹)")
        st.plotly_chart(chart_layout(fig3), use_container_width=True)

    # ── Revenue Tier over time ───────────────────────────────────────────────
    st.markdown('<div class="section-header">Revenue Tier Distribution</div>',
                unsafe_allow_html=True)
    tier_df = an.revenue_tier_distribution(dff)
    col5, col6 = st.columns(2)
    with col5:
        fig4 = px.bar(
            tier_df, x="Tier", y="Count",
            color="Tier", color_discrete_sequence=PALETTE,
            title="Order Count by Revenue Tier",
            text="Count",
        )
        fig4.update_traces(textposition="outside")
        fig4.update_layout(showlegend=False, xaxis_title="", yaxis_title="Orders")
        st.plotly_chart(chart_layout(fig4), use_container_width=True)
    with col6:
        fig5 = px.pie(
            tier_df, names="Tier", values="Count",
            color_discrete_sequence=PALETTE,
            title="Revenue Tier Share",
            hole=0.35,
        )
        fig5.update_traces(textposition="inside", textinfo="percent+label", textfont_size=11)
        st.plotly_chart(chart_layout(fig5), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 6 — PAYMENT & CUSTOMER
# ════════════════════════════════════════════════════════════════════════════

with TAB_PAYMENT:
    pay_df  = an.sales_by_payment(dff)
    ct_df   = an.sales_by_customer_type(dff)
    gen_df  = an.sales_by_gender(dff)

    st.markdown('<div class="section-header">Payment Methods</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            pay_df, x="Payment", y="Total_Sales",
            color="Payment", color_discrete_sequence=PALETTE,
            title="Revenue by Payment Method",
            text=pay_df["Total_Sales"].apply(lambda v: f"₹{v:,.0f}"),
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Revenue (₹)")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with col2:
        fig2 = px.pie(
            pay_df, names="Payment", values="Transactions",
            color_discrete_sequence=PALETTE,
            title="Transaction Share by Payment Method",
            hole=0.4,
        )
        fig2.update_traces(textposition="inside", textinfo="percent+label", textfont_size=11)
        st.plotly_chart(chart_layout(fig2), use_container_width=True)

    display_pay = pay_df.rename(columns={
        "Total_Sales": "Revenue (₹)",
        "Transactions": "Transactions",
        "Avg_Order_Value": "Avg Order (₹)",
        "% Share": "Tx Share (%)",
    })
    st.dataframe(
        display_pay.style.format({
            "Revenue (₹)": "₹{:,.2f}",
            "Avg Order (₹)": "₹{:,.2f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    st.markdown('<div class="section-header">Customer Type & Gender</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        fig3 = px.bar(
            ct_df, x="Customer Type", y="Total_Sales",
            color="Customer Type", color_discrete_sequence=[BLUE, ORANGE],
            title="Revenue: Member vs Normal",
            text=ct_df["Total_Sales"].apply(lambda v: f"₹{v:,.0f}"),
        )
        fig3.update_traces(textposition="outside")
        fig3.update_layout(showlegend=False, xaxis_title="", yaxis_title="Revenue (₹)")
        st.plotly_chart(chart_layout(fig3), use_container_width=True)

    with col4:
        fig4 = px.bar(
            gen_df, x="Gender", y="Total_Sales",
            color="Gender", color_discrete_sequence=[PURPLE, GREEN],
            title="Revenue by Gender",
            text=gen_df["Total_Sales"].apply(lambda v: f"₹{v:,.0f}"),
        )
        fig4.update_traces(textposition="outside")
        fig4.update_layout(showlegend=False, xaxis_title="", yaxis_title="Revenue (₹)")
        st.plotly_chart(chart_layout(fig4), use_container_width=True)

    # ── Category × Gender heatmap ────────────────────────────────────────────
    st.markdown('<div class="section-header">Category × Gender Revenue Heatmap</div>',
                unsafe_allow_html=True)
    heat_g = an.category_gender_heatmap(dff)
    fig_hg = go.Figure(go.Heatmap(
        z=heat_g.values.tolist(),
        x=heat_g.columns.tolist(),
        y=heat_g.index.tolist(),
        colorscale="Purples",
        text=[[f"₹{v:,.0f}" for v in row] for row in heat_g.values],
        texttemplate="%{text}",
        textfont_size=12,
    ))
    fig_hg.update_layout(
        title="Sales by Category and Gender",
        height=360, plot_bgcolor="#fff", paper_bgcolor="#fff",
        font=dict(family="Segoe UI, sans-serif", size=12),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig_hg, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 7 — RATINGS
# ════════════════════════════════════════════════════════════════════════════

with TAB_RATING:
    rat_cat = an.rating_by_category(dff)
    rat_dist = an.rating_distribution(dff)

    st.markdown('<div class="section-header">Customer Ratings Analysis</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Overall Avg Rating",  f"{dff['Rating'].mean():.2f} / 5")
    c2.metric("Highest-Rated Category", rat_cat.iloc[0]["Category"])
    c3.metric("Lowest-Rated Category",  rat_cat.iloc[-1]["Category"])

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            rat_cat.sort_values("Avg_Rating"),
            x="Avg_Rating", y="Category", orientation="h",
            color="Avg_Rating", color_continuous_scale="RdYlGn",
            range_color=[1, 5],
            title="Average Rating by Category",
            text=rat_cat.sort_values("Avg_Rating")["Avg_Rating"].apply(lambda v: f"{v:.2f}"),
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, coloraxis_showscale=False,
                          xaxis_title="Avg Rating", yaxis_title="")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with col2:
        fig2 = px.bar(
            rat_dist, x="Range", y="Count",
            color="Count", color_continuous_scale="Blues",
            title="Rating Distribution",
            text="Count",
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(showlegend=False, coloraxis_showscale=False,
                           xaxis_title="Rating Range", yaxis_title="# Orders")
        st.plotly_chart(chart_layout(fig2), use_container_width=True)

    # ── Scatter: Sales vs Rating ──────────────────────────────────────────
    st.markdown('<div class="section-header">Sales Amount vs Customer Rating</div>',
                unsafe_allow_html=True)
    fig3 = px.scatter(
        dff, x="Rating", y="Sales",
        color="Category", size="Quantity",
        color_discrete_sequence=PALETTE,
        opacity=0.65,
        title="Sales vs Rating (sized by Quantity)",
        hover_data=["Product", "Branch", "Payment"],
    )
    fig3.update_layout(xaxis_title="Rating", yaxis_title="Sales (₹)")
    st.plotly_chart(chart_layout(fig3, 440), use_container_width=True)

    # ── Branch × Customer Type rating ────────────────────────────────────
    st.markdown('<div class="section-header">Avg Rating: Branch × Customer Type</div>',
                unsafe_allow_html=True)
    rat_br = (
        dff.groupby(["Branch", "Customer Type"])["Rating"]
        .mean().round(2).reset_index()
    )
    fig4 = px.bar(
        rat_br, x="Branch", y="Rating",
        color="Customer Type", barmode="group",
        color_discrete_sequence=[BLUE, ORANGE],
        title="Rating by Branch and Customer Type",
        text=rat_br["Rating"].apply(lambda v: f"{v:.2f}"),
    )
    fig4.update_traces(textposition="outside")
    fig4.update_layout(xaxis_title="Branch", yaxis_title="Avg Rating", yaxis_range=[0, 5.5])
    st.plotly_chart(chart_layout(fig4), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 8 — BUSINESS INSIGHTS
# ════════════════════════════════════════════════════════════════════════════

with TAB_INSIGHTS:
    st.markdown('<div class="section-header">💡 Data-Driven Business Recommendations</div>',
                unsafe_allow_html=True)
    st.caption(
        "These insights are automatically derived from your filtered dataset. "
        "Adjust sidebar filters to see how recommendations change."
    )

    insights = an.generate_insights(dff)
    for ins in insights:
        st.markdown(
            f"""
            <div class="insight-card">
              <div class="insight-title">{ins['icon']} {ins['title']}</div>
              <div class="insight-detail">{ins['detail']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Summary comparison table ─────────────────────────────────────────
    st.markdown('<div class="section-header">Category vs Branch Revenue Summary</div>',
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**By Category**")
        cat_s = an.sales_by_category(dff)[["Category", "Total_Sales", "% Revenue Share"]]
        st.dataframe(
            cat_s.style.format({"Total_Sales": "₹{:,.2f}", "% Revenue Share": "{:.1f}%"})
                       .background_gradient(subset=["Total_Sales"], cmap="Blues"),
            use_container_width=True, hide_index=True,
        )
    with col2:
        st.markdown("**By Branch / City**")
        br_s = an.sales_by_branch(dff)[["Branch", "City", "Total_Sales", "% Revenue Share"]]
        st.dataframe(
            br_s.style.format({"Total_Sales": "₹{:,.2f}", "% Revenue Share": "{:.1f}%"})
                      .background_gradient(subset=["Total_Sales"], cmap="Greens"),
            use_container_width=True, hide_index=True,
        )

    # ── Radar chart: branch vs KPIs ─────────────────────────────────────────
    st.markdown('<div class="section-header">Branch KPI Radar Comparison</div>',
                unsafe_allow_html=True)
    radar_data = (
        dff.groupby("Branch").agg(
            Revenue=("Sales", "sum"),
            Transactions=("Invoice ID", "count"),
            Avg_Order=("Sales", "mean"),
            Avg_Rating=("Rating", "mean"),
            Units_Sold=("Quantity", "sum"),
        ).reset_index()
    )
    # normalise each metric to 0–100
    for col in ["Revenue", "Transactions", "Avg_Order", "Avg_Rating", "Units_Sold"]:
        mn, mx = radar_data[col].min(), radar_data[col].max()
        radar_data[col + "_n"] = ((radar_data[col] - mn) / (mx - mn + 1e-9) * 100).round(1)

    categories = ["Revenue", "Transactions", "Avg Order", "Avg Rating", "Units Sold"]
    fig_radar = go.Figure()
    for _, row in radar_data.iterrows():
        vals = [
            row["Revenue_n"], row["Transactions_n"], row["Avg_Order_n"],
            row["Avg_Rating_n"], row["Units_Sold_n"],
        ]
        vals += [vals[0]]  # close polygon
        fig_radar.add_trace(go.Scatterpolar(
            r=vals,
            theta=categories + [categories[0]],
            fill="toself",
            name=f"Branch {row['Branch']}",
            opacity=0.7,
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="Branch KPI Radar (normalised 0–100)",
        height=440,
        plot_bgcolor="#fff", paper_bgcolor="#fff",
        font=dict(family="Segoe UI, sans-serif", size=12),
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_radar, use_container_width=True)
