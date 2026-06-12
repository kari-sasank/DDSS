import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mssql+pyodbc://@SAMEERA\\SQLEXPRESS/sam?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

query = """
SELECT
    Supplier_Name,
    COUNT(*) AS Default_Count
FROM SupplierDelivery
WHERE Actual_Delivery_Time > Planned_Delivery_Time
GROUP BY Supplier_Name
"""

df = pd.read_sql(query, engine)

print(df)