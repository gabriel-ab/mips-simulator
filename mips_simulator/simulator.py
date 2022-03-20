import json
from typing import Sequence, Dict
import array
from .constants import REGS

class Register:

    def __init__(self, keys: Sequence[str]) -> None:
        self.map = {name: i for i, name in enumerate(keys)}
        self.regs = array.array('L', [0]*len(keys))
    
    def keys(self) -> Sequence[str]:
        return self.map.keys()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(keys={list(self.keys())}, mem={self.regs})'
    
    def __getitem__(self, id) -> int:
        if isinstance(id, str):
            id = self.regs[id]
        self.regs[id]

    def __setitem__(self, id, value) -> None:
        if isinstance(id, str):
            id = self.map[id]
        if id == 0: return
        self.regs[id] = value


class MipsSimulator:
    reg: Register
    mem: Dict[str, bytes]

    def __init__(self, input: Dict) -> None:
        self.mem = input['data']
        self.reg = Register(REGS)
        
        regs = input['config']['regs']
        for name, value in regs:
            self.reg[name] = value


with open('input/identify.input.json') as f:
    mips_input = json.load(f)

