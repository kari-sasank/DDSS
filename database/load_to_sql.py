import pandas as pd
from sqlalchemy import create_engine

# Read CSV file
df = pd.read_excel("data/Delivery schedule (1).xls", header=1)

# SQL Server connection
connection_string = (
    "mssql+pyodbc://@SAMEERA\\SQLEXPRESS/sam"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

engine = create_engine(connection_string)

# Load data into SQL Server table
df.to_sql(
    "SupplierDelivery",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data loaded successfully!")