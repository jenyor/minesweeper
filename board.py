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

    # Створює дошку з mines & cells, вставляючи у випадкові позиції міни
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

        self.calculate_adjacent_mines()

    def calculate_adjacent_mines(self):
        adjacent_cf = []
        for row in range(-1, 2):
            for col in range(-1, 2):
                if not (row == col == 0):
                    adjacent_cf.append((row, col))

        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                self.cells[row][col].adjacent_mines = 0
                for cf in adjacent_cf:
                    pos = (row + cf[0], col + cf[1])
                    if (
                        self.is_within_board(pos[0], pos[1])
                        and self.cells[pos[0]][pos[1]].type == cell.CellType.MINE
                    ):
                        self.cells[row][col].adjacent_mines += 1

    def is_within_board(self, x: int, y: int):
        return (
            x >= 0
            and x < self.cells_in_board[0]
            and y >= 0
            and y < self.cells_in_board[1]
        )

    def __repr__(self):
        return repr(self.cells)

    def click_cell(self, index: tuple[int, int], flag: bool):
        piece = self.cells[index[0]][index[1]]
        if piece.state == cell.CellState.OPEN:
            pass
        elif flag:
            piece.toogle_flag()
            return
        elif piece.state == cell.CellState.CLOSED:
            piece.open()

            # Recursively visit adjacent empty cells
            if piece.type == cell.CellType.MINE:
                return
            for hor in range(index[0] - 1, index[0] + 2):
                for vert in range(index[1] - 1, index[1] + 2):
                    if (hor, vert) == index:
                        continue
                    if (
                        self.is_within_board(hor, vert)
                        and self.cells[hor][vert].type == cell.CellType.PURE
                    ):
                        self.click_cell((hor, vert), False)
