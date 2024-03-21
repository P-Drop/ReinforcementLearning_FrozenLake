import pygame
import time
import constants as cte
from constants import Color, ImgPath, MyFonts

# Menu
class Menu:
    def __init__(self, parent_screen) -> None:
        self.parent_screen = parent_screen
        self.logo = pygame.image.load(ImgPath.NUCLIO_DS.value).convert()
        self.buttonPlayX = 250
        self.buttonPlayY = 450
        self.buttonQLX = 250
        self.buttonQLY = 600 
        self.buttonWidth = 300
        self.buttonHeight = 80
        self.font1 = pygame.font.Font(MyFonts.ROBOTO_BOLD.value, 46)
        self.font2 = pygame.font.Font(MyFonts.SIGNATRA.value, 210)
        self.font3 = pygame.font.Font(MyFonts.ROBOTO_BOLD.value, 32)
        self.action = 0  # (1: PLAY; 2: Q-LEARNING)  

    def menu_screen(self):
        # Background color
        self.parent_screen.fill(Color.LIGHTSKYBLUE.value)

        # Logo Nuclio
        pygame.draw.rect(self.parent_screen, Color.BLACK.value, [40, 40, 370, 116], 0)
        self.parent_screen.blit(self.logo, (50, 50))

        # text

        textG6 = self.font1.render('Grupo 6', True, Color.SELECTIVEYELLOW.value)
        textRectG6 = textG6.get_rect()
        textRectG6.center = (300, 100)

        title = self.font2.render('Frozen Lake', True, Color.DARKSLATEBLUE.value)
        titleRect = title.get_rect()
        titleRect.center = (cte.SCREEN_WIDTH // 2, 300)

        self.button('PLAY', self.buttonPlayX, self.buttonPlayY, self.buttonWidth, self.buttonHeight, 490)
        self.button('Q-LEARNING', self.buttonQLX, self.buttonQLY, self.buttonWidth, self.buttonHeight, 640)

        self.parent_screen.blit(textG6, textRectG6)
        self.parent_screen.blit(title, titleRect)

        return self.action

    def button(self, msg, x, y, w, h, textcenterY) -> int:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.parent_screen, Color.WHITE.value, [x, y, w, h], 0)
            text = self.font3.render(msg, True, Color.DARKSLATEBLUE.value)

            if click[0] == 1:
                if msg == 'PLAY':
                    self.action = 1
                elif msg == 'Q-LEARNING':
                    self.action = 2        
        else:
            pygame.draw.rect(self.parent_screen, Color.DARKSLATEBLUE.value, [x, y, w, h], 0)
            text = self.font3.render(msg, True, Color.WHITE.value)

        textRect = text.get_rect()
        textRect.center = (cte.SCREEN_WIDTH // 2, textcenterY)
        self.parent_screen.blit(text, textRect)


        

# Board
class Board:
    def __init__(self, parent_screen) -> None:
        self.parent_screen =  parent_screen

    def draw(self) -> None:
        # Background color
        self.parent_screen.fill(Color.WHITE.value)
        # Board edges
        pygame.draw.rect(self.parent_screen, Color.BLACK.value, [0, 0, cte.SCREEN_WIDTH, cte.SCREEN_HEIGHT], 5)
        # Board lines
        for i in range(200, cte.SCREEN_WIDTH, 200):
            pygame.draw.line(self.parent_screen, Color.BLACK.value, (i, 0), (i, cte.SCREEN_HEIGHT), 5)
            pygame.draw.line(self.parent_screen, Color.BLACK.value, (0, i), (cte.SCREEN_WIDTH, i), 5)

    def draw_start(self, startPos):
        font = pygame.font.Font(MyFonts.ROBOTO_BOLD.value, 42)
        text = font.render('START', True, Color.DARKSLATEBLUE.value)
        textRect = text.get_rect()
        textRect.center = (startPos[0] + 75, startPos[1] + 75)
        self.parent_screen.blit(text, textRect)

    def draw_back(self):
        font = pygame.font.Font(MyFonts.ROBOTO_BOLD.value, 32)
        text = font.render("<- Press (m)", True, Color.DARKERBLACK.value)
        textRect = text.get_rect()
        textRect.center = (100, cte.SCREEN_HEIGHT - 25)
        self.parent_screen.blit(text, textRect)

# Player
class Player:
    def __init__(self, parent_screen) -> None:
        self.parent_screen = parent_screen
        self.image = pygame.image.load(ImgPath.SEISITO.value).convert()
        self.startPosition = [25, 25] # start position
        self.position = self.startPosition.copy()
        self.failRadius = 75

    def draw(self, fail, victory) -> None:
        
        if fail:
            pygame.draw.circle(self.parent_screen, Color.SIENNARED.value, (self.position[0] + 75, self.position[1] + 75), self.failRadius, 0)
            self.failRadius -= 10
            if self.failRadius < 10:
                fail = False
                self.position = self.startPosition.copy()

        if not victory and not fail:
            self.failRadius = 75
            self.parent_screen.blit(self.image, self.position)

    def move_up(self) -> None:
        if self.position[1] - 200 > 0:
            self.position[1] -= cte.BOX_SIZE

    def move_down(self) -> None:
        if self.position[1] + 200 < cte.SCREEN_HEIGHT:
            self.position[1] += cte.BOX_SIZE

    def move_right(self) -> None:
        if self.position[0] + 200 < cte.SCREEN_WIDTH:
            self.position[0] += cte.BOX_SIZE

    def move_left(self) -> None:
        if self.position[0] - 200 > 0:
            self.position[0] -= cte.BOX_SIZE

# Goal
class Goal:
    def __init__(self, parent_screen) -> None:
        self.parent_screen = parent_screen
        self.image = pygame.image.load(ImgPath.CLOSE_CHEST.value).convert()
        self.victory_image = pygame.image.load(ImgPath.OPEN_CHEST.value).convert()
        self.position = [625, 625]
        self.counter = 1
        self.font = pygame.font.Font(MyFonts.ROBOTO_BOLD.value, 180)
        self.text = "G O A L"
        

    def draw(self, victory) -> None:
        if not victory:
            self.parent_screen.blit(self.image, self.position)
        else:
            self.parent_screen.blit(self.victory_image, self.position)
            self.draw_letters()
            

    def draw_letters(self):
        letters = self.font.render(self.text[:self.counter], True, Color.SIENNARED.value)
        lettersRect = letters.get_rect()
        lettersRect.center = (cte.SCREEN_WIDTH//2, cte.SCREEN_HEIGHT//2)
        self.parent_screen.blit(letters, lettersRect)
        self.counter += 1


# Ice
class Ice:
    def __init__(self, parent_screen, position) -> None:
        self.parent_screen = parent_screen
        self.position = [position[0] + 5, position[1] + 5]
        self.image = pygame.image.load(ImgPath.ICE.value).convert()

    def draw(self) -> None:
        self.parent_screen.blit(self.image, self.position)