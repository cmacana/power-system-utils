from utils.calculations.transformer import *
from utils.calculations.pu import *

z = short_circuit_impedance_by_voltage(vk_percent=6, vkr_percent=1.1425, net_sn=400e3, sn=400e3)
print(impedance_pu(z, sn_ref=400e3, vn_ref=400))

