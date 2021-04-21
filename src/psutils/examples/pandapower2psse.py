from grg_pssedata.struct import Case, Bus, Branch, Load, TwoWindingTransformer, TransformerParametersFirstLine, \
    TransformerParametersSecondLineShort, TransformerWinding, TransformerWindingShort

from minimal_example import *
from psutils.calculations.pu import impedance_pu
from psutils.calculations.transformer import short_circuit_impedance_by_voltage


def map_buses(pp_net: pp.pandapowerNet):
    new_buses = []
    print(pp_net.bus)
    for i, row in list(pp_net.bus.iterrows()):
        if i == 0:
            bus_type = 3
        else:
            bus_type = 1
        args = [row['name'], row.vn_kv, bus_type, 1, 1, 1, 1.0, 0.0, 1.1, 0.9, 1.1, 0.9]
        psse_bus = Bus(i + 1, *args)
        new_buses.append(psse_bus)
    return new_buses


def map_loads(pp_net: pp.pandapowerNet):
    new_loads = []
    print(pp_net.load)
    for i, row in list(pp_net.load.iterrows()):
        if row.in_service:
            status = 1
        else:
            status = 0

        psse_element = Load(
            index=i + 1,  # index (int): unique load identifier
            i=row.bus + 1,  # i (int): the identifier of the bus that this load is connected to
            id=row["name"],  # (string): load identifier(not unique)
            status=status,  # (int): load status (in service = 1, out of service = 0)
            area=1,  # (int): area id, 1-9999 (default = the area of the connecting bus)
            zone=1,  # (int): zone id, 1-9999 (default = the zone of the connecting bus)
            pl=row.p_mw,  # (float): active power load (MW) (default = 0.0)
            ql=row.q_mvar,  # (float): reactive power output (MVAr) (default = 0.0)
            ip=0.0,  # (float): real current load (MW per unit voltage) (default = 0.0)
            iq=0.0,  # (float): imaginary current load (MVAr per unit voltage) (default = 0.0)
            yp=0.0,  # (float): real admittance load (MW per unit voltage) (default = 0.0)
            yq=0.0,  # (float): imaginary admittance load (MVAr per unit voltage) (default = 0.0)
            owner=1,  # (int): owner id, 1-9999 (default = the owner of the connecting bus)
            scale=1,  # (int): scaling flag (scalable = 1, fixed = 0) (default = 1)
            intrpt=0  # (int): interruptible flag, (interruptible = 1, non-interruptible = 0) (optional, default = 0)
        )
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


def map_transformers(pp_net: pp.pandapowerNet):
    new_txs = []
    print(pp_net.trafo)
    for i, row in list(pp_net.trafo.iterrows()):
        if row["in_service"]:
            stat = 1
        else:
            stat = 0
            print(row.hv_bus)
        first_line = TransformerParametersFirstLine(
            i=row.hv_bus + 1,
            j=row.lv_bus + 1,  # i (int), j (int): the identifier of the primary bus/ secondary bus
            k=0,  # k (int): the identifier of the tertiary bus (0 if a two winding transformer)
            ckt="",  # ckt (string): circuit identifier
            cw=1,
            cz=1,  # cz (int): winding impedance units (1 = pu on system mva base, 2 = pu on specified mva base, 3 =)
            cm=1,  # cm (int): mag units (1 = pu on system mva, 2 = )
            mag1=0.0,  # mag1 (float): ground conductance on the primary bus
            mag2=0.0,  # (float): ground susceptance on the primary bus
            nmetr=1,  # nmetr (int): the nonmetered end of the transformer the primary,
            # secondary, and tertiary buses are specified by 1,2,3 respectively
            name=row["name"],  # name (string): name of the transformer
            stat=stat,  # stat (int): transformer status
            # (0 = out of service, 1 = in service, 2 = winding 2 out, 3 = winding 3 out, 4 = winding 1 out)
            o1=1, f1=1.0, o2=1, f2=1.0, o3=1, f3=1.0, o4=1, f4=1.0,
            vecgrp=" ")

        z12 = impedance_pu(short_circuit_impedance_by_voltage(
            vk_percent=row.vk_percent,
            vkr_percent=row.vkr_percent,
            net_sn=row.sn_mva,
            sn=row.sn_mva), sn_ref=row.sn_mva, vn_ref=row.vn_hv_kv)

        second_line = TransformerParametersSecondLineShort(r12=z12.real, x12=z12.imag, sbase12=row.sn_mva)
        w1 = TransformerWinding(
            index=1,  # (int): transformer winding identifier (1,2,3)
            windv=1,  # (float): off-nominal turn ratio (p.u.) (default = 1.0)
            nomv=row.hv_bus,  # (float): base voltage (kilo volts)
            ang=0.0,  # (float): angle shift (degrees) TODO: Check this value
            rata=row.sn_mva,  # (float): base rating (MVA)
            ratb=row.sn_mva,  # (float): shorter rating (MVA)
            ratc=row.sn_mva,  # (float): shortest rating (MVA)
            cod=0,  # (int): transformer control mode
            cont=0,  # (int): remote bus index for transformer voltage control ()
            rma=1.1,  # (float): off-nominal turn ratio upper bound
            rmi=0.9,  # (float): off-nominal turn ratio lower bound
            vma=1.1,  # (float): controller band upper limit
            vmi=0.9,  # (float): controller band lower limit
            ntp=33,  # (int): number of tap positions available 2-9999 (default = 33)
            tab=0,  # (int): the identifier of the transformer impedance correction table
            cr=0.0,  # (float): load drop compensation resistance (p.u.)
            cx=0.0,  # (float): load drop compensation reactance (p.u.)
            cnxa=0.0)  # (float): winding connection angle (degrees) (default = 0.0)
        transformer_winding_short_args = [2, 1.0, row.vn_lv_kv]
        w2 = TransformerWindingShort(*transformer_winding_short_args)
        psse_element = TwoWindingTransformer(index=i + 1, p1=first_line, p2=second_line, w1=w1, w2=w2)
        new_txs.append(psse_element)
    return new_txs


def validate_case(case):
    if case.validate() is None:
        print(case.to_psse())
        print("Successful case validation")
    else:
        print("Successful Case validation was not succesful.")


def write_raw_file(case):
    print("Writing .raw file")
    f = open("simple_example.raw", "w")
    f.write(case.to_psse())
    f.close()
    print("Writing file finished.")


def map_network_data(case_name: str = " "):
    net = ThreeBusesFeederPP().pp_network
    buses = map_buses(net)
    loads = map_loads(net)
    fixed_shunts = []
    generators = []
    branches = map_lines(net)
    transformers = map_transformers(net)
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
    record1, record2 = [case_name, ""]
    case_args = [ic, sbase, rev, xfrrat, nxfrat, basefrq, record1, record2,
                 buses, loads, fixed_shunts, generators, branches, transformers, areas,
                 tt_dc_lines, vsc_dc_lines, transformer_corrections, mt_dc_lines,
                 line_groupings, zones, transfers, owners, facts, switched_shunts,
                 gnes, induction_machines]
    return case_args


def main():
    args = map_network_data(case_name="PandaPower Minimal Example")
    case = Case(*args)
    write_raw_file(case)


if __name__ == "__main__":
    main()
