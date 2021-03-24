from grg_pssedata.struct import Case, Bus, Branch, Load

from minimal_example import *
from utils.calculations.pu import impedance_pu


def map_buses(pp_net: pp.pandapowerNet):
    new_buses = []
    print(net.bus)
    for i, row in list(pp_net.bus.iterrows()):
        if i == 0:
            bus_type = 2
        else:
            bus_type = 1
        args = [row['name'], row.vn_kv, bus_type, 1, 1, 1, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9]
        psse_bus = Bus(i + 1, *args)
        new_buses.append(psse_bus)
    return new_buses


def map_loads(pp_net: pp.pandapowerNet):
    new_loads = []
    print(net.load)
    for i, row in list(pp_net.load.iterrows()):
        args = [row.bus + 1, i + 1, 1, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1, 0]
        psse_element = Load(i + 1, *args)
        new_loads.append(psse_element)
    return new_loads


def map_lines(pp_net: pp.pandapowerNet):
    new_lines = []
    print(pp_net.line)
    for i, row in list(pp_net.line.iterrows()):
        psse_element = Branch(i + 1, i=row.from_bus + 1, j=row.to_bus + 1, ckt='',
                              # TODO: Complete computation of  r & x
                              r=impedance_pu(row.length_km * row.r_ohm_per_km, 1, 1),
                              x=impedance_pu(row.length_km * row.x_ohm_per_km, 1, 1),
                              b=0,
                              ratea=0, rateb=0, ratec=0,
                              gi=0, bi=0, gj=0, bj=0,
                              st=1, met=1,
                              len=row.length_km,
                              o1=1, f1=1.0, o2=1, f2=1.0, o3=1, f3=1.0, o4=1, f4=1.0)
        new_lines.append(psse_element)
    return new_lines


net = ThreeBusesFeederPP().pp_network
buses = map_buses(net)
loads = map_loads(net)
fixed_shunts = []
generators = []
branches = map_lines(net)
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

ic, sbase, rev, xfrrat, nxfrat, basefrq = [0, 100.0, 33, 0, 0, 50]
record1, record2 = ['PandaPower Minimal Example', ""]

case = Case(ic, sbase, rev, xfrrat, nxfrat, basefrq, record1, record2,
            buses, loads, fixed_shunts, generators, branches, transformers, areas,
            tt_dc_lines, vsc_dc_lines, transformer_corrections, mt_dc_lines,
            line_groupings, zones, transfers, owners, facts, switched_shunts,
            gnes, induction_machines)

print(case.to_psse())
print(case.validate())
f = open("simple_example.raw", "w")
f.write(case.to_psse())
f.close()
