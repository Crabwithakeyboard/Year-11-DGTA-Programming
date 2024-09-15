import os
import pygame as p

BASE_IMAGE_PATH = 'Data/images/'

def load_image(path):
    img = p.image.load(BASE_IMAGE_PATH + path).convert_alpha()
    return img

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMAGE_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images

ENTITY_SURROUND_TILES = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

PHYSICS_TILES = {'grass', 'path', 'axe_head'}

INTERACTABLE_TILES = {'stool'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.decor_tiles = []

        for i in range(20):
            self.tilemap[str(i) + ';13'] = {'type': 'path', 'var': 0, 'pos': (i, 13)}
        for i in range(12):
            self.tilemap[str(7 + i) + ';12'] = {'type': 'axe_head', 'var': 0, 'pos': (7 + i, 12)}
        for i in range(1):
            self.tilemap[str(3 + i) + ';12'] = {'type': 'stool', 'var': 0, 'pos': (3 + i, 12)}

    def tiles_around_entity(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in ENTITY_SURROUND_TILES:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around_entity(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(p.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def interact_rects(self, pos):
        inter_rects = []
        for tile in self.tiles_around_entity(pos):
            if tile['type'] in INTERACTABLE_TILES:
                inter_rects.append(p.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return inter_rects

    def render(self, surf):
        for tile in self.decor_tiles:
            surf.blit(self.game.assets[tile['type']][tile['var']], tile['pos'])

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['var']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))

class EntityPhysics:
    def __init__(self, main, entity_type, pos, size):
        self.main = main
        self.type = entity_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.interact = False

    def physics_rect(self):
        return p.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        perFrame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        self.velocity[1] += 0.1
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        self.pos[0] += perFrame_movement[0]
        entity_rect = self.physics_rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if perFrame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if perFrame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += perFrame_movement[1]
        entity_rect = self.physics_rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if perFrame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if perFrame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        for rect in tilemap.interact_rects(self.pos):
            if entity_rect.colliderect(rect) and self.interact:
                self.main.handle_interaction(tilemap, rect)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    def render(self, surf):
        surf.blit(self.main.assets['player'], self.pos)

class Game:
    def __init__(self):
        p.init()

        self.screen_size = (1280, 960)
        self.win = p.display.set_mode(self.screen_size)

        self.display = p.Surface((640, 480))

        p.display.set_caption("Book 20")

        self.clock = p.time.Clock()

        self.bg = p.image.load('Data/images/Background/Indoor/0.png')

        self.movement = [False, False]
        self.interact = False

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

    def handle_interaction(self, tilemap, rect):
        for tile_key, tile in tilemap.tilemap.items():
            tile_rect = p.Rect(tile['pos'][0] * tilemap.tile_size, tile['pos'][1] * tilemap.tile_size, tilemap.tile_size, tilemap.tile_size)
            if tile_rect.colliderect(rect) and tile['type'] == 'stool':
                print('Interacted with stool at position:', tile['pos'])

    def run(self):
        while True:
            self.clock.tick(60)
            self.display.blit(self.bg, (0, 0))
            self.tilemap.render(self.display)

            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()
                if event.type == p.KEYDOWN:
                    if event.key == p.K_a:
                        self.movement[0] = True
                    if event.key == p.K_d:
                        self.movement[1] = True
                    if event.key == p.K_w:
                        self.player.velocity[1] = -4
                    if event.key == p.K_s:
                        self.interact = True
                if event.type == p.KEYUP:
                    if event.key == p.K_a:
                        self.movement[0] = False
                    if event.key == p.K_d:
                        self.movement[1] = False
                    if event.key == p.K_s:
                        self.interact = False

            self.player.interact = self.interact
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            self.win.blit(p.transform.scale(self.display, self.screen_size), (0, 0))
            p.display.flip()

Game().run()
