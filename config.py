class Config:
    def __init__(
        self,
        cells_in_board: tuple[int, int],
        num_of_mines: int,
        screen_size: tuple[int, int],
    ):
        self.cells_in_board = cells_in_board
        """к-сть рядків та стовпчиків"""
        self.num_of_mines = num_of_mines
        self.screen_size = screen_size
