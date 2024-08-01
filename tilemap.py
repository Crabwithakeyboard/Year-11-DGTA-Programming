class Tilemap:
    def __init__(self, game, tile_size = 32):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.decor_tiles = []

        for i in range (10):
            self.tilemap[str(3 + i) + ';0'] = {'type' : 'grass', 'var' : 0, 'pos' : (3 + i, 0)}
            self.tilemap['0;' + str(3 + i)] = {'type' : 'decor', 'var' : 0, 'pos' : (0, 3 + i)}

    def render(self, surf):
        for tile in self.decor_tiles:
            surf.blit(self.game.assets[tile['type']][tile['var']], tile['pos'])
            
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['var']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
            

