import numpy as np

from utils.transformer import *


def test_impedance_pu():
    z_pu = impedance_pu(z=2.77128, sn_ref=200e6, vn_ref=12e3)
    assert z_pu == 3.84900


def test_short_circuit_impedance():
    pass  # TODO:


def test_short_circuit_impedance_by_power():
    z = np.round(short_circuit_impedance_by_power(uk=0.1185, vn_kv_ref=400e3, power=2020.180e3, sn_mva_ref=1630e6), 3)
    assert z == [0.122 + 1j * 11.631]
