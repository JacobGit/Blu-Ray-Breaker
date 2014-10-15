#!/usr/bin/env python
# Jacob Newman
# Created 12/26/2013

import pygame, sys, random, math
from pygame.locals import *


####### Constants ##########
disc_diameter = 10
number_of_discs = 3
#testing speeds = [1,-1]
speeds = [-10,-9,-8,-7,-6,6,7,8,9,10]
font_color = (0,0,0)
one = 1000
two = 2000
three = 3000
four = 4000
############################



# Helper Functions
def countdown():
    if time > one and time < two:
        myfont = pygame.font.SysFont("helvetica", 100)
        label = myfont.render("3", 1, font_color)
        screen.blit(label, (500, 250))
    elif time >= two and time < three:
        myfont = pygame.font.SysFont("helvetica", 100)
        label = myfont.render("2", 1, font_color)
        screen.blit(label, (500, 250))
    elif time >= three and time < four:
        myfont = pygame.font.SysFont("helvetica", 100)
        label = myfont.render("1", 1, font_color)
        screen.blit(label, (500, 250))

def texts(score):
   myfont=pygame.font.SysFont('helvetica',30)
   scoretext=myfont.render("Score: "+str(score), 1, (96,96,96))
   screen.blit(scoretext, (865, 600))

def distance(xdiff, ydiff):
    distance = math.sqrt(xdiff**2 + ydiff**2)
    return int(round(distance))



######## Model ###########
class Disc(object):
    """The discs that are thrown onto the screen"""
    def __init__(self, image, position, diameter, xspeed, yspeed):
        self.image = image
        self.position = position
        self.diameter = diameter
        self.xspeed = xspeed
        self.yspeed = yspeed

    def bounce(self):
        if self.position[0] <= 0 or self.position[0] >= 1024-110:
            self.xspeed *= -1
        if self.position[1] <= 0 or self.position[1] >= 640-110:
            self.yspeed *= -1

class Bullet(object):
    def __init__(self, image):
        self.image = image

###########################




# Initialize game screen
pygame.init()
screen=pygame.display.set_mode((1024,640),0,32)  
pygame.display.set_caption('Blu-Ray Breaker')    

bg='grey-bg(2).jpg'
mimage='crosshair.png'
dimage='blu-ray.png'
bimage='bullet.png'

# Background image
background = pygame.image.load(bg).convert()
# Curser; transparent crosshair   
mouse_c = pygame.image.load(mimage).convert_alpha() 
# Disc objects
disc_list = []
for ints in range(number_of_discs):
    disc_list.append(Disc(pygame.image.load(dimage).convert_alpha(),
            [512-55,320-55],disc_diameter, random.choice(speeds), random.choice(speeds)))
#Bullet objects
bullet_list = []
for ints in range(number_of_discs):
    bullet_list.append(Bullet(pygame.image.load(bimage).convert_alpha()))

#Time control
clock = pygame.time.Clock()
time = 0

#Initialize score
score = 0





# Main Event-Loop
while True:
    #Limit the fps and count each frame
    clock.tick(60)
    time += clock.get_time()
    # Background
    screen.blit(background, (0,0))
    
    #Discs
    if time >= four and disc_list != []:
        disc_list[0].position[0] += disc_list[0].xspeed
        disc_list[0].position[1] += disc_list[0].yspeed
        screen.blit(disc_list[0].image, (disc_list[0].position[0],disc_list[0].position[1]))
        disc_list[0].bounce()

    #Bullets
    for remaining in range(len(bullet_list)):
        screen.blit(bullet_list[remaining].image, (0+(25*remaining),550))

    #Score
    texts(score)

    # Mouse controls
    mouse_x,mouse_y = pygame.mouse.get_pos()
    mouse_x -= mouse_c.get_width()/2
    mouse_y -= mouse_c.get_height()/2
    screen.blit(mouse_c, (mouse_x,mouse_y))

    if disc_list != []:
        countdown()

    if disc_list == [] and time <= four:
            myfont = pygame.font.SysFont("helvetica", 100)
            label = myfont.render("Game Over", 1, font_color)

            #Display Score
            screen.blit(label, (270, 220))
            score_label = myfont.render("Final Score: " + str(score), 1, font_color)
            screen.blit(score_label, (180, 340))

            
    if disc_list == [] and time > four:
            pygame.quit()
            sys.exit()

    #Event controller
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN and time > four:
            x,y=event.pos
            x_diff = math.fabs(x - (disc_list[0].position[0]+55))
            y_diff = math.fabs(y - (disc_list[0].position[1]+55))

            # Hitting the disc
            if distance(x_diff, y_diff) < 55: # Hitting the disc
                pygame.mixer.Sound('glass_break.wav').play() # http://soundbible.com/1765-Glass-Break.html
                disc_list.pop(0)
                bullet_list.pop(0)
                time = 0

                # Determine score by pixel distance to center
                score += (55 - distance(x_diff, y_diff))

            # Missing the disc
            else:   
                pygame.mixer.Sound('gunshot(2).wav').play() # http://www.soundjay.com/mechanical/sounds/gun-gunshot-02.mp3
                disc_list.pop(0)
                bullet_list.pop(0)
                time = 0

                # Determine score loss by pixel distance (no more than 55)
                score -= min((distance(x_diff,y_diff) - 55), 55)


    pygame.display.update()
    