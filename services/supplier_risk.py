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
          Pending=("Received QTY", lambda x: x.isna().sum())
      )
      .reset_index()
)

result["Risk_Percentage"] = (
    result["Pending"] /
    result["Total_Deliveries"]
) * 100

print(result)