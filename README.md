# Interactive Dashboard Development

An interactive sales and business performance dashboard built with Python, Streamlit, Plotly, and Pandas.

## Features
- KPI cards: total revenue, total orders, average order value, and units sold
- Interactive filters for region, category, and date range
- Monthly revenue trend
- Revenue by product category
- Sales by region
- Top products table
- Download filtered data as CSV

## Dataset
The included CSV is synthetic sample data created for learning and demonstration. It is not real company data.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Project structure
```text
Interactive-Dashboard-Development/
├── app.py
├── analysis.py
├── requirements.txt
├── README.md
├── PROJECT_REPORT.md
├── .gitignore
└── data/
    └── sales_dashboard_data.csv
```

## Tools
Python, Pandas, Streamlit, Plotly.

## Note
The sample dataset and dashboard are for educational use. Replace the sample data with verified business data before making real business decisions.
