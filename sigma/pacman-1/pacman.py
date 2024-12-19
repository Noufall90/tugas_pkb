import copy
from board import boards
import pygame
import math

pygame.init()

WIDTH = 700
HEIGHT = 750
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards



run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    draw_board()
    
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            run = event
            
    pygame.display.flip()
pygame.quit