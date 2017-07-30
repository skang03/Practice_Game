import pygame
import time
import random
import threading
from Character import *
from Items import *
from Maps import *

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
gold = (212, 175, 55)
clock = pygame.time.Clock()

#set size of window
#to do: make this adjustable in-game
gameDisplay = pygame.display.set_mode((800, 600))
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
	box = character.box
	color = character.color

	pygame.draw.rect(gameDisplay, color, box)


#draws borders
def map_draw():
	gameDisplay.fill(black)
	gameDisplay.fill(white, [50, 50, 700, 500])


#draws walls
def wall_draw(wall):
	box = wall.box
	color = wall.color
	pygame.draw.rect(gameDisplay, color, box)


#main function that contains game loop
def gameLoop():
	#parameters that check game state
	gameExit = False
	gameOver = False

	#player's current direction.  to do: add in-between directions
	dir = 'none'
	#makes the controllable player
	dood = Player()

	#list of monsters and walls, gets sent to all methods that use collision detection like move and attack
	monsterlist = []
	walllist = []

#makes monsters spawn in a separate thread with its own timing, only needs to be called once outside of the game loop
	mon_spawn(monsterlist)
	populate_map(walllist)

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

		#draw the map
		map_draw()
		for wall in walllist:
			wall_draw(wall)
		check_hp(monsterlist)

		#moves the player in the direction of the currently pressed arrow keys
		#assigns player direction for use in directional player actions
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

		dood.move(dx, dy, walllist)

		#gets list of all key presses and makes the player do actions based on what is pressed
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if (event.type == pygame.KEYDOWN):
				if event.key == pygame.K_z:
					dood.attack(dir, monsterlist)

		#moves and draws all the monsters
		for mon in monsterlist:
			mon.move(dood, walllist)
			char_draw(mon)
		#finally draws our dood
		char_draw(dood)

		#must call this to see what we've drawn
		pygame.display.update()
		#framerate
		clock.tick(60)

	#pressing the quit button
	pygame.quit()
	quit()

gameLoop()