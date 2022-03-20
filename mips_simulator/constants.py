"""Mips Constants

Constants for registers, instructions and all mips related strings
"""

NAMED_REGS = (
    '$zero',
    '$at',
    '$v0', '$v1',
    '$a0', '$a1', '$a2', '$a3',
    '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
    '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
    '$t8', '$t9',
    '$k0', '$k1',
    'gp', 'sp', 'fp', 'ra'
)

NUM_REGS = tuple(f'${i}' for i in range(len(NAMED_REGS)))

REGS = NUM_REGS

FUNCTIONS = { 0: "sll", 2: "srl", 3: "sra", 4: "sllv", 6: "srlv", 7: "srav", 8: "jr", 16: "mfhi", 18: "mflo", 24: "mult", 25: "multu", 26: "div", 27: "divu", 32: "add", 33: "addu", 34: "sub", 35: "subu", 36: "and", 37: "or", 38: "xor", 39: "nor", 42: "slt"}
OPCODES = {
    0: FUNCTIONS,
    1: "bltz", 2: "j", 3: "jal", 4: "beq", 5: "bne", 6: "blez", 7: "bgtz", 8: "addi", 9: "addiu", 10: "slti", 12: "andi", 13: "ori", 14: "xori", 15: "lui", 32: "lb", 35: "lw", 36: "lbu", 40: "sb", 43: "sw"
}

allregs = lambda: REGS + ('pc', 'hi', 'lo')

def set_regs_type(type: str) -> None:
    global REGS
    if type == 'named':
        REGS = NAMED_REGS
    if type == 'numeric':
        REGS = NUM_REGS
