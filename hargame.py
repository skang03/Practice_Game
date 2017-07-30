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

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('supdoods')

pygame.display.update()

smallfont = pygame.font.SysFont(None, 25)
largefont = pygame.font.SysFont(None, 50)

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


def char_draw(character):
	character.update()
	box = character.box
	color = character.color

	pygame.draw.rect(gameDisplay, color, box)
	score(1)

	
def map_draw():
	gameDisplay.fill(black)
	gameDisplay.fill(white, [50, 50, 700, 500])


def wall_draw(wall):
	box = wall.box
	color = wall.color
	pygame.draw.rect(gameDisplay, color, box)

		
def gameLoop():
	gameExit = False
	gameOver = False

	dir = 'none'
	dood = Player()

	monsterlist = []
	walllist = []

	mon_spawn(monsterlist)
	populate_map(walllist)

	while not gameExit:
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

		map_draw()
		for wall in walllist:
			wall_draw(wall)

		check_hp(monsterlist)

		for mon in monsterlist:
			mon.move(dood, walllist)
			char_draw(mon)

		keys = pygame.key.get_pressed()


		if keys[pygame.K_UP]:
			dood.move('up')
			dir = 'up'
		if keys[pygame.K_DOWN]:
			dood.move('down')
			dir = 'down'
		if keys[pygame.K_LEFT]:
			dood.move('left')
			dir = 'left'
		if keys[pygame.K_RIGHT]:
			dood.move('right')
			dir = 'right'

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if (event.type == pygame.KEYDOWN):
				if event.key == pygame.K_z:
					dood.attack(dir, monsterlist)


		char_draw(dood)

		pygame.display.update()
		clock.tick(60)

	pygame.quit()
	quit()

gameLoop()