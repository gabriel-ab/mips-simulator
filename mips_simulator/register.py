import array
import enum

class Register:
    def __init__(self):
        self.buffer = array.array('l', [0]*35)

    def __getitem__(self, id: str) -> int:
        if isinstance(id, str):
            id: int = int(id[1:])
        return self.buffer[id]

    def __setitem__(self, id: str, value) -> None:
        if isinstance(id, str):
            id = int(id[1:])
        if id == 0:
            raise Exception("Register can't write at $0")
        self.buffer[id] = value


    @property
    def dict(self):
        result = {f'${i}': value for i, value in enumerate(self.buffer[:-3]) if value != 0}
        result.update(pc=self.pc, hi=self.hi, lo=self.lo)
        return result

    @property
    def pc(self): return self.buffer[32]
    @property
    def hi(self): return self.buffer[33]
    @property
    def lo(self): return self.buffer[34]

    @pc.setter
    def pc(self, value): self.buffer[32] = value
    @hi.setter
    def pc(self, value): self.buffer[33] = value
    @lo.setter
    def pc(self, value): self.buffer[34] = value
