from dataclasses import dataclass

from numpy import sqrt
from zepben.evolve import PowerTransformerEnd, TransformerStarImpedance, ShortCircuitTest, OpenCircuitTest, NoLoadTest

__all__ = ["TransformerStarImpedance", "ShortCircuitTest", "OpenCircuitTest", "NoLoadTest",
           "transformer_test_to_rx"]

"""Script to compute cim: TransformerStarImpedance from cim: TransformerTests"""


def transformer_test_to_rx(pte: PowerTransformerEnd, sc_test: ShortCircuitTest):
    r, x, r0, x0 = 0, 0, 0, 0
    if sc_test.power:
        r = sc_test.power * (pte.rated_u / pte.rated_s) ** 2
    elif sc_test.voltage_ohmic_part:
        r = (pte.rated_u ** 2 * sc_test.voltage_ohmic_part / (pte.rated_s * 100))
    else:
        raise Exception('r ShortCircuitTest.power or ShortCircuitTest.voltage_ohmic_part required')

    if sc_test.power:
        x = sqrt(((sc_test.voltage / 100) * pte.rated_u ** 2 / pte.rated_s) ** 2 - r ** 2)
    elif sc_test.voltage_ohmic_part:
        x = pte.rated_u ** 2 * (sqrt(sc_test.voltage ** 2 - sc_test.voltage_ohmic_part ** 2) / (pte.rated_s * 100))
    else:
        raise Exception('r ShortCircuitTest.power or ShortCircuitTest.voltage_ohmic_part required')
    return TransformerStarImpedance(r=r, r0=r0, x=x, x0=x0)


@dataclass
class StdThreeWindingTransformer:
    un1: float = 7.0
    un2: float = 8.0
    un3: float = 9.0
    sn12: float = 10.0
    sn23: float = 11.0
    sn31: float = 12.0
    uk12: float = 28.0
    uk23: float = 29.0
    uk31: float = 30.0
    ur12: float = 25.0
    ur23: float = 26.0
    ur31: float = 27.0
    flagZ0Input: int = 2
    z0z1_12 = 37
    z0z1_23 = 38
    z0z1_31 = 39
    r0X0_12: float = 40
    r0X0_23: float = 41
    r0X0_31: float = 42
    r0_12: float = 43
    r0_23: float = 44
    r0_31: float = 45
    x0_12: float = 46
    x0_23: float = 47
    x0_31: float = 48
    x0X1_12: float = 49
    x0X1_23: float = 50
    x0X1_31: float = 51
    r0R1_12: float = 52
    r0R1_23: float = 53
    r0R1_31: float = 54


@dataclass
class StdTwoWindingTransformer(object):
    element_id = 1
    un1: float = 2.0
    un2: float = 3.0
    sn: float = 4.0
    sMax: float = 5.0
    uk: float = 7.0
    ur: float = 6.0
    flagZ0Input: int = 1
    z0z1 = 18.0
    r0X0: float = 19.0
    r0R1: float = 20.0
    x0X1: float = 21.0
    r0: float = 22.0
    x0: float = 23.0


def sincal_3wt_to_cim_sct(ur: float, uk: float):
    sct: ShortCircuitTest = ShortCircuitTest()
    sct.voltage_ohmic_part = ur
    sct.voltage = uk
    return sct


def sincal_3wt_to_cim_tsi(twt: StdThreeWindingTransformer):
    pte1 = PowerTransformerEnd()
    pte1.rated_s = twt.sn12
    pte1.rated_u = twt.un1
    sct1 = ShortCircuitTest(voltage=twt.uk12, voltage_ohmic_part=twt.ur12)
    pte2 = PowerTransformerEnd()
    pte2.rated_s = twt.sn23
    pte2.rated_u = twt.un2
    pte3 = PowerTransformerEnd()
    sct2 = ShortCircuitTest(voltage=twt.uk23, voltage_ohmic_part=twt.ur23)
    pte3.rated_s = twt.sn31
    pte3.rated_u = twt.un3
    sct3 = ShortCircuitTest(voltage=twt.uk31, voltage_ohmic_part=twt.ur31)
    tsi1: TransformerStarImpedance = transformer_test_to_rx(pte=pte1, sc_test=sct1)
    tsi2: TransformerStarImpedance = transformer_test_to_rx(pte=pte2, sc_test=sct2)
    tsi3: TransformerStarImpedance = transformer_test_to_rx(pte=pte3, sc_test=sct3)
    if twt.flagZ0Input == 1:
        tsi1 = z0z1_r0x0(tsi1, twt, 1)
        tsi2 = z0z1_r0x0(tsi2, twt, 2)
        tsi3 = z0z1_r0x0(tsi3, twt, 3)
    elif twt.flagZ0Input == 2:
        tsi1 = from_r0x0(tsi1, twt, 1)
        tsi2 = from_r0x0(tsi2, twt, 2)
        tsi3 = from_r0x0(tsi3, twt, 3)
    elif twt.flagZ0Input == 3:
        # TODO: Implement this case
        pass
    else:
        raise Exception(f'flagZ0Input : {twt.flagZ0Input} not supported')

    print(f'tsi1: r = {round(tsi1.r, 3)}, x = {tsi1.x}, r0: {round(tsi1.r0, 3)}, x0 = {round(tsi1.x0, 3)} ')
    print(f'tsi2: r = {round(tsi2.r, 3)}, x = {tsi2.x}, r0: {round(tsi2.r0, 3)}, x0 = {round(tsi2.x0, 3)}')
    print(f'tsi3: r = {round(tsi3.r, 3)}, x = {tsi3.x}, r0: {round(tsi3.r0, 3)}, x0 = {round(tsi3.x0, 3)}')


