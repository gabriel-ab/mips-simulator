from typing import Callable, Tuple
from .register import MipsRegister
from .decoder import hex2bin, split_bits, translate, base2

class MipsSimulator:
    reg: MipsRegister
    mem: dict[str, bytes]
    

    def __init__(self, input: dict) -> None:
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
        def _add   (a,b,c): reg[a] = reg[b] + reg[c]
        def _sub   (a,b,c): reg[a] = reg[b] - reg[c]
        def _addu  (a,b,c): reg[a] = reg[b] + abs(reg[c])
        def _subu  (a,b,c): reg[a] = reg[b] - abs(reg[c])
        def _mult  (a,b): reg['hi'], reg['lo'] = map(base2, split_bits(hex2bin(reg[a] * reg[b], 64), (None, 32, None)))
        def _multu (a,b): _mult(a,b)
        def _div   (a,b): reg['hi'], reg['lo'] = reg[a] % reg[b], reg[a] // reg[b]
        def _divu  (a,b): _div(a,b)
        def _mfhi  (a): reg[a] = reg['hi']
        def _mflo  (a): reg[a] = reg['lo']
        
        def _slt   (a,b,c): reg[a] = 1 if reg[b] < reg[c] else 0
        def _and   (a,b,c): reg[a] = reg[b] & reg[c]
        def _or    (a,b,c): reg[a] = reg[b] | reg[c]
        def _xor   (a,b,c): reg[a] = reg[b] ^ reg[c]
        def _nor   (a,b,c): reg[a] = ~(reg[b] | reg[c])
        def _sll   (a,b,c): reg[a] = reg[b] << c
        def _sllv  (a,b,c): reg[a] = reg[b] << reg[c]
        def _srl   (a,b,c): reg[a] = reg[b] >> c
        def _srlv  (a,b,c): reg[a] = reg[b] >> reg[c]
        # TODO
        def _sra   (a,b,c): reg[a] = reg[b] >> reg[c]
        def _srav  (a,b,c): reg[a] = reg[b] - reg[c]


        # I type
        # J type
        def _addi  (a,b,c): reg[a] = reg[b] + c
        def _addiu (a,b,c): reg[a] = reg[b] + abs(c)
        
        # logical
        def _andi  (a,b,c): reg[a] = reg[b] & c
        def _ori   (a,b,c): reg[a] = reg[b] | c
        def _xori  (a,b,c): reg[a] = reg[b] ^ c
        # TODO
        
        def _addi  (a,b,c): reg[a] = reg[b] - reg[c]
        def _slti  (a,b,c): reg[a] = reg[b] - reg[c]
        

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



    
    def __call__(self, json: dict[str, dict]) -> dict[str, dict]:
        # logic and aritmetic 
        for line in translate(json):
            text = line['text']

            self.alu



with open('input/identify.input.json') as f:
    mips_input = json.load(f)

