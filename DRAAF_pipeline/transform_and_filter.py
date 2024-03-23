import os
import pprint
import pandas as pd

input_dir = "/home/jason/Code/research-paper-analysis/scripts/msdq_sensitivity_analysis_new"

sca_files = [f for f in os.listdir(input_dir) if f.endswith(".sca")]
sca_files.sort()

data_sources = set([",".join(f.split(",")[:-1]) for f in sca_files])
pprint.pprint(data_sources)
