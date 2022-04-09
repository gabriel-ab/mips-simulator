
from abc import ABC, abstractstaticmethod
from dataclasses import dataclass, field
from typing import Tuple

from mips_simulator import utils, constants


@dataclass
class MipsCommand(ABC):
    hex: str = field(init=False)
    op: int

    @abstractstaticmethod
    def split(bin_instruction: str) -> Tuple[str]:
        pass

    @classmethod
    def from_hex(cls, value: str):
        parts = cls.split(utils.hex2bin(value))
        parts = tuple(map(utils.bin2int, parts))
        result = cls(*parts)
        result.hex = value
        return result


@dataclass
class MipsCommandR(MipsCommand):
    rs: int
    rt: int
    rd: int
    sh: int
    fn: int

    @staticmethod
    def split(bin_instruction: str) -> Tuple[str]:
        return utils.split_bits(bin_instruction, indexes=(0, 6, 11, 16, 21, 26, 32))

    @property
    def name(self):
        return constants.FUNCTIONS[self.fn]

    def __str__(self) -> str:
        if self.fn == 12: return 'syscall'

        rs, rt, rd = constants.REGS[self.rs], constants.REGS[self.rt], constants.REGS[self.rd]
        name = self.name

        if name in 'mfhimflo':
            return f'{name} {rd}'

        if name in 'jr': # one argument cases
            return f'{name} {rs}'

        if name in 'multudivu': # two argument cases
            return f'{name} {rs}, {rt}'

        return f'{name} {rd}, {rs}, {rt}'


@dataclass
class MipsCommandI(MipsCommand):
    rs: int
    rt: int
    operand_or_offset: int

    @staticmethod
    def split(bin_instruction: str) -> Tuple[str]:
        return utils.split_bits(bin_instruction, indexes=(0, 6, 11, 16, 32))

    @property
    def name(self):
        return constants.OPCODES[self.op]
    
    def __str__(self) -> str:
        name, rs, rt = self.name, constants.REGS[self.rs], constants.REGS[self.rt]

        if name in 'lwswlbusb': # offset cases
            return f'{name} {rt}, {self.operand_or_offset}({rs})'

        if name == 'bltz': # one argument cases
            return f'{name} {rs}, {self.operand_or_offset}'

        if name == 'lui':
            return f'{name} {rt}, {self.operand_or_offset}'

        return f'{name} {rt}, {rs}, {self.operand_or_offset}'


@dataclass
class MipsCommandJ(MipsCommand):
    jump: int

    @staticmethod
    def split(bin_instruction: str) -> Tuple[str]:
        return utils.split_bits(bin_instruction, indexes=(0, 6, 32))

    @property
    def name(self):
        return constants.OPCODES[self.op]

    def __str__(self) -> str:
        return f'{self.name} {self.jump*4}'
