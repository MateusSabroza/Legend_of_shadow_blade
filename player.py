import pygame
import sys
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((tile_size, 2*tile_size))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.jump_time = 0
        self.climb_time=0
    def get_input(self):
        # metodo para pegar o input do teclado
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            self.direction.x = 1
        elif key[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if key[pygame.K_SPACE]:
            self.jump_time += 1
            if self.jump_time < 5 and self.climb_time<3:#define o tempo de pulo e escalada maximo do player
                self.jump()

    def apply_gravity(self):
        # metodo para aplicar a gravidade
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        # metodo para atualizar o player
        self.get_input()
