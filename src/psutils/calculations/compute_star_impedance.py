from dataclasses import dataclass

from numpy import sqrt
from zepben.evolve import PowerTransformerEnd

__all__ = ["TransformerStarImpedance", "ShortCircuitTest", "OpenCircuitTest", "NoLoadTest",
           "transformer_test_to_star_impedance"]

"""Script to compute cim: TransformerStarImpedance from cim: TransformerTests"""


@dataclass
class TransformerStarImpedance:
    r: float = 0
    """Resistance	Resistance of the transformer end."""
    r0: float = 0
    """ Resistance	Zero sequence series resistance of the transformer end."""
    x: float = 0
    """Reactance	Positive sequence series reactance of the transformer end."""
    x0: float = 0
    """ Reactance	Zero sequence series reactance of the transformer end."""


@dataclass
class ShortCircuitTest:
    """Short-circuit test results determine mesh impedance parameters.
    They include load losses and leakage impedance. For three-phase windings,
    the excitation can be a positive sequence (the default) or a zero sequence.
    There shall be at least one grounded winding."""

    power: int
    """ApparentPower	Short circuit apparent power."""
    energisedEndStep: int = 0
    """Integer	Tap step number for the energised end of the test pair."""
    groundedEndStep: int = 0
    """Integer	Tap step number for the grounded end of the test pair."""
    leakageImpedance: int = 0
    """Impedance	Leakage impedance measured from a positive-sequence or single-phase short-circuit test."""
    leakageImpedanceZero: int = 0
    """Impedance	Leakage impedance measured from a zero-sequence short-circuit test."""
    loss: int = 0
    """KiloActivePower	Load losses from a positive-sequence or single-phase short-circuit test."""
    lossZero: int = 0
    """KiloActivePower	Load losses from a zero-sequence short-circuit test."""
    voltage: float = 0
    """PerCent	Short circuit voltage.."""


@dataclass
class OpenCircuitTest:
    """ Open-circuit test results verify winding turn ratios and phase shifts.
    They include induced voltage and phase shift measurements on open-circuit windings, with voltage applied to the energised end.
    For three-phase windings, the excitation can be a positive sequence (the default) or a zero sequence."""
    openEndVoltage: int
    """ [V] Voltage	Voltage measured at the open-circuited end, 
    ith the energised end set to rated voltage and all other ends open."""
    phaseShift: float
    """AngleDegrees	Phase shift measured at the open end with 
    the energised end set to rated voltage and all other ends open."""
    energisedEndStep: int = 0
    """  Integer	Tap step number for the energised end of the test pair."""
    energisedEndVoltage: int = 0
    """ Voltage	Voltage applied to the winding (end) during test."""
    openEndStep: int = 0
    """ Integer	Tap step number for the open end of the test pair."""


@dataclass
class NoLoadTest:
    """ No-load test results determine core admittance parameters.
    They include exciting current and core loss measurements from applying voltage to one winding.
    The excitation may be positive sequence or zero sequence.
    The test may be repeated at different voltages to measure saturation."""

    energisedEndVoltage: int = 0
    """Voltage	Voltage applied to the winding (end) during test"""
    excitingCurrent: int = 0
    """ PerCent	Exciting current measured from a positive-sequence or single-phase excitation test."""
    excitingCurrentZero = 0
    """ PerCent Exciting current measured from a zero-sequence open-circuit excitation test."""
    loss = 0
    """ KiloActivePower	Losses measured from a positive-sequence or single-phase excitation test."""
    lossZero = 0
    """ KiloActivePower	Losses measured from a zero-sequence excitation test."""


def transformer_test_to_star_impedance(pte: PowerTransformerEnd, sc_test: ShortCircuitTest, nl_test: NoLoadTest):
    r, x, r0, x0 = 0, 0, 0, 0
    r = sc_test.power * (pte.rated_u / pte.rated_s) ** 2
    x = sqrt(((sc_test.voltage / 100) * pte.rated_u ** 2 / pte.rated_s) ** 2 - r ** 2)
    return TransformerStarImpedance(r, r0, x, x0)


if __name__ == '__main__':
    # Validation with example 4.3.3.1, p 35. ENTSO-E, COMMON INFORMATION MODEL (CIM) – MODEL EXCHANGE PROFILE 1, Ed 1.
    # https://eepublicdownloads.entsoe.eu/clean-documents/CIM_documents/Grid_Model_CIM/140610_ENTSO-E_CIM_Profile_v1_UpdateIOP2013.pdf
    print('Computing TransformerStartImpedance attributes...')
    pte = PowerTransformerEnd()
    pte.rated_s = 1630e6
    pte.rated_u = 400e3
    sc_test = ShortCircuitTest(power=2020180, voltage=11.85)
    nl_test = NoLoadTest()
    tsi: TransformerStarImpedance = transformer_test_to_star_impedance(pte=pte, sc_test=sc_test, nl_test=nl_test)
    print(f'r = {tsi.r}, x = {tsi.x}')
