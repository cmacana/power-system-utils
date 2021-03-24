import grg_pssedata.struct as grg

from minimal_example import *

net = ThreeBusesFeederPP()
print(net.get_load_flow_results())
pp_network: pp.pandapowerNet = net.pp_network
# print(list(pp_network.bus.iterrows()))
print(pp_network.bus)

buses = []
loads = []
fixed_shunts = []
generators = []
branches = []
transformers = []
areas = []
tt_dc_lines = []
vsc_dc_lines = []
transformer_corrections = []
mt_dc_lines = []
line_groupings = []
zones = []
transfers = []
owners = []
facts = []
switched_shunts = []
gnes = []
induction_machines = []

for i, row in list(pp_network.bus.iterrows()):
    if i == 0:
        bus_type = 2
    else:
        bus_type = 1
    args = [row['name'], row.vn_kv, bus_type, 1, 1, 1, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9]
    psse_bus = grg.Bus(i+1, *args)
    buses.append(psse_bus)

ic, sbase, rev, xfrrat, nxfrat, basefrq = [0, 100.0, 33, 0, 0, 50]
record1, record2 = ['PandaPower Mimimal Example', ""]
case_defaults = [[] for _ in range(18)]

case = grg.Case(ic, sbase, rev, xfrrat, nxfrat, basefrq, record1, record2,
                buses, *case_defaults)

print(case.to_psse())
print(case.validate())
f = open("simple_example.raw", "w")
f.write(case.to_psse())
f.close()
