import pygame
from sys import exit

from gameLogic import GameLogic
from sprites import get_game_tiles


pygame.init()
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 40)
game = GameLogic()
game.initialise_board()

tiles_group = pygame.sprite.Group()
tiles = get_game_tiles(screen.get_height(), screen.get_width(), game)

for tile in tiles:
    tiles_group.add(tile)

# game score box
score_box = pygame.Surface((screen.get_width(), 100))
score_box.fill(pygame.Color('#BBADA0'))
score_box_rect = score_box.get_rect(top=0, left=0)
score_text = font.render('Score: ' + str(game.get_score()), True, pygame.Color('black'))
score_text_rect = score_text.get_rect(center=(score_box_rect.width / 2, score_box_rect.height / 2))
score_box.blit(score_text, score_text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if game.get_over() or game.get_won():
                pygame.quit()
                exit()
            if event.key == pygame.K_UP:
                game.capture_move_up()
            elif event.key == pygame.K_DOWN:
                game.capture_move_down()
            elif event.key == pygame.K_LEFT:
                game.capture_move_left()
            elif event.key == pygame.K_RIGHT:
                game.capture_move_right()

    screen.fill(pygame.Color('#FAF8EF'))
    score_box.fill(pygame.Color('#BBADA0'))
    score_text = font.render('Score: ' + str(game.get_score()), True, pygame.Color('black'))
    score_text_rect = score_text.get_rect(center=(score_box_rect.width / 2, score_box_rect.height / 2))
    score_box.blit(score_text, score_text_rect)
    screen.blit(score_box, score_box_rect)
    if game.get_over():
        font = pygame.font.SysFont('Comic Sans MS', 50)
        text = font.render('You Lost', True, pygame.Color('black'))
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(text, text_rect)
    elif game.get_won():
        font = pygame.font.SysFont('Comic Sans MS', 50)
        text = font.render('You Won', True, pygame.Color('black'))
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(text, text_rect)
    else:
        tiles_group.update(game)
        tiles_group.draw(screen)

    pygame.display.flip()
    # this line ensures that the game runs at 60 fps max, we are doing this so that the game does not run too fast
    # the problem with running to fast would be that we would do the changes in pixel on each frame and the user would
    # not be able to see the changes or the changes will cause large effects on the game
    # for example if we move a player 1px each frame we would move 100px if the game runs at 100 fps,
    # and we will run 60px if the game runs at 60 fps
    clock.tick(60)
