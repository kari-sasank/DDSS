import pandas as pd

df = pd.read_csv("data/supplier_delivery.csv")

# Convert to datetime
df["Planned_Delivery_Time"] = pd.to_datetime(df["Planned_Delivery_Time"])
df["Actual_Delivery_Time"] = pd.to_datetime(df["Actual_Delivery_Time"])

# Calculate delay in minutes
df["Delay_Minutes"] = (
    df["Actual_Delivery_Time"] -
    df["Planned_Delivery_Time"]
).dt.total_seconds() / 60

# Save report
df.to_csv("output/supplier_report.csv", index=False)

print("Report saved successfully!")
print(df.head())