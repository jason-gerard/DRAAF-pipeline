import math


def compute_time_on_air(packet_len_bits: int, SF: int, BW: int, CR: int) -> float:
    nPreamble = 8
    payloadBytes = float(packet_len_bits) / 8.0

    payloadSymbNb = 8
    payloadSymbNb += math.ceil((8 * payloadBytes - 4 * SF + 28 + 16 - 20 * 0) / (4 * (SF - 2 * 0))) * (CR + 4)
    payloadSymbNb = max(payloadSymbNb, 8)

    Tsym = pow(2, SF) / BW
    Tpreamble = (nPreamble + 4.25) * Tsym
    Theader = 0.5 * (8 + payloadSymbNb) * Tsym
    Tpayload = 0.5 * (8 + payloadSymbNb) * Tsym

    return Tpreamble + Theader + Tpayload
