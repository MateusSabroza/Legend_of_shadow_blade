import pygame
from settings import *
from os import walk

def import_folder(path):
    surface_list = []
    for _,_,img_files in walk(path):
        for image in img_files:
            #print(image)
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.initial_pos = pos
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations['Idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.6
        self.jump_speed = -15
        self.jump_time = 0
        self.climb_time=0
        self.status = 'Idle'
        self.faceright = True
        self.onleft = False
        self.onright = False
        self.death = False
        self.attack_time = 0
        self.attack_bool = False
        self.max_stamina = 3
        self.stamina = self.max_stamina
        self.max_health = 100
        self.actual_health = self.max_health
        self.taking_dmg = False
        
    def import_character_assets(self):
        character_path = 'graphics//hero//Martial Hero 2.0//'
        self.animations = {'Idle':[],'Run':[],'Jump':[],'Fall':[], 'Attack1':[], 'Attack2':[], 'Death':[], 'Take hit': []}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        #print(self.animations)
    def get_input(self):
        # metodo para pegar o input do teclado
        key = pygame.key.get_pressed()

        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.direction.x = 1
            self.faceright = True
        elif key[pygame.K_a] or key[pygame.K_LEFT]:
            self.direction.x = -1
            self.faceright = False
        else:
            self.direction.x = 0
        if key[pygame.K_SPACE] or key[pygame.K_UP]:
            self.jump_time += 1
            if self.jump_time < 5 and self.climb_time<3: #define o tempo de pulo e escalada maximo do player
                self.jump()
        if key[pygame.K_KP_ENTER] and not(self.attack_bool) and self.stamina>1:
            self.attack()
        if key[pygame.K_i]:
            self.actual_health = -1

    def apply_gravity(self):
        # metodo para aplicar a gravidade
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
    
    def attack(self):
        self.stamina-=1
        self.direction.y = self.jump_speed/1.5
        self.attack_time+=1
        self.attack_bool = True
    
    def take_dmg(self):
        self.actual_health-=1
        self.taking_dmg = True

    def get_status(self):
        if self.taking_dmg:
            self.status = 'Take hit'
        elif self.attack_bool:
            i = self.attack_time % 2 + 1
            self.status = "Attack"+str(i)
        elif self.direction.y > 0:
            self.status = "Fall"
        elif self.direction.y < 0 and not(self.onleft) and not(self.onright):
            self.status = "Jump"
        else: 
            self.status = 'Run'
        if self.direction == (0,0) and not(self.attack_bool):
            self.status = "Idle"
        
    def animate(self):
        self.get_status()
        animation = self.animations[self.status]
        self.frame_index+=self.animation_speed
        if self.frame_index > len(animation):
            if self.status == 'Attack1' or self.status == 'Attack2':
                self.attack_bool = False
            elif self.status == 'Take hit':
                self.taking_dmg = False
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]
        if self.faceright:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)
        if self.onright:
            self.image = pygame.transform.rotate(image, -240)
        elif self.onleft:
            image = pygame.transform.rotate(image, -60)
            self.image = pygame.transform.flip(image, False, True)
    
    def out_of_bounds(self):
        if self.rect.top > screen_height:
            self.actual_health-=2

   
    def update(self):
        # metodo para atualizar o player
        self.get_input()
        self.animate()
        self.out_of_bounds()
        if self.jump_time>1:
            self.onleft = False
            self.onright = False 
        if self.stamina<0:
            self.stamina = 0
        if self.stamina<self.max_stamina:    
            self.stamina+=0.01
        if self.actual_health<0:
            self.death = True

