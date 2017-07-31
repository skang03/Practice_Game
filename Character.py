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
		self.direction = 'up'
		self.index = 0

	# dx and dy are the amounts that the character will move per frame.  negative is left/up, positive is right/down
		# splits the dx and dy into two separate moves for easy collision detection
	def move(self, dx, dy, walllist):
		if dx != 0:
			self.move_single_axis(dx, 0, walllist)
		if dy != 0:
			self.move_single_axis(0, dy, walllist)

	# checks collision, one axis at a time.  if a character moves into a wall, then it is immediately placed so that the
		# leading face of the character is placed on the edge of the wall.  If a character is moving right and is
		# suddenly in a wall, that means it must have hit the left face of the wall.  we put the right face of the
		# character onto the left side of the wall and nothing ever gets stuck or phases through corners etc
	def move_single_axis(self, dx, dy, walllist):
		self.box.x += dx
		self.box.y += dy

		for wall in walllist:
			if self.box.colliderect(wall.box):
				if dx < 0: self.box.left = wall.box.right
				if dx > 0: self.box.right = wall.box.left
				if dy < 0: self.box.top = wall.box.bottom
				if dy > 0: self.box.bottom = wall.box.top

	def update(self, frames):
		if self.index < frames:
			self.index += 1
			return False
		self.index = 0
		return True


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
		self.direction = 'up'

	def attack(self, monsterlist):
		self.attbox = pygame.Rect(0, 0, self.size, self.size)
		if self.direction == 'right':
			self.attbox.midleft = self.box.midright

		elif self.direction == 'left':
			self.attbox.midright = self.box.midleft

		if self.direction == 'down':
			self.attbox.midtop = self.box.midbottom

		elif self.direction == 'up':
			self.attbox.midbottom = self.box.midtop

		for mon in monsterlist:
			if self.attbox.colliderect(mon.box):
				mon.hp = 0




class Monster(Character):
	def __init__(self, x, y):
		self.hp = 1
		self.movespeed = 1
		self.att = 1
		self.size = 10
		self.color = gold
		self.box = pygame.Rect(x, y, self.size, self.size)
		self.index = 0
		self.direction = 'up'

	def move(self, player, walllist):
		if self.box.centerx < player.box.centerx:
			self.move_single_axis(self.movespeed, 0, walllist)
		elif self.box.centerx > player.box.centerx:
			self.move_single_axis(-self.movespeed, 0, walllist)
		if self.box.centery < player.box.centery:
			self.move_single_axis(0, self.movespeed, walllist)
		elif self.box.centery > player.box.centery:
			self.move_single_axis(0, -self.movespeed, walllist)

	def attack(self, player):
		pass