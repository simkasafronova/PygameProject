import pygame


all_sprites = pygame.sprite.Group()
other_balls = pygame.sprite.Group()
main_balls = pygame.sprite.Group()
animated = pygame.sprite.Group()
particles = pygame.sprite.Group()


TO_GENERATE_STARS = [0]
TO_GENERATE_HEARTS = [0]

GRAVITY = 0.1

SCORE_COUNTER = [0]
LIVES_COUNTER = [3]

RUNNING_STATE = [0]

RECORD = [0]