"""Mips Interpreter

This module ofer methods to translate hexadecimal mips code to assembly
"""

from abc import ABC, abstractstaticmethod
from dataclasses import dataclass
from typing import Dict, Literal, Sequence, Tuple
from functools import partial
from .constants import REGS, OPCODES, FUNCTIONS


def hex2bin(text: str, num_bits: int = 32) -> str:
    value = int(text, base=16)
    return int2bin(value, num_bits)

def int2bin(value: int, num_bits: int = 32) -> str:
    result = f'{value:0{num_bits}b}'
    return result[-num_bits:] if len(result) > num_bits else result

def bin2int(value: str, num_bits: int = 32) -> int:
    result = int(value, base=2)
    return result % (num_bits**2)

def split_bits(text: str, indexes: Sequence[int]) -> Tuple[str]:
    b_iter = iter(indexes)
    e_iter = iter(indexes)
    next(e_iter)
    return tuple(
        text[begin:end] 
        for begin, end in
        zip(b_iter, e_iter)
    )

split_r = partial(split_bits, indexes=(0, 6, 11, 16, 21, 26, 32))
split_i = partial(split_bits, indexes=(0, 6, 11, 16, 32))
split_j = partial(split_bits, indexes=(0, 6, 32))


def check_type(bin_instruction: str) -> Literal['R', 'I', 'J']:
    opcode = bin2int(bin_instruction[:6])
    if opcode == 0:
        return 'R'
    elif opcode in [2,3]:
        return 'J'
    return 'I'


@dataclass
class MipsCommand(ABC):
    op: int

    @abstractstaticmethod
    def split(bin_instruction: str) -> Tuple[str]:
        pass
    
    @classmethod
    def from_hex(cls, value: str):
        parts = cls.split(hex2bin(value))
        parts = tuple(map(bin2int, parts))
        return cls(*parts)


@dataclass
class MipsCommandR(MipsCommand):
    rs: int
    rt: int
    rd: int
    sh: int
    fn: int

    @staticmethod
    def split(bin_instruction: str) -> Tuple[str]:
        return split_bits(bin_instruction, indexes=(0, 6, 11, 16, 21, 26, 32))

    def __str__(self) -> str:
        if self.fn == 12: return 'syscall'

        rs, rt, rd = REGS[self.rs], REGS[self.rt], REGS[self.rd]
        name = FUNCTIONS[self.fn]

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
        return split_i(bin_instruction)

    def __str__(self) -> str:
        name, rs, rt = OPCODES[self.op], REGS[self.rs], REGS[self.rt]

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
        return split_j(bin_instruction)
    
    def __str__(self) -> str:
        return f'{OPCODES[self.op]} {self.jump*4}'


def translate(input: Dict):
    result = []
    for command in input['text']:
        command_type = check_type(hex2bin(command))

        if command_type == 'R':
            translated = str(MipsCommandR.from_hex(command))
        elif command_type == 'I':
            translated = str(MipsCommandI.from_hex(command))
        elif command_type == 'J':
            translated = str(MipsCommandJ.from_hex(command))
        
        result.append(translated)
    return '\n'.join(result)