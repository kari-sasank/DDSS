import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mssql+pyodbc://@SAMEERA\\SQLEXPRESS/sam?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

query = """
SELECT
    Supplier_Name,
    COUNT(*) AS Total_Deliveries,
    SUM(
        CASE
            WHEN Actual_Delivery_Time > Planned_Delivery_Time
            THEN 1
            ELSE 0
        END
    ) AS Default_Count
FROM SupplierDelivery
GROUP BY Supplier_Name
"""

df = pd.read_sql(query, engine)

df["Risk_Percentage"] = (
    df["Default_Count"] /
    df["Total_Deliveries"]
) * 100

print(df)