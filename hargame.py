import pygame
import time
import random
import threading
from Character import *
from Items import *
from Maps import *


#camera
#no attack thru wall
#mon spawn
#mon colliding w player //knockback and invulnerability
#sprites

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
gold = (212, 175, 55)
clock = pygame.time.Clock()

#set size of window
#to do: make this adjustable in-game
screen_width = 1280
screen_height = 720
gameDisplay = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
pygame.display.set_caption('supdoods')

pygame.display.update()

smallfont = pygame.font.SysFont(None, 25)
largefont = pygame.font.SysFont(None, 50)


#makes text into an object for blitting to game surface in message_to_screen
def text_objects(text, color, size):
	if size == "small":
		textSurface = smallfont.render(text, True, color)
	else:
		textSurface = largefont.render(text, True, color)
	return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
	textSurface, textRect = text_objects(msg, color, size)
	textRect.center = 400, 300 + y_displace
	gameDisplay.blit(textSurface, textRect)


def score(score):
	text = smallfont.render("$" + str(score), True, green)
	gameDisplay.blit(text, (700, 50))


#call this to draw any Character
def char_draw(character):
	rect = character.rect
	color = character.color

	pygame.draw.rect(gameDisplay, color, rect)


#draws borders
def map_draw():
	gameDisplay.fill(black)
	gameDisplay.fill(white, [50, 50, 700, 500])


# when the player moves a certain number of pixels away from the camera position, we create a new surface and "stamp" it
#  onto the display at the new camera position
def world_shift(player, monsterlist, walllist, camera):
	world = pygame.Surface((1000,1000)).convert()
	world.fill(black)
	world.fill(white, [50, 50, 700, 500])
	for wall in walllist:
		world.blit(wall.image, (wall.rect.x, wall.rect.y))
	for mon in monsterlist:
		mon.render(world)
	player.render(world)
	gameDisplay.blit(world, (camera[0], camera[1]))

# finds all the Background_Tiles that the rect is currently touching and returns those tiles, which will be put into a
#  list and fed to pygame.display.update(dirtytiles)
def findtiles(rect, tiles):
	left = int(rect.left/100)
	right = int(rect.right/100)      # get the sides of the rect
	top = int(rect.top/100)
	bottom = int(rect.bottom/100)
	dirtytiles = []               # the list of tiles we will be returning
	i = [left]
	j = [top]
	if left != right:
		i.append(right)
	if top != bottom:
		j.append(bottom)

	for ii in i:
		for jj in j:
			dirtytiles.append(tiles[ii][jj])

	return dirtytiles



# main function that contains game loop
# main loop structure:
#	-draw sprites
#	-update screen
# 	-listen for input
#	-do actions

