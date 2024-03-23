from abc import ABC, abstractmethod
import DRAAF_pipeline.constants as constants


class ProtocolStrategy(ABC):

    @abstractmethod
    def get_energy_consumed_satellite(self, df):
        pass

    @abstractmethod
    def get_energy_consumed_nodes(self, df):
        pass

    @abstractmethod
    def get_overhead_bits(self, df):
        pass


class ProtocolMSDQ(ProtocolStrategy):

    def get_energy_consumed_satellite(self, df):
        num_rounds = int(df.loc[df['name'] == "numFBPPacketsSent"].value.iloc[0])

        # Sat always sends a FBP
        t_fbp = float(df.loc[df['name'] == "fbpPacketTime"].value.iloc[0])
        e_fbp = num_rounds * constants.p_tx * t_fbp

        # Sat always listens for all contention slots
        t_ars = float(df.loc[df['name'] == "arsPacketTime"].value.iloc[0])
        n_slots = int(df.loc[df['name'] == "numContentionSlots"].value.iloc[0])
        e_ars = num_rounds * constants.p_rx * t_ars * n_slots

        # Sat only listens when a data packet will be sent len(dtq) != 0
        t_data = float(df.loc[df['name'] == "dataPacketTime"].value.iloc[0])
        num_data_packets = float(df.loc[df['name'] == "numDataPacketsReceived"].value.iloc[0])
        e_data = num_data_packets * constants.p_rx * t_data

        return e_fbp + e_ars + e_data

    def get_energy_consumed_nodes(self, df):
        num_rounds = int(df.loc[df['name'] == "numFBPPacketsSent"].value.iloc[0])
        num_nodes = int(df.loc[df['name'] == 'nrOfNodes'].value.iloc[0])

        # Nodes always listen for FBP
        t_fbp = float(df.loc[df['name'] == "fbpPacketTime"].value.iloc[0])
        e_fbp = num_nodes * num_rounds * constants.p_rx * t_fbp

        # Nodes only send ARS when the constraints are met
        t_ars = float(df.loc[df['name'] == "arsPacketTime"].value.iloc[0])
        total_num_ars_packets_sent = df.loc[df['name'] == "numARSPacketsSent"].value.astype(int).sum()
        e_ars = total_num_ars_packets_sent * constants.p_tx * t_ars

        # Only one or zero data packets can be sent each round
        t_data = float(df.loc[df['name'] == "dataPacketTime"].value.iloc[0])
        num_data_packets = float(df.loc[df['name'] == "numDataPacketsReceived"].value.iloc[0])
        e_data = num_data_packets * constants.p_tx * t_data

        return e_fbp + e_ars + e_data

    def get_overhead_bits(self, df):
        keys = [
            ('numARSPacketsSent', 'arsPacketLenBits'),
            ('numFBPPacketsSent', 'fbpPacketLenBits'),
        ]

        overhead_bits = 0
        for key in keys:
            total_num_packets = df.loc[df['name'] == key[0]].value.astype(int).sum()
            bits_per_packet = int(df.loc[df['name'] == key[1]].value.iloc[0])
            overhead_bits += (total_num_packets * bits_per_packet)

        return overhead_bits


class ProtocolDQ(ProtocolStrategy):

    def get_energy_consumed_satellite(self, df):
        num_rounds = int(df.loc[df['name'] == "numFBPPacketsSent"].value.iloc[0])

        # Sat always sends a FBP
        t_fbp = float(df.loc[df['name'] == "fbpPacketTime"].value.iloc[0])
        e_fbp = num_rounds * constants.p_tx * t_fbp

        # Sat always listens for all contention slots
        t_ars = float(df.loc[df['name'] == "arsPacketTime"].value.iloc[0])
        n_slots = int(df.loc[df['name'] == "numContentionSlots"].value.iloc[0])
        e_ars = num_rounds * constants.p_rx * t_ars * n_slots

        # Sat only listens when a data packet will be sent len(dtq) != 0
        t_data = float(df.loc[df['name'] == "dataPacketTime"].value.iloc[0])
        num_data_packets = float(df.loc[df['name'] == "numDataPacketsReceived"].value.iloc[0])
        e_data = num_data_packets * constants.p_rx * t_data

        return e_fbp + e_ars + e_data

    def get_energy_consumed_nodes(self, df):
        num_rounds = int(df.loc[df['name'] == "numFBPPacketsSent"].value.iloc[0])
        num_nodes = int(df.loc[df['name'] == 'nrOfNodes'].value.iloc[0])

        # Nodes always listen for FBP
        t_fbp = float(df.loc[df['name'] == "fbpPacketTime"].value.iloc[0])
        e_fbp = num_nodes * num_rounds * constants.p_rx * t_fbp

        # Nodes only send ARS when the constraints are met
        t_ars = float(df.loc[df['name'] == "arsPacketTime"].value.iloc[0])
        total_num_ars_packets_sent = df.loc[df['name'] == "numARSPacketsSent"].value.astype(int).sum()
        e_ars = total_num_ars_packets_sent * constants.p_tx * t_ars

        # Only one or zero data packets can be sent each round
        t_data = float(df.loc[df['name'] == "dataPacketTime"].value.iloc[0])
        num_data_packets = float(df.loc[df['name'] == "numDataPacketsReceived"].value.iloc[0])
        e_data = num_data_packets * constants.p_tx * t_data

        return e_fbp + e_ars + e_data

    def get_overhead_bits(self, df):
        keys = [
            ('numARSPacketsSent', 'arsPacketLenBits'),
            ('numFBPPacketsSent', 'fbpPacketLenBits'),
        ]

        overhead_bits = 0
        for key in keys:
            total_num_packets = df.loc[df['name'] == key[0]].value.astype(int).sum()
            bits_per_packet = int(df.loc[df['name'] == key[1]].value.iloc[0])
            overhead_bits += (total_num_packets * bits_per_packet)

        return overhead_bits


