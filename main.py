from initialization import *
import pygame_gui
import random
from functions import load_image, draw_lives, draw_score
from constants import *


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    many_stars = [load_image("star.png")]
    for scale in (5, 10, 20):
        many_stars.append(pygame.transform.scale(many_stars[0], (scale, scale)))

    many_hearts = [load_image("heart.png")]
    for scale in (5, 10, 20):
        many_hearts.append(pygame.transform.scale(many_hearts[0], (scale, scale)))

    def __init__(self, pos, dx, dy, name):
        super().__init__(all_sprites)
        self.add(stars)
        if name == 'star':
            self.image = random.choice(self.many_stars)
        elif name == 'heart':
            self.image = random.choice(self.many_hearts)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, item):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    if item == 'star':
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(
                numbers), 'star')
    else:
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(
                numbers), 'heart')


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
        if args[0][0]:
            main_balls.sprites()[0].rect = main_balls.sprites()[
                0].rect.move(0, -6)


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
        if self.rect.x >= 720:
            self.kill()
        self.rect = self.rect.move(3, self.vy)
        if pygame.sprite.spritecollideany(self, main_balls):
            TO_GENERATE_STARS[0] += 1
            TO_GENERATE_HEARTS[0] += 1
            coords = self.rect.x, self.rect.y
            if TO_GENERATE_STARS[0] % 7 == 0:
                create_particles(coords, 'star')
                SCORE_COUNTER[0] += 1
            if TO_GENERATE_HEARTS[0] % 11 == 0:
                create_particles(coords, 'heart')
                LIVES_COUNTER[0] += 1
            self.vy = 2
            main_balls.sprites()[0].kill()
            self.kill()
            RUNNING_STATE[0] = 0
            SCORE_COUNTER[0] += 1


for i in range(10):
    MainBall(300, 350)

clock = pygame.time.Clock()


def finish():
    finish_menu_manager = pygame_gui.UIManager((720, 720))

    another_play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 100), (150, 100)),
        text='PLAY AGAIN',
        manager=finish_menu_manager
    )

    go_to_start_menu_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 200), (150, 100)),
        text='GO TO START MENU',
        manager=finish_menu_manager
    )

    finish_menu_clock = pygame.time.Clock()
    finish_menu_running = True
    while finish_menu_running:
        time_delta2 = finish_menu_clock.tick(60) / 100
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish_menu_running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == go_to_start_menu_button:
                        finish_menu_running = False
                    elif event.ui_element == another_play_button:
                        LIVES_COUNTER[0] = 3
                        play()
                        finish_menu_running = False
            finish_menu_manager.process_events(event)
        finish_menu_manager.update(time_delta2)
        finish_menu_manager.draw_ui(screen)
        pygame.display.flip()


def play():
    main_play_running = True
    while main_play_running:
        screen.fill((50, 68, 71))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_play_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    RUNNING_STATE[0] = 1
            if event.type == TIMER_GENERATE_OTHERBALLS:
                OtherBall(0, 150)
            if event.type == TIMER_CHECK_MAINBALLS:
                try:
                    assert len(main_balls.sprites()) > 3
                    if main_balls.sprites()[0].rect.y < 0:
                        LIVES_COUNTER[0] -= 1
                        main_balls.sprites()[0].kill()
                        RUNNING_STATE[0] = 0
                        if LIVES_COUNTER[0] == 0:
                            SCORE_COUNTER[0] = 0
                            main_play_running = False
                            other_balls.empty()
                            finish()
                            for i in range(len(other_balls.sprites())):
                                other_balls.sprites()[i].kill()
                except AssertionError:
                    print('only 3 balls')
                    for i in range(7):
                        MainBall(300, 350)
        draw_score(screen)
        draw_lives(screen)
        stars.draw(screen)
        stars.update()
        all_sprites.draw(screen)
        other_balls.draw(screen)
        other_balls.update()
        main_balls.update(RUNNING_STATE)
        pygame.display.flip()
        clock.tick(60)


start_menu_manager = pygame_gui.UIManager((720, 720))
start_playing_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((330, 330), (100, 50)),
    text='PLAY',
    manager=start_menu_manager
)

start_menu_clock = pygame.time.Clock()
first_menu_running = True
while first_menu_running:
    time_delta = start_menu_clock.tick(60) / 100
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            first_menu_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_playing_button:
                    play()
        start_menu_manager.process_events(event)
    start_menu_manager.update(time_delta)
    start_menu_manager.draw_ui(screen)
    pygame.display.flip()
pygame.quit()

