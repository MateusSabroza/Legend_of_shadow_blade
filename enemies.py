# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 22:17:12 2023

@author: Kauan
"""

import pygame
from sys import exit
from settings import *
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.initial_pos = pos