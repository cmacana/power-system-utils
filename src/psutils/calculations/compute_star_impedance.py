from dataclasses import dataclass

from numpy import sqrt
from zepben.evolve import PowerTransformerEnd, TransformerStarImpedance, ShortCircuitTest, OpenCircuitTest, NoLoadTest

__all__ = ["TransformerStarImpedance", "ShortCircuitTest", "OpenCircuitTest", "NoLoadTest",
           "transformer_test_to_star_impedance"]

"""Script to compute cim: TransformerStarImpedance from cim: TransformerTests"""


def transformer_test_to_star_impedance(pte: PowerTransformerEnd, sc_test: ShortCircuitTest):
    r, x, r0, x0 = 0, 0, 0, 0
    if sc_test.power:
        r = sc_test.power * (pte.rated_u / pte.rated_s) ** 2
    elif sc_test.voltage_ohmic_part:
        r = (pte.rated_u ** 2 * sc_test.voltage_ohmic_part / (pte.rated_s * 100))
    else:
        raise Exception('Value for ShortCircuitTest.power or ShortCircuitTest.voltage_ohmic_part required')

    if sc_test.power:
        x = sqrt(((sc_test.voltage / 100) * pte.rated_u ** 2 / pte.rated_s) ** 2 - r ** 2)
    elif sc_test.voltage_ohmic_part:
        x = pte.rated_u ** 2 * (sqrt(sc_test.voltage**2 - sc_test.voltage_ohmic_part**2) / (pte.rated_s * 100))
    else:
        raise Exception('Value for ShortCircuitTest.power or ShortCircuitTest.voltage_ohmic_part required')
    return TransformerStarImpedance(r=r, r0=r0, x=x, x0=x0)


def entso_e_example():
    # Validation with example 4.3.3.1, p 35. ENTSO-E, COMMON INFORMATION MODEL (CIM) – MODEL EXCHANGE PROFILE 1, Ed 1.
    # https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/140610_ENTSO-E_CIM_Profile_v1_UpdateIOP2013.pdf
    print('Computing TransformerStartImpedance attributes...')
    pte = PowerTransformerEnd()
    pte.rated_s = 1630e6
    pte.rated_u = 400e3
    sc_test = ShortCircuitTest(power=2020180, voltage=11.85)
    tsi: TransformerStarImpedance = transformer_test_to_star_impedance(pte=pte, sc_test=sc_test)
    print(f'r = {tsi.r}, x = {tsi.x}')


def create_start_impedance_from_sincal(un: float, sn: float, uk: float, ur: float):
    pte = PowerTransformerEnd()
    pte.rated_s = sn
    pte.rated_u = un
    sc_test = ShortCircuitTest(voltage=uk, voltage_ohmic_part=ur)
    tsi: TransformerStarImpedance = transformer_test_to_star_impedance(pte=pte, sc_test=sc_test)
    print(f'r = {tsi.r}, x = {tsi.x}')


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


def migrator_sdk_example(twt: StdThreeWindingTransformer = StdThreeWindingTransformer()):
    print('Computing StartImpedances StdThreeWindingTransformer ...')
    create_start_impedance_from_sincal(twt.un1, twt.sn12, twt.uk12, twt.ur12)
    create_start_impedance_from_sincal(twt.un2, twt.sn23, twt.uk23, twt.ur23)
    create_start_impedance_from_sincal(twt.un3, twt.sn31, twt.uk31, twt.ur31)


if __name__ == '__main__':
    entso_e_example()
    migrator_sdk_example()
