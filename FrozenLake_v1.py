''' 
The aim of the agent is to move from initial point S to final point G without falling in holes H
The agent can move up/down/left/right from any point if that move is possible

SFFF       (S: starting point, safe)
FHFH       (F: frozen surface, safe)
FFFH       (H: hole, fall to your doom)
HFFG       (G: goal, where the frisbee is located)

A reward of 1 is given if the agent reaches G 
Initially all others Q(s,a) pairs are given value 0

Action space
	0 - Right
	1 - Up
	2 - Left
	3 - Down

The observation space is 16 cells on the board

Positions are given index = 4*row + col where row,col belongs to {0,1,2,3}
'''

import numpy as np
import pygame, sys
import matplotlib.pyplot as plt
import time
import random
#import gym

# Proyect files
import constants as cte
from constants import Color, ImgPath
from components import Board, Menu, Player, Goal, Ice


class Game():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Frozen Lake - Grupo 6 Nuclio Digital School 2024 (c)")
        pygame.display.set_icon(pygame.image.load(ImgPath.NUCLIO_FAVICON.value))

        #self.env = gym.make('FrozenLake-v0', desc=None, map_name='4x4', is_slippery=False)
        self.surface = pygame.display.set_mode((cte.SCREEN_WIDTH, cte.SCREEN_HEIGHT))
        self.menu = Menu(self.surface)
        self.board = Board(self.surface)
        self.player = Player(self.surface)
        self.goal = Goal(self.surface)
        self.ice1 = Ice(self.surface, (cte.BOX_SIZE, cte.BOX_SIZE))
        self.ice2 = Ice(self.surface, (cte.BOX_SIZE * 3, cte.BOX_SIZE))
        self.ice3 = Ice(self.surface, (cte.BOX_SIZE * 3, cte.BOX_SIZE * 2))
        self.ice4 = Ice(self.surface, (0, cte.BOX_SIZE * 3))


        self.fail = False
        self.victory = False
        self.clock = pygame.time.Clock()

        self.action = 0

    def check_collision(self, object) -> bool:
        collision = False
        if object[0] <= self.player.position[0] and self.player.position[0] <= object[0] + cte.BOX_SIZE:
            if object[1] <= self.player.position[1] and self.player.position[1] <= object[1] + cte.BOX_SIZE:
                collision = True
        return collision
    
    def check_all_collisions(self):
        isCollision = False
        for ice in [self.ice1, self.ice2, self.ice3, self.ice4]:
                    if self.check_collision(ice.position):
                        self.fail = True
                        isCollision = True  
        if self.check_collision(self.goal.position):
            self.victory = True
            isCollision = True
        
        return isCollision

        
    
    def new_position(self):
        while self.check_all_collisions():
            x = random.choice([25, 225, 425, 625])
            y = random.choice([25, 225, 425, 625])
            self.player.position = [x, y]

        self.player.startPosition = [x, y]

    def render_background(self) -> None:
        if self.action == 0:
            pygame.mouse.set_visible(1)
            self.action = self.menu.menu_screen()

        elif self.action == 1 or self.action == 2:
            pygame.mouse.set_visible(0)
            self.board.draw()
            self.board.draw_start(self.player.startPosition)
            self.ice1.draw()
            self.ice2.draw()
            self.ice3.draw()
            self.ice4.draw()
            self.board.draw_back()
            self.player.draw(fail = self.fail, victory = self.victory)
            self.goal.draw(victory = self.victory)



        pygame.display.flip()

    def reset(self):
        self.action = 0
        self.player = Player(self.surface)
        self.menu = Menu(self.surface)

    def run(self) -> None:
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_m:
                            self.reset()

                    if self.action == 1 and not self.fail and not self.victory:
                        if event.key == pygame.K_UP:
                            self.player.move_up()
                        if event.key == pygame.K_DOWN:
                            self.player.move_down()
                        if event.key == pygame.K_LEFT:
                            self.player.move_left()
                        if event.key == pygame.K_RIGHT:
                            self.player.move_right()

                        

            if self.action == 1:
                if not self.fail or self.player.position == self.player.startPosition:
                    self.fail = False
                    self.check_all_collisions()

                if self.victory and self.goal.counter == 8:
                    time.sleep(0.75)
                    self.new_position()
                    self.victory = False
                    self.goal.counter = 1

            self.render_background()
            self.clock.tick(10)


if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()