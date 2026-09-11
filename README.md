# 🛒 Supermarket Sales Analytics

A full-stack data analytics project for supermarket sales data, built with **Python**, **Pandas**, **Plotly**, and **Streamlit**.

---

## Project Structure

```
supermarket_analysis/
├── app.py            ← Streamlit frontend (8 tabbed sections)
├── data_loader.py    ← CSV loading, cleaning, validation, feature engineering
├── analytics.py      ← All aggregations, KPIs, and business insight generation
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Place the dataset
Make sure the CSV file is in the **parent folder** (one level above `supermarket_analysis/`):
```
SUPER MARKET DATA - supermarket_sales_500_rows.csv
```
Or upload it directly through the app's sidebar file uploader.

### 3. Run the app
```bash
cd supermarket_analysis
streamlit run app.py
```
The app will open at **http://localhost:8501** in your browser.

---

## Features

| Tab | Content |
|-----|---------|
| **📊 Overview** | KPI cards, revenue by category (bar + pie), monthly trend line |
| **🔍 Data Quality** | Missing values, duplicates, dtype summary, descriptive stats, mismatch flags |
| **📦 Category Analysis** | Revenue table, avg order, units sold, heatmap, top-10 products |
| **🏪 Branch & City** | Branch comparison, revenue funnel, category stack per branch |
| **📅 Time Trends** | Monthly dual-axis chart, day-of-week analysis, revenue tier distribution |
| **💳 Payment & Customer** | Payment breakdown, member vs normal, gender split, heatmap |
| **⭐ Ratings** | Avg rating by category, rating distribution, scatter Sales vs Rating |
| **💡 Business Insights** | 8 auto-generated, data-driven recommendations + radar chart |

### Sidebar Filters
- Branch, City, Category, Payment (multi-select)
- Date range picker
- CSV file uploader (optional)

---

## Analytics Covered

1. **Data Collection & Loading** — CSV ingestion with column validation
2. **Data Quality Checks** — null detection, duplicate removal, Sales = Qty × Price verification
3. **Sales Calculation** — `Sales = Quantity × Unit Price` recalculated and cross-checked
4. **Grouping & Summarization** — totals, counts, averages by Category / Branch / Month / Payment / Gender / Customer Type
5. **Charts** — bar, line, pie, donut, heatmap, scatter, funnel, radar
6. **Business Decisions** — 8 actionable insights derived from the data

---

## Dataset Columns

| Column | Type | Description |
|--------|------|-------------|
| Invoice ID | String | Unique transaction ID |
| Date | Date | Transaction date |
| Branch | String | Store branch (A/B/C/D) |
| City | String | Store city |
| Customer Type | String | Member / Normal |
| Gender | String | Male / Female |
| Product | String | Product name |
| Category | String | Product category |
| Quantity | Integer | Units purchased |
| Unit Price | Float | Price per unit (₹) |
| Payment | String | UPI / Card / Cash / Net Banking |
| Rating | Float | Customer satisfaction (1–5) |
| Sales | Float | Total sale amount (₹) |
