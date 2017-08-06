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
	#replace this with random generation
	wall_loc = [[100, 100, 105, 450], [100, 450, 600, 455], [595, 450, 600, 200],[45, 45, 950, 50],[950, 45, 955, 755], [955, 755, 45, 750], [45, 755, 50, 45]]
	for i in range(0, len(wall_loc)):
		wall = Wall(wall_loc[i][0], wall_loc[i][1], wall_loc[i][2], wall_loc[i][3])
		walllist.append(wall)

class Wall():
	def __init__(self, x1, y1, x2, y2):
		self.box = pygame.Rect(x1, y1, x2-x1, y2-y1)
		self.image = pygame.Surface((abs(x2-x1), abs(y2-y1))).convert()
		self.box.normalize()
		self.color = black
		

# Class made in order to determine what gets updated.  prevents entire screen from being re-rendered.
class Background_Tile():
	def __init__(self, x, y, size):
		self.box = pygame.Rect((x, y), (size, size))
		self.image = pygame.Surface((size,size)).convert()
		self.image.fill(white)# white should be replaced with ground tile sprite
		self.is_touched = False