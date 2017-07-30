import pygame
import time
import random
import threading

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
gold = (212, 175, 55)
clock = pygame.time.Clock()

def populate_map(walllist):
	wall_loc = [[100, 100, 105, 450], [100, 450, 600, 455], [595, 250, 600, 450]]
	for i in range(0, len(wall_loc)):
		wall = Wall(wall_loc[i][0], wall_loc[i][1], wall_loc[i][2], wall_loc[i][3])
		walllist.append(wall)

class Wall():
	def __init__(self, x1, y1, x2, y2):
		self.box = pygame.Rect(x1, y1, x2-x1, y2-y1)
		self.color = green

