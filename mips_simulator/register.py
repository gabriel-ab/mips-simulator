import array
from typing import Literal
from mips_simulator import constants

class Register:
    def __init__(self):
        self.map = {reg:i for i, reg in enumerate(constants.REGS)}
        self.buffer = array.array('l', [0]*35)
        self.buffer[28] = 0x10008000 # gp
        self.buffer[29] = 0x7fffeffc # sp
        self.buffer[32] = 0x00400000 # pc

    def __getitem__(self, id) -> int:
        if isinstance(id, str):
            id = self.map[id]
        return self.buffer[id]

    def __setitem__(self, id, value) -> None:
        if isinstance(id, str):
            id = self.map[id]
        if id == 0:
            raise Exception("Register can't write at $0")
        self.buffer[id] = value

    @property
    def dict(self):
        result = {f'${i}': value for i, value in enumerate(self.buffer[:-3]) if value != 0}
        result.update(pc=self['pc'], hi=self['hi'], lo=self['lo'])
        return result
