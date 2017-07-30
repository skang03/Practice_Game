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




#checks hp and removes it from the list if its hp drops to 0
def check_hp(monsterlist):
	for mon in monsterlist:
		if mon.hp <= 0:
			monsterlist.remove(mon)


#base class for all actors
#contains a rectangle that is used for collision detection and drawing
class Character():
	def __init__(self):
		self.hp = 0
		self.movespeed = 0
		self.att = 0
		self.size = 0
		self.color = black
		self.box = pygame.Rect(0, 0,self.size,self.size)


	def move(self, dx, dy, walllist):
		if dx != 0:
			self.move_single_axis(dx, 0, walllist)
		if dy != 0:
			self.move_single_axis(0, dy, walllist)

	def move_single_axis(self, dx, dy, walllist):
		self.box.x += dx
		self.box.y += dy

		for wall in walllist:
			if self.box.colliderect(wall.box):
				if dx < 0: self.box.left = wall.box.right
				if dx > 0: self.box.right = wall.box.left
				if dy < 0: self.box.top = wall.box.bottom
				if dy > 0: self.box.bottom = wall.box.top


class Player(Character):
	def __init__(self):
		self.hp = 5
		self.movespeed = 5
		self.att = 1
		self.color = red
		self.size = 30
		self.box = pygame.Rect(300, 400, self.size, self.size)
		self.attbox = None
		self.index = 0

	def attack(self, dir, monsterlist):
		self.attbox = pygame.Rect(0, 0, self.size, self.size)
		if dir == 'right':
			self.attbox.midleft = self.box.midright

		elif dir == 'left':
			self.attbox.midright = self.box.midleft

		elif dir == 'down':
			self.attbox.midtop = self.box.midbottom

		else:
			self.attbox.midbottom = self.box.midtop

		for mon in monsterlist:
			if self.attbox.colliderect(mon.box):
				mon.hp = 0

	def update(self, frames):
		if self.index < frames:
			self.index += 1
			return False
		self.index = 0
		return True




class Monster(Character):
	def __init__(self, x, y):
		self.hp = 1
		self.movespeed = 1
		self.att = 1
		self.size = 10
		self.color = gold
		self.box = pygame.Rect(x, y, self.size, self.size)


	def attack(self, player):
		pass