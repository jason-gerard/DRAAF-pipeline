import json
import os
import numpy as np
from pathlib import Path
import DRAAF_pipeline.constants as constants
import matplotlib.pyplot as plt


class GraphManager:
    OUTPUT_GRAPH_DIR = "output_graphs"
    
    def __init__(self, workspace_name):
        self.workspace_path = os.path.join(constants.PROJECT_ROOT, constants.WORKSPACES_ROOT, workspace_name)
        with open(os.path.join(self.workspace_path, constants.METRICS_DUMP_NAME), "r") as f:
            self.metric_data = json.load(f)
            
        # Create output graph directory if it doesn't exist
        Path(os.path.join(self.workspace_path, GraphManager.OUTPUT_GRAPH_DIR)).mkdir(parents=True, exist_ok=True)
    
    def save_plot(self, file_name):
        plt.savefig(
            os.path.join(self.workspace_path, GraphManager.OUTPUT_GRAPH_DIR, f"{file_name}.pdf"),
            format="pdf",
            bbox_inches='tight'
        )
        plt.show()


class GenericPlotter:
    
    def __init__(self, graph_manager, data_sources, node_counts):
        self.graph_manager = graph_manager
        self.data_sources = data_sources
        self.node_counts = node_counts
    
    def plot(self, metric_names, label, ylims, is_log=False, show_metric_name=False, legend_pos="lower left"):
        plt.rcParams.update({'font.size': 18})
        plt.rc('legend', fontsize=14)
        plt.rcParams.update({'font.family': 'Times New Roman'})

        fig = plt.figure()
        ax = fig.add_subplot(111)

        for metric_name in metric_names:
            for data_source in self.data_sources:
                x = self.node_counts
                ys = [self.graph_manager.metric_data[data_source][str(node_count)][metric_name] for node_count in x]
                y = [np.average(y) for y in ys]
                y_err = [np.std(y) for y in ys]

                # This avoids issues when the metric falls to 0 for log graphs
                if is_log:
                    y = [y_p for y_p in y if y_p > 0]
                    y_err = y_err[:len(y)]
                    x = x[:len(y)]

                protocol_name = "-".join(data_source.split("-")[:-1])
                key_label = protocol_name if not show_metric_name else f"{metric_name} - {protocol_name}"
                if "Survivability" in key_label:
                    key_label = f"{metric_name.split(' ')[0]} - {protocol_name}"

                plt.errorbar(x, y, yerr=y_err, label=key_label, capsize=4, clip_on=False, linewidth=2.5)

        if "Energy Efficiency" in label:
            y_label = "Energy Efficiency [bytes / joule]"
        else:
            y_label = label
        plt.ylabel(y_label)
        plt.xlabel("Number of nodes")
        if len(metric_names) > 1:
            plt.legend(loc=legend_pos, ncol=2)
        else:
            plt.legend(loc=legend_pos, ncol=1)
        plt.grid(linestyle='-', color='0.95')

        if is_log:
            plt.yscale("log")

        plt.ylim(ylims[0], ylims[1])
        plt.xlim(min(self.node_counts), max(self.node_counts))

        x_ticks = np.append(ax.get_xticks()[1:], min(self.node_counts))  # Remove tick at 0 on x-axis
        x_ticks = np.append(x_ticks, 500)
        ax.set_xticks(x_ticks)

        if not is_log:
            ax.set_yticks(np.arange(ylims[0], ylims[1] + 1, 50))
            if len(ax.get_yticks()) < 5:
                ax.set_yticks(np.arange(ylims[0], ylims[1] + 1, 10))
            if len(ax.get_yticks()) > 12:
                ax.set_yticks(np.arange(ylims[0], ylims[1] + 1, 100))

        file_name = f"{label.replace(' ', '_').replace('/', '_')}"
        self.graph_manager.save_plot(file_name)
