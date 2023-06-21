# arquivo_principal
import pygame
from sys import exit

pygame.init()
FPS = 60
WIDTH, HEIGHT = 1280, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("New Game")

BG = pygame.image.load("assets/Background1.jpg")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("C:\WINDOWS\FONTS\INFROMAN.ttf", size)


class Button:
    def __init__(
        self,
        image,
        pos,
        text_input,
        font=get_font(75),
        base_color="#ff1900",
        hovering_color="#40140f",
    ):
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
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


class Player(pygame.sprite.Sprite):
    GRAVITY = 1

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(
            pygame.image.load("assets/Players/mcree.png").convert_alpha(), 0, 0.34
        )
        self.pos = pygame.math.Vector2(10, 10)
        self.speed = 7
        self.fallcount = 0
        self.velx = 0
        self.vely = 0

    def user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.velx = self.speed
        elif keys[pygame.K_a]:
            self.velx = -self.speed
        else:
            self.velx = 0

    def move(self):
        # self.vely+= min(1,(self.fallcount/FPS )*self.GRAVITY)
        if self.velx < 0:
            self.image = pygame.transform.rotozoom(
                pygame.image.load("assets/Players/mcree.png").convert_alpha(), 0, 0.34
            )
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.velx > 0:
            self.image = pygame.transform.rotozoom(
                pygame.image.load("assets/Players/mcree.png").convert_alpha(), 0, 0.34
            )
        self.pos += pygame.math.Vector2(self.velx, self.vely)

    def update(self):
        self.user_input()
        self.move()

        self.fallcount += 1


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


PLAYER = Player()


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        WINDOW.fill("black")
        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        WINDOW.blit(PLAY_TEXT, PLAY_RECT)
        WINDOW.blit(PLAYER.image, PLAYER.pos)
        PLAYER.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
        pygame.display.update()


def main_menu():
    while True:
        WINDOW.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#ff1900")
        MENU_RECT = MENU_TEXT.get_rect(center=(645, 80))
        PLAY_BUTTON = Button(
            image=pygame.image.load("assets/Rect.png"),
            pos=(170, 450),
            text_input="PLAY",
        )
        QUIT_BUTTON = Button(
            image=pygame.image.load("assets/Rect.png"),
            pos=(170, 600),
            text_input="QUIT",
        )
        WINDOW.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WINDOW)
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
