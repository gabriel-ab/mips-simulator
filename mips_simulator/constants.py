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

ALL_REGS = REGS + ('pc', 'hi', 'lo')


def set_regs_type(type: str) -> None:
    global REGS
    if type == 'named':
        REGS = NAMED_REGS
    if type == 'numeric':
        REGS = NUM_REGS
