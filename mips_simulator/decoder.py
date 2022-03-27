"""Mips Interpreter

This module ofer methods to translate hexadecimal mips code to assembly
"""

from typing import Dict, Literal, Sequence, Tuple
from functools import partial
from .constants import REGS, OPCODES, FUNCTIONS


def hex2bin(text: str, num_bits: int = 32) -> str:
    value = int(text, base=16)
    return int2bin(value, num_bits)

def int2bin(value: int, num_bits: int = 32) -> str:
    result = f'{value:0{num_bits}b}'
    return result[-num_bits:] if len(result) > num_bits else result

def bin2int(value: str, num_bits: int):
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


def check_type(binary_text: str) -> Literal['R', 'I', 'J']:
    opcode = bin2int(binary_text[:6])
    if opcode == 0:
        return 'R'
    elif opcode in [2,3]:
        return 'J'
    return 'I'


def translate_r_command(text: str) -> str:
    parts = split_r(text)
    parts = tuple(map(bin2int, parts))

    op, rs, rt, rd, sh, fn = parts
    rs, rt, rd = REGS[rs], REGS[rt], REGS[rd]
    
    if fn == 12:
        return 'syscall'
    
    name = FUNCTIONS[fn]
    
    if name in 'mfhimflo':
        return f'{name} {rd}'

    if name in 'jr': # one argument cases
        return f'{name} {rs}'

    if name in 'multudivu': # two argument cases
        return f'{name} {rs}, {rt}'

    return f'{name} {rd}, {rs}, {rt}'


def translate_i_command(text: str) -> str:
    parts = split_i(text)
    parts = tuple(map(bin2int, parts))

    op, rs, rt, operand_or_offset = parts
    name, rs, rt = OPCODES[op], REGS[rs], REGS[rt]

    if name in 'lwswlbusb': # offset cases
        return f'{name} {rt}, {operand_or_offset}({rs})'

    if name == 'bltz': # one argument cases
        return f'{name} {rs}, {operand_or_offset}'

    if name == 'lui':
        return f'{name} {rt}, {operand_or_offset}'

    return f'{name} {rt}, {rs}, {operand_or_offset}'


def translate_j_command(text: str) -> str:
    parts = split_j(text)
    op, jump = tuple(map(bin2int,parts))
    
    return f'{OPCODES[op]} {jump*4}'


def translate(input: Dict):
    commands = map(hex2bin, input['text'])

    result = []
    for command in commands:
        command_type = check_type(command)

        if command_type == 'R':
            translated = translate_r_command(command)
        elif command_type == 'I':
            translated = translate_i_command(command)
        elif command_type == 'J':
            translated = translate_j_command(command)
        
        result.append(translated)
    return '\n'.join(result)