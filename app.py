from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "sales_dashboard_data.csv"

st.set_page_config(page_title="Interactive Sales Dashboard", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    return df

df = load_data()
st.title("Interactive Sales Performance Dashboard")
st.caption("Explore revenue, orders, products, and regional performance using interactive filters.")

st.sidebar.header("Dashboard Filters")
regions = ["All"] + sorted(df["region"].unique().tolist())
categories = ["All"] + sorted(df["category"].unique().tolist())
chosen_region = st.sidebar.selectbox("Region", regions)
chosen_category = st.sidebar.selectbox("Category", categories)
min_date, max_date = df["order_date"].min().date(), df["order_date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)

filtered = df.copy()
if chosen_region != "All":
    filtered = filtered[filtered["region"] == chosen_region]
if chosen_category != "All":
    filtered = filtered[filtered["category"] == chosen_category]
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = date_range
    filtered = filtered[filtered["order_date"].dt.date.between(start, end)]

if filtered.empty:
    st.warning("No records match the selected filters. Please change the filters.")
    st.stop()

revenue = filtered["revenue"].sum()
orders = filtered["order_id"].nunique()
aov = revenue / orders if orders else 0
units = int(filtered["quantity"].sum())

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"₹{revenue:,.0f}")
k2.metric("Total Orders", f"{orders:,}")
k3.metric("Average Order Value", f"₹{aov:,.0f}")
k4.metric("Units Sold", f"{units:,}")

monthly = (filtered.assign(month=filtered["order_date"].dt.to_period("M").dt.to_timestamp())
           .groupby("month", as_index=False)["revenue"].sum())
category = filtered.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
region = filtered.groupby("region", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)

left, right = st.columns(2)
with left:
    st.subheader("Monthly Revenue Trend")
    fig = px.line(monthly, x="month", y="revenue", markers=True,
                  labels={"month": "Month", "revenue": "Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Revenue by Category")
    fig = px.pie(category, names="category", values="revenue", hole=0.45)
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Revenue by Region")
    fig = px.bar(region, x="region", y="revenue", color="region",
                 labels={"region": "Region", "revenue": "Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Top Products")
    top_products = (filtered.groupby("product", as_index=False)
                    .agg(revenue=("revenue", "sum"), units_sold=("quantity", "sum"))
                    .sort_values("revenue", ascending=False).head(10))
    st.dataframe(top_products, use_container_width=True, hide_index=True)

st.subheader("Filtered Sales Records")
st.dataframe(filtered.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)
csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data (CSV)", data=csv_bytes,
                   file_name="filtered_sales_data.csv", mime="text/csv")

st.info("This dashboard uses synthetic sample data for demonstration. It should not be treated as actual company performance.")
