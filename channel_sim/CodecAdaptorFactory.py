import NoneAdapter
import ReedSolomonAdapter
import BCHAdapter
import LDPCAdapter


def get(channel_code):
    if channel_code == "None":
        return NoneAdapter.NoneAdapter()
    if channel_code == "ReedSolomon":
        return ReedSolomonAdapter.ReedSolomonAdapter()
    if channel_code == "BCH":
        return BCHAdapter.BCHAdapter()
    if channel_code == "LDPC":
        return LDPCAdapter.LDPCAdapter()

    raise Exception("Invalid channel code name")
