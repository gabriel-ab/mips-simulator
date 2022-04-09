from typing import Sequence, Tuple, Literal


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

def check_type(bin_instruction: str) -> Literal['R', 'I', 'J']:
    opcode = bin2int(bin_instruction[:6])
    if opcode == 0:
        return 'R'
    elif opcode in [2,3]:
        return 'J'
    return 'I'