import pygame as p
from pygame import image as img
import sys

#initalise/ activate pygame

p.init()

#display size
screen_size = ((500, 500))
win = p.display.set_mode((screen_size))

#game caption
p.display.set_caption("Pygame demo for 11DGTA - 2024")

#setting the time in pygame to computer time
clock = p.time.Clock()


#<--------- All other functions, variables, and classes go here ----------->

#main game loop

done = True
while done:
    #fps set to 60
    clock.tick(60)
    
    #<--------- All other game code goes here --------->

    #quit the game
    for event in p.event.get():
        if event.type == p.QUIT:
            done = False

    p.display.flip()

p.quit()
quit()
