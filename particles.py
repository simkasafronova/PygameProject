from initialization import *
from constants import GRAVITY
from functions import load_image
import random


class Particle(pygame.sprite.Sprite):
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
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, item):
    particle_count = 20
    numbers = range(-5, 6)
    if item == 'star':
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(
                numbers), 'star')
    else:
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(
                numbers), 'heart')