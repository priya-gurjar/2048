import pygame
from uitls import get_digits_of_number


class Tile(pygame.sprite.Sprite):
    def __init__(self, value, top, left, tile_board_location_i, tile_board_location_j, width=100, height=100,
                 font_size=50):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color(pygame.Color('#FFDAB9')))
        self.rect = self.image.get_rect()
        self.i = tile_board_location_i
        self.j = tile_board_location_j
        self.font = pygame.font.SysFont('Comic Sans MS', font_size)
        self.value = value
        self.top = top
        self.left = left
        self.rect = self.image.get_rect(top=top, left=left)

    def get_color(self):
        # generate color in gradient from light orange to orange for values till 64
        # and generate colors from dark yellow to bright yellow for values from 128 to 2048
        color_choice = {
            2: pygame.Color('#FFDAB9'),
            4: pygame.Color('#FFC0CB'),
            8: pygame.Color('#FFB6C1'),
            16: pygame.Color('#FFAEB9'),
            32: pygame.Color('#FFA07A'),
            64: pygame.Color('#FF8C00'),
            128: pygame.Color('#FFD700'),
            256: pygame.Color('#FFFF00'),
            512: pygame.Color('#FFFFE0'),
            1024: pygame.Color('#FFFFF0'),
            2048: pygame.Color('#FFFFFF')
        }
        return color_choice[self.value]

    def update(self, *args, **kwargs):
        game_state = args[0]
        current_game_board = game_state.get_current_board()
        self.value = current_game_board[self.i][self.j]

        if self.value:
            self.image.fill(self.get_color())

            if get_digits_of_number(self.value) > 3:
                self.font = pygame.font.SysFont('Comic Sans MS', 30)
            elif get_digits_of_number(self.value) > 2:
                self.font = pygame.font.SysFont('Comic Sans MS', 40)
            else:
                self.font = pygame.font.SysFont('Comic Sans MS', 50)
            text = self.font.render(str(self.value), True, pygame.Color('black'))
            text_rect = text.get_rect(center=(self.rect.width / 2, self.rect.height / 2))
            self.image.blit(text, text_rect)
        else:
            self.image.fill(pygame.Color('#FFDAB9'))


def get_game_tiles(game_height, game_width, game_logic_state=None):
    margin_left = (game_width - (100 * 4 + 10 * 3)) / 2
    margin_top = (game_height - (100 * 4 + 10 * 3)) / 2
    tiles = []
    board = game_logic_state.get_current_board()
    for row in range(4):
        for column in range(4):
            tiles.append(
                Tile(board[row][column], margin_top + (100 + 10) * row, margin_left + (100 + 10) * column, row, column))
    return tiles
