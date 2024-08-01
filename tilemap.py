class Tilemap:
    def __init__(self, game, tile_size = 32):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range (10):
            self.tilemap[str(3 + i) + ';10'] = {'type' : 'grass', 'var' : 1, 'pos' : (3 + i, 10)}
            self.tilemap['10;' + str(3 + i)] = {'type' : 'decor', 'var' : 1, 'pos' : (10, 3 + i)}




