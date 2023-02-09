from enum import Enum
import os
import pygame

import config
import board
import cell


class GameState(Enum):
    RUN = 0
    WIN = 1
    LOSE = 2


class Game:
    def __init__(self, config: config.Config):
        self.state = GameState.RUN
        self.sizes = config.screen_size
        self.board = board.Board().generate_random(config)
        self.cell_size = (
            self.sizes[0] // self.board.cells_in_board[1],
            self.sizes[1] // self.board.cells_in_board[0],
        )
        """ x-width x y-height """

        self.load_images()

    def run(self):
        self.screen = pygame.display.set_mode(self.sizes)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.state == GameState.RUN and event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    is_right_click = pygame.mouse.get_pressed()[2]
                    self.handle_click(position, is_right_click)
            self.draw()
            pygame.display.flip()

    def handle_click(self, position: tuple[int, int], right_click: bool):
        idx = position[1] // self.cell_size[1], position[0] // self.cell_size[0]
        self.board.click_cell(idx, right_click)
        print("Pure: ", self.board.found_pure, "Flags: ", self.board.marked_mines)
        if (
            not right_click
            and self.board.cells[idx[0]][idx[1]].type == cell.CellType.MINE
        ):
            self.state = GameState.LOSE
        if (
            self.board.found_pure
            == self.board.cells_in_board[0] * self.board.cells_in_board[1]
            - self.board.num_of_mines
        ):
            self.state = GameState.WIN

        print(self.state)

    def draw(self):
        for row in range(self.board.cells_in_board[0]):
            for column in range(self.board.cells_in_board[1]):
                cur_cell = self.board.cells[row][column]
                if cur_cell.state == cell.CellState.MARKED:
                    image = self.images["flag"]
                elif cur_cell.state == cell.CellState.OPEN:
                    if cur_cell.type == cell.CellType.MINE:
                        image = self.images["bomb"]
                    else:
                        image = (
                            self.images["background"]
                            if cur_cell.adjacent_mines == 0
                            else self.images[str(cur_cell.adjacent_mines)]
                        )
                else:
                    image = self.images["block"]
                self.screen.blit(
                    image, (column * self.cell_size[0], row * self.cell_size[1])
                )

    def load_images(self):
        self.images = {}
        for filename in os.listdir("sprites"):
            if not filename.endswith(".png"):
                continue
            image = pygame.image.load(r"sprites/" + filename)
            image = pygame.transform.scale(image, self.cell_size)
            self.images[filename.split(".")[0]] = image
