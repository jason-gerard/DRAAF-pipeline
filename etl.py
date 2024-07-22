import pandas as pd
import os
import json

from metric_engine import MetricEngine
from protocol_definitions import ProtocolStrategyFactory
import constants as constants


class ETLPipeline:

    def __init__(self, data_sources, data_source_to_protocol, node_counts, workspace_name):
        self.data_sources = data_sources
        self.data_source_to_protocol = data_source_to_protocol
        self.node_counts = node_counts
        self.workspace_name = workspace_name

        self.dfs = {data_source: {"SCA": {}, "VEC": {}, } for data_source in self.data_sources}
        self.metrics = {data_source: {
            node_count: {
                metric_name: [] for metric_name in MetricEngine.METRICS
            } for node_count in self.node_counts
        } for data_source in self.data_sources}

    def extract(self):
        print("Starting extract phase")

        for data_source in self.data_sources:
            print(f"Processing data source: {data_source}")

            data_source_path = os.path.join(constants.PROJECT_ROOT, constants.DATA_SOURCES_ROOT, data_source, constants.DATA_DIR)
            print(f"Data source path: {data_source_path}")
            sca_files = [f for f in os.listdir(data_source_path) if ".sca" in f]
            vec_files = [f for f in os.listdir(data_source_path) if ".vec" in f]

            file_names = sca_files + vec_files
            for file_name in file_names:
                node_count = int(file_name.split("N=")[1].split("-")[0])
                if node_count not in self.node_counts:
                    continue
                
                df = pd.read_csv(f"{os.path.join(data_source_path, file_name)}", dtype=str)

                file_type = "SCA" if ".sca" in file_name else "VEC"

                try:
                    self.dfs[data_source][file_type][node_count].append(df)
                except KeyError:
                    self.dfs[data_source][file_type][node_count] = [df]

            # Order dataframes for protocol by node count
            self.dfs[data_source]["SCA"] = {node_count: self.dfs[data_source]["SCA"][node_count] for node_count in self.node_counts}
            # self.dfs[protocol]["VEC"] = {node_count: self.dfs[protocol]["VEC"][node_count] for node_count in self.node_counts}
            
        return self

    def transform(self):
        print("Starting transform phase")
        
        metric_engine = MetricEngine()
        
        for data_source in self.dfs:
            print(f"Processing data source: {data_source}")
            protocol_name = self.data_source_to_protocol[data_source]
            protocol_strategy = ProtocolStrategyFactory().get(protocol_name)
            metric_engine.set_protocol(protocol_strategy)
            
            for node_count in self.dfs[data_source]["SCA"]:
                for df in self.dfs[data_source]["SCA"][node_count]:
                    metric_engine.set_df(df)
                    
                    for metric_name in MetricEngine.METRICS:
                        metric_value = metric_engine.compute_metric(metric_name)
                        self.metrics[data_source][node_count][metric_name].append(metric_value)
        
        return self
    
    def load(self):
        print("Starting load phase")

        workspace_path = os.path.join(constants.PROJECT_ROOT, constants.WORKSPACES_ROOT, self.workspace_name, constants.METRICS_DUMP_NAME)
        print(f"Writing data to {workspace_path}")
        
        with open(workspace_path, "w", encoding="utf-8") as f:
            json.dump(self.metrics, f, ensure_ascii=False, indent=4)
        
        return self
