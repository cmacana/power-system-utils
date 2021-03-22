from numpy import sqrt


# Utilities for typical power system calculations

def short_circuit_impedance(vk_percent: float, vkr_percent: float, net_sn_mva: float, sn_mva: float):
    """
    :param vk_percent: short circuit voltage [%]
    :param vkr_percent: real component of short circuit voltage [%]
    :param net_sn_mva: reference apparent power for per unit system [MVA]
    :param sn_mva: rated apparent power of the transformer [MVA]
    :return: Transformer short-circuit impedance [Ohm]
    """
    zk = (vk_percent / 100) * (sn_mva / net_sn_mva)
    rk = (vkr_percent / 100) * (net_sn_mva / sn_mva)
    xk = sqrt(zk ** 2 - rk ** 2)
    return rk + xk * 1j


def impedance_pu(z: float, net_sn_mva: float, net_vn_kv: float):
    """
    :param z: per-unit Impedance
    :param net_sn_mva:
    :param net_vn_kv:
    :return:
    """
    z_base = net_vn_kv ** 2 / net_sn_mva
    return z / z_base


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(short_circuit_impedance(vk_percent=0.06, vkr_percent=0.01425, net_sn_mva=0.4, sn_mva=0.4))
