import tcod as libtcod

from entity import Entity
from map_objects.tile import Tile
from random import randint

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        for x in range(10):
            self.smooth_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        
        fill_percentage = 43
        map_bound = 2
        for y in range(self.height):
            for x in range(self.width):
                if randint(0,100) <= fill_percentage:
                    tiles[x][y].blocked = True
                    tiles[x][y].block_sight = True
                elif x < map_bound or y < map_bound or x >= self.width-map_bound or y >= self.height-map_bound:
                    tiles[x][y].blocked = True
                    tiles[x][y].block_sight = True
        return tiles
    
    def smooth_tiles(self):
        temp = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)
                if (neighbors > 4):
                    temp[x][y].blocked = True
                    temp[x][y].block_sight = True
                elif (neighbors < 4):
                    temp[x][y].blocked = False
                    temp[x][y].block_sight = False
                else:
                    temp[x][y].blocked = self.tiles[x][y].blocked
                    temp[x][y].block_sight = self.tiles[x][y].block_sight
        self.tiles = temp
 

    def count_neighbors(self, x, y):
        num_neighbors = 0
        for j in range (y-1, y+2):
            for i in range(x-1, x+2):
                if (i >= 0 and j >= 0 and j < self.height and i < self.width):
                    if ((j != y or i != x) and self.tiles[i][j].blocked and self.tiles[i][j].block_sight):
                        num_neighbors = num_neighbors + 1
                else:
                    num_neighbors = num_neighbors + 1
        return num_neighbors

    def place_entities(self, room, entities, max_monsters_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    monster = Entity(x, y, 'B', libtcod.desaturated_green)
                else:
                    monster = Entity(x, y, 'W', libtcod.darker_green)

                entities.append(monster)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
