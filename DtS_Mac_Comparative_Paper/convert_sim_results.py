import os

results_path = "/home/jason/Applications/omnetpp-6.0.1/samples/florasat/simulations/dtsiot/results/results"
sca_files = [f for f in os.listdir(results_path) if f.endswith(".sca")]
vec_files = [f for f in os.listdir(results_path) if f.endswith(".vec")]

data_dir = "sensitivity_data"

for file_name in sca_files + vec_files:
    print(file_name)
    os.system(f"opp_scavetool x {os.path.join(results_path, file_name)} -o {os.path.join(data_dir, file_name)}.csv")