class ProtocolRESSIoT(ProtocolStrategy):

    def get_energy_consumed_satellite(self, df):
        num_rounds = int(df.loc[df['name'] == "numBeaconPacketsSent"].value.iloc[0])

        t_beacon = float(df.loc[df['name'] == "beaconPacketTime"].value.iloc[0])
        w_rx = float(df.loc[df['name'] == "wrx"].value.iloc[0])
        e_rp_sat = num_rounds * ((constants.p_tx * t_beacon) + (constants.p_rx * w_rx))

        t_vcts = float(df.loc[df['name'] == "vctsPacketTime"].value.iloc[0])
        t_data = float(df.loc[df['name'] == "dataPacketTime"].value.iloc[0])
        num_data_packets = float(df.loc[df['name'] == "numDataPacketsReceived"].value.iloc[0])
        e_tp_sat = (num_rounds * constants.p_tx * t_vcts) + (num_data_packets * constants.p_rx * t_data)

        return e_rp_sat + e_tp_sat

    def get_energy_consumed_nodes(self, df):
        num_rounds = int(df.loc[df['name'] == "numBeaconPacketsSent"].value.iloc[0])
        num_nodes = int(df.loc[df['name'] == 'nrOfNodes'].value.iloc[0])

        t_beacon = float(df.loc[df['name'] == "beaconPacketTime"].value.iloc[0])
        t_rts = float(df.loc[df['name'] == "rtsPacketTime"].value.iloc[0])
        total_num_rts_packets_sent = df.loc[df['name'] == "numRTSPacketsSent"].value.astype(int).sum()
        e_rp_nodes = ((num_nodes * num_rounds * constants.p_rx * t_beacon)
                      + (total_num_rts_packets_sent * constants.p_tx * t_rts))

        t_vcts = float(df.loc[df['name'] == "vctsPacketTime"].value.iloc[0])
        t_data = float(df.loc[df['name'] == "dataPacketTime"].value.iloc[0])
        num_data_packets = float(df.loc[df['name'] == "numDataPacketsReceived"].value.iloc[0])
        e_tp_nodes = (num_rounds * num_nodes * constants.p_rx * t_vcts) + (num_data_packets * constants.p_tx * t_data)

        return e_rp_nodes + e_tp_nodes

    def get_overhead_bits(self, df):
        keys = [
            ('numRTSPacketsSent', 'rtsPacketLenBits'),
            ('numBeaconPacketsSent', 'beaconPacketLenBits'),
            ('numVCTSPacketsSent', 'vctsPacketLenBits'),
        ]

        overhead_bits = 0
        for key in keys:
            total_num_packets = df.loc[df['name'] == key[0]].value.astype(int).sum()
            bits_per_packet = int(df.loc[df['name'] == key[1]].value.iloc[0])
            overhead_bits += (total_num_packets * bits_per_packet)

        return overhead_bits


class ProtocolLoRaWAN(ProtocolStrategy):

    def get_energy_consumed_satellite(self, df):
        sim_time_seconds = float(df.loc[df['name'] == 'simulated time'].value.iloc[0])
        # t_ack = float(df.loc[df['name'] == "ackPacketTime"].value.iloc[0])
        # num acks is the same as num data packets received
        # num_acks = int(df.loc[df['name'] == 'numDataPacketsReceived'].value.iloc[0])
        # t_listening = sim_time_seconds - (t_ack * num_acks)
        # num_data_packets_received = int(df.loc[df['name'] == 'numDataPacketsReceived'].value.iloc[0])

        # return (p_rx * t_listening) + (p_tx * t_ack * num_data_packets_received) # Confirmed energy model
        return constants.p_rx * sim_time_seconds  # unconfirmed energy model

    def get_energy_consumed_nodes(self, df):
        # t_ack = float(df.loc[df['name'] == "ackPacketTime"].value.iloc[0])
        # num_data_packets_received = int(df.loc[df['name'] == 'numDataPacketsReceived'].value.iloc[0])
        t_data = float(df.loc[df['name'] == "dataPacketTime"].value.iloc[0])
        num_data_packets_sent = df.loc[df['name'] == 'numDataPacketsSent'].value.astype(int).sum()

        # return (p_rx * t_ack * num_data_packets_received) + (p_tx * t_data * num_data_packets_sent) # Confirmed energy model
        return constants.p_tx * t_data * num_data_packets_sent  # unconfirmed energy model

    def get_overhead_bits(self, df):
        return 0


class ProtocolStrategyFactory:

    @staticmethod
    def get(protocol_name):
        match protocol_name:
            case "RESS-IoT":
                return ProtocolRESSIoT()
            case "DQ":
                return ProtocolDQ()
            case "MSDQ":
                return ProtocolMSDQ()
            case "LoRaWAN":
                return ProtocolLoRaWAN()

        raise Exception("No protocol found")
