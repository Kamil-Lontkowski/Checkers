import pygame
import pygame_menu

from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, WHITE, ROWS
from checkers.game import Game

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CHECKERS")
FPS = 60
DIFF = 3
pygame.init()
MODE = 1
PBLACK = 1
PWHITE = 1


def end_screen(winner: str, moves: int):
    pygame.font.init()
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        WIN.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(WIN, (128, 128, 50),
                                 (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        large_font = pygame.font.SysFont('comicsans', 80)
        title = large_font.render(f'{winner} wins!', True, WHITE)
        h, w = title.get_rect().height, title.get_rect().width
        moves_info = large_font.render(f'In {moves} moves!', True, WHITE)
        hm, wm = title.get_rect().height, title.get_rect().width
        WIN.blit(title, (WIDTH // 2 - w // 2, (HEIGHT // 2 - h // 2) - h // 2))
        WIN.blit(moves_info, (WIDTH // 2 - wm // 2, (HEIGHT // 2 - hm // 2) + h // 2))
        pygame.display.update()


def get_pos_from_mouse(pos: tuple[int, int]):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def bgfun():
    for row in range(ROWS):
        for col in range(row % 2, ROWS, 2):
            pygame.draw.rect(WIN, (128, 128, 50),
                             (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def set_diff(value, diff):
    global DIFF
    DIFF = diff


def set_black(value, algo):
    global PBLACK
    PBLACK = algo


def set_white(value, algo):
    global PWHITE
    PWHITE = algo


def set_mode(value, mode):
    global MODE
    MODE = mode


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN, MODE, DIFF, PWHITE, PBLACK)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_pos_from_mouse(pos)
                game.select(row, col)
        if game.winner == 'BLACK':
            end_screen('Black', game.black_moves)
            break
        elif game.winner == 'WHITE':
            end_screen('White', game.white_moves)
            break
        if not run:
            break
        game.update()


def menu_display():
    menu = pygame_menu.Menu('Checkers', WIDTH // 1.6, HEIGHT // 1.6,
                            theme=pygame_menu.themes.THEME_DARK)

    menu.add.button('Play', main)
    menu.add.selector('Difficulty :', [('Easy', 1), ('Not so easy', 2), ('Medium', 3),
                                       ('Hard', 4), ('Harder', 5)], onchange=set_diff, default=2)
    menu.add.selector('Mode: ', [('PvP', 1), ('Player vs AI', 2), ('AI vs AI', 3), ('AI vs Random', 4)],
                      onchange=set_mode)
    menu.add.selector('Black algo: ', [("Minimax", 1), ("Alfabeta", 2)], onchange=set_black)
    menu.add.selector('White algo: ', [("Minimax", 1), ("Alfabeta", 2)], onchange=set_white)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(WIN, bgfun=bgfun)


if __name__ == "__main__":
    menu_display()
