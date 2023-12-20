import math
import config

THROUGHPUT = "Throughput"
DATA = "Data"
OVERHEAD = "Overhead"
ENERGY_CONSUMPTION_NODE = "Energy Consumption Node"
ENERGY_EFFICIENCY_NODE = "Energy Efficiency Node"
ENERGY_CONSUMPTION_SATELLITE = "Energy Consumption Satellite"
ENERGY_EFFICIENCY_SATELLITE = "Energy Efficiency Satellite"

metrics_list = [
    THROUGHPUT,
    DATA,
    OVERHEAD,
    ENERGY_CONSUMPTION_NODE,
    ENERGY_EFFICIENCY_NODE,
    ENERGY_CONSUMPTION_SATELLITE,
    ENERGY_EFFICIENCY_SATELLITE,
]


def ec_uncoded():
    e_encoding = 0
    e_decoding = 0

    return e_encoding, e_decoding


def ec_rep():
    n = config.codec_params["REP"]["N"]
    k = config.codec_params["REP"]["K"]
    M = math.ceil(config.data_packet_length_bits / k)

    iter_encoding = M * n
    iter_decoding = M * n

    e_encoding = iter_encoding * config.e_cycle_node
    e_decoding = iter_decoding * config.e_cycle_sat

    return e_encoding, e_decoding


def ec_bch():
    n = config.codec_params["BCH"]["N"]
    k = config.codec_params["BCH"]["K"]
    M = math.ceil(config.data_packet_length_bits / k)
    t = config.codec_params["BCH"]["T"]
    d_min = 2 * t + 1

    iter_encoding = M * k * (n - k)
    iter_decoding = M * n * d_min

    e_encoding = iter_encoding * config.e_cycle_node
    e_decoding = iter_decoding * config.e_cycle_sat

    return e_encoding, e_decoding


def ec_rs():
    n = config.codec_params["RS"]["N"]
    k = config.codec_params["RS"]["K"]
    M = math.ceil(config.data_packet_length_bits / k)

    iter_encoding = M * k * (n - k)
    iter_decoding = M * n * (n - k)

    e_encoding = iter_encoding * config.e_cycle_node
    e_decoding = iter_decoding * config.e_cycle_sat

    return e_encoding, e_decoding


def ec_turbo():
    n = config.codec_params["TURBO"]["N"]
    k = config.codec_params["TURBO"]["K"]
    M = math.ceil(config.data_packet_length_bits / k)
    N_trellis = config.codec_params["TURBO"]["N_trellis"]
    N_turbo = config.codec_params["TURBO"]["N_turbo"]

    iter_encoding = M * n
    iter_decoding = M * N_turbo * k * N_trellis

    e_encoding = iter_encoding * config.e_cycle_node
    e_decoding = iter_decoding * config.e_cycle_sat

    return e_encoding, e_decoding


def ec_ldpc():
    n = config.codec_params["LDPC"]["N"]
    k = config.codec_params["LDPC"]["K"]
    M = math.ceil(config.data_packet_length_bits / k)
    N_ldpc = config.codec_params["LDPC"]["N_ldpc"]
    w_r = config.codec_params["LDPC"]["w_r"]
    w_c = config.codec_params["LDPC"]["w_c"]

    iter_encoding = M * n * k
    iter_decoding = M * N_ldpc * n * w_c * w_r

    e_encoding = iter_encoding * config.e_cycle_node
    e_decoding = iter_decoding * config.e_cycle_sat

    return e_encoding, e_decoding
