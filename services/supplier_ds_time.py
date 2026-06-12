import pandas as pd

data = {
    "Truck_ID": ["TR001", "TR002", "TR003", "TR004"],
    "Supplier": [
        "ASK AUTOMOTIVE",
        "VARROC ENGINEERING",
        "FIEM",
        "ASK AUTOMOTIVE"
    ],
    "Arrival_Time": [
        "08:00",
        "08:15",
        "08:30",
        "08:45"
    ]
}

df = pd.DataFrame(data)

DOCKS_AVAILABLE = 2
UNLOADING_TIME = 30

df["DS_Slot"] = ""

for i in range(len(df)):
    dock = (i % DOCKS_AVAILABLE) + 1

    slot_start = pd.Timestamp("2026-06-12 08:00") + pd.Timedelta(
        minutes=(i // DOCKS_AVAILABLE) * UNLOADING_TIME
    )

    df.loc[i, "DS_Slot"] = (
        f"Dock-{dock} : "
        f"{slot_start.strftime('%H:%M')}"
    )

print(df)