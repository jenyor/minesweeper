from enum import Enum


class CellType(Enum):
    """Type of cell: normal or mine"""

    PURE = 0
    MINE = 1


class CellState(Enum):
    """Cell state: closed, open or marked with flag"""

    CLOSED = 0
    OPEN = 1
    MARKED = 2


class Cell:
    """
    The smallest unit of the minesweeper game - a cell that can have different types and states

    Also stores the number of neighboring fields that have a mine so that recursively opening neighboring fields is easier,
    and the neighboring cells themselves (so as not to go beyond the boundaries of the field, which will hold the cells)
    """

    def __init__(self, cell_type=CellType.PURE):
        self.state = CellState.CLOSED
        """Cell state"""
        self.type = cell_type
        """Cell type"""
        self.adjacent_mines = None
        """The number of adjacent cells that have the type `MINE`"""
        self.adjacent_cells = []
        """All neighboring cells within a 3x3 square where the current cell is the center and is not added to this list"""

    @classmethod
    def new_mine(cls):
        """Creating a mine cell"""
        return cls(CellType.MINE)

    @classmethod
    def new_pure(cls):
        """Creating a normal cell"""
        return cls(CellType.PURE)

    def __repr__(self):
        return f"{self.state} {self.type} MinesAround={self.adjacent_mines}"

    def toogle_flag(self):
        """Toggle the flag state"""
        self.state = CellState.CLOSED if self.state == CellState.MARKED else CellState.MARKED

    def open(self):
        """Open the cell"""
        self.state = CellState.OPEN

    def close(self):
        self.state = CellState.CLOSED

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
