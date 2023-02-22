import cell
import config
import random


class Board:
    """
    Board containing a table of cells and storing various statistics to understand the game state
    """

    def __init__(self, cells_in_board: tuple[int, int], num_of_mines: int, cells=[]):
        """
        It is recommended to use the class method `generate_random`. __init__ for testing or generating a non-random board
        """
        self.cells_in_board = cells_in_board
        """Size of table with cells: height x width"""
        self.num_of_mines = num_of_mines
        """Number of mines on the field"""
        self.found_pure = 0
        """How many cells on the field are ordinary and open"""
        self.marked_mines = 0
        """How many cells on the field are marked with a flag"""
        self.cells = cells
        """Table with cells"""

    @classmethod
    def generate_random(cls, config: config.Config):
        """
        Generates a board by randomly placing mines. Use instead of the constructor `__init__`
        """
        inst = cls(config.cells_in_board, config.num_of_mines)

        inst.generate_cells()

        return inst

    def get_cells_x(self):
        """Size of the field along the x axis - width"""
        return self.cells_in_board[1]

    def get_cells_y(self):
        """Size of the field along the y axis - height"""
        return self.cells_in_board[0]

    def get_cell_in_pos(self, idx: tuple[int, int]):
        """The cell at a certain position in the table"""
        return self.cells[idx[0]][idx[1]]

    def get_all_cells(self):
        return self.cells

    def get_board_area(self):
        """Field area: total number of cells"""
        return self.cells_in_board[0] * self.cells_in_board[1]

    def tuple_index_to_raw(self, index: tuple[int, int]):
        """Number in the table by index, as if the rows of the table were in one row"""
        return index[0] * self.get_cells_x() + index[1]

    def generate_cells(self):
        """Randomly generate a table of cells and place mines"""
        # Generate all table indexes and select those where we will put mines
        mines_position = random.sample(list(range(0, self.get_board_area())), self.num_of_mines)
        mines_position.sort(reverse=True)

        for row in range(self.get_cells_y()):
            cell_row = []
            for col in range(self.get_cells_x()):
                is_mine = len(mines_position) and mines_position[-1] == self.tuple_index_to_raw((row, col))
                # Create a mine or an ordinary cell depending on whether the number of this cell was randomly selected
                if is_mine:
                    cell_row.append(cell.Cell.new_mine())
                    mines_position.pop(-1)
                else:
                    cell_row.append(cell.Cell.new_pure())

            self.cells.append(cell_row)
        self.process_adjacent_cells()

    def find_adjacent_cells(self):
        """For each cell, form a list containing all neighboring cells that do not go beyond the table boundaries"""
        adjacent_cf = []
        # 3x3 - without the center
        for row in range(-1, 2):
            for col in range(-1, 2):
                if not (row == col == 0):
                    adjacent_cf.append((row, col))

        for row in range(self.get_cells_y()):
            for col in range(self.get_cells_x()):
                neighbors = []

                for cf in adjacent_cf:
                    pos = (row + cf[0], col + cf[1])
                    # Check that the coordinate does not go beyond the table boundaries
                    if self.is_within_board((pos[0], pos[1])):
                        neighbors.append(self.get_cell_in_pos(pos))

                self.get_cell_in_pos((row, col)).adjacent_cells = neighbors

    def process_adjacent_cells(self):
        """Find out how many neighboring mines each cell on the board has"""
        self.find_adjacent_cells()

        for row in range(self.get_cells_y()):
            for col in range(self.get_cells_x()):
                adjacent_mines = 0

                for neighbor in self.get_cell_in_pos((row, col)).adjacent_cells:
                    adjacent_mines += 1 if neighbor.is_mine() else 0

                self.get_cell_in_pos((row, col)).adjacent_mines = adjacent_mines

    def is_within_board(self, pos: tuple[int, int]):
        """Does the coordinate not go beyond the table boundaries"""
        (y, x) = pos
        return x >= 0 and x < self.get_cells_x() and y >= 0 and y < self.get_cells_y()

    def __repr__(self):
        return repr(self.cells)

    def click_cell(self, piece: cell.Cell, flag: bool):
        """Click on a cell. Recursively called for all adjacent empty cells in some cases"""
        if piece.is_open():
            return

        elif flag:
            if piece.is_marked():
                self.marked_mines -= 1
                piece.toogle_flag()
            elif (self.marked_mines < self.num_of_mines):
                self.marked_mines += 1
                piece.toogle_flag()

        elif piece.is_closed():
            piece.open()

            if piece.is_mine():
                return

            self.found_pure += 1
            if piece.adjacent_mines != 0:
                return

            # Recursive call for adjacent cells if they are closed, not mines, and if the current cell has no mines nearby
            for neighbor in piece.adjacent_cells:
                if neighbor.is_pure() and neighbor.is_closed():
                    self.click_cell(neighbor, False)

    def close_all_cells(self):
        for row in range(self.get_cells_y()):
            for col in range(self.get_cells_x()):
                self.get_cell_in_pos((row, col)).close()
