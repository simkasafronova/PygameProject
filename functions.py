import pygame
import os
import sys
from constants import *


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_score(surf):
    score_text = str(SCORE_COUNTER[0])
    font = pygame.font.Font(None, 50)
    text = font.render('Счет: ' + score_text, True, (100, 255, 100))
    text_x, text_y = 20, 600
    text_w, text_h = text.get_width(), text.get_height()
    surf.blit(text, (text_x, text_y))
    pygame.draw.rect(surf, (0, 255, 0), (text_x - 10, text_y - 10, text_w +
                                         20, text_h + 20), 1)


def draw_lives(surf):
    score_text = str(LIVES_COUNTER[0])
    font = pygame.font.Font(None, 50)
    text = font.render('Жизни: ' + score_text, True, (255, 100, 100))
    text_x, text_y = 540, 600
    text_w, text_h = text.get_width(), text.get_height()
    surf.blit(text, (text_x, text_y))
    pygame.draw.rect(surf, (255, 0, 0), (text_x - 10, text_y - 10, text_w +
                                         20, text_h + 20), 1)