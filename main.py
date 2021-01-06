import pygame

pygame.init()
size = width, height = 720, 720
screen = pygame.display.set_mode(size)
center = width // 2, height // 2

all_sprites = pygame.sprite.Group()
other_balls = pygame.sprite.Group()
main_balls = pygame.sprite.Group()

TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 700)


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
        self.vy = 0

    def update(self, *args):
        self.rect = self.rect.move(3, self.vy)
        if pygame.sprite.spritecollideany(self, main_balls):
            self.vy = 2


for i in range(5):
    MainBall(300, 350)


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
        if event.type == TIMER_EVENT:
            print('Timer works well!')
            OtherBall(0, 150)
    all_sprites.draw(screen)
    other_balls.draw(screen)
    other_balls.update()
    main_balls.update(running_states, main_ball_number)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()