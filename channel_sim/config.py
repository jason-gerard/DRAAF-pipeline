# General
num_rounds = 500
num_repetitions = 1  # 21 for statistical significance


# GE Error Model
# Tuples of (good, bad), BER in bad state is higher, closer to 0 than in the good state
BERs = [
    (1 * 10 ** -0, 1 * 10 ** -0),  # 1 i.e. every bit is an error
    (1 * 10 ** -1, 2 * 10 ** -1),  # 0.1 10% of bits are errors
    (1 * 10 ** -2, 1 * 10 ** -1),
    (1 * 10 ** -3, 1 * 10 ** -2),
    (2 * 10 ** -4, 2 * 10 ** -3),
    (1 * 10 ** -4, 1 * 10 ** -3),
    (1 * 10 ** -6, 1 * 10 ** -7),
    (1 * 10 ** -9, 1 * 10 ** -8),
    (0, 0)  # No errors
]

SNRs = [
    35,
    30,
    25,
    22,
    22,
    22,
    20,
    15,
    10,
]

# Channel codes
channel_codes = [
    "None",
    "ReedSolomon",
    "BCH",
    "LDPC",
]

# Reed-Solomon Coding
rs_config = {
    "num_ecc": 10,
}

# BCH Coding
bch_config = {
    "num_ecc": 16,
    "m": 13,
}

# LDPC
ldpc_config = {
    "n": 80,
    "d_v": 16,
    "d_c": 40,
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
