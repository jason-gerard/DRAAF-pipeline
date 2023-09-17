import CodecAdaptorFactory
import LoRa
import network
import random
import metrics
import pprint
import numpy as np

channel_codes = [
    "None",
    "ReedSolomon",
]

num_rounds = 100

results = {channel_code: {
    metric: {
        BER: [] for BER in network.BERs
    } for metric in metrics.metrics_list
} for channel_code in channel_codes}

for channel_code in channel_codes:
    for BER in network.BERs:
        random.seed(42)
        np.random.seed(42)

        channel = network.Channel(BER)

        codec = CodecAdaptorFactory.get(channel_code)

        data_packets_sent = 0
        data_packets_received = 0
        data_packets_error = 0

        # Compute encoded data packet length
        frame = channel.frame_factory(LoRa.data_packet_length_bits)
        encoded_frame = codec.encode(frame)
        encoded_data_packet_length_bits = len(encoded_frame)

        for _ in range(num_rounds):
            data_packets_sent += 1

            node_frame = channel.frame_factory(LoRa.data_packet_length_bits)
            node_encoded_frame = codec.encode(node_frame)

            satellite_encoded_frame = channel.broadcast_frame(node_encoded_frame)
            satellite_frame = codec.decode(satellite_encoded_frame)

            if node_encoded_frame != satellite_encoded_frame:
                data_packets_error += 1

            if node_frame == satellite_frame:
                data_packets_received += 1

        satellite_altitude = 600.0 * 1000  # meters
        propagation_speed = 299792458.0  # speed of light m/s
        propagation_delay = satellite_altitude / propagation_speed

        propagation_delay_guard = 0.005

        SF = 10
        BW = 125000
        CR = 1
        # Important to use the encoded packet length here
        data_transmission_delay = LoRa.compute_time_on_air(encoded_data_packet_length_bits, SF, BW, CR)

        data_time_slot = data_transmission_delay + propagation_delay + propagation_delay_guard
        round_duration = data_time_slot
        simulation_duration = round_duration * num_rounds

        print(f"Channel Code: {channel_code}")

        print(f"Duration of a round: {round_duration} seconds")
        print(f"Duration of simulation: {simulation_duration} seconds")

        print(f"Number packet sent: {data_packets_sent}")
        print(f"Number packet received: {data_packets_received}")

        print(f"BER: {BER}")
        packet_error_rate = data_packets_error / data_packets_sent
        print(f"PER before correction: {packet_error_rate}")
        packet_error_rate = 1 - (data_packets_received / data_packets_sent)
        print(f"PER after correction: {packet_error_rate}")

        print(f"Number of packet errors: {data_packets_error}")
        print(f"Percent of successful transmission: {(1 - packet_error_rate) * 100}%")

        # Throughput
        throughput_b_s = data_packets_received * LoRa.data_packet_length_bits / simulation_duration
        print(f"Throughput: {throughput_b_s} bits / second")
        throughput_k_h = (data_packets_received * (LoRa.data_packet_length_bits / 8 / 1000)) / (simulation_duration / 60 / 60)
        print(f"Throughput: {throughput_k_h} kilobytes / hour")

        # Data and Overhead
        data_bytes = data_packets_received * LoRa.data_packet_length_bits / 8
        print(f"Data: {data_bytes} bytes")
        overhead_bytes = (data_packets_sent * (encoded_data_packet_length_bits - LoRa.data_packet_length_bits)) / 8
        print(f"Overhead: {overhead_bytes} bytes")

        # Energy consumption
        p_rx = 25.74 / 1000  # W
        p_tx = 389.4 / 1000  # W
        e_data = p_rx * data_time_slot + p_tx * data_time_slot
        ec_data = e_data * data_packets_sent
        print(f"Energy consumption: {ec_data} joules")

        # Energy efficiency
        ee_data = data_bytes / ec_data
        print(f"Energy efficiency: {ee_data} bytes / joule")

        print("\n\n\n")

        results[channel_code][metrics.THROUGHPUT][BER].append(throughput_k_h)
        results[channel_code][metrics.DATA][BER].append(data_bytes)
        results[channel_code][metrics.OVERHEAD][BER].append(overhead_bytes)
        results[channel_code][metrics.ENERGY_CONSUMPTION][BER].append(ec_data)
        results[channel_code][metrics.ENERGY_EFFICIENCY][BER].append(ee_data)


pprint.pprint(results)