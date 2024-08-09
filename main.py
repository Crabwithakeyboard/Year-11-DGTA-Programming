import pygame as p
from pygame import image
from Scripts.utility_code import load_image, load_images
from Scripts.entities import EntityPhysics
from Scripts.tilemap import Tilemap
import sys

INTERACTABLE_TILES = {'stool'}  # These are the tiles that can be interacted with

class Game:
    def __init__(self):
        # Initialize/activate pygame
        p.init()

        # Display size
        self.screen_size = (1280, 960)
        self.win = p.display.set_mode(self.screen_size)  # Window size

        self.display = p.Surface((640, 480))  # Actual game render surface size

        # Game caption
        p.display.set_caption("Book 20")

        # Setting the time in pygame to computer time
        self.clock = p.time.Clock()

        # Background image
        self.bg = p.image.load('Data/images/Background/Indoor/0.png')

        self.movement = [False, False]
        

        self.assets = {
            'grass': load_images('Tiles/Grass'),
            'path': load_images('Tiles/Path'),
            'axe_head': load_images('Tiles/Axe_head'),
            'decor': load_images('Tiles/Decor'),
            'stool': load_images('Tiles/Stool'),
            'player': load_image('Entity_sprites/Player/Player.png')
        }

        self.player = EntityPhysics(self, 'player', (80, 1), (32, 32))
        self.tilemap = Tilemap(self, tile_size=32)

       

    def run(self):
        while True:
            # This is the code to set the fps
            self.clock.tick(60)
            # Background always renders first to prevent things from being covered by it
            self.display.blit(self.bg, (0, 0))

            self.tilemap.render(self.display)

            # ==== INPUTS ====#
            for event in p.event.get():
                if event.type == p.QUIT:  # Quit the game
                    p.quit()  # Closes pygame
                    sys.exit()  # Quits the program
                if event.type == p.KEYDOWN:  # Movement
                    if event.key == p.K_a:
                        self.movement[0] = True  # Moves left
                    if event.key == p.K_d:
                        self.movement[1] = True  # Moves right
                    if event.key == p.K_w:
                        self.player.velocity[1] = -4
                    if event.key == p.K_s:
                        self.interact = True
                        for rect in self.tilemap.interact_rects(self.player.pos):
                            if self.player.physics_rect().colliderect(rect):
                                print('Interacted with stool!')
                                for loc, tile in self.tilemap.tilemap.items():
                                    if tile['type'] == 'stool' and tile['pos'] == (rect.x // self.tilemap.tile_size, rect.y // self.tilemap.tile_size):
                                        tile['var'] = 1
                if event.type == p.KEYUP:
                    if event.key == p.K_a:
                        self.movement[0] = False  # Stops moving left
                    if event.key == p.K_d:
                        self.movement[1] = False  # Stops moving right
                    if event.key == p.K_s:
                        self.interact = False


            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)
            self.win.blit(p.transform.scale(self.display, self.screen_size), (0, 0))

            p.display.flip()

# Calls the class and runs the game.
Game().run()
