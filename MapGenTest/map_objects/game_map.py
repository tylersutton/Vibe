import tcod as libtcod
from random import randint

from entity import Entity
from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        return tiles
    
    def make_map(self, player, entities, max_monsters_per_room):
        fill_percentage = 43
        map_bound = 3
        spawn_radius = 3
        path_half_width = (self.width + self.height) // 16

        for y in range(self.height):
            for x in range(self.width):
                if randint(0,100) <= fill_percentage:
                    self.tiles[x][y].blocked = True
                    self.tiles[x][y].block_sight = True
                elif x < map_bound or y < map_bound or x >= self.width-map_bound or y >= self.height-map_bound:
                    self.tiles[x][y].blocked = True
                    self.tiles[x][y].block_sight = True
                
                #temp addition to see map
                self.tiles[x][y].explored = True
        
        #open_side = randint(0,3)
        open_side = 3
        print(open_side)
        y_mid = self.height // 2
        x_mid = self.width // 2
        y_bot = 0
        y_top = 0
        x_bot = 0
        x_top = 0

        if open_side == 0: #right side
            x_bot = self.width - (path_half_width*2)
            x_top = self.width
            y_bot = y_mid - path_half_width
            y_top = y_mid + path_half_width
        if open_side == 1: #top side
            x_bot = x_mid - path_half_width
            x_top = x_mid + path_half_width
            y_bot = 0
            y_top = (path_half_width*2)
        if open_side == 2: #left side
            x_bot = 0
            x_top = path_half_width*2
            y_bot = y_mid - path_half_width
            y_top = y_mid + path_half_width

        if open_side == 3: #bottom side
            x_bot = x_mid - path_half_width
            x_top = x_mid + path_half_width
            y_bot = self.height - (path_half_width*2)
            y_top = self.height
        
        for y in range(y_bot, y_top):
            for x in range(x_bot, x_top):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

        for x in range(10):
            self.smooth_tiles()
        
        (player.x, player.y) = self.find_spawn(spawn_radius)
        self.place_entities(entities, max_monsters_per_room)

    def find_spawn(self, radius):
        spawn_found = False
        while (not spawn_found):
            spawn_found = True
            new_x = randint(radius,self.width-radius)
            new_y = randint(radius,self.height-radius)
            for x in range( new_x - radius, new_x + radius + 1):
                for y in range(new_y - radius, new_y + radius + 1):
                    x_dist = new_x - x
                    y_dist = new_y - y
                    if(((x_dist*x_dist) + (y_dist*y_dist)) <= (radius*radius)) and self.tiles[x][y].blocked:
                        spawn_found = False
                    if not spawn_found:
                        break
                if not spawn_found:
                    break

        return (new_x, new_y)

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

    def place_entities(self, entities, max_monsters_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        for _ in range(number_of_monsters):
            # Choose a random location in the room
            # radius of 1 because enemies will just walk around anyway
            (x, y) = self.find_spawn(1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 50:
                    monster = Entity(x, y, 'B', libtcod.white, 'Bobcat', blocks=True)
                else:
                    monster = Entity(x, y, 'W', libtcod.white, 'Wolf', blocks=True)

                entities.append(monster)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
