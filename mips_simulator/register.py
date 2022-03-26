from typing import Sequence
import array

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
            id = self.map[id]
        return self.regs[id]

    def __setitem__(self, id, value) -> None:
        if isinstance(id, str):
            id = self.map[id]
        if id == 0: return
        self.regs[id] = value

class MipsRegister(Register):
    def __init__(self) -> None:
        from .constants import allregs
        super().__init__(allregs())