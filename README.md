# 🛒 Supermarket Sales Analytics Dashboard

An interactive **Supermarket Sales Analytics Dashboard** built with **Python, Pandas, Plotly, and Streamlit** to analyze sales performance, customer behavior, product categories, payment methods, branch performance, ratings, and business trends.

🔗 **Live Dashboard:** https://supermarket-analysis-f6mn2jqmil43ypeasmq4ea.streamlit.app/

---

## 📌 Project Overview

This project transforms supermarket sales data into an interactive analytics dashboard that helps identify:

* 📈 Overall sales and revenue performance
* 🛍️ Category and product-level performance
* 🏪 Branch and city-wise sales trends
* 💳 Payment method preferences
* 👥 Customer and gender distribution
* 📅 Monthly and day-wise sales trends
* ⭐ Customer ratings and satisfaction
* 💡 Data-driven business insights and recommendations

The dashboard is designed to make supermarket data easier to explore and support better business decision-making.

---

## 🛠️ Tech Stack

* **Python** — Data processing and application development
* **Pandas** — Data cleaning, transformation, and analysis
* **NumPy** — Numerical operations
* **Plotly** — Interactive charts and visualizations
* **Matplotlib** — Data styling and gradient formatting
* **Streamlit** — Interactive web dashboard
* **Git & GitHub** — Version control and project hosting
* **Streamlit Community Cloud** — Dashboard deployment

---

## 📂 Project Structure

```text
supermarket-analysis/
│
├── app.py
├── data_loader.py
├── analytics.py
├── requirements.txt
├── supermarket_sales_500_rows.csv
├── Supermarket_Sales_Report.pptx
└── README.md
```

### File Description

| File                             | Purpose                                                        |
| -------------------------------- | -------------------------------------------------------------- |
| `app.py`                         | Main Streamlit dashboard and user interface                    |
| `data_loader.py`                 | Dataset loading, cleaning, validation, and feature preparation |
| `analytics.py`                   | KPIs, aggregations, analysis, and business insights            |
| `requirements.txt`               | Required Python libraries                                      |
| `supermarket_sales_500_rows.csv` | Supermarket sales dataset                                      |
| `Supermarket_Sales_Report.pptx`  | Project presentation/report                                    |
| `README.md`                      | Project documentation                                          |

---

## 📊 Dashboard Sections

The dashboard contains **8 interactive sections**:

### 📊 Overview

* Key performance indicators
* Revenue by category
* Category distribution
* Monthly revenue trends

### 🔍 Data Quality

* Missing-value analysis
* Duplicate detection
* Data-type summary
* Descriptive statistics
* Sales consistency checks

### 📦 Category Analysis

* Revenue by category
* Average order value
* Units sold
* Category heatmap
* Top-performing products

### 🏪 Branch & City

* Branch performance comparison
* Revenue funnel
* Category performance by branch
* City-level analysis

### 📅 Time Trends

* Monthly sales trends
* Day-of-week performance
* Revenue tier distribution
* Time-based comparisons

### 💳 Payment & Customer

* Payment method distribution
* Member vs. Normal customers
* Gender analysis
* Customer behavior comparison

### ⭐ Ratings

* Average rating by category
* Rating distribution
* Sales vs. rating analysis
* Customer satisfaction trends

### 💡 Business Insights

* Automatically generated business insights
* Data-driven recommendations
* Interactive insight visualizations
* Actionable findings for decision-making

---

## 🎛️ Interactive Filters

The dashboard provides interactive sidebar filters for:

* 🏪 Branch
* 📍 City
* 📦 Category
* 💳 Payment method
* 📅 Date range

Users can dynamically filter the dashboard and explore specific segments of the dataset.

The application also supports an **optional CSV uploader** for analyzing another compatible dataset.

---

## 📈 Analytics Performed

The project covers several important stages of the data analytics workflow:

### 1. Data Loading & Validation

CSV data is loaded and checked against the expected dataset structure.

### 2. Data Cleaning

* Missing-value detection
* Duplicate identification
* Data-type validation
* Date conversion
* Column validation

### 3. Sales Calculation

Sales values are validated using:

```text
Sales = Quantity × Unit Price
```

### 4. Grouping & Aggregation

Data is analyzed across:

* Category
* Product
* Branch
* City
* Month
* Payment Method
* Gender
* Customer Type
* Ratings

### 5. Data Visualization

The dashboard includes:

* 📊 Bar charts
* 📈 Line charts
* 🥧 Pie/Donut charts
* 🔥 Heatmaps
* 🎯 Scatter plots
* 🔻 Funnel charts
* 🕸️ Radar charts
* 📋 Interactive tables

### 6. Business Insights

The dashboard automatically generates actionable insights based on the analyzed data to help identify sales patterns, customer preferences, and improvement opportunities.

---

## 🗃️ Dataset

The project uses a supermarket sales dataset containing **500 transaction records**.

### Dataset Columns

| Column        | Type    | Description                   |
| ------------- | ------- | ----------------------------- |
| Invoice ID    | String  | Unique transaction identifier |
| Date          | Date    | Transaction date              |
| Branch        | String  | Store branch                  |
| City          | String  | Store location                |
| Customer Type | String  | Member / Normal               |
| Gender        | String  | Customer gender               |
| Product       | String  | Product name                  |
| Category      | String  | Product category              |
| Quantity      | Integer | Number of units purchased     |
| Unit Price    | Float   | Price per unit                |
| Payment       | String  | Payment method                |
| Rating        | Float   | Customer satisfaction rating  |
| Sales         | Float   | Total transaction value       |

---

## 🚀 Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/sanafirdausofficial-maker/supermarket-analysis.git
```

### 2. Navigate to the project

```bash
cd supermarket-analysis
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit dashboard

```bash
streamlit run app.py
```

The application will open locally at:

```text
http://localhost:8501
```

The dataset is already included in the repository, so the dashboard can load the default dataset directly.

---


<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/e3c18017-4569-4b9c-ac22-61d6b21bec55" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/41f0580f-d4ee-4e7f-854e-35baf11dddb0" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/6c8d8dfd-9ee3-45ca-b66b-0bf3af441d02" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/80ccd8da-793a-44a2-93e0-c7cfeca33940" />


## ☁️ Live Deployment

The dashboard is deployed using **Streamlit Community Cloud**.

🔗 **Live App:**
https://supermarket-analysis-f6mn2jqmil43ypeasmq4ea.streamlit.app/

The live application allows users to interact with the dashboard directly from a web browser without installing Python or any dependencies.

---

## 📄 Project Report

A detailed project presentation is included in the repository:

📑 `Supermarket_Sales_Report.pptx`

---

## 🎯 Project Goals

The main objectives of this project are to:

* Understand supermarket sales patterns
* Identify high-performing categories and products
* Compare branch and city performance
* Analyze customer purchasing behavior
* Understand payment preferences
* Evaluate customer satisfaction
* Identify meaningful trends over time
* Generate actionable business recommendations

---

## 🌟 Key Highlights

✅ Interactive Streamlit dashboard
✅ 500-row supermarket sales dataset
✅ Automated data validation and cleaning
✅ Multiple interactive visualizations
✅ Business-focused analytics
✅ Optional custom CSV analysis
✅ GitHub-hosted source code
✅ Live Streamlit deployment

---

## 👩‍💻 Author

**Sana Firdaus**

🔗 GitHub: https://github.com/sanafirdausofficial-maker

---

⭐ **If you find this project useful, consider giving the repository a star!**
