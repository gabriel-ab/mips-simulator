import array

class Register(array.array):
    def __init__(self, size=32, dsize='L'):
        super().__init__(dsize, [0]*size)


class MipsRegister(Register):
    def __init__(self):
        super().__init__(35)

    def __getitem__(self, id: str) -> int:
        if isinstance(id, str):
            id: int = int(id[1:])
        return super().__getitem__(id)

    def __setitem__(self, id: str, value) -> None:
        if isinstance(id, str):
            id = int(id[1:])
        if id == 0:
            raise Exception("Register can't write at $0")
        super().__setitem__(id, value)

    @property
    def pc(self): return self[32]
    @property
    def hi(self): return self[33]
    @property
    def lo(self): return self[34]

    @pc.setter
    def pc(self, value): self[32] = value
    @hi.setter
    def pc(self, value): self[33] = value
    @lo.setter
    def pc(self, value): self[34] = value
