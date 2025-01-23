import pygame
# Directory: utils/styles.py
WIDTH = 1400
HEIGHT = 800

# New color palette
RED_BG = (41, 54, 111)  # #29366f
WHITE = (244, 244, 244)  # #f4f4f4
BLACK = (51, 60, 87)  # #333c57
GREEN = (58, 93, 201)  # #3b5dc9
YELLOW = (65, 166, 246)  # #41a6f6
BLUE = (115, 239, 247)  # #73eff7
GRAY = (148, 176, 194)  # #94b0c2
BACKGROUND_COLOR = (41, 54, 111)  # #29366f

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Fonts & Colors
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 25)
TITLE_FONT = pygame.font.SysFont("None", 50, bold= False)
INSTR_FONT = pygame.font.SysFont("None", 32)
