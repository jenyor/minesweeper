import cell
import config
import random


class Board:
    def generate_random(self, config: config.Config):
        """
        Замінник конструктора

        Генерує випадкову дошку з переданого config'а
        """
        self.cells_in_board = config.cells_in_board
        self.num_of_mines = config.num_of_mines
        self.found_pure = 0
        self.marked_mines = 0
        self.cells = []

        self.generate_cells()

        return self

    # Створює дошку з mines & cells випадковим чином, вставляючи у випадкові позиції міни
    def generate_cells(self):
        # Генерує всі індекси клітинок.
        # Випадковим чином вибирає позиції для мін
        mines_position = random.sample(
            list(range(0, self.cells_in_board[0] * self.cells_in_board[1])),
            self.num_of_mines,
        )
        mines_position.sort(reverse=True)

        # Створює двовимірний список з клітинок.
        # Пушить або звичайну клітинку, або міну, беручи до уваги `mines_position` список
        for row in range(self.cells_in_board[0]):
            cell_row = []
            for column in range(self.cells_in_board[1]):
                if (
                    len(mines_position) > 0
                    and mines_position[-1] == row * self.cells_in_board[1] + column
                ):
                    cell_row.append(cell.Cell(cell_type=cell.CellType.MINE))
                    mines_position.pop(-1)
                else:
                    cell_row.append(cell.Cell())
            self.cells.append(cell_row)

    def __repr__(self):
        return repr(self.cells)
