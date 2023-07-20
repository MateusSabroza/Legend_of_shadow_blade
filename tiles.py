from typing import Any
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        #cria um tile com superficie, retangulo e imagem
        super().__init__()
        self.image = pygame.Surface((size, size))
        #converte a imagem para o formato do pygame, e redimensiona para o tamanho do tile
        self.base_image = pygame.transform.scale(pygame.image.load("graphics/tile1.png").convert() , (size, size))
        self.image.blit(self.base_image, (0,0))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        # atualiza a posição do tile no eixo x
        self.rect.x += x_shift
        
class Inv_Wall(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        #cria um tile com superficie, retangulo e imagem
        super().__init__()
        self.image = pygame.Surface((size, size))
        #converte a imagem para o formato do pygame, e redimensiona para o tamanho do tile
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        # atualiza a posição do tile no eixo x
        self.rect.x += x_shift

