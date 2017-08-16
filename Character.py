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
			if wall.rect.collidepoint(x,y):
				continue
		spawner = MonsterSpawner(x, y, 'lol')
		monsterlist.append(spawner)

# base class for all actors
# contains a rectangle that is used for collision detection and drawing
#
class Character(pygame.sprite.DirtySprite):
	def __init__(self):
		pygame.sprite.DirtySprite.__init__(self)
		self.hp = 0
		self.movespeed = 0
		self.att = 0
		self.size = 0
		self.color = None
		self.rect = pygame.Rect(0, 0, self.size, self.size)
		self.direction = 'up'
		self.index = 0
		self.image = pygame.Surface((16,16)).convert()
		self.dirty = 1

	# dx and dy are the amounts that the character will move per frame.  negative is left/up, positive is right/down
		# splits the dx and dy into two separate moves for easy collision detection
	def move(self, dx, dy, wallsprites):
		if dx != 0:
			self.move_single_axis(dx, 0, wallsprites)
		if dy != 0:
			 self.move_single_axis(0, dy, wallsprites)

	# checks collision, one axis at a time.  if a character moves into a wall, then it is immediately placed so that the
		# leading face of the character is placed on the edge of the wall.  If a character is moving right and is
		# suddenly in a wall, that means it must have hit the left face of the wall.  we put the right face of the
		# character onto the left side of the wall and nothing ever gets stuck or phases through corners etc
	def move_single_axis(self, dx, dy, wallsprites):
		def move_single_axis(self, dx, dy, wallsprites, camera_pos):
			x, y = camera_pos
			self.rect.x += dx
			x -= dx
			self.rect.y += dy
			y -= dy

			boopedwalls = pygame.sprite.spritecollide(self, wallsprites, False)
			for wall in boopedwalls:
				if dx < 0:
					self.rect.left = wall.rect.right
					x = camera_pos[0]
				if dx > 0:
					self.rect.right = wall.rect.left
					x = camera_pos[0]
				if dy < 0:
					self.rect.top = wall.rect.bottom
					y = camera_pos[1]
				if dy > 0:
					self.rect.bottom = wall.rect.top
					y = camera_pos[1]

			camera_pos = (x, y)
			return camera_pos


	# called when we want character to count frames.  would be called once per game loop until it returns true, and then
	# 	something would happen and the count resets
	def wait(self, frames):
		if self.index < frames:
			self.index += 1
			return False
		self.index = 0
		return True

	def update(self):
		self.dirty = 1


