import pygame as p
from pygame import image
from Scripts.utility_code import load_image, load_images
from Scripts.entities import EntityPhysics
import sys

class Game: # Object Oriented Programming. This makes the code more efficient and less prone to corruption
    def __init__(self):

        #initalise/ activate pygame
        p.init()

        #display size
        self.screen_size = (640, 480)
        self.win = p.display.set_mode(self.screen_size) #window size

        self.display = p.Surface((320, 240)) #actual game render surface size

        #game caption
        p.display.set_caption("Book 20")

        #setting the time in pygame to computer time
        self.clock = p.time.Clock()

        #bg image 
        self.bg = p.image.load('Data/images/Background/Indoor/Indoor_1.png')
        


        self.movement = [False, False]

        self.assets = {
            'grass' : load_images('Tiles/Grass'),
            'path' : load_images('Tiles/Path'),
            'axe_head' : load_images('Tiles/Axe_head'),
            'decor' : load_images('Tiles/Decor'),
            'player': load_image('Entity_sprites/Player/Player.png')
        }
        
        print(self.assets)

        self.player = EntityPhysics(self, 'player', (50, 50), (32, 32))

    def run(self):

        while True:
            #this is the code to set the fps
            self.clock.tick(60)
            #background always renders first to prevent things from being covered by it
            self.display.blit(self.bg, (0,0))

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)


            #==== INPUTS ====#
            for event in p.event.get():
                if event.type == p.QUIT: #quit the game
                    p.quit() #closes pygame
                    sys.exit() #quits the program
                if event.type == p.KEYDOWN: # movement
                    if event.key == p.K_a:
                        self.movement[0] = True #moves left
                    if event.key == p.K_d:
                        self.movement[1] = True #moves right
                if event.type == p.KEYUP:
                    if event.key == p.K_a:
                        self.movement[0] = False #stops moving left
                    if event.key == p.K_d:
                        self.movement[1] = False #stops moving right
            self.win.blit(p.transform.scale(self.display, self.screen_size), (0, 0))
            p.display.update() 
            p.display.flip()

# Calls the class and runs the game.    
Game().run()