import pygame as p




ENTITY_SURROUND_TILES = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] #list of all the tiles around an entity. this is used in collision detection to only check for collision with the tiles surrounding the entity

PHYSICS_TILES = {'grass', 'path', 'axe_head'} #These are the tiles that are meant to have collision (a set is more efficient at checking for presence of an object within a group than a list)

INTERACTABLE_TILES = {'stool'} #These are the tiles that can be interacted with
class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.decor_tiles = []

        ###============= GRID IS 20 X 13 GRIDS ===========###

        for i in range (20):
            self.tilemap[str (i) + ';13'] = {'type' : 'path', 'var' : 0, 'pos' : (i, 13)}
        for i in range(12):
            self.tilemap[str(7 + i) + ';12'] = {'type' : 'axe_head', 'var' : 0, 'pos' : (7 + i, 12)}
        for i in range(1):
            self.tilemap[str(3 + i) + ';12'] = {'type' : 'stool', 'var' : 1, 'pos' : (3 + i, 12)}

    def tiles_around_entity(self, pos): #this checks for all the tiles surrounding an entity and compiles them into a list
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in ENTITY_SURROUND_TILES:
            check_loc = str(tile_loc[0] + offset[0]) + ';' +  str(tile_loc[1] + offset[1])
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
            



