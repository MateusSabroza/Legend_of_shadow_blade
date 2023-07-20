import pygame
from tiles import Tile, Inv_Wall
from settings import tile_size, screen_width, screen_height
from player import Player
from enemy import Enemy
screen_width_v = 1200

class Level:
    def __init__(self, level_data, surface):
        #
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0  # movimento do personagem
        self.death = False

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.inv_wall = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index*tile_size
                y = row_index*tile_size
                if cell == "x":
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == "P":
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                if cell == "I":
                    enemy_sprite = Enemy((x, y))
                    self.enemies.add(enemy_sprite)   
                if cell == "A":
                    wall = Inv_Wall((x,y), tile_size)
                    self.inv_wall.add(wall)
                    

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width_v/4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width_v)/2 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x*player.speed
        for sprite in self.tiles.sprites():
            # checa se o player colidiu com algum tile
            if sprite.rect.colliderect(player.rect):
                player.onleft = False
                player.onright = False
                if player.direction.x < 0:
                    player.onleft = True
                    #player.onright = False
                    player.rect.left = sprite.rect.right
                    if player.climb_time < 10:
                        player.jump_time = 0
                elif player.direction.x > 0:
                    player.onright = True
                    #player.onleft = False
                    player.rect.right = sprite.rect.left
                    if player.climb_time < 10:
                        player.jump_time = 0

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():
            # checa se o player colidiu com algum tile
            if sprite.rect.colliderect(player.rect):
                player.onleft = False
                player.onright = False
                if player.direction.y < 0:  # se ele encosta no teto
                    player.rect.top = sprite.rect.bottom
                    #player.climb_time += 1
                    if player.climb_time < 10:
                        player.direction.y = 0
                elif player.direction.y > 0:  # se ele cai no chão
                    player.rect.bottom = sprite.rect.top
                    player.jump_time = 0
                    player.climb_time = 0
                    player.direction.y = 0
                    
    def vertical_movement_collision_enemy(self):
        for enemy in self.enemies:
            for sprite in self.tiles.sprites():
                # checa se o player colidiu com algum tile
                if sprite.rect.colliderect(enemy.rect):
                    enemy.rect.bottom = sprite.rect.top
                    enemy.direction.y = 0
            for wall in self.inv_wall.sprites():
                if wall.rect.colliderect(enemy.rect):
                    enemy.direction.x*=-1
    
    def collision_enemy(self):
        player = self.player.sprite
        for enemy in self.enemies:
            enemy.apply_gravity()
            if enemy.rect.colliderect(player.rect):
                if player.attack_bool and not(enemy.attack_bool):
                    enemy.kill()
                elif not(player.attack_bool) and enemy.attack_bool:
                    player.take_dmg()
        if player.death:
            self.death = True
    

    def show_health_stamina(self, x, y, surface):
        player = self.player.sprite
        # Health bar dimensions
        bar_width = 300
        bar_height = 20
        # Calculate the width of the health bar based on the player's current health
        health_percentage = player.actual_health / player.max_health
        health_bar_width = int(bar_width * health_percentage)
        stamina_percentage = player.stamina / player.max_stamina
        stamina_bar_width = int(bar_width/2 * stamina_percentage)
        # Draw the background of the health bar (red color)
        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 0, 0), (x, y+bar_height, bar_width/2, bar_height))
        # Draw the current health level (green color)
        pygame.draw.rect(surface, (0, 255, 0), (x, y, health_bar_width, bar_height))
        pygame.draw.rect(surface, (0, 0, 255), (x, y+bar_height, stamina_bar_width, bar_height))
    
    def run(self):
        # atualiza a posição do tile no eixo x
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.inv_wall.update(self.world_shift)
        self.scroll_x()
        # parte do player
        self.player.update()
        self.enemies.update(self.world_shift,self.player.sprite)
        # chamado dos metodos de colisao
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.collision_enemy()
        self.vertical_movement_collision_enemy()
        # desenhar as barras e o inimigo
        self.show_health_stamina(10,50,self.display_surface)
        self.player.draw(self.display_surface)
        self.enemies.draw(self.display_surface)
