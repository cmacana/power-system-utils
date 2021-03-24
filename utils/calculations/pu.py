def impedance_pu(z: float, sn_ref: float, vn_ref: float):
    """
    :param z: Impedance [Ohms]
    :param sn_mva_ref: reference apparent power for per unit system [VA]
    :param vn_kv_ref:  reference voltage line-line [V]
    :return: Impedance in p.u
    """
    z_base = vn_ref ** 2 / sn_ref
    return round(z / z_base, 3)
