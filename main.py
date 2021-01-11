import pygame
import pygame_gui

pygame.init()
size = width, height = 720, 720
screen = pygame.display.set_mode((720, 720))

all_sprites = pygame.sprite.Group()
other_balls = pygame.sprite.Group()
main_balls = pygame.sprite.Group()
0
TIMER_GENERATE_OTHERBALLS = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_GENERATE_OTHERBALLS, 700)

TIMER_CHECK_MAINBALLS = pygame.USEREVENT + 2
pygame.time.set_timer(TIMER_CHECK_MAINBALLS, 200)


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
        self.rect = self.rect.move(3, self.vy)
        if pygame.sprite.spritecollideany(self, main_balls):
            self.vy = 2
            main_balls.sprites()[0].kill()
            RUNNING_STATE[0] = 0
            SCORE_COUNTER[0] += 1


# почему-то последний спрайт летит медленнее предыдущих
for i in range(10):
    MainBall(300, 350)


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


SCORE_COUNTER = [0]
LIVES_COUNTER = [3]
RUNNING_STATE = [0]
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
        #print('finish menu')
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
                            main_play_running = False
                            finish()
                except AssertionError:
                    print('only 3 balls')
                    for i in range(7):
                        MainBall(300, 350)
        #print('play')
        draw_score(screen)
        draw_lives(screen)
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
    #print('first menu')
    pygame.display.flip()
pygame.quit()

