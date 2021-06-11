import pygame
import textwrap
import math
import random

import timer
import text

pygame.init()
v = pygame.math.Vector2


def int_tuple(vector):
    return (int(vector[0]), int(vector[1]))


class Cell:
    def __init__(self,pos=v(0,0)):
        self.capacity = 100
        self.radius = 30
        self.pos = pos

        self.team = ""
        self.fill = 0

        self.inc_rate = 5.1

        self.give_rate = 1

        self.pressed = False

    def update(self,connected,cell_list):
        pygame.draw.circle(screen, (0,0,0), self.pos, self.radius)
        pygame.draw.circle(screen,(100,100,100),self.pos,self.radius,1)

        fill_img = text.generate_text(str(int(self.fill)),(255,255,255))
        fill_rect = fill_img.get_rect()
        fill_rect.center = self.pos
        screen.blit(fill_img,fill_rect)

        if self.team != "":
            self.fill = min(self.fill+((dt/1000)*self.inc_rate),self.capacity)

        if self.fill == 0:
            self.team = ""

        for connection in connected:
            cell = cell_list[connection]
            if cell.team == "":
                cell.team = self.team
            elif cell.team == self.team:
                cell.fill += (dt/1000)*self.give_rate
                self.fill -= (dt/1000)*self.give_rate
            else:
                cell.fill -= (dt / 1000) * self.give_rate
                self.fill -= (dt / 1000) * self.give_rate

        if (pygame.mouse.get_pos() - v(self.pos)).magnitude() < self.radius:
            if pygame.mouse.get_pressed(3)[0] and not self.pressed:
                self.pressed = True
                return True
        else:
            if pygame.mouse.get_pressed(3)[0]:
                self.pressed = True
        if not pygame.mouse.get_pressed(3)[0]:
            self.pressed = False
        return False




class Board:
    def __init__(self):
        self.cells = []

        for x in range(100,int(screen_dims[0]-100),int((screen_dims[0]-100)/4)):
            for y in range(100, int(screen_dims[1]-100), int((screen_dims[1]-100)/4)):
                self.cells.append(Cell(v(x,y)))
        self.cells[0].team = "friendly"

        self.connections = []

        # for i in self.cells:
        #     for j in self.cells:
        #         if i is not j and [i,j] not in self.connections:
        #             self.connections.append([j,i])

        self.creating_connection = False
        self.creating_index = 0

    def get_connections_to(self,index):
        connections_to = []
        for connection in self.connections:
            if connection[0] == index:
                connections_to.append(connection[1])
        return connections_to

    def update(self):
        for connection in self.connections:
            pygame.draw.line(screen,(100,100,100),self.cells[connection[0]].pos,self.cells[connection[1]].pos)

        for i in range(len(self.cells)):
            cell = self.cells[i]
            clicked = cell.update(self.get_connections_to(i),self.cells)

            if clicked and not self.creating_connection:
                self.creating_connection = True
                self.creating_index = i

            if self.creating_connection and clicked and self.creating_index != i:
                self.connections.append([self.creating_index,i])
                self.creating_connection = False


scale = 3
screen_dims = v(600, 370)
screen = pygame.display.set_mode(int_tuple(screen_dims), pygame.RESIZABLE | pygame.SCALED)
clock = pygame.time.Clock()
keys = []

running = True

states = {}
current_state = "game"

board = Board()

while True:

    dt = clock.tick(130)
    pygame.display.set_caption(str(clock.get_fps()))

    screen.fill((0,0,0))

    board.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            key = event.key
            name = pygame.key.name(key)
            if event.type == pygame.KEYDOWN:
                if name not in keys:
                    keys.append(name)
            else:
                if name in keys:
                    keys.remove(name)


    pygame.display.flip()
