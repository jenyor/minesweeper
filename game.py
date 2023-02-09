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
        self.board.click_cell(self.board.get_cell_in_pos(idx), right_click)

        if not right_click and self.board.get_cell_in_pos(idx).is_mine():
            self.state = GameState.LOSE
        if self.board.found_pure == self.board.get_board_area() - self.board.num_of_mines:
            self.state = GameState.WIN

        print(self.state)

    def draw(self):
        for row in range(self.board.get_cells_y()):
            for col in range(self.board.get_cells_x()):
                cur_cell = self.board.get_cell_in_pos((row, col))
                image_path = None

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
                self.screen.blit(image, (col * self.cell_size[0], row * self.cell_size[1]))

    def load_images(self):
        self.images = {}
        for filename in os.listdir("sprites"):
            if not filename.endswith(".png"):
                continue
            image = pygame.image.load(r"sprites/" + filename)
            image = pygame.transform.scale(image, self.cell_size)
            self.images[filename.split(".")[0]] = image
