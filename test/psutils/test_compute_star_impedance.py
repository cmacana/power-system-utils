from zepben.evolve import PowerTransformerEnd

from psutils.calculations.compute_star_impedance import ShortCircuitTest, NoLoadTest, TransformerStarImpedance, \
    transformer_test_to_rx


def test_compute_star_impedance():
    # Validation parameter from example 4.3.3.1, p 35. ENTSO-E, COMMON INFORMATION MODEL (CIM) – MODEL EXCHANGE PROFILE 1, Ed 1.
    # https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/140610_ENTSO-E_CIM_Profile_v1_UpdateIOP2013.pdf
    r = 0.1216563664420942
    x = 11.63126562998702
    pte = PowerTransformerEnd()
    pte.rated_s = 1630e6
    pte.rated_u = 400e3
    sc_test = ShortCircuitTest(power=2020180, voltage=11.85)
    nl_test = NoLoadTest()
    tsi: TransformerStarImpedance = transformer_test_to_rx(pte=pte, sc_test=sc_test, nl_test=nl_test)
    assert tsi.r == r
    assert tsi.x == x
