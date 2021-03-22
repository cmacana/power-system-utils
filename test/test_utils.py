from utils.transformer_utils import *


def test_impedance_pu():
    z_pu = impedance_pu(z=2.77128, net_sn_mva=200, net_vn_kv=12)
    assert z_pu == 3.84900
