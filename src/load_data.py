import pandas as pd

def load_data():
    """
    تحميل بيانات المبيعات من ملف CSV وعرض معلومات أساسية عنها.
    """
    # نقرأ الملف مباشرة من مجلد data
    df = pd.read_csv("data/ecommerce_sales_large.csv", encoding='ISO-8859-1')

    # طباعة معلومات أساسية
    print("✅ Data loaded successfully!\n")
    print(f"عدد الصفوف: {len(df)}")
    print(f"عدد الأعمدة: {len(df.columns)}\n")
    print("أسماء الأعمدة:")
    print(df.columns.tolist())
    print("\nأول خمس صفوف من البيانات:")
    print(df.head())

    return df

if __name__ == "__main__":
    df = load_data()
