from enum import Enum


class CellType(Enum):
    """Тип клітинки: звичайна або міна"""

    PURE = 0
    MINE = 1


class CellState(Enum):
    """Стан клітики: закрита, відкрита чи відмічена прапорцем"""

    CLOSED = 0
    OPEN = 1
    MARKED = 2


class Cell:
    """
    Найменша одиниця сапера - клітинка, яка може бути різних типів і мати різний стан

    Також зберігає у собі кільксть сусідніх полів, які мають у собі міну, щоб легше було відкривати рекурсивно сусідні поля, \
    і самі сусідні клітинки (щоб не виходити за межі поля, яке буде тримати клітинки у собі)
    """

    def __init__(self, cell_type=CellType.PURE):
        self.state = CellState.CLOSED
        """Стан клітинки"""
        self.type = cell_type
        """Тип клітинки"""
        self.adjacent_mines = None
        """Кількість сусідніх клітинок, що мають тип - `MINE`"""
        self.adjacent_cells = []
        """Всі сусідні клітинки у межах квадрата 3х3, де поточна клітинка є центром і не додається у цей список"""

    @classmethod
    def new_mine(cls):
        """Створення клітинку-міну"""
        return cls(CellType.MINE)

    @classmethod
    def new_pure(cls):
        """Створення звичайну клітинку"""
        return cls(CellType.PURE)

    def __repr__(self):
        return f"{self.state} {self.type} MinesAround={self.adjacent_mines}"

    def toogle_flag(self):
        """Змінити стан прапорця на протилежний"""
        self.state = CellState.CLOSED if self.state == CellState.MARKED else CellState.MARKED

    def open(self):
        """Відкрити клітинку"""
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