def gameLoop():
	#parameters that check game state
	gameExit = False
	gameOver = False

	# make this a multiple of 100
	worldsize = 1000

	# makes the world surface
	world = pygame.Surface((worldsize, worldsize)).convert()
	camera = basecamera = (0,0)

	# background tiles of size 100x100 pixels.
	tiles = [[]]
	for i in range(0, int(worldsize/100)):
		tiles.append([])
		for j in range(0, int(worldsize/100)):
			tile = Background_Tile(i*100, j*100, 100)
			tiles[i].append(tile)

	#makes the controllable player
	dood = Player()
	wall = Wall(200, 200, 900, 220)
	dood.rect.center = (400, 300)
	doodsprites = pygame.sprite.LayeredDirty((dood))
	monsprites = pygame.sprite.LayeredDirty((dood))
	wallsprites = pygame.sprite.LayeredDirty((wall))


	#a queue for directions that enables strafing.  Example below
	dirqueue = []
	playermode = 'none'

	# #list of monsters and walls, gets sent to all methods that use collision detection like move and attack
	# monsterlist = []
	# monsterspawnerlist = []
	# walllist = []
	# itemlist = []
	# openitemlist = []
	#
	# # populates the list with walls and monster spawners
	# populate_map(walllist)
	# populate_spawner(walllist, monsterspawnerlist, 3)
	# make_item(itemlist)
	#
	# # draw the map
	# gameDisplay.fill(black)
	# for tilelist in tiles:
	# 	for tile in tilelist:
	# 		gameDisplay.blit(tile.image, (tile.rect.x, tile.rect.y))
	# for wall in walllist:
	# 	gameDisplay.blit(wall.image, (wall.rect.x, wall.rect.y))
	# for item in itemlist:
	# 	gameDisplay.blit(item.image, (item.rect.x, item.rect.y))

	background = pygame.Surface((screen_width, screen_height))
	background.fill(black)
	background.fill(white, (50, 50 , screen_width - 100, screen_height - 100))

	doodsprites.clear(gameDisplay, background)
	monsprites.clear(gameDisplay, background)
	wallsprites.clear(gameDisplay, background)

	gameDisplay.blit(background,(0,0))
	wallsprites.draw(gameDisplay)

	pygame.display.update()


	#main loop, happens 60 times per second
	while not gameExit:
		#happens if gameover boolean becomes true, aka when player dies or something
		while gameOver == True:
			message_to_screen("Game over.", red, -50, "large")
			message_to_screen("Press a to restart or press q to quit.", black, 50)
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOver = False
					gameExit = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					if event.key == pygame.K_a:
						gameLoop()

		# DRAW THE SPRITES
		doodsprites.update()
		monsprites.update()

		rects1 = doodsprites.draw(gameDisplay)
		rects2 = monsprites.draw(gameDisplay)
		rects3 = wallsprites.draw(gameDisplay)

		if rects2 == None:
			rects2 = []
		if rects3 == None:
			rects3 = []

		rects = rects1 + rects2 + rects3
		pygame.display.update(rects)

		# attack mode exists because it calls dood.update instead of listening for button presses.  this disables the
		#	user until the attack animation is complete.  delete this if that's annoying to you but I like my
		#	gameboy legend of zelda combat
		if playermode == 'attack':
			dood.attack(monsprites, wallsprites)
			if dood.wait(20):  # if the dood waited 20 frames
				playermode = 'none'
			else:
				gameDisplay.blit(dood.attack_image, (dood.attbox.x, dood.attbox.y))

		if playermode == 'open':
			dood.open(monsprites, wallsprites)
			if dood.wait(20):  # if the dood waited 20 frames
				playermode = 'none'
			else:
				gameDisplay.blit(dood.attack_image, (dood.attbox.x, dood.attbox.y))

		else:
			# gets list of all key presses for this frame and makes the player do actions based on what is pressed
			events = pygame.event.get()

			for event in events:
				# always goes first when listening for events
				if event.type == pygame.QUIT:
					gameExit = True

				# changes the player's direction to the currently pressed arrow keys and assigns player direction for
				# use in directional player actions.  This does so using a queue for directions (dirqueue)
				# For example: you press up first, and up gets added to the queue.  Up is first in queue so dood's
				# direction becomes up.
				# Then you let go of up and it gets removed from the queue.  Nothing happens because dirqueue.len !> 0
				# Next you press left and it gets added to the queue. Then you press up and it gets added too.
				# dirqueue = [up, left]
				# Dood's direction becomes up because up is first in the queue.
				# You are moving up and left while facing up because after this "for event in events" loop there is a
				# thing that listens for any direction keys and moves the player without worrying about what direction
				# they're facing.
				# You let go of up and up is removed from the queue.
				# dirqueue = [left]
				# Now left is first in the queue and dood's direction becomes left.

				if (event.type == pygame.KEYUP):
					if event.key == pygame.K_UP:
						dirqueue.remove('up')
					elif event.key == pygame.K_DOWN:
						dirqueue.remove('down')
					elif event.key == pygame.K_LEFT:
						dirqueue.remove('left')
					elif event.key == pygame.K_RIGHT:
						dirqueue.remove('right')
					if dirqueue.__len__() > 0:
						dood.direction = dirqueue[0]

				if (event.type == pygame.KEYDOWN):
					if event.key == pygame.K_UP:
						dirqueue.append('up')
					elif event.key == pygame.K_DOWN:
						dirqueue.append('down')
					elif event.key == pygame.K_LEFT:
						dirqueue.append('left')
					elif event.key == pygame.K_RIGHT:
						dirqueue.append('right')
					if dirqueue.__len__() > 0:
						dood.direction = dirqueue[0]
					if event.key == pygame.K_z:
						playermode = 'attack'
					if event.key == pygame.K_a:
						playermode = 'open'

				# checks what keys are currently pressed and changes the movement parameters dy and dx to the appropriate values
			keys = pygame.key.get_pressed()
			dx = 0
			dy = 0
			if keys[pygame.K_UP]:
				dy = -dood.movespeed
			if keys[pygame.K_DOWN]:
				dy = dood.movespeed
			if keys[pygame.K_LEFT]:
				dx = -dood.movespeed
			if keys[pygame.K_RIGHT]:
				dx = dood.movespeed

			camera = dood.move(dx, dy, wallsprites, camera)
		# # go through the monsterlist and if there's a monsterspawner then make it run the spawn function
		# for monspawn in monsterspawnerlist:
		# 		monspawn.spawn(600, monsterlist)
		#
		# # moves and draws all the monsters
		# check_hp(monsterlist)
		# for mon in monsterlist:
		# 	monbox = pygame.Rect(mon.box)
		# 	mon.move(dood, walllist)
		# 	allsprites.append(mon)
		#
		#





		# 	#moves in the x direction by dx pixels and in the y direction by dy pixels
		# 	doodbox = pygame.Rect(dood.box) # create new rect that saves previous position so we can erase the previous image before drawing the new one
		#
		#
		#
		# # now we take dirtyboxes, a list of all the places where there was once a box and now there is none, or there was not a box and now there is one,
		# #  and go figure out what tiles have been touched.
		#
		# for wall in walllist:
		# 	gameDisplay.blit(wall.image, (wall.box.x, wall.box.y))
		# for item in itemlist:
		# 	gameDisplay.blit(item.image, ((item.box.x, item.box.y)))
		# for mon in monsterlist:
		# 	mon.draw(gameDisplay)
		# dood.draw(gameDisplay)
		# #must call this to see what we've drawn
		# pygame.display.update()
		#framerate
		clock.tick(60)

	#pressing the quit button
	pygame.quit()
	quit()

gameLoop()



# C:\Python36\python.exe "C:\Users\iho\Desktop\My Projects\top-down gamu\Practice_Game\hargame.py"