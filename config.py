class Config:
    """
    Налаштуваня гри, яке передається мій компонентами гри, щоб вони дістали потрібні їм атрибути
    """

    def __init__(
        self,
        cells_in_board: tuple[int, int],
        num_of_mines: int,
        screen_size: tuple[int, int],
    ):
        self.cells_in_board = cells_in_board
        """К-сть рядків та стовпчиків клітинок (полів для потенційних мін)"""
        self.num_of_mines = num_of_mines
        """К-сть мін на дошці гри"""
        self.screen_size = screen_size
        """Розмір полотна гри, тобто самого застосунку"""
