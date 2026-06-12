import pandas as pd

truck_data = {
    "Truck_ID": ["TR001", "TR002", "TR003", "TR004"],
    "Supplier": [
        "ASK AUTOMOTIVE",
        "VARROC ENGINEERING",
        "FIEM",
        "ASK AUTOMOTIVE"
    ],
    "Gate_In_Time": [
        "08:05",
        "08:20",
        "08:35",
        "08:50"
    ],
    "Unloading_Start": [
        "08:10",
        "08:30",
        "08:40",
        "09:00"
    ],
    "Unloading_End": [
        "08:25",
        "08:45",
        "08:55",
        "09:15"
    ]
}

df = pd.DataFrame(truck_data)

df["Status"] = "Completed"

print(df)