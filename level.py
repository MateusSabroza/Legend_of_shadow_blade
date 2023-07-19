import pygame
from tiles import Tile
from settings import tile_size, screen_width, screen_height
from player import Player
screen_width_v = 1200

class Level:
    def __init__(self, level_data, surface):
        #
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0  # movimento do personagem

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
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
        # checa se o player colidiu com algum tile
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.onleft = True
                    player.rect.left = sprite.rect.right
                    if player.climb_time < 10:
                        player.jump_time = 0
                elif player.direction.x > 0:
                    player.onright = True
                    player.rect.right = sprite.rect.left
                    if player.climb_time < 10:
                        player.jump_time = 0
        
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        # checa se o player colidiu com algum tile
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
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

    def run(self):
        # atualiza a posição do tile no eixo x
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        # parte do player
        self.player.update()
        # chamado dos metodos de colisao
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
