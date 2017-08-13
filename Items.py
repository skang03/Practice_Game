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
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.color = green
		self.taken = False
		self.cooldown = False
		self.worn = False
		self.box = pygame.Rect(x, y, 30, 30)
		self.image = pygame.Surface((30, 30)).convert()
		self.image.fill(self.color)
		self.box.normalize()

		
class Hat(Item):
	def __init__(self, x, y, min_level, defense):
		self.x = x
		self.y = y
		self.min_level = min_level
		self.defense = defense
		
	def worn(player):
		player.defense += self.defense 
		
def make_item(itemlist):
	item_loc = [[130, 130]]
	for i in range(0, len(item_loc)):
		item = Item(item_loc[i][0], item_loc[i][1])
		itemlist.append(item)
