from enum import Enum
import os
import pygame

import config
import board


class GameState(Enum):
    RUN = 0
    WIN = 1
    LOSE = 2


class Game:
    """
    Creates and manages the game

    Creates a game with the passed config (`Config`), manages it, tracks the current state.
    Displays the image on the screen using the `pygame library`. The game is considered over if `state != RUN`
    """

    def __init__(self, config: config.Config):
        self.state = GameState.RUN
        self.sizes = config.screen_size
        """The size of the application window: width x height"""
        self.board = board.Board.generate_random(config)
        """A randomly generated game field that stores various game statistics"""
        self.cell_size = (
            self.sizes[0] // self.board.cells_in_board[1],
            (self.sizes[1] - 50) // self.board.cells_in_board[0],
        )
        """The size of one cell on the screen: width x height"""

        self.load_images()

    def run(self):
        """
        Initializes and runs the game, if the user opens all free cells, he wins.
        Opens a forbidden cell - loses. Accordingly, the state of the game is stored in the `state` attribute
        """
        self.screen = pygame.display.set_mode(self.sizes)
        running = True
        restart = False
        """Value restart returns true, when Space key pressed, and sends it to main.py"""
        stopwatch_image = self.get_image("stopwatch")
        flags_image = self.get_image("flags")
        """Gets images for stopwatch and flags only once per game run, unlike draw() method, which runs every turn"""
        pygame.font.init()
        """Initialization of fonts, used for results screen, stopwatch and flags counter"""

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Processes mouse button clicks
                if self.state == GameState.RUN and event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    # [2] - the third element of the tuple, which contains a bool value, whether the right button is pressed
                    is_right_click = pygame.mouse.get_pressed()[2]
                    self.handle_click(position, is_right_click)
                # Processes keyboard buttons press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Game restarted")
                        restart = True
                        running = False
                    if event.key == pygame.K_ESCAPE:
                        print("Goodbye")
                        running = False
                    # In any case, if Space or Escape pressed, the game should end
            if self.state == GameState.RUN:
                self.draw()
                pygame.display.flip()
            # draw() will only run if the game still goes, otherwise get_results() will draw results window
            self.stopwatch(stopwatch_image)
            self.flags_left(flags_image)
        self.board.close_all_cells()
        # before the restart we should close all the cells on the board
        return restart

    def handle_click(self, position: tuple[int, int], right_click: bool):
        """
        Processes the event - pressing a button on a certain pixel on the screen.

        According to the coordinates, it finds the necessary cell on the board (`board`) and calls the click function for it
        """
        # Index of the cell according to the passed coordinates. 50 is the height of top panel with stopwatch and flag counter
        if position[1] - 50 > 0:
            idx = (position[1] - 50) // self.cell_size[1], position[0] // self.cell_size[0]
            self.board.click_cell(self.board.get_cell_in_pos(idx), right_click)

            # Check if the game can be considered finished
            if not right_click and self.board.get_cell_in_pos(idx).is_mine():
                self.state = GameState.LOSE
            if self.board.found_pure == self.board.get_board_area() - self.board.num_of_mines:
                self.state = GameState.WIN
            # creates result window
            self.get_results()

    def draw(self):
        """
        Displays the game image on the screen

        Draws all game fields, selecting an image according to the state of the cell
        """
        for row in range(self.board.get_cells_y()):
            for col in range(self.board.get_cells_x()):
                cur_cell = self.board.get_cell_in_pos((row, col))
                image_path = None

                # Select the file name with the required image
                if cur_cell.is_marked():
                    image_path = "flag"
                elif cur_cell.is_open():
                    if cur_cell.is_mine():
                        image_path = "bomb"
                    else:
                        image_path = "background" if cur_cell.adjacent_mines == 0 else str(cur_cell.adjacent_mines)
                else:
                    image_path = "block"

                image = self.images[image_path]
                # Display the image on the screen, specifying the upper left pixel
                # The images were transformed to the correct sizes for us in the `load_images` method
                self.screen.blit(image, (col * self.cell_size[0], 50 + row * self.cell_size[1]))

    def load_images(self):
        """
        Loads sprites from the local device into a dictionary, transforming them to the required size
        """
        self.images = {}
        for filename in os.listdir("sprites"):
            if not filename.endswith(".png"):
                continue
            image = pygame.image.load(r"sprites/" + filename)
            # Resize
            image = pygame.transform.scale(image, self.cell_size)
            # We don't need the extension in the sprite name
            self.images[filename.split(".")[0]] = image

    """Gets images for stopwatch and flag counter. It runs only once per game for each of them"""

    def get_image(self, path):
        image = pygame.image.load(os.path.join("sprites", f"{path}.png"))
        image = pygame.transform.scale(image, (32, 32))
        return image

    """Function for stopwatch, counts time from the start of the game"""

    def stopwatch(self, stopwatch_image):
        self.screen.fill("black")
        clock = pygame.time.Clock()
        # Creates stopwatch image in the right half of the screen
        self.screen.blit(stopwatch_image, (self.sizes[0] / 1.45, 8))
        ticks = pygame.time.get_ticks()
        # Number of seconds and minutes from the beginning of the game
        # After 59 seconds it will be set to 0 seconds and add 1 to minutes
        seconds = int(ticks / 1000 % 60)
        minutes = int(ticks / 60000 % 24)
        # Better looking after 1 minute
        if seconds < 10 and minutes > 0:
            seconds = f"0{seconds}"
        # If time spent < 1 minute, we don't need to show 0 minutes
        if minutes == 0:
            font = pygame.font.SysFont("Times New Roman", 40).render(f"{seconds}", True, "gray")
        else:
            font = pygame.font.SysFont("Times New Roman", 40).render(f"{minutes:2d}:{seconds}", True, "gray")
        self.screen.blit(font, (self.sizes[0] / 1.3, 3))
        clock.tick(60)

    """Function for flags counter. It shows how much flags can be placed"""

    def flags_left(self, flags_image):
        # Number of flags left is a difference between number of mines and used flags
        flags_left = self.board.num_of_mines - self.board.marked_mines
        font = pygame.font.SysFont("Times New Roman", 40).render(f"{flags_left:2d}", True, "gray")
        self.screen.blit(flags_image, (self.sizes[0] / 3.8, 8))
        self.screen.blit(font, (self.sizes[0] / 3.3, 3))

    """Draws text for result: win or lose"""

    def get_picture_result(self, result):
        # shows the mines if we lose
        self.draw()
        pygame.display.flip()
        pygame.time.wait(1000)
        # creates another display to lay on the previous screen with board
        scrn = pygame.display.set_mode((self.sizes[0], self.sizes[1]))
        scrn.fill("black")
        # different colors of text for win and lose
        if result == "win":
            color = "#159951"
        else:
            color = "#800d0d"
        text = pygame.font.SysFont("Times New Roman", 80).render(f"You {result}!", True, color)
        text2 = pygame.font.SysFont("Times New Roman", 32).render("Press SPACE to restart", True, "gray")
        text3 = pygame.font.SysFont("Times New Roman", 32).render("ESC to exit", True, "gray")
        # field for the text
        textRect = text.get_rect()
        # result will be shown higher than info about restarting game
        textRect.center = (self.sizes[0] / 2, self.sizes[1] / 2.6)
        scrn.blit(text, textRect)
        textRect.center = (self.sizes[0] / 2, self.sizes[1] / 1.7)
        scrn.blit(text2, textRect)
        textRect.center = (self.sizes[0] / 2, self.sizes[1] / 1.4)
        scrn.blit(text3, textRect)
        pygame.display.flip()

    """Gets results for the game. GameState contains info about game state"""

    def get_results(self):
        match self.state:
            case GameState.WIN:
                self.get_picture_result("win")
            case GameState.LOSE:
                # if we lose, we can see all the mines on the field. This function opens all the mines
                for x in range(0, self.board.get_cells_x()):
                    for y in range(0, self.board.get_cells_y()):
                        if self.board.get_cell_in_pos((y, x)).is_mine():
                            self.board.get_cell_in_pos((y, x)).open()
                self.get_picture_result("lose")
