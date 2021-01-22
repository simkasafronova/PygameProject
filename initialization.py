import pygame

pygame.init()
size = width, height = 720, 720
screen = pygame.display.set_mode((720, 720))
screen_rect = (0, 0, width, height)

TIMER_GENERATE_OTHERBALLS = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_GENERATE_OTHERBALLS, 1000)

TIMER_CHECK_MAINBALLS = pygame.USEREVENT + 2
pygame.time.set_timer(TIMER_CHECK_MAINBALLS, 400)

TIMER_CHANGE_MODE = pygame.USEREVENT + 3
pygame.time.set_timer(TIMER_CHANGE_MODE, 4000)
