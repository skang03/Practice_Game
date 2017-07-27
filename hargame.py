import pygame
import time
import random
import threading

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

monsterlist = []


class Character():
    def __init__(self):
        self.hp = 0
        self.movespeed = 0
        self.att = 0
        self.size = 0
        self.x = 0
        self.y = 0
        self.color = black


class Player(Character):
    def __init__(self):
        self.hp = 5
        self.movespeed = 5
        self.att = 1
        self.x = 400
        self.y = 300
        self.color = red
        self.size = 30

    def move(self):
        pass

    def attack(self, facing):
        size = self.size
        px = self.x
        py = self.y

        ax = px
        ay = py
        print(facing)
        # square made by the four points ax, ay, px, py is the area where monster hp is reduced
        if facing == 0:  # facing left
            ax -= size
            px += int(size/2)
            ay += size
        # check if there are any monsters on (px, py) and decrease monster hp (damage: self.att += randint(-4, 4))
        elif facing == 1:  # facing right
            ax += size * 2
            px += int(size/2)
            ay += size

        elif facing == 2:  # facing up
            ay -= size
            py += int(size/2)
            ax += size
        elif facing == 3:  # facing down
            ay += size * 2
            py += int(size/2)
            ax += size

        pygame.draw.rect(gameDisplay, green, [ax, ay, size, size])


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

    def move(self, player):
        px = player.x
        py = player.y

        if px > self.x + 50:
            self.x += self.movespeed
        if px < self.x - 50:
            self.x -= self.movespeed
        if py > self.y + 50:
            self.y += self.movespeed
        if py < self.y - 50:
            self.y -= self.movespeed

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


class Item():
    def __init__(self):
        self.x = 0
        self.y = 0


def mon_spawn():
    threading.Timer(5.0, mon_spawn).start()
    x = random.randint(50, 700)
    y = random.randint(50, 500)
    mon = Monster(x, y)
    monsterlist.append(mon)


def check_hp():
    for mon in monsterlist:
        if mon.hp <= 0:
            monsterlist.remove(mon)


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
    x = character.x
    y = character.y
    charsize = character.size
    color = character.color

    pygame.draw.rect(gameDisplay, color, [x, y, charsize, charsize])
    score(1)


def map_draw():
    gameDisplay.fill(black)
    gameDisplay.fill(white, [50, 50, 700, 500])




def gameLoop():
    gameExit = False
    gameOver = False

    dood = Player()

    mon_spawn()

    lead_x_change = 0
    lead_y_change = 0
    current_x = 'null'
    current_y = 'null'
    dir = 0

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

        check_hp()

        for mon in monsterlist:
            mon.move(dood)
            char_draw(mon)

        char_draw(dood)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_g:
                    gameOver = True
                if event.key == pygame.K_LEFT:
                    lead_x_change = -dood.movespeed
                    current_x = 'left'
                if event.key == pygame.K_RIGHT:
                    lead_x_change = dood.movespeed
                    current_x = 'right'
                if event.key == pygame.K_UP:
                    lead_y_change = -dood.movespeed
                    current_y = 'up'
                if event.key == pygame.K_DOWN:
                    lead_y_change = dood.movespeed
                    current_y = 'down'

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and current_x == 'left':
                    lead_x_change = 0
                    dir = 0
                if event.key == pygame.K_RIGHT and current_x == 'right':
                    lead_x_change = 0
                    dir = 1
                if event.key == pygame.K_UP and current_y == 'up':
                    lead_y_change = 0
                    dir = 2
                if event.key == pygame.K_DOWN and current_y == 'down':
                    lead_y_change = 0
                    dir = 3
                if event.key == pygame.K_v:
                    dood.attack(dir)

        if dood.x + lead_x_change <= 720 and dood.x + lead_x_change >= 50:
            dood.x += lead_x_change
        if dood.y + lead_y_change <= 520 and dood.y + lead_y_change >= 50:
            dood.y += lead_y_change


        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()
gameLoop()
