from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Generator

from mips_simulator import utils
from mips_simulator.register import Register
from mips_simulator.entities import MipsCommand, MipsCommandR, MipsCommandI, MipsCommandJ

@dataclass
class MipsSimulator:
    mem: Dict = field(default_factory=dict)
    data: Dict = field(default_factory=dict)
    reg: Register = field(default_factory=Register)
    hist: List[MipsCommand] = field(default_factory=list, init=False, repr=False)
    stdout: str = ''

    def __post_init__(self):
        self.load_functions()

    @property
    def config(self):
        return self._config
    
    @config.setter
    def config(self, config):
        self._config = config

        self.mem = config['mem']
        regs = config.get('regs', {})
        for key in regs:
            self.reg[key] = regs[key]

        self.stdout = ''
        self.load_functions()

    def check_overflow(self, value: int) -> int:
        result = value >= 2**32
        self.stdout = 'overflow' if result else ''
        return result

    def load_functions(self):
        reg = self.reg
        # R type
        def _add(input: MipsCommandR):
            result = reg[input.rs] + reg[input.rt]
            if not self.check_overflow(result):
                reg[input.rd] = result

        def _sub(input: MipsCommandR):
            result = reg[input.rs] - reg[input.rt]
            if not self.check_overflow(result):
                reg[input.rd] = result

        def _addu(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] + reg[input.rt]

        def _subu(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] - reg[input.rt]

        def _mult(input: MipsCommandR):
            temp = utils.int2bin(reg[input.rs] * reg[input.rt], 64)
            temp = utils.split_bits(temp, (None, 32, None))
            reg.hi, reg.lo = map(utils.bin2int, temp)

        def _multu(input: MipsCommandR):
            _mult(input)

        def _div(input: MipsCommandR):
            reg.hi = reg[input.rs] % reg[input.rt]
            reg.lo = reg[input.rs] // reg[input.rt]

        def _divu(input: MipsCommandR):
            _div(input)

        def _mfhi(input: MipsCommandR):
            reg[input.rd] = reg['hi']

        def _mflo(input: MipsCommandR):
            reg[input.rd] = reg['lo']

        def _slt(input: MipsCommandR):
            reg[input.rd] = 1 if reg[input.rs] < reg[input.rt] else 0

        def _and(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] & reg[input.rt]

        def _or(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] | reg[input.rt]

        def _xor(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] ^ reg[input.rt]

        def _nor(input: MipsCommandR):
            reg[input.rd] = ~(reg[input.rs] | reg[input.rt])

        def _sll(input: MipsCommandR):
            reg[input.rd] = reg[input.rt] << input.sh

        def _sllv(input: MipsCommandR):
            reg[input.rd] = reg[input.rt] << reg[input.rs]

        def _srl(input: MipsCommandR):
            reg[input.rd] = reg[input.rt] >> input.sh

        def _srlv(input: MipsCommandR):
            reg[input.rd] = reg[input.rt] >> reg[input.rs]

        def _sra(input: MipsCommandR):
            reg[input.rd] = reg[input.rt] >> input.sh

        def _srav(input: MipsCommandR):
            reg[input.rd] = reg[input.rt] >> reg[input.rs]

        def _jr(input: MipsCommandR):
            reg[31] = reg['pc']
            reg['pc'] = input.rs


        # I type

        def _addi(input: MipsCommandI):
            result = reg[input.rs] + input.operand_or_offset
            if not self.check_overflow(result):
                reg[input.rt] = result

        def _addiu(input: MipsCommandI):
            reg[input.rt] = input.rs + input.operand_or_offset

        def _andi(input: MipsCommandI):
            reg[input.rt] = reg[input.rs] & input.operand_or_offset

        def _ori(input: MipsCommandI):
            reg[input.rt] = reg[input.rs] | input.operand_or_offset

        def _xori(input: MipsCommandI):
            reg[input.rt] = reg[input.rs] ^ input.operand_or_offset

        def _slti(input: MipsCommandI):
            reg[input.rt] = 1 if reg[input.rs] < input.operand_or_offset else 0

        def _lui(input: MipsCommandI): pass
        #     reg[input.rt] = input.rs << 16

        def _lw(input: MipsCommandI): pass
        #     reg[input.rt] = self.mem[input.rs + input.operand_or_offset]

        def _sw(input: MipsCommandI): pass
        #     self.mem[input.rt] = self.reg[input.rs + input.operand_or_offset]

        def _bltz(input: MipsCommandI): pass
        #     if input.rs < 0:
        #         reg['pc'] += input.operand_or_offset << 2

        def _beq(input: MipsCommandI): pass
        #     if reg[input.rs] == reg[input.rt]:
        #         reg['pc'] += input.operand_or_offset << 2

        def _bne(input: MipsCommandI): pass
        #     if reg[input.rs] != reg[input.rt]:
        #         reg['pc'] += input.operand_or_offset << 2

        def _lb(input: MipsCommandI): pass
        #     reg[input.rt] = self.mem[input.rs + input.operand_or_offset]

        def _lbu(input: MipsCommandI): pass
        #     reg[input.rt] = self.mem[input.rs + input.operand_or_offset]

        def _sb(input: MipsCommandI): pass
        #     self.mem[input.rt] = self.reg[input.rs + input.operand_or_offset]

        # J type

        def _j(input: MipsCommandJ): pass
        #     pass
        
        def _jal(input: MipsCommandJ): pass
        #     reg[31] = reg['pc'] + 4
        #     reg['pc'] = input.rs

        def _syscall(input):
            if self.reg[2] == 1: # print integer
                self.stdout += str(self.reg[4])
            elif self.reg[2] == 4: # print string
                pass
                # self.stdout += str(self.data[self.reg[4]])

        self.functions = {
            key: value 
            for key, value in 
            locals().items() 
            if isinstance(value, Callable)
        }

    def decode_instruction(self, instruction: str) -> MipsCommand:
        type = utils.check_type(utils.hex2bin(instruction))
        if type == 'R':
            return MipsCommandR.from_hex(instruction)
        if type == 'I':
            return MipsCommandI.from_hex(instruction)
        if type == 'J':
            return MipsCommandJ.from_hex(instruction)

    def exec(self, instructions: Sequence[str], debug=False) -> List[Dict]:
        info = []
        for instruction in instructions:
            instruction = self.decode_instruction(instruction)
            self.hist.append(instruction)
            self.functions['_'+instruction.name](instruction)

            if debug:
                info.append({
                    'hex': instruction.hex,
                    'text': str(instruction),
                    'mem': self.mem,
                    'regs': self.reg.dict,
                    'stdout': self.stdout
                })
        return info

    def __call__(self, input: Dict, debug=False) -> List[Dict]:
        config = input.get('config', None)
        if config:
            self.config = config

        return self.exec(input['text'], debug=debug)