class Player(Character):
	def __init__(self):
		super(Player, self).__init__()
		self.hp = 5
		self.movespeed = 2
		self.att = 1
		self.color = red
		self.size = 30
		self.image = pygame.Surface((self.size, self.size)).convert()
		self.image.fill(self.color)
		self.rect = pygame.Rect(200, 300, self.size, self.size)
		self.attrect = None
		self.attack_image = None
		self.index = 0
		self.direction = 'up'
		self.openrect = None
		self.dirty = 1


	def move(self, dx, dy, wallsprites, camera):
		if dx != 0:
			camera = self.move_single_axis(dx, 0, wallsprites, camera)
		if dy != 0:
			camera = self.move_single_axis(0, dy, wallsprites, camera)
		return camera

	# checks collision, one axis at a time.  if a character moves into a wall, then it is immediately placed so that the
		# leading face of the character is placed on the edge of the wall.  If a character is moving right and is
		# suddenly in a wall, that means it must have hit the left face of the wall.  we put the right face of the
		# character onto the left side of the wall and nothing ever gets stuck or phases through corners etc
	def move_single_axis(self, dx, dy, wallsprites, camera_pos):
		x,y = camera_pos
		self.rect.x += dx
		x -= dx
		self.rect.y += dy
		y -= dy

		boopedwalls = pygame.sprite.spritecollide(self, wallsprites, False)
		for wall in boopedwalls:
			if dx < 0:
				self.rect.left = wall.rect.right
				x = camera_pos[0]
			if dx > 0:
				self.rect.right = wall.rect.left
				x = camera_pos[0]
			if dy < 0:
				self.rect.top = wall.rect.bottom
				y = camera_pos[1]
			if dy > 0:
				self.rect.bottom = wall.rect.top
				y = camera_pos[1]

		camera_pos = (x, y)
		return camera_pos

	def attack(self, monsterlist, walllist):
		self.attrect = pygame.Rect(0, 0, self.size, self.size)
		
		if self.direction == 'right':
			self.attrect.midleft = self.rect.midright
			for wall in walllist:
				if self.attrect.colliderect(wall.rect):
					self.attrect = pygame.Rect(0, 0, wall.rect.left - self.rect.right, self.size)
					self.attrect.midleft = self.rect.midright

		elif self.direction == 'left':		
			self.attrect.midright = self.rect.midleft
			for wall in walllist:
				if self.attrect.colliderect(wall.rect):
					self.attrect = pygame.Rect(0, 0, self.rect.left - wall.rect.right, self.size)
					self.attrect.midright = self.rect.midleft			
			
		if self.direction == 'down':
			self.attrect.midtop = self.rect.midbottom
			for wall in walllist:
				if self.attrect.colliderect(wall.rect):
					self.attrect = pygame.Rect(0, 0, self.size, wall.rect.top - self.rect.bottom)
					self.attrect.midtop = self.rect.midbottom	

		elif self.direction == 'up':
			self.attrect.midbottom = self.rect.midtop
			for wall in walllist:
				if self.attrect.colliderect(wall.rect):
					self.attrect = pygame.Rect(0, 0, self.size, self.rect.top - wall.rect.bottom)
					self.attrect.midbottom = self.rect.midtop	

		# this is what actually gets drawn so we need to make sure the attack image is the same size as the attack rect
		self.attack_image = pygame.Surface((self.attrect.width, self.attrect.height)).convert()

		for mon in monsterlist:
			if self.attrect.colliderect(mon.rect):
				mon.hp = 0
				
	def open(self, itemlist, openitemlist):
		self.openrect = pygame.Rect(0, 0, self.size, self.size)
		
		if self.direction == 'right':
			self.openrect.midleft = self.rect.midright
					
		elif self.direction == 'left':
			self.openrect.midright = self.rect.midleft
					
		if self.direction == 'down':
			self.openrect.midtop = self.rect.midbottom

		elif self.direction == 'up':
			self.openrect.midbottom = self.rect.midtop

		for item in itemlist:
			if self.openrect.colliderect(item.rect):
				openitemlist.append(item)
				itemlist.remove(item)


class Monster(Character):
	def __init__(self, x, y):
		super(Monster, self).__init__()
		self.hp = 1
		self.movespeed = 1
		self.att = 1
		self.size = 10
		self.color = gold
		self.image = pygame.Surface((self.size, self.size)).convert()
		self.image.fill(self.color)
		self.rect = pygame.Rect(x, y, self.size, self.size)
		self.index = 0
		self.direction = 'up'
		self.exp = 10
		
	def move(self, player, walllist):
		if self.rect.centerx < player.rect.centerx:
			self.move_single_axis(self.movespeed, 0, walllist)
		elif self.rect.centerx > player.rect.centerx:
			self.move_single_axis(-self.movespeed, 0, walllist)
		if self.rect.centery < player.rect.centery:
			self.move_single_axis(0, self.movespeed, walllist)
		elif self.rect.centery > player.rect.centery:
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
		self.rect = pygame.Rect(x, y, self.size, self.size)
		self.index = 0
		self.direction = 'up'
		self.exp = 10
		self.type = type

	def spawn(self, timer, monsterlist):
		if self.index > timer:
			x = random.randint(self.rect.centerx - 50, self.rect.centerx + 50)
			y = random.randint(self.rect.centery - 50, self.rect.centery - 50)
			mon = Monster(x, y)
			monsterlist.append(mon)
			self.index = 0

		else: self.index += 1
