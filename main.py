import pygame as p
from pygame import image as img
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
    def run(self):

        while True:
            #this is the code to set the fps
            self.clock.tick(30)
            
            #quit the game
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit() #closes pygame
                    sys.exit() #quits the program


            p.display.flip()

# Calls the class and runs the game.
Game().run()