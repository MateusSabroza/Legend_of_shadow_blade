# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 22:17:12 2023

@author: Kauan
"""

import pygame
from sys import exit
from settings import *
from os import walk

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.initial_pos = pos
        self.frame.index  =0
        self.image = self.animations['Idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.6
        self.status = 'Idle'
        
    def move(self):
        if self.status=='Idle':
            if random.randint(0,30)==2:
                self.direction*=-1
                