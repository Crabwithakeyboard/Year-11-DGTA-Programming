ENTITY_SURROUND_TILES = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1), (0, 0)] #list of all the tiles around an entity. this is used in collision detection to only check for collision with the tiles surrounding the entity

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.decor_tiles = []

        ###============= GRID IS 20 X 13 GRIDS ===========###

        for i in range (20):
            self.tilemap[str (3+i) + ';0'] = {'type' : 'path', 'var' : 0, 'pos' : (i, 13)}
        for i in range(12):
            self.tilemap['0;' + str(3 + i)] = {'type' : 'axe_head', 'var' : 0, 'pos' : (7 + i, 12)}

    def tiles_around_entity(self, pos): #
        tile_loc = (int(pos[0] // self.tile_size)) 

    def render(self, surf):
        for tile in self.decor_tiles:
            surf.blit(self.game.assets[tile['type']][tile['var']], tile['pos'])
            
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['var']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
            

