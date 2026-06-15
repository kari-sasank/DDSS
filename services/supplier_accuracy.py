import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mssql+pyodbc://@SAMEERA\\SQLEXPRESS/sam?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

df = pd.read_sql("SELECT * FROM SupplierDelivery", engine)

result = (
    df.groupby("Supplier Name")
      .agg(
          Total_Deliveries=("Lot No.", "count"),
          Delivered=("Status", lambda x: (x.notna()).sum())
      )
      .reset_index()
)

result["Accuracy_Percentage"] = (
    result["Delivered"] /
    result["Total_Deliveries"]
) * 100

print(result)