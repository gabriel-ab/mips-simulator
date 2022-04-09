"""Mips Interpreter

This module ofer methods to translate hexadecimal mips code to assembly
"""

from typing import List
from mips_simulator.utils import check_type, hex2bin
from mips_simulator.entities import MipsCommandR, MipsCommandI, MipsCommandJ

def decode(commands: List[str]) -> List[str]:
    result = []
    for command in commands:
        command_type = check_type(hex2bin(command))

        if command_type == 'R':
            translated = MipsCommandR.from_hex(command)
        elif command_type == 'I':
            translated = MipsCommandI.from_hex(command)
        elif command_type == 'J':
            translated = MipsCommandJ.from_hex(command)
        
        result.append(translated)
    return result
