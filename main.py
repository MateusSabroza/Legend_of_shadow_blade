import pygame
from sys import exit
from settings import *
from tiles import Tile
from level import Level
import random

# pygame setup
FPS = 60
pygame.init()
screen_width_v = 1200
screen_height_v =800
screen = pygame.display.set_mode((screen_width_v, screen_height_v))
clock = pygame.time.Clock()
level = Level(level_map, screen)
background = pygame.transform.scale(pygame.image.load(
    "graphics/bg.png").convert(), (screen_width_v, screen_height_v+40))
BG = pygame.transform.scale(pygame.image.load(
    "graphics/Background1.jpeg").convert(), (screen_width_v, screen_height_v))
lista_de_mortes = ['Foi pro vasco!','Foi de arrasta!','Foi de americanas!','Foi de rainha Elizabeth!',
                   'Wasted', 'Se fudeu!','Reprovou em Calculo 1!']
# button setup


def get_font(size):
    return pygame.font.Font("graphics/samurai.ttf", size)


class Button():
    def __init__(self, image, pos, text_input, font=get_font(75), base_color='#ff1900', hovering_color='#40140f'):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color)


def play():
    clock = pygame.time.Clock()
    fim = 0
    while True:
        screen.fill("black")
        screen.blit(background, (0, 0))
        level.run()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
        if level.death:
            after_life()
        if len(level.enemies)==0:
            fim+=1
            MENU_TEXT = get_font(200).render('GG!', True, "#000080")
            MENU_RECT = MENU_TEXT.get_rect(center=(645, 150))
            screen.blit(MENU_TEXT, MENU_RECT)
        if fim>FPS:
            MENU_TEXT = get_font(60).render('Thanks for playing!!', True, "#000080")
            MENU_RECT = MENU_TEXT.get_rect(center=(600, screen_height_v/2))
            screen.blit(MENU_TEXT, MENU_RECT)
        if fim>3*FPS:
            win()
        
        pygame.display.update()
        clock.tick(FPS)

def after_life():
    frase = lista_de_mortes[random.randint(0,len(lista_de_mortes))]
    screen.fill('black')
    while True:
        screen.blit(BG, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        QUIT_BUTTON = Button(image=pygame.image.load(
            "graphics/Rect.png"), pos=(520, 650), text_input="QUIT")
        MENU_TEXT = get_font(50).render(frase, True, "#ff1900")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width_v/2, 50))
        screen.blit(MENU_TEXT, MENU_RECT)
        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    exit()
        pygame.display.update()

def win():
    screen.fill('black')
    timer = 0
    while True:
        timer+=1
        screen.blit(BG, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        QUIT_BUTTON = Button(image=pygame.image.load(
            "graphics/Rect.png"), pos=(520, 650), text_input="QUIT")
        MENU_TEXT = get_font(50).render('Fala que nao merece o 10!', True, "red")
        MENU_RECT = MENU_TEXT.get_rect(center=(620, 80))
        screen.blit(MENU_TEXT, MENU_RECT)
        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    exit()
        if timer>4*FPS:
            MENU_TEXT = get_font(170).render('EXQUEECE', True, "red")
            MENU_RECT = MENU_TEXT.get_rect(center=(screen_width_v/2, screen_height_v/2))
            screen.blit(MENU_TEXT, MENU_RECT)
        pygame.display.update()

def main_menu():
    while True:
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#ff1900")
        MENU_RECT = MENU_TEXT.get_rect(center=(645, 80))
        PLAY_BUTTON = Button(image=pygame.image.load(
            "graphics/Rect.png"), pos=(170, 450), text_input="PLAY")
        QUIT_BUTTON = Button(image=pygame.image.load(
            "graphics/Rect.png"), pos=(170, 600), text_input="QUIT")
        screen.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    exit()

        pygame.display.update()

main_menu()
