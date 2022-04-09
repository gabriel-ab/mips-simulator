from dataclasses import dataclass, field
from typing import Callable, Dict

from mips_simulator import utils
from mips_simulator.register import MipsRegister
from mips_simulator.entities import MipsCommand, MipsCommandR, MipsCommandI, MipsCommandJ


@dataclass
class MipsSimulator:
    config: Dict = {}
    mem: Dict[str, str] = {}
    reg: MipsRegister = field(default_factory=MipsRegister)

    def __post_init__(self):
        self.load_functions()

    def from_config(self, input: Dict) -> None:
        self.mem = input['data']
        self.reg = MipsRegister()
        
        config: dict = input['config']
        for key in config.get('reg', {}):
            self.reg[int(key[1:])] = config[key]

        self.stdout = ''
        
        regs = input['config']['regs']
        for name, value in regs:
            self.reg[name] = value
        self.load_functions()

    def check_overflow(self, value: int) -> int:
        if value >= 2**32:
            self.stdout.write('overflow')
        return value

    def load_functions(self):
        reg = self.reg
        # R type
        def _add(input: MipsCommandR):
            result = reg[input.rs] + reg[input.rt]
            reg[input.rd] = self.check_overflow(result)

        def _sub(input: MipsCommandR):
            result = reg[input.rs] - reg[input.rt]
            reg[input.rd] = self.check_overflow(result)

        def _addu(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] + reg[input.rt]

        def _subu(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] - reg[input.rt]

        def _mult(input: MipsCommandR):
            temp = utils.int2bin(reg[input.rs] * reg[input.rt], 64)
            temp = utils.split_bits(temp, (None, 32, None))
            reg.hi, reg.lo = map(utils.bin2int, temp)

        def _multu(input: MipsCommandR):
            _mult(input.rs, input.rt)

        def _div(input: MipsCommandR):
            reg.hi = reg[input.rs] % reg[input.rt]
            reg.lo = reg[input.rs] // reg[input.rt]

        def _divu(input: MipsCommandR):
            _div(input.rs, input.rt)

        def _mfhi(input: MipsCommandR):
            reg[input.rd] = reg.hi

        def _mflo(input: MipsCommandR):
            reg[input.rd] = reg.lo

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
            reg[input.rd] = reg[input.rs] << input.rt

        def _sllv(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] << reg[input.rt]

        def _srl(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] >> input.rt

        def _srlv(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] >> reg[input.rt]

        def _sra(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] >> reg[input.rt]

        def _srav(input: MipsCommandR):
            reg[input.rd] = reg[input.rs] >> input.rt

        def _jr(input: MipsCommandR):
            reg[31] = reg.pc
            reg.pc = input.rs


        # I type


        def _lui(input: MipsCommandI):
            reg[input.rt] = input.rs << 16

        def _addi(input: MipsCommandI):
            reg[input.rt] = reg[input.rs] + input.operand_or_offset

        def _slti(input: MipsCommandI):
            reg[input.rt] = 1 if reg[input.rs] < input.operand_or_offset else 0

        def _andi(input: MipsCommandI):
            reg[input.rt] = reg[input.rs] & input.operand_or_offset

        def _ori(input: MipsCommandI):
            reg[input.rt] = reg[input.rs] | input.operand_or_offset

        def _xori(input: MipsCommandI):
            reg[input.rt] = reg[input.rs] ^ input.operand_or_offset

        def _lw(input: MipsCommandI):
            reg[input.rt] = self.mem[input.rs] + input.operand_or_offset

        def _sw(input: MipsCommandI):
            self.mem[input.rt + input.operand_or_offset] = self.reg[input.rs]

        def _bltz(input: MipsCommandI):
            if input.rs < 0:
                reg.pc += input.operand_or_offset << 2

        def _beq(input: MipsCommandI):
            if reg[input.rs] == reg[input.rt]:
                reg.pc += input.operand_or_offset << 2

        def _bne(input: MipsCommandI):
            if reg[input.rs] != reg[input.rt]:
                reg.pc += input.operand_or_offset << 2

        def _addiu(input: MipsCommandI):
            reg[input.rt] = input.rs + input.operand_or_offset

        # Maybe wrong
        def _lb(input: MipsCommandI):
            reg[input.rt] = self.mem[input.rs + input.operand_or_offset] 

        def _lbu(input: MipsCommandI):
            reg[input.rt] = self.mem[input.rs + input.operand_or_offset]

        def _sbu(input: MipsCommandI):
            self.mem[input.rt] = self.reg[input.rs + input.operand_or_offset]

        def _syscall(input):
            if self.reg[2] == 1: # print integer
                self.stdout += str(self.reg[4])
            elif self.reg[2] == 4: # print string
                pass
                # self.stdout += str(self.data[self.reg[4]])

        # TODO: J type
        self.functions = {
            key: value 
            for key, value in 
            locals().items() 
            if isinstance(value, Callable)
        }
    

    def exec(self, instruction: MipsCommand):
        utils.check_type()
        self.functions


    def run(self, instruction: Dict):
        text: str = instruction['text']
        splited = text.replace(',', '').split(' ')
        func, args = splited[0], splited[1:]
        output = {}
        try:
            self.functions['_'+func](*args)
        except OverflowError:
            output['stdout'] = 'overflow'

    def __call__(self, json: Dict[str, Dict]) -> Dict[str, Dict]:
        pass
