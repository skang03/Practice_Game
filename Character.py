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

#fills map with monster spawners that arent in the wall
def populate_spawner(walllist, monsterlist, iter):
	for i in range(0, iter):
		x = random.randint(50, 750)
		y = random.randint(50, 550)
		for wall in walllist:
			if wall.box.collidepoint(x,y):
				continue
		spawner = MonsterSpawner(x, y, 'lol')
		monsterlist.append(spawner)

#base class for all actors
#contains a rectangle that is used for collision detection and drawing
class Character():
	def __init__(self):
		self.hp = 0
		self.movespeed = 0
		self.att = 0
		self.size = 0
		self.color = None
		self.box = pygame.Rect(0, 0, self.size, self.size)
		self.direction = 'up'
		self.index = 0
		self.image = pygame.Surface((16,16)).convert()

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


	# called when we want character to count frames.  would be called once per game loop until it returns true, and then
	# 	something would happen and the count resets
	def wait(self, frames):
		if self.index < frames:
			self.index += 1
			return False
		self.index = 0
		return True

	def render(self, display, box):
		background = pygame.Surface((box.width, box.height))
		background.fill(white) # this should be the background.
		display.blit(background, (box.x, box.y))
		display.blit(self.image, (self.box.x, self.box.y))


class Player(Character):
	def __init__(self):
		super(Player, self).__init__()
		self.hp = 5
		self.movespeed = 5
		self.att = 1
		self.color = red
		self.size = 30
		self.image = pygame.Surface((self.size, self.size)).convert()
		self.image.fill(self.color)
		self.box = pygame.Rect(200, 300, self.size, self.size)
		self.attbox = None
		self.attack_image = None
		self.index = 0
		self.direction = 'up'


	def move(self, dx, dy, walllist, camera):
		if dx != 0:
			camera = self.move_single_axis(dx, 0, walllist, camera)
		if dy != 0:
			camera = self.move_single_axis(0, dy, walllist, camera)

		return camera

	# checks collision, one axis at a time.  if a character moves into a wall, then it is immediately placed so that the
		# leading face of the character is placed on the edge of the wall.  If a character is moving right and is
		# suddenly in a wall, that means it must have hit the left face of the wall.  we put the right face of the
		# character onto the left side of the wall and nothing ever gets stuck or phases through corners etc
	def move_single_axis(self, dx, dy, walllist, camera_pos):
		x,y = camera_pos
		self.box.x += dx
		x -= dx
		self.box.y += dy
		y -= dy


		for wall in walllist:
			if self.box.colliderect(wall.box):
				if dx < 0:
					self.box.left = wall.box.right
					x = camera_pos[0]
				if dx > 0:
					self.box.right = wall.box.left
					x = camera_pos[0]
				if dy < 0:
					self.box.top = wall.box.bottom
					y = camera_pos[1]
				if dy > 0:
					self.box.bottom = wall.box.top
					y = camera_pos[1]

		camera_pos = (x, y)
		return camera_pos

	def attack(self, monsterlist, walllist):
		status = False #whether attack got through or not; used to see if green box should be drawn or not
		self.attbox = pygame.Rect(0, 0, self.size, self.size)
		
		if self.direction == 'right':
			self.attbox.midleft = self.box.midright
			for wall in walllist:
				if self.attbox.colliderect(wall.box):
					self.attbox = pygame.Rect(0, 0, wall.box.left - self.box.right, self.size)
					self.attbox.midleft = self.box.midright

		elif self.direction == 'left':		
			self.attbox.midright = self.box.midleft
			for wall in walllist:
				if self.attbox.colliderect(wall.box):
					self.attbox = pygame.Rect(0, 0, self.box.left - wall.box.right, self.size)
					self.attbox.midright = self.box.midleft			
			
		if self.direction == 'down':
			self.attbox.midtop = self.box.midbottom
			for wall in walllist:
				if self.attbox.colliderect(wall.box):
					self.attbox = pygame.Rect(0, 0, self.size, wall.box.top - self.box.bottom)
					self.attbox.midtop = self.box.midbottom	

		elif self.direction == 'up':
			self.attbox.midbottom = self.box.midtop
			for wall in walllist:
				if self.attbox.colliderect(wall.box):
					self.attbox = pygame.Rect(0, 0, self.size, self.box.top - wall.box.bottom)
					self.attbox.midbottom = self.box.midtop	

		# this is what actually gets drawn so we need to make sure the attack image is the same size as the attack box
		self.attack_image = pygame.Surface((self.attbox.width, self.attbox.height)).convert()



		for mon in monsterlist:
			if self.attbox.colliderect(mon.box):
				mon.hp = 0

class Monster(Character):
	def __init__(self, x, y):
		super(Monster, self).__init__()
		self.hp = 1
		self.movespeed = 1
		self.att = 1
		self.size = 10
		self.color = gold
		self.image.fill(self.color)
		self.box = pygame.Rect(x, y, self.size, self.size)
		self.index = 0
		self.direction = 'up'
		self.exp = 10
		
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

#spawns monsters in a small radius of the spawner on a timer and places them in the monster list
class MonsterSpawner(Character):
	def __init__(self, x, y, type):
		self.hp = 1
		self.movespeed = 1
		self.att = 1
		self.size = 10
		self.color = gold
		self.box = pygame.Rect(x, y, self.size, self.size)
		self.index = 0
		self.direction = 'up'
		self.exp = 10
		self.type = type

	def spawn(self, timer, monsterlist):
		if self.index > timer:
			x = random.randint(self.box.centerx - 50, self.box.centerx + 50)
			y = random.randint(self.box.centery - 50, self.box.centery - 50)
			mon = Monster(x, y)
			monsterlist.append(mon)
			self.index = 0

		else: self.index += 1
