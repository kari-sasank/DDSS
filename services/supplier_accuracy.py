import pandas as pd

df = pd.read_csv("data/supplier_delivery.csv")

df["Planned_Delivery_Time"] = pd.to_datetime(df["Planned_Delivery_Time"])
df["Actual_Delivery_Time"] = pd.to_datetime(df["Actual_Delivery_Time"])

df["On_Time"] = df["Actual_Delivery_Time"] <= df["Planned_Delivery_Time"]

result = df.groupby("Supplier_Name").agg(
    Total_Deliveries=("Lot_No", "count"),
    On_Time_Deliveries=("On_Time", "sum")
)

result["Accuracy_Percentage"] = (
    result["On_Time_Deliveries"] /
    result["Total_Deliveries"]
) * 100

print(result)