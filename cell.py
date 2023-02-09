from enum import Enum


class CellType(Enum):
    PURE = 0
    MINE = 1


class CellState(Enum):
    CLOSED = 0
    OPEN = 1
    MARKED = 2


class Cell:
    def __init__(self, cell_type=CellType.PURE):
        self.state = CellState.CLOSED
        self.type = cell_type
        self.adjacent_mines = None
        self.adjacent_cells = []

    @classmethod
    def new_mine(cls):
        return cls(CellType.MINE)

    @classmethod
    def new_pure(cls):
        return cls(CellType.PURE)

    def __repr__(self):
        return f"{self.state} {self.type} MinesAround={self.adjacent_mines}"

    def toogle_flag(self):
        self.state = CellState.CLOSED if self.state == CellState.MARKED else CellState.MARKED

    def open(self):
        self.state = CellState.OPEN

    def is_mine(self):
        return self.type == CellType.MINE

    def is_pure(self):
        return self.type == CellType.PURE

    def is_closed(self):
        return self.state == CellState.CLOSED

    def is_open(self):
        return self.state == CellState.OPEN

    def is_marked(self):
        return self.state == CellState.MARKED
