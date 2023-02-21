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
    Створює та управляє грою

    За переданим конфігом (`Config`) створює гру, керує нею, відслідковує поточний стан.
    Виводить картинку на екран через `pygame library`. Гра вважається звершеною, якщо `state != RUN`
    """

    def __init__(self, config: config.Config):
        self.state = GameState.RUN
        self.sizes = config.screen_size
        """ Розмір вікна застосунку: ширина х висота"""
        self.board = board.Board.generate_random(config)
        """Випадкового згенероване поле гри, яке зберігає в собі різну статистику гри"""
        self.cell_size = (
            self.sizes[0] // self.board.cells_in_board[1],
            self.sizes[1] // self.board.cells_in_board[0],
        )
        """Розмір одної клітинки на екрані: ширина х висота """
        self.load_images()

    def run(self):
        """
        Ініціалізує і запускає гру, якщо користувач відкриє всі вільні клітинки, то переможе.
        Відкриє заборонену клітинку - програє. Відповідно, стан гри зберігається у атрибуті `state`
        """
        self.screen = pygame.display.set_mode(self.sizes)
        running = True
        restart = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Опрацьовує настискання кнопок миші
                if self.state == GameState.RUN and event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    # [2] - третій елемент tuple, який містить у собі bool значення, чи натиснута права кнопка
                    is_right_click = pygame.mouse.get_pressed()[2]
                    self.handle_click(position, is_right_click)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Game restarted")
                        restart = True
                    if event.key == pygame.K_ESCAPE:
                        print("Goodbye")
                    running = False
            if self.state == GameState.RUN:
                self.draw()
                pygame.display.flip()
        self.board.close_all_cells()
        return restart

    def handle_click(self, position: tuple[int, int], right_click: bool):
        """
        Опрацьовує подію - натискання кнопки на певний піксель на екрані.

        Відповідно до координат знаходить потрібну клітинку на дошці (`board`) і викликає для неї функцію натискання
        """
        # Індекс клітинки відповідно до переданих координат
        idx = position[1] // self.cell_size[1], position[0] // self.cell_size[0]
        self.board.click_cell(self.board.get_cell_in_pos(idx), right_click)

        # Перевірка, чи гру можна вважати завершеною
        if not right_click and self.board.get_cell_in_pos(idx).is_mine():
            self.state = GameState.LOSE
        if self.board.found_pure == self.board.get_board_area() - self.board.num_of_mines:
            self.state = GameState.WIN
        self.get_results()

    def draw(self):
        """
        Виводить картинку гри на екран

        Малює всі поля гри, підбираючи картинку відповідно до стану клітинки
        """
        for row in range(self.board.get_cells_y()):
            for col in range(self.board.get_cells_x()):
                cur_cell = self.board.get_cell_in_pos((row, col))
                image_path = None

                # Обираємо назву файлу з потрібною картинкою
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
                # Виводимо картинку на екран, вказуючи лівий верхній піксель
                # Картинки були трансформовані у правильні нам розміри у методі `load_images`
                self.screen.blit(image, (col * self.cell_size[0], row * self.cell_size[1]))

    def load_images(self):
        """
        Завантажує спрайти з локального девайсу у словник, перетворюючи на потрібні нам розміри
        """
        self.images = {}
        for filename in os.listdir("sprites"):
            if not filename.endswith(".png"):
                continue
            image = pygame.image.load(r"sprites/" + filename)
            # Змінюємо розмір
            image = pygame.transform.scale(image, self.cell_size)
            # Розширення нам не потрібне у назві спрайта
            self.images[filename.split(".")[0]] = image

    def get_picture_result(self, result):
        pygame.font.init()
        self.draw()
        pygame.display.flip()
        pygame.time.wait(2000)
        scrn = pygame.display.set_mode((self.sizes[0], self.sizes[1]))
        if result == 'win':
            scrn.fill("black")
            color = "#159951"
        else:
            scrn.fill("black")
            color = "#800d0d"
        text = pygame.font.SysFont('Times New Roman', 80).render(f"You {result}!", True, color)
        text2 = pygame.font.SysFont('Times New Roman', 32).render('Press SPACE to restart, ESC to exit', True, "gray")
        textRect = text.get_rect()
        textRect.center = (self.sizes[0]/2, self.sizes[1]/2.6)
        scrn.blit(text, textRect)
        textRect.center = (self.sizes[0]/2.3, self.sizes[1]/1.9)
        scrn.blit(text2, textRect)
        pygame.display.flip()

    def get_results(self):
        match self.state:
            case GameState.WIN:
                self.get_picture_result("win")
            case GameState.LOSE:
                for x in range(0, self.board.get_cells_x()):
                    for y in range(0, self.board.get_cells_y()):
                        if self.board.get_cell_in_pos((y, x)).is_mine():
                            self.board.get_cell_in_pos((y, x)).open()
                self.get_picture_result("lose")
