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

class Item():
	def __init__(self):
		self.x = 0
		self.y = 0