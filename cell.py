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

    def __repr__(self):
        return f"{self.state} {self.type} MinesAround={self.adjacent_mines}"

    def toogle_flag(self):
        self.state = (
            CellState.CLOSED if self.state == CellState.MARKED else CellState.MARKED
        )

    def open(self):
        self.state = CellState.OPEN
