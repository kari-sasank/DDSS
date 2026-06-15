import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mssql+pyodbc://@SAMEERA\\SQLEXPRESS/sam?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

df = pd.read_sql("SELECT * FROM SupplierDelivery", engine)

result = (
    df.groupby("Supplier Name")
      .agg(
          Total_Shipment=("Shipment QTY", "sum"),
          Total_Received=("Received QTY", "sum")
      )
      .reset_index()
)

result["Delivery_Performance"] = (
    result["Total_Received"] /
    result["Total_Shipment"]
) * 100

print(result)