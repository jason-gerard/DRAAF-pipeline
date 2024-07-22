import constants as constants
from protocol_definitions import ProtocolStrategy


class MetricEngine:
    AVERAGE_DELAY = "Average Delay [seconds]"
    JFI = "Jain Fairness Index"
    THROUGHPUT = "Throughput [kilobytes / hour]"
    OVERHEAD = "Overhead"
    DATA = "Data"
    SATELLITE_ENERGY_EFFICIENCY = "Satellite Energy Efficiency [bytes / joule]"
    AVG_NODE_ENERGY_EFFICIENCY = "Average Energy Efficiency per Node [bytes / joule]"
    NETWORK_ENERGY_EFFICIENCY = "Network Energy Efficiency [bytes / joule]"
    NODE_SURVIVABILITY = "Node Survivability [hours]"
    SATELLITE_SURVIVABILITY = "Satellite Survivability [hours]"
    
    METRICS = [
        AVERAGE_DELAY,
        JFI,
        THROUGHPUT,
        OVERHEAD,
        DATA,
        SATELLITE_ENERGY_EFFICIENCY,
        AVG_NODE_ENERGY_EFFICIENCY,
        NETWORK_ENERGY_EFFICIENCY,
        NODE_SURVIVABILITY,
        SATELLITE_SURVIVABILITY,
    ]

    def __init__(self):
        self.protocol_strategy: ProtocolStrategy = None
        self.df = None

    def set_protocol(self, protocol_strategy):
        self.protocol_strategy = protocol_strategy

    def set_df(self, df):
        self.df = df

    def compute_metric(self, metric):
        match metric:
            case MetricEngine.AVERAGE_DELAY:
                return self.get_avg_delay()
            case MetricEngine.JFI:
                return self.get_jfi()
            case MetricEngine.THROUGHPUT:
                return self.get_throughput_kilobytes_per_hour()
            case MetricEngine.OVERHEAD:
                return self.get_overhead_kilobytes()
            case MetricEngine.DATA:
                return self.get_data_kilobytes()
            case MetricEngine.SATELLITE_ENERGY_EFFICIENCY:
                return self.get_energy_efficiency_satellite()
            case MetricEngine.AVG_NODE_ENERGY_EFFICIENCY:
                return self.get_avg_energy_efficiency_node()
            case MetricEngine.NETWORK_ENERGY_EFFICIENCY:
                return self.get_energy_efficiency_network()
            case MetricEngine.NODE_SURVIVABILITY:
                return self.get_survivability_node()
            case MetricEngine.SATELLITE_SURVIVABILITY:
                return self.get_survivability_sat()

        raise Exception(f"Metric: {metric} not found")

    def get_data_bits(self):
        bits_per_data_packet = int(self.df.loc[self.df['name'] == 'dataPacketLenBits'].value.iloc[0])
        num_data_packets = int(self.df.loc[self.df['name'] == 'numDataPacketsReceived'].value.iloc[0])

        return bits_per_data_packet * num_data_packets

    def get_data_bytes(self):
        return self.get_data_bits() / 8

    def get_data_kilobytes(self):
        return self.get_data_bits() / 8 / 1000

    def get_throughput_kilobytes_per_hour(self):
        # Throughput kB / hr
        sim_time_hours = float(self.df.loc[self.df['name'] == 'simulated time'].value.iloc[0]) / 60 / 60
        data_kilobytes = self.get_data_bits() / 8 / 1000

        return data_kilobytes / sim_time_hours

    def get_jfi(self):
        # Jain's Fairness Index
        num_nodes = int(self.df.loc[self.df['name'] == 'nrOfNodes'].value.iloc[0])
        denominator = num_nodes * self.df[self.df['name'].str.startswith('numDataPacketsReceivedByNodeId', na=False)].value.astype(int).pow(2).sum()
        numerator = self.df[self.df['name'].str.startswith('numDataPacketsReceivedByNodeId', na=False)].value.astype(int).sum() ** 2.0
        jfi = numerator / denominator if denominator != 0 else 0
        return jfi

    def get_overhead_kilobytes(self):
        overhead_bits = self.protocol_strategy.get_overhead_bits(self.df)
        return overhead_bits / 8 / 1000

    def get_avg_delay(self):
        num_data_packets = int(self.df.loc[self.df['name'] == 'numDataPacketsReceived'].value.iloc[0])
        total_delay = float(self.df.loc[self.df['name'] == 'totalPacketDelay'].value.iloc[0])

        return total_delay / num_data_packets if num_data_packets > 0 else 0

    def get_avg_energy_efficiency_node(self):
        energy_consumed = self.protocol_strategy.get_energy_consumed_nodes(self.df)
        num_nodes = int(self.df.loc[self.df['name'] == 'nrOfNodes'].value.iloc[0])

        return (self.get_data_bytes() / num_nodes) / (energy_consumed / num_nodes)

    def get_energy_efficiency_satellite(self):
        energy_consumed = self.protocol_strategy.get_energy_consumed_satellite(self.df)

        return self.get_data_bytes() / energy_consumed

    def get_energy_efficiency_network(self):
        energy_consumed_nodes = self.protocol_strategy.get_energy_consumed_nodes(self.df)
        energy_consumed_satellite = self.protocol_strategy.get_energy_consumed_satellite(self.df)
        energy_consumed = energy_consumed_nodes + energy_consumed_satellite

        return self.get_data_bytes() / energy_consumed

    def get_survivability_sat(self):
        sim_time_seconds = float(self.df.loc[self.df['name'] == 'simulated time'].value.iloc[0])
        energy_consumed = self.protocol_strategy.get_energy_consumed_satellite(self.df)

        P_c_sat = energy_consumed / sim_time_seconds
        L_seconds = constants.E_b_sat / P_c_sat
        return L_seconds / 60 / 60  # hours

    def get_survivability_node(self):
        sim_time_seconds = float(self.df.loc[self.df['name'] == 'simulated time'].value.iloc[0])
        num_nodes = int(self.df.loc[self.df['name'] == 'nrOfNodes'].value.iloc[0])
        energy_consumed = self.protocol_strategy.get_energy_consumed_nodes(self.df)

        P_c_node = energy_consumed / num_nodes / sim_time_seconds  # Watts
        L_seconds = constants.E_b_node / P_c_node
        return L_seconds / 60 / 60  # hours
