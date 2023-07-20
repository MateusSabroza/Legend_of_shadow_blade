import pygame
from settings import *
from player import import_folder
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.initial_pos = pos
        self.import_character_assets()
        self.frame_index = 0
        self.image = self.animations['Idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.6
        self.status = 'Idle'
        self.attack_bool = False
        self.health = 10 
        
    def import_character_assets(self):
        character_path = 'graphics//Enemies//enemy//'
        self.animations = {'Idle':[],'Run':[],'Jump':[],'Fall':[], 'Attack1':[], 'Attack2':[], 'Death':[], 'Take hit': []}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def apply_gravity(self):
        # metodo para aplicar a gravidade
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def move(self):
        self.apply_gravity()
        if self.status=='Idle':
            if random.randint(1,5)>3:
                self.direction.x*=-1
        self.rect.x+=self.direction.x
        self.rect.y+=self.direction.y
        
    def update(self, x_shift):
        self.rect.x += x_shift
        self.move()
    
