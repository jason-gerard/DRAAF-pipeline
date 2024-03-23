import os
import pprint
import pandas as pd
from pathlib import Path
import shutil
import constants

DEFAULT_INPUT_PATH = "/home/jason/omnetpp-6.0.1/samples/florasat/simulations/dtsiot/results"
DATA_SOURCES_PATH = os.path.join(constants.PROJECT_ROOT, constants.DATA_SOURCES_ROOT)

rows_to_keep = [
    "nrOfNodes",
    "simulated time",
    "dataPacketTime",
    "fbpPacketTime",
    "arsPacketTime",
    "beaconPacketTime",
    "vctsPacketTime",
    "rtsPacketTime",
    "ackPacketTime",
    "numDataPacketsReceived",
    "numDataPacketsSent",
    "numARSPacketsSent",
    "numFBPPacketsSent",
    "numRTSPacketsSent",
    "numVCTSPacketsSent",
    "numBeaconPacketsSent",
    "numACKPacketsSent",
    "dataPacketLenBits",
    "arsPacketLenBits",
    "fbpPacketLenBits",
    "rtsPacketLenBits",
    "beaconPacketLenBits",
    "vctsPacketLenBits",
    "ackPacketLenBits",
    "totalPacketDelay",
    "numContentionSlots",
    "wrx",
]

rows_to_keep = (
        rows_to_keep
        + [f"dtqLength[{i}]" for i in range(5000)]
        + [f"crqLength[{i}]" for i in range(5000)]
)

sca_files = [f for f in os.listdir(DEFAULT_INPUT_PATH) if f.endswith(".sca")]
sca_files.sort()

# Get set of data sources
data_sources = set([",".join(f.split(",")[:-1]) for f in sca_files])
pprint.pprint(data_sources)

for data_source in data_sources:
    data_source_path = os.path.join(DATA_SOURCES_PATH, data_source)
    if Path(data_source_path).is_dir():
        raise Exception(f"Data source: {data_source} at path {data_source_path} already exists")


for data_source in data_sources:
    data_source_path = os.path.join(DATA_SOURCES_PATH, data_source)
    Path(data_source_path).mkdir()

for file_name in sca_files:
    print(file_name)
    data_source = ",".join(file_name.split(",")[:-1])
    
    raw_file_path = os.path.join(DEFAULT_INPUT_PATH, file_name)  # From
    raw_data_data_source_path = os.path.join(DATA_SOURCES_PATH, data_source, constants.RAW_DATA_DIR)  # To
    Path(raw_data_data_source_path).mkdir(parents=True, exist_ok=True)

    raw_data_data_source_file_name_path = os.path.join(raw_data_data_source_path, file_name)

    # Copy raw file to datasource
    shutil.copyfile(raw_file_path, raw_data_data_source_file_name_path)

    # Convert to csv
    output_csv_path = f"{raw_data_data_source_file_name_path}.csv"
    os.system(f"opp_scavetool x {raw_data_data_source_file_name_path} -o {output_csv_path}")

    # Filter
    df = pd.read_csv(output_csv_path, dtype=str)
    df1 = df[df["name"].isin(rows_to_keep)]
    df2 = df[df['name'].str.startswith("numDataPacketsReceivedByNodeId", na=False)]
    df = pd.concat([df1, df2])
    
    data_dir_path = os.path.join(DATA_SOURCES_PATH, data_source, constants.DATA_DIR)
    Path(data_dir_path).mkdir(parents=True, exist_ok=True)
    
    data_file_path = os.path.join(data_dir_path, file_name)

    # Save filtered df to data source folder
    df.to_csv(data_file_path, encoding='utf-8', index=False)

    # Clean up tmp converted csvs
    os.remove(output_csv_path)
