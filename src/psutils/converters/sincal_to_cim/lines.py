import math
from dataclasses import dataclass

from zepben.evolve import AcLineSegment, PerLengthSequenceImpedance


@dataclass
class StdLine:
    r: float = 7.0
    x: float = 8.0
    c: float = 9.0
    un: float = 10.0
    va: float = 13.0
    ith: float = 14.0
    fn: float = 50.0
    flagZ0Input: int = 2
    x0X1: float = 18.0
    r0R1: float = 19.0
    r0: float = 20.0
    x0: float = 21.0
    c0: float = 9.0
    q0: float = 23.0


@dataclass
class StdLineConverter:
    stdLine: StdLine

    def __post_init__(self):
        self.acls = AcLineSegment()
        self.plsi = PerLengthSequenceImpedance()
        self.acls.per_length_sequence_impedance = self.plsi

    def convert(self):
        self.acls.per_length_sequence_impedance.r = round(self.stdLine.r / 1000, 6)
        self.acls.per_length_sequence_impedance.x = round(self.stdLine.x / 1000, 6)
        self.acls.per_length_sequence_impedance.bch = round(
            2 * math.pi * self.stdLine.fn * self.stdLine.c * 10e-9 / 1000, 12)
        self.acls.per_length_sequence_impedance.gch = round(
            self.stdLine.va * 10e-3 / (1000 * self.stdLine.un ** 2), 15)
        if self.stdLine.flagZ0Input == 1:
            self.x0x1_r0r1()
        elif self.stdLine.flagZ0Input == 2:
            self.r0x0()
        else:
            raise Exception(f'flagZ0Input: {self.stdLine.flagZ0Input} is not supported.')

    def x0x1_r0r1(self):
        self.acls.per_length_sequence_impedance.r0 = self.stdLine.r * self.stdLine.r0R1
        self.acls.per_length_sequence_impedance.x0 = self.stdLine.r * self.stdLine.x0X1
        self.acls.per_length_sequence_impedance.b0ch = round(
            2 * math.pi * self.stdLine.fn * self.stdLine.c0 * 10e-9 / 1000, 12)
        self.acls.per_length_sequence_impedance.g0ch = 0

    def r0x0(self):
        self.acls.per_length_sequence_impedance.r0 = self.stdLine.r0 / 1000
        self.acls.per_length_sequence_impedance.x0 = self.stdLine.x0 / 1000
        self.acls.per_length_sequence_impedance.b0ch = round(
            2 * math.pi * self.stdLine.fn * self.stdLine.c0 * 10e-9 / 1000, 12)
        self.acls.per_length_sequence_impedance.g0ch = 0

    def print_impedance(self):
        print(f'r: {self.acls.per_length_sequence_impedance.r}')
        print(f'x: {self.acls.per_length_sequence_impedance.x}')
        print(f'bch: {self.acls.per_length_sequence_impedance.bch}')
        print(f'gch: {self.acls.per_length_sequence_impedance.gch}')
        print(f'r0: {self.acls.per_length_sequence_impedance.r0}')
        print(f'x0: {self.acls.per_length_sequence_impedance.x0}')
        print(f'b0ch: {self.acls.per_length_sequence_impedance.b0ch}')
        print(f'g0ch: {self.acls.per_length_sequence_impedance.g0ch}')


if __name__ == '__main__':
    stdLineConverter = StdLineConverter(StdLine())
    stdLineConverter.convert()
    stdLineConverter.print_impedance()
