import pygame as p
from pygame import image
import sys

class Game: # Object Oriented Programming. This makes the code more efficient and less prone to corruption
    def __init__(self):

        #initalise/ activate pygame
        p.init()

        #display size
        self.screen_size = ((640, 480))
        self.win = p.display.set_mode((self.screen_size))

        #game caption
        p.display.set_caption("Book 20")

        #setting the time in pygame to computer time
        self.clock = p.time.Clock()

        #Player Character Sprite
        self.img = p.image.load('Data/images/Sprites/Player/Player.png') #Takes 'Player.png' from the specifies folder and assigns it to 'self.img'
        self.img.set_colorkey((0,0,0))
        #bg image 
        self.bg = p.image.load('Data/images/Background/Indoor/Indoor_1.png')
        
        self.bg = p.transform.scale(self.bg, self.screen_size)
        #more player sprite attributes
        self.img_pos = [160, 260]
        self.movement = [False, False]
        self.vel = 5
    def run(self):

        while True:
            #this is the code to set the fps
            self.clock.tick(30)
            
            self.img_pos[0] += (self.movement[1] - self.movement[0]) * self.vel

            self.win.blit(self.bg, (0,0))
            self.win.blit(self.img, self.img_pos) #prints the image assigned to self.img at the specifies coordinates.


             #==== INPUTS ====#
            for event in p.event.get():
                if event.type == p.QUIT: #quit the game
                    p.quit() #closes pygame
                    sys.exit() #quits the program
                if event.type == p.KEYDOWN: # movement
                    if event.key == p.K_a:
                        self.movement[0] = True
                    if event.key == p.K_d:
                        self.movement[1] = True
                if event.type == p.KEYUP:
                    if event.key == p.K_a:
                        self.movement[0] = False
                    if event.key == p.K_d:
                        self.movement[1] = False
                
            p.display.flip()

# Calls the class and runs the game.    
Game().run()