def from_r0x0(tsi: TransformerStarImpedance, twt: StdThreeWindingTransformer, endNumber: int):
    if endNumber == 1:
        tsi.r0 = twt.r0_12
        tsi.x0 = twt.x0_12
    if endNumber == 2:
        tsi.r0 = twt.r0_23
        tsi.x0 = twt.x0_23
    if endNumber == 3:
        tsi.r0 = twt.r0_31
        tsi.x0 = twt.x0_31
    return tsi


def from_r0x0_for_s2wt(tsi: TransformerStarImpedance, twt: StdTwoWindingTransformer):
    tsi.r0 = twt.r0
    tsi.x0 = twt.x0
    return tsi


def z0z1_r0x0_from_s2wt(tsi: TransformerStarImpedance, twt: StdTwoWindingTransformer):
    z1 = sqrt(tsi.r ** 2 + tsi.x ** 2)
    z0 = z1 * twt.z0z1
    tsi.x0 = z0 / sqrt(twt.r0X0 ** 2 + 1)
    tsi.r0 = twt.r0X0 * tsi.x0
    return tsi


def from_r0R1_for_s2wt(tsi: TransformerStarImpedance, twt: StdTwoWindingTransformer):
    tsi.x0 = twt.x0X1 * tsi.x
    tsi.r0 = twt.r0R1 * tsi.r
    return tsi


def z0z1_r0x0(tsi: TransformerStarImpedance, twt: StdThreeWindingTransformer, endNumber: int):
    if endNumber == 1:
        z1 = sqrt(tsi.r ** 2 + tsi.x ** 2)
        z0 = z1 * twt.z0z1_12
        tsi.x0 = z0 / sqrt(twt.r0X0_12 ** 2 + 1)
        tsi.r0 = twt.r0X0_12 * tsi.x0
    if endNumber == 2:
        z1 = sqrt(tsi.r ** 2 + tsi.x ** 2)
        z0 = z1 * twt.z0z1_23
        tsi.x0 = z0 / sqrt(twt.r0X0_23 ** 2 + 1)
        tsi.r0 = twt.r0X0_23 * tsi.x0
    if endNumber == 3:
        z1 = sqrt(tsi.r ** 2 + tsi.x ** 2)
        z0 = z1 * twt.z0z1_31
        tsi.x0 = z0 / sqrt(twt.r0X0_31 ** 2 + 1)
        tsi.r0 = twt.r0X0_31 * tsi.x0
    return tsi


def entso_e_example():
    # Validation with example 4.3.3.1, p 35. ENTSO-E, COMMON INFORMATION MODEL (CIM) – MODEL EXCHANGE PROFILE 1, Ed 1.
    # https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/140610_ENTSO-E_CIM_Profile_v1_UpdateIOP2013.pdf
    print('Computing TransformerStartImpedance attributes...')
    pte = PowerTransformerEnd()
    pte.rated_s = 1630e6
    pte.rated_u = 400e3
    sc_test = ShortCircuitTest(power=2020180, voltage=11.85)
    tsi: TransformerStarImpedance = transformer_test_to_rx(pte=pte, sc_test=sc_test)
    print(f'r = {tsi.r}, x = {tsi.x}')


def sincal_2wt_to_cim(twt: StdTwoWindingTransformer):
    print("Computing TransformerStarImpedance for ThreeWindingTransformer...")
    pte1 = PowerTransformerEnd()
    pte1.rated_s = twt.sn
    pte1.rated_u = twt.un1
    sc_test1 = ShortCircuitTest(voltage=twt.uk, voltage_ohmic_part=twt.ur)
    tsi: TransformerStarImpedance = transformer_test_to_rx(pte=pte1, sc_test=sc_test1)
    if twt.flagZ0Input == 1:
        tsi = z0z1_r0x0_from_s2wt(tsi, twt)
    elif twt.flagZ0Input == 2:
        tsi = from_r0x0_for_s2wt(tsi, twt)
    elif twt.flagZ0Input == 3:
        tsi = from_r0R1_for_s2wt(tsi, twt)
    else:
        raise Exception(f'flagZ0Input : {twt.flagZ0Input} not supported')
    print(f'tsi: r = {round(tsi.r, 3)}, x = {tsi.x}, r0: {round(tsi.r0, 3)}, x0 = {round(tsi.x0, 3)} ')


def migrator_sdk_example():
    print('Computing StartImpedances StdThreeWindingTransformer ...')
    s3wt: StdThreeWindingTransformer = StdThreeWindingTransformer()
    sincal_3wt_to_cim_tsi(s3wt)
    s2wt = StdTwoWindingTransformer(flagZ0Input=3)
    sincal_2wt_to_cim(s2wt)


if __name__ == '__main__':
    migrator_sdk_example()
