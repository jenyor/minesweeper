class Config:
    """
    Налаштуваня гри, яке передається мій компонентами гри, щоб вони дістали потрібні їм атрибути
    """

    def __init__(
        self,
        cells_in_board: tuple[int, int],
        num_of_mines: int,
        screen_size: tuple[int, int],
        difficulty: str
    ):
        self.cells_in_board = cells_in_board
        """К-сть рядків та стовпчиків клітинок (полів для потенційних мін)"""
        self.num_of_mines = num_of_mines
        """К-сть мін на дошці гри"""
        self.screen_size = screen_size
        """Розмір полотна гри, тобто самого застосунку"""
        self.difficulty = difficulty
        """Один з пресетів складності гри (easy, medium, hard, custom)"""
    def check_values(self):
        if (self.difficulty != "easy" and self.difficulty != "medium" and
                self.difficulty != "hard" and self.difficulty != "custom"):
            raise Exception("There is no such difficulty")
        elif (self.screen_size[0] <= 0 or self.screen_size[1] <= 0 or
              self.num_of_mines <= 0 or self.cells_in_board[0] <= 0 or self.cells_in_board[1] <= 0):
            raise Exception("Values of screen size, number of mines and fields can't be 0 or negative")
        elif (self.num_of_mines >= self.cells_in_board[0] * self.cells_in_board[1]):
            raise Exception("Too much mines for this field")

    def set_difficulty(self):
        match self.difficulty:
            case "easy":
                self.num_of_mines = 10
                self.cells_in_board = (9, 9)
            case "medium":
                self.num_of_mines = 40
                self.cells_in_board = (16, 16)
            case "hard":
                self.num_of_mines = 99
                self.cells_in_board = (16, 30)
                self.screen_size = (1240, 670)
