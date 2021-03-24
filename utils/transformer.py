from numpy import sqrt, round


# Utilities for typical power system calculations

def short_circuit_impedance_by_voltage(vk_percent: float, vkr_percent: float, net_sn: float, sn: float):
    """
    :param vk_percent: short circuit voltage [%]
    :param vkr_percent: real component of short circuit voltage [%]
    :param net_sn: reference apparent power for per unit system [VA]
    :param sn: rated apparent power of the transformer [VA]
    :return: Transformer short-circuit impedance [Ohm]
    """
    zk = (vk_percent / 100) * (sn / net_sn)
    rk = (vkr_percent / 100) * (net_sn / sn)
    xk = sqrt(zk ** 2 - rk ** 2)
    return rk + xk * 1j


def impedance_pu(z: float, sn_ref: float, vn_ref: float):
    """
    :param z: Impedance [Ohms]
    :param sn_mva_ref: reference apparent power for per unit system [VA]
    :param vn_kv_ref:  reference voltage line-line [V]
    :return: Impedance in p.u
    """
    z_base = vn_ref ** 2 / sn_ref
    return round(z / z_base, 3)


def short_circuit_impedance_by_power(uk: float, vn_kv_ref: float, power: float, sn_mva_ref: float):
    """
    :param uk: Short circuit voltage [%].
    :param vn_kv_ref: reference voltage line-line [V]
    :param power: Short circuit active power [W].
    :param sn_mva_ref: reference apparent power [VA]
    :return:
    """
    rk = power * (vn_kv_ref / sn_mva_ref) ** 2
    xk = sqrt((uk * vn_kv_ref ** 2 / sn_mva_ref) ** 2 - rk ** 2)
    return rk + xk * 1j

# TODO: Add https://github.com/zepben/pp-translator/blob/BasicNetwork/src/pp-translator/conversion/Transformer_to_pp.py