from enum import Enum

import pygame

class DisplayFigure(Enum):
    P = '♟'
    K = '♚'
    Q = '♛'
    R = '♜'
    B = '♝'
    N = '♞'

class DisplayManager:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.screen_width, self.screen_height = 920, 920
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.margin = 0
        self.width = 0
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)


        self.font = pygame.font.Font("data/Segoe-UI-Symbol.ttf", 32)
        self.fields = self.generate_fields()

    def run(self):

        running = True
        dt = 0

        input_text = ""


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Naciśnięcie Enter
                        print(f"Entered: {input_text}")
                        self.game_manager.process_move(input_text)
                        input_text = ""  # Resetuj tekst po wprowadzeniu
                    elif event.key == pygame.K_BACKSPACE:  # Naciśnięcie Backspace
                        input_text = input_text[:-1]  # Usuń ostatni znak
                    else:
                        input_text += event.unicode  # Dodaj wprowadzony znak


            self.display_all(input_text)

            pygame.display.flip()
            dt = self.clock.tick(15) / 1000


    def generate_fields(self):
        self.margin = 40
        self.width = (self.screen_width - 2 * self.margin) / 8
        fields = []

        for i in range(8):
            row = []
            for j in range(8):
                rect = pygame.Rect(self.margin + j * self.width, self.margin + i * self.width, self.width, self.width)
                row.append(rect)
            fields.append(row)


        return fields

    def display_all(self, input_text):
        self.display_backgroudn()
        self.display_text(input_text)
        self.display_figures()

    def display_backgroudn(self):
        self.screen.fill((125, 125, 125))

        k = 0
        for i in self.fields:
            for j in i:
                color = self.white if k % 2 == 0 else self.black
                pygame.draw.rect(self.screen, color, j)
                k += 1
            k += 1

    def display_text(self, input_text):
        letter = 97
        for i in self.fields[0]:

            text_surface = self.font.render(chr(letter), True, (0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = i.center
            text_rect.y = text_rect.y // 2 - text_rect.height

            self.screen.blit(text_surface,  text_rect)
            letter += 1

        number = 8
        for row in self.fields:

            text_surface = self.font.render(str(number), True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = row[0].center
            text_rect.x = text_rect.x // 2 - text_rect.width - self.margin // 2
            self.screen.blit(text_surface, text_rect)
            number -= 1

        text_surface = self.font.render(input_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (0, self.screen.get_height() - text_surface.get_height()))


    def display_figures(self):

        k = 0
        piece_font = pygame.font.Font("data/Segoe-UI-Symbol.ttf", 64)


        for i in range(8):
            for j in range(8):
                piece = self.game_manager.game_board.get_figure_from_coords(i, j)
                if piece is not None:
                    color = self.white if piece.is_white() else self.black
                    piece_sign = piece.get_letter()
                    icon = DisplayFigure[piece_sign].value
                    rect = self.fields[i][j]

                    if piece_sign == 'K' and piece.is_white():
                        if self.game_manager.tell_if_king_under_attack(self.game_manager.white_player):
                            outline_surface = piece_font.render(icon, True, (255,0 ,0))
                        else:
                            outline_surface = piece_font.render(icon, True, (0, 255, 0))
                    elif piece_sign == 'K' and not piece.is_white():
                        if self.game_manager.tell_if_king_under_attack(self.game_manager.black_player):
                            outline_surface = piece_font.render(icon, True, (255,0 ,0))
                        else:
                            outline_surface = piece_font.render(icon, True, (0, 255, 0))
                    else:
                        outline_surface = piece_font.render(icon, True, (0,255,0))
                    outline_rect = outline_surface.get_rect()
                    outline_rect.center = rect.center

                    for x_offset in [-2, 0, 2]:
                        for y_offset in [-2, 0, 2]:
                            if x_offset != 0 or y_offset != 0:
                                self.screen.blit(outline_surface, (outline_rect.x + x_offset, outline_rect.y + y_offset))

                    text_surface = piece_font.render(icon, True, color)
                    text_rect = text_surface.get_rect()
                    text_rect.center = rect.center

                    self.screen.blit(text_surface, text_rect)
                k += 1
            k += 1







