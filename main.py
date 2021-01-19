from initialization import *
import pygame_gui
from functions import draw_lives, draw_score, draw_title, draw_game_over
from functions import load_image, draw_new_record
from constants import *
from classes import MainBall, OtherBall, AnimatedSprite


for i in range(10):
    MainBall(320, 350)

clock = pygame.time.Clock()


firework = AnimatedSprite(load_image("Firework.png"), 6, 5, 250, 150)


def congratulation():
    congr_running = True
    congr_clock = pygame.time.Clock()
    while congr_running:
        screen.fill((25, 25, 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                congr_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    congr_running = False
                    finish()
        animated.draw(screen)
        animated.update()
        draw_new_record(screen)
        pygame.display.flip()
        congr_clock.tick(30)


def finish():
    finish_menu_manager = pygame_gui.UIManager((720, 720))

    another_play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((285, 300), (190, 70)),
        text='PLAY AGAIN',
        manager=finish_menu_manager
    )

    go_to_start_menu_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((285, 400), (190, 70)),
        text='GO TO START MENU',
        manager=finish_menu_manager
    )

    delete_previous_record = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((285, 500), (190, 70)),
        text='DELETE PREVIOUS RECORD',
        manager=finish_menu_manager
    )

    finish_menu_clock = pygame.time.Clock()
    finish_menu_running = True
    while finish_menu_running:
        time_delta2 = finish_menu_clock.tick(60) / 100
        screen.fill((25, 25, 25))
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
                    if event.ui_element == delete_previous_record:
                        confirmation_dialog = \
                            pygame_gui.windows.UIConfirmationDialog(
                                rect=pygame.Rect((260, 260), (200, 200)),
                                manager=finish_menu_manager,
                                window_title='Подтверждение',
                                action_long_desc='Вы уверены, что хотите '
                                                 'обнулить свой рекорд?',
                                action_short_name='YES',
                                blocking=True
                            )
                if event.user_type == \
                        pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    RECORD[0] = 0
                    print('record has been switched off')
            finish_menu_manager.process_events(event)
        finish_menu_manager.update(time_delta2)
        finish_menu_manager.draw_ui(screen)
        draw_game_over(screen)
        pygame.display.flip()


def play():
    main_play_running = True
    while main_play_running:
        screen.fill((25, 25, 25))
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
                            if SCORE_COUNTER[0] > RECORD[0]:
                                print('new record!')
                                congratulation()
                                main_play_running = False
                                RECORD[0] = SCORE_COUNTER[0]
                            SCORE_COUNTER[0] = 0
                            main_play_running = False
                            other_balls.empty()
                            finish()
                            try:
                                for i in range(len(other_balls.sprites())):
                                    other_balls.sprites()[i].kill()
                            except IndexError:
                                pass
                except AssertionError:
                    print('only 3 balls')
                    for i in range(7):
                        MainBall(320, 350)
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
    relative_rect=pygame.Rect((310, 335), (100, 50)),
    text='PLAY',
    manager=start_menu_manager
)

start_menu_clock = pygame.time.Clock()
first_menu_running = True
while first_menu_running:
    time_delta = start_menu_clock.tick(60) / 100
    screen.fill((25, 25, 25))
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
    draw_title(screen)
    pygame.display.flip()
pygame.quit()

