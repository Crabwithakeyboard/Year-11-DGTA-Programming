import pygame as p
from pygame import image
from Scripts.utility_code import load_image, load_images
from Scripts.entities import EntityPhysics
from Scripts.entities import Arrow
from Scripts.entities import Bullet
from Scripts.tilemap import Tilemap
import sys



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
            'player': load_image('Entity_sprites/Player/Player.png'),
            'arrow' : load_image('Entity_sprites/Arrow/arrow.png')
        }
        print(self.assets)
        self.player = EntityPhysics(self, 'player', (400, 400), (32, 32))#Runs the EntityPhysics code on self.player
        
        self.tilemap = Tilemap(self, tile_size=32) #render's the tilemap
        self.cam_scroll = [0, 0] # camera movement, it in itially starts at the top corner of the screen.
        self.arrows = []
        self.bullets = []
        


    def run(self):
        while True:
            # This is the code to set the fps
            self.clock.tick(60)
            # Background always renders first to prevent things from being covered by it
            self.display.blit(self.bg, (0, 0))
            # print(str(self.cam_scroll[0]) + ',' + str(self.cam_scroll[1]))
            self.cam_scroll[0] += (self.player.physics_rect().centerx - self.display.get_width() / 2 - self.cam_scroll[0]) / 1

            self.tilemap.render(self.display, camera_scroll = self.cam_scroll)
            
            self.pos = self.player.pos
            

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
                        self.player.velocity[1] = -4 #upward velocity set to 4, makes player jump
                    if event.key == p.K_s:
                        self.interact = True #If player presses 's' key, then the player is trying to interact with something, so set the interact value to true.
                        for rect in self.tilemap.interact_rects(self.player.pos): # runs the indented code for every tile in the 'inter_rects' list in the interact_rects function in tilemap.py
                            if self.player.physics_rect().colliderect(rect): # Checks if the player's collision hitbox collides with the interactive rects' hitbox
                                print('Interacted') #Used in testing to check if the player has actually interacted with the tile
                                for loc, tile in self.tilemap.tilemap.items(): 
                                    if tile['type'] == 'stool' and tile['pos'] == (rect.x // self.tilemap.tile_size, rect.y // self.tilemap.tile_size):
                                        if len(self.assets[tile['type']]) > 1:
                                            tile['var'] = 1  # Set the stool variant to 1
                                            #print(f"Stool at {tile['pos']} changed to variant {tile['var']}")  # Debugging
                                        #else:
                                            #print(f"No variant 1 available for {tile['type']}")  # Debugging
                    if event.key == p.K_SPACE:
                        """# Spawn a new arrow at the player's position
                        arrow_instance = Arrow(self, 'arrow', (100, 100), self.arrow.size)

                        # Start charging the arrow
                        arrow_instance.charge = True
                        self.arrows.append(arrow_instance)
                        self.bullets.append(Bullet(*self.pos))"""
                if event.type == p.MOUSEBUTTONDOWN:
                    self.bullets.append(Bullet(self, 'arrow', (self.pos[0] - self.cam_scroll[0], self.pos[1] - self.cam_scroll[1]), (32, 32), self.pos, self.cam_scroll))
                    # self.bullets.append(Bullet(self, 'arrow', (self.pos[0] - self.cam_scroll[0], self.pos[1] - self.cam_scroll[1]), (32, 32), self.pos))
                if event.type == p.KEYUP:
                    if event.key == p.K_a:
                        self.movement[0] = False  # Stops moving left
                    if event.key == p.K_d:
                        self.movement[1] = False  # Stops moving right
                    if event.key == p.K_s:
                        self.interact = False
                    if event.key == p.K_SPACE:
                        # For the latest arrow, stop charging and apply velocity
                        if len(self.arrows) > 0:
                            last_arrow = self.arrows[-1]
                            last_arrow.charge = False
                            last_arrow.velocity[0] +=  last_arrow.arrow_charge  # Apply velocity in X
                            last_arrow.velocity[1] +=  last_arrow.arrow_charge  # Apply velocity in Y
                            last_arrow.arrow_charge = 0  # Reset the charge
            

            for bullet in self.bullets[:]:
                bullet.update()
                """if not self.display.get_rect().collidepoint(bullet.pos):
                    self.arrows.remove(bullet)"""
            for bullet in self.bullets:
                bullet.draw(self.display)

            self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]) * 2, 0)) # calculates player movement. x-axis movement boolean from y-adis movement boolean
            self.player.render(self.display, camera_scroll = self.cam_scroll) #renders the player entity onto the display
            self.win.blit(p.transform.scale(self.display, self.screen_size), (0, 0))

            p.display.flip()

# Calls the class and runs the game.
if __name__ == "__main__":
    Game().run()
