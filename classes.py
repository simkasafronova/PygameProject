from constants import *
from particles import create_particles


class MainBall(pygame.sprite.Sprite):
    def __init__(self, main_x, main_y, radius=20):
        super().__init__(all_sprites)
        self.add(main_balls)
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (48, 217, 255), (radius, radius), radius)
        self.rect = pygame.Rect(main_x, main_y, radius * 2, radius * 2)
        self.pos = 350

    def update(self, *args):
        if args[0][0]:
            main_balls.sprites()[0].rect = main_balls.sprites()[
                0].rect.move(0, -2)


class OtherBall(pygame.sprite.Sprite):
    def __init__(self, x_coord, y_coord, radius=15):
        super().__init__(other_balls)
        self.x = x_coord
        self.y = y_coord
        self.r = radius
        self.add(other_balls)
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA,
                                    32)
        pygame.draw.circle(self.image, (80, 255, 80), (radius, radius),
                           radius)
        self.rect = pygame.Rect(self.x, self.y, radius * 2, radius * 2)
        self.pos = 0

    def update(self, *args):
        if self.rect.x >= 720:
            self.kill()
        self.pos += args[0]
        vx = self.pos - self.rect.x
        self.rect = self.rect.move(vx, 0)
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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(animated)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]