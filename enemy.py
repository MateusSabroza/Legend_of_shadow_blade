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
        self.animation_speed = 0.1
        self.image = self.animations['Idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(1, 0)
        self.speed = 4
        self.gravity = 0.6
        self.status = 'Idle'
        self.attack_bool = False
        self.health = 10 
        self.faceright = True
        self.attack_dist = 100
        self.attack_time = 0
        self.follow_dist = 250
        self.follow = False
        
    def import_character_assets(self):
        character_path = 'graphics//Enemies//enemy//'
        self.animations = {'Idle':[],'Run':[],'Fall':[], 'Attack1':[]}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def apply_gravity(self):
        # metodo para aplicar a gravidade
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
        
    def hit(self, player):
        distância = ((player.rect.x - self.rect.x)**2 + (player.rect.y-self.rect.y)**2)**(0.5)
        if distância<=self.attack_dist and self.attack_time==0:
            self.attack_bool = True
            self.attack_time += 1 
        if distância<self.follow_dist:
            self.follow_player(player)
        else: self.follow = False
    
    def follow_player(self, player):
        self.follow = True
        side = player.rect.x - self.rect.x
        self.direction.x = side/(abs(side)+0.1)
        
        
    def cooldown(self):
        if 0<self.attack_time<=110:
            self.attack_time+=1 
        elif self.attack_time > 110:
            self.attack_time = 0
            
    def get_status(self):
        if self.attack_bool:
            self.status = "Attack1"
        elif self.direction.y>0:
            self.status = "Fall"
        elif self.direction.x!=0:    
            self.status = 'Run'
        else:
            self.status = "Idle"

    def animate(self):
        self.get_status()
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index > len(animation):
            if self.status == 'Attack1':
                self.attack_bool = False
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        if self.faceright:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)
            
    def move(self):
        #if random.randint(1,30)==1:
            #self.direction.x*=-1
        if self.direction.x<0:
            self.faceright = False
        elif self.direction.x>0:
            self.faceright = True
        self.rect.x+=self.direction.x
        self.rect.y+=self.direction.y
    
    def update(self, x_shift, player):
        self.rect.x += x_shift
        self.move()
        self.animate()
        self.hit(player)
        self.cooldown()
        if self.rect.top>screen_height:
            self.kill() 
