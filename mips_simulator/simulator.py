from typing import Callable, Tuple, Dict
from .register import MipsRegister
from . import decoder

class MipsSimulator:
    reg: MipsRegister
    mem: Dict[str, bytes]
    

    def __init__(self, input: Dict) -> None:
        self.mem = input['data']
        self.reg = MipsRegister()
        
        regs = input['config']['regs']
        for name, value in regs:
            self.reg[name] = value
        self.load_functions()
    def split_hilo(number: int) -> Tuple[int, float]:
        number.to_bytes(64)
    
    def load_functions(self):
        reg = self.reg
        # R type
        def _add    (rs, rt, rd): reg[rd] = reg[rs] + reg[rt]
        def _sub    (rs, rt, rd): reg[rd] = reg[rs] - reg[rt]
        def _addu   (rs, rt, rd): reg[rd] = reg[rs] + abs(reg[rt])
        def _subu   (rs, rt, rd): reg[rd] = reg[rs] - abs(reg[rt])
        def _mult   (rs, rt):
            temp = decoder.int2bin(reg[rs] * reg[rt], 64)
            temp = decoder.split_bits(temp, (None, 32, None))
            reg.hi, reg.lo = map(decoder.bin2int, temp)
        def _multu  (rs, rt): _mult(rs, rt)
        def _div    (rs, rt): reg.hi, reg.lo = reg[rs] % reg[rt], reg[rs] // reg[rt]
        def _divu   (rs, rt): _div(rs, rt)
        def _mfhi   (rd): reg[rd] = reg.hi
        def _mflo   (rd): reg[rd] = reg.lo
        
        def _slt    (rs, rt, rd): reg[rd] = 1 if reg[rs] < reg[rt] else 0
        def _and    (rs, rt, rd): reg[rd] = reg[rs] & reg[rt]
        def _or     (rs, rt, rd): reg[rd] = reg[rs] | reg[rt]
        def _xor    (rs, rt, rd): reg[rd] = reg[rs] ^ reg[rt]
        def _nor    (rs, rt, rd): reg[rd] = ~(reg[rs] | reg[rt])

        def _sll    (rs, rt, rd): reg[rd] = reg[rs] << rt
        def _sllv   (rs, rt, rd): reg[rd] = reg[rs] << reg[rt]
        def _srl    (rs, rt, rd): reg[rd] = reg[rs] >> rt
        def _srlv   (rs, rt, rd): reg[rd] = reg[rs] >> reg[rt]
        def _sra    (rs, rt, rd): reg[rd] = reg[rs] >> reg[rt]
        def _srav   (rs, rt, rd): reg[rd] = reg[rs] >> rt
        def _jr     (rs, rt, rd): reg[31], reg.pc = reg.pc ,rs

        # I type

        def _lui    (rs, rt, immediate): reg[rt] = rs << 16
        def _addi   (rs, rt, immediate): reg[rt] = reg[rs] + immediate
        def _slti   (rs, rt, immediate): reg[rt] = 1 if reg[rs] < immediate else 0
        def _andi   (rs, rt, immediate): reg[rt] = reg[rs] & immediate
        def _ori    (rs, rt, immediate): reg[rt] = reg[rs] | immediate
        def _xori   (rs, rt, immediate): reg[rt] = reg[rs] ^ immediate
        def _lw     (rs, rt, immediate): reg[rt] = self.mem[rs] + immediate
        def _sw     (rs, rt, immediate): self.mem[rt] = self.reg[rs] + immediate
        def _bltz   (rs, rt, immediate):
            if rs < 0: reg.pc += immediate << 2
        def _beq    (rs, rt, immediate):
            if reg[rs] == reg[rt]: reg.pc += immediate << 2
        def _bne    (rs, rt, immediate):
            if reg[rs] != reg[rt]: reg.pc += immediate << 2
        def _addiu  (rs, rt, immediate): reg[rt] = rs + immediate

        # Maybe wrong
        def _lb     (rs, rt, immediate): reg[rt] = self.mem[rs + immediate]
        def _lbu    (rs, rt, immediate): reg[rt] = self.mem[rs + immediate]
        def _sbu    (rs, rt, immediate): self.mem[rt] = self.reg[rs + immediate]

        # TODO: J type
        self.functions = {
            key: value 
            for key, value in 
            locals().items() 
            if isinstance(value, Callable)
        }
    

    def run(self, instruction):
        text: str = instruction['text']
        splited = text.replace(',', '').split(' ')
        func, args = splited[0], splited[1:]
        output = {}
        try:
            self.functions['_'+func](*args)
        except OverflowError:
            output['stdout'] = 'overflow'

    def __call__(self, json: Dict[str, Dict]) -> Dict[str, Dict]:
        # logic and aritmetic 
        for line in decoder.translate(json):
            text = line['text']

            self.alu
