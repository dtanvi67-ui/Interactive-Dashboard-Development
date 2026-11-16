from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "data" / "sales_dashboard_data.csv", parse_dates=["order_date"])
df["revenue"] = df["quantity"] * df["unit_price"]

print("DATASET OVERVIEW")
print(f"Rows: {len(df)}")
print(f"Date range: {df['order_date'].min().date()} to {df['order_date'].max().date()}")
print(f"Total revenue: ₹{df['revenue'].sum():,.2f}")
print(f"Unique orders: {df['order_id'].nunique()}")
print("\nREVENUE BY REGION")
print(df.groupby("region")["revenue"].sum().sort_values(ascending=False))
print("\nREVENUE BY CATEGORY")
print(df.groupby("category")["revenue"].sum().sort_values(ascending=False))
print("\nTOP PRODUCTS")
print(df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(10))
