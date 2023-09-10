import pandas as pd
import os

input_dir = "data"
output_dir = "filtered_data"
sca_files = [f for f in os.listdir(input_dir) if f.endswith(".sca.csv")]

rows_to_keep = [
    "nrOfNodes",
    "simulated time",
    "dataPacketTime",
    "fbpPacketTime",
    "arsPacketTime",
    "beaconPacketTime",
    "vctsPacketTime",
    "rtsPacketTime",
    "numDataPacketsReceived",
    "numARSPacketsSent",
    "numFBPPacketsSent",
    "numRTSPacketsSent",
    "numVCTSPacketsSent",
    "numBeaconPacketsSent",
    "dataPacketLenBits",
    "arsPacketLenBits",
    "fbpPacketLenBits",
    "rtsPacketLenBits",
    "beaconPacketLenBits",
    "vctsPacketLenBits",
    "totalPacketDelay",
    "numContentionSlots",
    "wrx",
]

rows_to_keep = (
    rows_to_keep
    + [f"dtqLength[{i}]" for i in range(5000)]
    + [f"crqLength[{i}]" for i in range(5000)]
)

for file_name in sca_files:
    print(file_name)
    df = pd.read_csv(os.path.join(input_dir, file_name), dtype=str)
    df1 = df[df["name"].isin(rows_to_keep)]
    df2 = df[df['name'].str.startswith("numDataPacketsReceivedByNodeId", na=False)]
    df = pd.concat([df1, df2])
    df.to_csv(os.path.join(output_dir, file_name), encoding='utf-8', index=False)
