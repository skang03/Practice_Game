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


#spawns monsters at specific coordinates and places them in the monster list
#to do: give rules for monster spawns
def mon_spawn(monsterlist):
	#threading.Timer(5.0, mon_spawn).start()
	x = random.randint(50, 700)
	y = random.randint(50, 500)
	mon = Monster(x, y)
	monsterlist.append(mon)

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
		self.x = 0
		self.y = 0
		self.color = black
		self.box = pygame.Rect(self.x, self.y,self.size,self.size)


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





	#Other methods just update Character's x and y, but the box's position does not change.  this needs to be called
	# after movement so the box's position moves too.
	def update(self):
		self.box = pygame.Rect(self.x, self.y,self.size,self.size)



class Player(Character):
	def __init__(self):
		self.hp = 5
		self.movespeed = 5
		self.att = 1
		self.x = 400
		self.y = 300
		self.color = red
		self.size = 30
		self.box = pygame.Rect(self.x, self.y, self.size, self.size)

	def attack(self, facing, monsterlist):
		size = self.size
		px = self.x
		py = self.y

		ax = px
		ay = py
		print(facing)
		# square made by the four points ax, ay, px, py is the area where monster hp is reduced
		if facing == 'left':  # facing left
			ax -= size * 2
			px += int(size / 2)
			ay += size

		# check if there are any monsters on (px, py) and decrease monster hp (damage: self.att += randint(-4, 4))
		elif facing == 'right':  # facing right
			ax += size * 3
			px += int(size / 2)
			ay += size

		elif facing == 'up':  # facing up
			ay -= size * 2
			py += int(size / 2)
			ax += size
		elif facing == 'down':  # facing down
			ay += size * 3
			py += int(size / 2)
			ax += size

		for mon in monsterlist:
			mx = mon.x
			my = mon.y
			rx = range(*sorted((ax, px)))
			ry = range(*sorted((ay, py)))
			if mx in rx and my in ry:
				mon.hp -= self.att


class Monster(Character):
	def __init__(self, x, y):
		self.hp = 1
		self.movespeed = 1
		self.att = 1
		self.size = 10
		self.x = x
		self.y = y
		self.color = gold
		self.box = pygame.Rect(self.x, self.y, self.size, self.size)

	def move(self, player, walllist):
		px = player.box.center[0]
		py = player.box.center[1]
		pbox = player.box
		mbox = self.box



		if px <= self.x + 50 and px >= self.x - 50 and py <= self.y + 50 and py >= self.y - 50:
			if px > self.x + self.size:
				self.x += self.movespeed
			if px < self.x - 30:
				self.x -= self.movespeed
			if py > self.y + self.size:
				self.y += self.movespeed
			if py < self.y - 30:
				self.y -= self.movespeed

	def attack(self, player):
		pass