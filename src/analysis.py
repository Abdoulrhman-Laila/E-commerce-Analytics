import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# إعدادات العرض العامة
sns.set(style="whitegrid", font="Arial")
plt.rcParams['figure.figsize'] = (10, 6)


def load_cleaned(path_csv="data/cleaned_ecommerce.csv"):
    """
    Load cleaned e-commerce dataset from CSV.
    If not found, automatically clean and recreate it.
    """
    if os.path.exists(path_csv):
        df = pd.read_csv(path_csv, parse_dates=['OrderDate'])
        print("✅ Loaded cleaned CSV file.")
    else:
        from load_data import load_data
        from cleaning import clean_data
        df = load_data()
        df = clean_data(df)
        df.to_csv(path_csv, index=False)
        print("⚙️ Data cleaned and saved as CSV.")
    return df


def basic_stats(df):
    print("\n=== Basic Info ===")
    print(df.info())
    print("\n=== Numeric Describe ===")
    print(df.describe())


def top_products_by_quantity(df, n=10):
    """Top-selling products by quantity."""
    res = df.groupby('SubCategory')['Quantity'].sum().sort_values(ascending=False).head(n)
    print("\n📦 Top products by quantity:")
    print(res)
    return res


def sales_by_country(df, n=15):
    """Top countries by total revenue."""
    res = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(n)
    print("\n🌍 Top countries by revenue:")
    print(res)
    return res


def monthly_trend(df):
    """Monthly revenue trend."""
    if 'Order_Month' not in df.columns and 'OrderDate' in df.columns:
        df['Order_Month'] = df['OrderDate'].dt.to_period('M')

    res = df.groupby('Order_Month')['TotalPrice'].sum().sort_index()
    print("\n📅 Monthly revenue (last 10 months):")
    print(res.tail(10))
    return res


def save_summary(df):
    """Save summary reports as CSV in outputs/reports."""
    os.makedirs("outputs/reports", exist_ok=True)

    top_prod = top_products_by_quantity(df)
    sales_country = sales_by_country(df)
    monthly = monthly_trend(df)

    top_prod.to_csv("outputs/reports/top_products_quantity.csv")
    sales_country.to_csv("outputs/reports/top_countries_revenue.csv")
    monthly.to_csv("outputs/reports/monthly_revenue.csv")

    print("\n💾 Saved summary reports as CSV in outputs/reports/")


# ------------------- Visualization -------------------

def plot_top_products(df, n=10, save_dir="charts"):
    """Plot and save top-selling products."""
    data = top_products_by_quantity(df, n)
    plt.figure()
    sns.barplot(x=data.values, y=data.index, palette="viridis")
    plt.title("Top Selling Products", fontsize=14)
    plt.xlabel("Total Quantity Sold")
    plt.ylabel("Product")
    plt.tight_layout()
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(f"{save_dir}/top_selling_products.png", dpi=300)
    plt.close()
    print(f"📊 Saved chart: {save_dir}/top_selling_products.png")


def plot_sales_by_country(df, n=10, save_dir="charts"):
    """Plot and save top revenue by country."""
    data = sales_by_country(df, n)
    plt.figure()
    sns.barplot(x=data.values, y=data.index, palette="crest")
    plt.title("Top Countries by Revenue", fontsize=14)
    plt.xlabel("Total Revenue")
    plt.ylabel("Country")
    plt.tight_layout()
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(f"{save_dir}/top_countries_revenue.png", dpi=300)
    plt.close()
    print(f"📊 Saved chart: {save_dir}/top_countries_revenue.png")


def plot_monthly_trend(df, save_dir="charts"):
    """Plot and save monthly revenue trend."""
    data = monthly_trend(df)
    plt.figure()
    data.plot(kind='line', marker='o', color='teal')
    plt.title("Monthly Revenue Trend", fontsize=14)
    plt.xlabel("Month")
    plt.ylabel("Total Revenue")
    plt.grid(True)
    plt.tight_layout()
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(f"{save_dir}/monthly_revenue_trend.png", dpi=300)
    plt.close()
    print(f"📊 Saved chart: {save_dir}/monthly_revenue_trend.png")


# ------------------- Main Execution -------------------

if __name__ == "__main__":
    print("🚀 Starting E-commerce Data Analysis...")

    df = load_cleaned()
    basic_stats(df)
    save_summary(df)

    # Generate and save charts
    plot_top_products(df)
    plot_sales_by_country(df)
    plot_monthly_trend(df)

    print("\n✅ All reports and charts saved successfully!")
