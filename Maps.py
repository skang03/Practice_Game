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
	wall_loc = [[100, 100, 100, 450], [100, 450, 600, 450], [600, 450, 600, 250]]
	for i in range(0, len(wall_loc)):
		wall = Wall(wall_loc[i][0], wall_loc[i][1], wall_loc[i][2], wall_loc[i][3])
		walllist.append(wall)

class Wall():
	def __init__(self, x1, y1, x2, y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
<<<<<<< HEAD
		self.color = green
=======
		self.color = green

>>>>>>> 9ab5fcd76c3756675103c35aad6d3f7fbaf90825
