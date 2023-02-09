import cell
import config
import random


class Board:
    def generate_random(self, config: config.Config):
        self.cells_in_board = config.cells_in_board
        self.num_of_mines = config.num_of_mines
        self.found_pure = 0
        self.marked_mines = 0
        self.cells = []

        self.generate_cells()

        return self

    def get_cells_x(self):
        return self.cells_in_board[1]

    def get_cells_y(self):
        return self.cells_in_board[0]

    def get_cell_in_pos(self, idx: tuple[int, int]):
        return self.cells[idx[0]][idx[1]]

    def get_board_area(self):
        return self.cells_in_board[0] * self.cells_in_board[1]

    def tuple_index_to_raw(self, index: tuple[int, int]):
        return index[0] * self.get_cells_x() + index[1]

    def generate_cells(self):
        mines_position = random.sample(list(range(0, self.get_board_area())), self.num_of_mines)
        mines_position.sort(reverse=True)

        for row in range(self.get_cells_y()):
            cell_row = []
            for col in range(self.get_cells_x()):
                is_mine = len(mines_position) and mines_position[-1] == self.tuple_index_to_raw((row, col))
                if is_mine:
                    cell_row.append(cell.Cell.new_mine())
                    mines_position.pop(-1)
                else:
                    cell_row.append(cell.Cell.new_pure())

            self.cells.append(cell_row)
        self.process_adjacent_cells()

    def find_adjacent_cells(self):
        adjacent_cf = []
        for row in range(-1, 2):
            for col in range(-1, 2):
                if not (row == col == 0):
                    adjacent_cf.append((row, col))

        for row in range(self.get_cells_y()):
            for col in range(self.get_cells_x()):
                neighbors = []

                for cf in adjacent_cf:
                    pos = (row + cf[0], col + cf[1])
                    if self.is_within_board((pos[0], pos[1])):
                        neighbors.append(self.get_cell_in_pos(pos))

                self.get_cell_in_pos((row, col)).adjacent_cells = neighbors

    def process_adjacent_cells(self):
        self.find_adjacent_cells()

        for row in range(self.get_cells_y()):
            for col in range(self.get_cells_x()):
                adjacent_mines = 0

                for neighbor in self.get_cell_in_pos((row, col)).adjacent_cells:
                    adjacent_mines += 1 if neighbor.is_mine() else 0

                self.get_cell_in_pos((row, col)).adjacent_mines = adjacent_mines

    def is_within_board(self, pos: tuple[int, int]):
        (x, y) = pos
        return x >= 0 and x < self.get_cells_x() and y >= 0 and y < self.get_cells_y()

    def __repr__(self):
        return repr(self.cells)

    def click_cell(self, piece: cell.Cell, flag: bool):
        if piece.is_open():
            return

        elif flag:
            self.marked_mines += -1 if piece.is_marked() else 1
            piece.toogle_flag()

        elif piece.is_closed():
            piece.open()

            if piece.is_mine():
                return

            self.found_pure += 1
            if piece.adjacent_mines != 0:
                return

            for neighbor in piece.adjacent_cells:
                if neighbor.is_pure() and neighbor.is_closed():
                    self.click_cell(neighbor, False)
