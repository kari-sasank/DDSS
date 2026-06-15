import pandas as pd
from sqlalchemy import create_engine

server = "SAMEERA\\SQLEXPRESS"
database = "sam"

connection_string = (
    f"mssql+pyodbc://@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(connection_string)

df = pd.read_csv("output/supplier_report.csv")

df.to_sql(
    "supplier_report",
    engine,
    if_exists="replace",
    index=False
)

print("Data loaded to SQL Server successfully!")