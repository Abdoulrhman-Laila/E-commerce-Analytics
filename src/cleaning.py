import pandas as pd
from load_data import load_data

def clean_data(df):
    """
    تنظيف وتحضير بيانات المبيعات الإلكترونية
    متوافق مع الأعمدة:
    OrderID, CustomerID, Gender, Age, Country, ProductCategory, SubCategory,
    Quantity, UnitPrice, OrderDate, TotalPrice
    """
    print("\n🔍 Starting cleaning...")

    # 1. إزالة التكرارات
    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed duplicates: {before - len(df)} rows")

    # 2. تحويل التاريخ
    if 'OrderDate' in df.columns:
        df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

    # 3. تحويل الأعمدة الرقمية
    numeric_cols = ['Quantity', 'UnitPrice', 'TotalPrice']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 4. إنشاء عمود للشهر
    if 'OrderDate' in df.columns:
        df['Order_Month'] = df['OrderDate'].dt.to_period('M')

    # 5. حساب TotalPrice إذا لم يوجد
    if 'TotalPrice' not in df.columns:
        if 'Quantity' in df.columns and 'UnitPrice' in df.columns:
            df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    # 6. إزالة صفوف بقيم رقمية مفقودة
    before = len(df)
    df = df.dropna(subset=[c for c in numeric_cols if c in df.columns])
    print(f"Dropped rows with missing numeric essentials: {before - len(df)}")

    # 7. إعادة ضبط الفهرس
    df = df.reset_index(drop=True)

    print("✅ Cleaning finished. Shape:", df.shape)
    return df


if __name__ == "__main__":
    df = load_data()
    df_clean = clean_data(df)

    # حفظ النسخ النهائية
    csv_path = "data/cleaned_ecommerce.csv"
    parquet_path = "data/cleaned_ecommerce.parquet"

    # حفظ CSV دائمًا
    df_clean.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"💾 Saved cleaned data to {csv_path}")

    # حفظ Parquet (إن كانت المكتبة متوفرة)
    try:
        df_clean.to_parquet(parquet_path, index=False)
        print(f"💾 Saved cleaned data to {parquet_path}")
    except Exception as e:
        print(f"⚠️ Could not save Parquet (missing optional lib). Exception: {e}")
