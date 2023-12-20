# General
num_rounds = 10000
num_repetitions = 5  # 21 for statistical significance


BERs = []
channel_codes = []
ber_table = {}
with open("./ber_table.csv", "r") as f:
    lines = f.readlines()
    for ber in lines[0].split(",")[1:]:
        BERs.append(float(ber))

    for line in lines[1:]:
        parts = line.split(",")
        corrected_bers = [float(ber) for ber in parts[1:]]
        codec = parts[0]

        ber_table[codec] = {}
        for index, corrected_ber in enumerate(corrected_bers):
            ber_table[codec][BERs[index]] = corrected_ber
        channel_codes.append(codec)

codec_params = {
    "UNCODED": {
        "N": 64,
        "K": 64,
    },
    "REP": {
        "N": 192,
        "K": 64,
    },
    "BCH": {
        "N": 31,
        "K": 21,
        "T": 2,
    },
    "RS": {
        "N": 15,
        "K": 11,
    },
    "TURBO": {
        "N": 204,
        "K": 64,
        "N_trellis": 2,
        "N_turbo": 6,
    },
    "LDPC": {
        "N": 128,
        "K": 64,
        "N_ldpc": 5,
        "w_r": 5,
        "w_c": 1,
    }
}


# LoRa
SF = 10
BW = 125000
CR = 1

data_packet_length_bits = 504

satellite_altitude = 600.0 * 1000  # meters
propagation_speed = 299792458.0  # speed of light m/s
propagation_delay = satellite_altitude / propagation_speed

propagation_delay_guard = 0.005

# Physical Hardware
p_rx = 25.74 / 1000  # W
p_tx = 389.4 / 1000  # W
e_cycle_node = 0.0000082  # J
e_cycle_sat = 0.0000082  # J
