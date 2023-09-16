import NoneAdapter
import ReedSolomonAdapter


def get(channel_code):
    if channel_code == "None":
        return NoneAdapter.NoneAdapter()
    if channel_code == "ReedSolomon":
        return ReedSolomonAdapter.ReedSolomonAdapter()

    raise Exception("Invalid channel code name")
