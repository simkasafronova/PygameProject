import pygame
import math

pygame.init()
size = width, height = 720, 720
screen = pygame.display.set_mode(size)
center = width // 2, height // 2

all_sprites = pygame.sprite.Group()
other_balls = pygame.sprite.Group()


class MainBall(pygame.sprite.Sprite):
    def __init__(self, radius=20):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (252, 186, 3), (radius, radius), radius)
        self.rect = pygame.Rect(350, 350, radius * 2, radius * 2)

    def update(self, *args):
        if args[0]:
            self.rect = self.rect.move(0, -4)


class OtherBall(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=15):
        super().__init__(all_sprites)
        self.add(other_balls)
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA,
                                    32)
        pygame.draw.circle(self.image, (63, 176, 196), (radius, radius),
                           radius)
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.alpha = 0

    def update(self, *args):
        pass


ball = MainBall()
OtherBall(50, 350)
OtherBall(150, 150)
OtherBall(150, 550)
OtherBall(350, 50)
OtherBall(350, 650)
OtherBall(550, 150)
OtherBall(550, 550)
OtherBall(650, 350)


running = True
ball_running = False
clock = pygame.time.Clock()
while running:
    screen.fill((50, 68, 71))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_running = True
    all_sprites.draw(screen)
    all_sprites.update(ball_running)
    pygame.display.flip()
    clock.tick(50)
pygame.quit()