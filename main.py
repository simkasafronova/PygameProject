from initialization import *
import sys
from random import choice
import pygame_gui
from functions import draw_lives, draw_score, draw_title, draw_game_over
from functions import load_image, draw_new_record
from constants import *
from classes import MainBall, OtherBall, AnimatedSprite


def terminate():
    open('record.txt', mode='w').write(str(RECORD[0]))
    pygame.quit()
    sys.exit()


for i in range(10):
    MainBall(320, 350)

clock = pygame.time.Clock()


firework = AnimatedSprite(load_image("Firework.png"), 6, 5, 250, 150)


def congratulation():
    while True:
        screen.fill((25, 25, 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    finish()
        animated.draw(screen)
        animated.update()
        draw_new_record(screen)
        pygame.display.flip()
        clock.tick(30)


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

    while True:
        time_delta2 = clock.tick(60) / 100
        screen.fill((25, 25, 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == another_play_button:
                        play()
                    elif event.ui_element == go_to_start_menu_button:
                        start_menu()
                    if event.ui_element == delete_previous_record:
                        confirmation_dialog = \
                            pygame_gui.windows.UIConfirmationDialog(
                                rect=pygame.Rect((230, 230), (300, 300)),
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
            finish_menu_manager.process_events(event)
        finish_menu_manager.update(time_delta2)
        finish_menu_manager.draw_ui(screen)
        draw_game_over(screen)
        pygame.display.flip()
        clock.tick(30)


def play():
    v_otherballs, position_otherballs = 300, 0
    while True:
        screen.fill((25, 25, 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    RUNNING_STATE[0] = 1
            if event.type == TIMER_GENERATE_OTHERBALLS:
                OtherBall(0, 150)
            if event.type == TIMER_CHANGE_MODE:
                v_otherballs = choice(MOVING_MODES)
            if event.type == TIMER_CHECK_MAINBALLS:
                if len(main_balls) <= 5:
                    for i in range(5):
                        MainBall(320, 350)
                if main_balls.sprites()[0].rect.y < 0:
                    LIVES_COUNTER[0] -= 1
                    main_balls.sprites()[0].kill()
                    RUNNING_STATE[0] = 0
                if LIVES_COUNTER[0] == 0:
                    if SCORE_COUNTER[0] > RECORD[0]:
                        RECORD[0] = SCORE_COUNTER[0]
                        SCORE_COUNTER[0] = 0
                        other_balls.empty()
                        LIVES_COUNTER[0] = 3
                        congratulation()
                    else:
                        LIVES_COUNTER[0] = 3
                        SCORE_COUNTER[0] = 0
                        other_balls.empty()
                        finish()

        draw_score(screen)
        draw_lives(screen)

        particles.draw(screen)
        particles.update()
        all_sprites.draw(screen)

        position_otherballs = v_otherballs * clock.tick() / 1000
        other_balls.draw(screen)
        other_balls.update(position_otherballs)

        main_balls.draw(screen)
        main_balls.update(RUNNING_STATE)
        pygame.display.flip()


start_menu_manager = pygame_gui.UIManager((720, 720))
start_playing_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((310, 335), (100, 50)),
    text='PLAY',
    manager=start_menu_manager
)


def start_menu():
    while True:
        time_delta = clock.tick(60) / 100
        screen.fill((25, 25, 25))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_playing_button:
                        play()
            start_menu_manager.process_events(event)
        start_menu_manager.update(time_delta)
        start_menu_manager.draw_ui(screen)
        draw_title(screen)
        pygame.display.flip()
        clock.tick(30)


start_menu()
