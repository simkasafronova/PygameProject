import pygame
import math

pygame.init()
size = width, height = 720, 720
screen = pygame.display.set_mode(size)
center = width // 2, height // 2

all_sprites = pygame.sprite.Group()
other_balls = pygame.sprite.Group()
main_balls = pygame.sprite.Group()


class MainBall(pygame.sprite.Sprite):
    def __init__(self, main_x, main_y, radius=20):
        super().__init__(all_sprites)
        self.add(main_balls)
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (252, 186, 3), (radius, radius), radius)
        self.rect = pygame.Rect(main_x, main_y, radius * 2, radius * 2)
        self.alpha = 0

    def update(self, *args):
        state_of_sprites = args[0]
        sprite_index = args[1]
        if state_of_sprites[sprite_index]:
            main_balls.sprites()[sprite_index].rect = main_balls.sprites()[
                sprite_index].rect.move(0, -6)


class OtherBall(pygame.sprite.Sprite):
    def __init__(self, x_coord, y_coord, radius=15):
        super().__init__(other_balls)
        self.x = x_coord
        self.y = y_coord
        self.r = radius
        self.add(other_balls)
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA,
                                    32)
        pygame.draw.circle(self.image, (63, 176, 196), (radius, radius),
                           radius)
        self.rect = pygame.Rect(self.x, self.y, radius * 2, radius * 2)
        self.alpha = 0

    def update(self, *args):
        # круговое движение, работает почему-то только на 1 спрайт
        # x_hear = round(args[0]) - self.rect.x
        # y_hear = round(args[1]) - self.rect.y
        # print(x_hear, y_hear)
        # self.rect = self.rect.move(x_hear, y_hear)
        self.rect = self.rect.move(1, 0)
        if self.rect.x == 720:
            self.rect.x = -10


ball = MainBall(300, 350)
ball2 = MainBall(300, 350)
ball3 = MainBall(300, 350)
# шары, построенные по кругу
# OtherBall(50, 350)
# OtherBall(150, 150)
# OtherBall(150, 550)
# OtherBall(350, 50)
# OtherBall(350, 650)
# OtherBall(550, 150)
# OtherBall(550, 550)
# OtherBall(650, 350)

o_b1 = OtherBall(20, 150)
o_b2 = OtherBall(200, 150)
o_b3 = OtherBall(380, 150)
o_b4 = OtherBall(560, 150)


# big_radius = 230
# alpha = 0
# v = 0.03


running_states = [0] * 20
clock = pygame.time.Clock()
main_ball_number = -1

running = True
while running:
    screen.fill((50, 68, 71))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main_ball_number += 1
                running_states[main_ball_number] = 1
    # x = center[0] + big_radius * math.cos(alpha)
    # y = center[1] + big_radius * math.sin(alpha)
    all_sprites.draw(screen)
    other_balls.draw(screen)
    other_balls.update()
    main_balls.update(running_states, main_ball_number)
    pygame.display.flip()
    clock.tick(60)
    # alpha -= v
pygame.quit()