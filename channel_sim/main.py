import math
import LoRa
from channel import Channel
import config
import random
import metrics
import pprint
import numpy as np
import pickle
import os


results = {channel_code: {
    metric: {
        ber: [] for ber in config.BERs
    } for metric in metrics.metrics_list
} for channel_code in config.channel_codes}

for channel_code in config.channel_codes:
    for index, ber in enumerate(config.BERs):
        for repetition in range(config.num_repetitions):
            seed = 42 + repetition
            random.seed(seed)
            np.random.seed(seed)

            corrected_ber = config.ber_table[channel_code][ber]
            channel = Channel(corrected_ber)

            data_packets_sent = 0
            data_packets_received = 0
            data_packets_error = 0

            # Compute encoded data packet length
            M = math.ceil(config.data_packet_length_bits / config.codec_params[channel_code]["K"])
            encoded_data_packet_length_bits = M * config.codec_params[channel_code]["N"]

            for _ in range(config.num_rounds):
                data_packets_sent += 1

                frame = channel.frame_factory(encoded_data_packet_length_bits)

                is_error = channel.broadcast_frame(frame)
                if is_error:
                    data_packets_error += 1
                else:
                    data_packets_received += 1

            # Important to use the encoded packet length here
            data_transmission_delay = LoRa.compute_time_on_air(encoded_data_packet_length_bits, config.SF, config.BW, config.CR)

            data_time_slot = data_transmission_delay + config.propagation_delay + config.propagation_delay_guard
            round_duration = data_time_slot
            simulation_duration = round_duration * config.num_rounds

            print(f"Channel Code: {channel_code}")

            print(f"Duration of a round: {round_duration} seconds")
            print(f"Duration of simulation: {simulation_duration} seconds")

            print(f"Number packet sent: {data_packets_sent}")
            print(f"Number packet received: {data_packets_received}")

            print(f"BER: {ber}")
            packet_error_rate = data_packets_error / data_packets_sent
            print(f"PER before correction: {packet_error_rate}")
            packet_error_rate = 1 - (data_packets_received / data_packets_sent)
            print(f"PER after correction: {packet_error_rate}")

            print(f"Number of packet errors: {data_packets_error}")
            print(f"Percent of successful transmission: {(1 - packet_error_rate) * 100}%")

            # Throughput
            throughput_b_s = data_packets_received * config.data_packet_length_bits / simulation_duration
            print(f"Throughput: {throughput_b_s} bits / second")
            throughput_k_h = (data_packets_received * (config.data_packet_length_bits / 8 / 1000)) / (simulation_duration / 60 / 60)
            print(f"Throughput: {throughput_k_h} kilobytes / hour")

            # Data and Overhead
            data_bytes = data_packets_received * config.data_packet_length_bits / 8
            print(f"Data: {data_bytes} bytes")
            overhead_bytes = (data_packets_sent * (encoded_data_packet_length_bits - config.data_packet_length_bits)) / 8
            print(f"Overhead: {overhead_bytes} bytes")

            # Energy consumption
            if channel_code == "UNCODED":
                e_encoding, e_decoding = metrics.ec_uncoded()
            elif channel_code == "REP":
                e_encoding, e_decoding = metrics.ec_rep()
            elif channel_code == "BCH":
                e_encoding, e_decoding = metrics.ec_bch()
            elif channel_code == "RS":
                e_encoding, e_decoding = metrics.ec_rs()
            elif channel_code == "TURBO":
                e_encoding, e_decoding = metrics.ec_turbo()
            elif channel_code == "LDPC":
                e_encoding, e_decoding = metrics.ec_ldpc()

            # Node, tx + encoding
            e_tx = config.p_tx * data_time_slot
            e_node_r = e_tx + e_encoding
            e_node = e_node_r * data_packets_sent

            # Satellite, rx + decoding
            e_rx = config.p_rx * data_time_slot
            e_satellite_r = e_rx + e_decoding
            e_satellite = e_satellite_r * data_packets_sent

            print(f"Energy consumption node: {e_node} joules")
            print(f"Energy consumption satellite: {e_satellite} joules")

            # Energy efficiency
            ee_node = data_bytes / e_node
            ee_satellite = data_bytes / e_satellite
            print(f"Energy efficiency node: {ee_node} bytes / joule")
            print(f"Energy efficiency satellite: {ee_satellite} bytes / joule")

            print("\n\n\n")

            results[channel_code][metrics.THROUGHPUT][ber].append(throughput_k_h)
            results[channel_code][metrics.DATA][ber].append(data_bytes)
            results[channel_code][metrics.OVERHEAD][ber].append(overhead_bytes)
            results[channel_code][metrics.ENERGY_CONSUMPTION_NODE][ber].append(e_node)
            results[channel_code][metrics.ENERGY_EFFICIENCY_NODE][ber].append(ee_node)
            results[channel_code][metrics.ENERGY_CONSUMPTION_SATELLITE][ber].append(e_satellite)
            results[channel_code][metrics.ENERGY_EFFICIENCY_SATELLITE][ber].append(ee_satellite)


pprint.pprint(results)

with open(os.path.join("sim_results", "results.pkl"), "wb") as f:
    pickle.dump(results, f)
