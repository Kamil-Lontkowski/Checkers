import pygame

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

PADDING = 15
BORDER = 2

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 100)
GREY = (128, 128, 128)
PURPLE = (230, 230, 250)
GREEN = (63, 219, 139)
PINK = (235, 71, 164)
COLORS = [BLUE, PURPLE, PINK, GREEN]
CROWN = pygame.image.load('./checkers/assets/crown.png')
CROWN = pygame.transform.scale(CROWN, (HEIGHT // 20, WIDTH // 35))
