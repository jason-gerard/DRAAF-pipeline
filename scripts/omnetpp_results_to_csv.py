import os

input_dir = "raw_data"
output_dir = "data"

sca_files = [f for f in os.listdir(input_dir) if f.endswith(".sca")]

for file_name in sca_files:
    print(file_name)
    os.system(f"opp_scavetool x {os.path.join(input_dir, file_name)} -o {os.path.join(output_dir, file_name)}.csv")
