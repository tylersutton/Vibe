import tcod as libtcod
import time

from components.fighter import Fighter
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    fov_algorithm = 2
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 10

    time_moved_last = time.time()

    colors = {
        'dark_wall': libtcod.Color(10, 45, 25),
        'dark_ground': libtcod.Color(12, 60, 37),
        'light_wall': libtcod.Color(40, 80, 20),
        'light_ground': libtcod.Color(45, 115, 50)
    }

    fighter_component = Fighter(hp=30, defense=2, power=5, speed=10)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, fighter=fighter_component)
    entities = [player]
    
    libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

    con = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(player, entities, max_monsters_per_room)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        smooth = action.get('smooth')

        if move:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if(time.time() - time_moved_last > (1/player.fighter.speed)):
                    if target:
                        print('You kick the ' + target.name + ' in the shins, much to its annoyance!')
                    else:
                        player.move(dx, dy)
                        fov_recompute = True
                    time_moved_last = time.time()

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        
        if smooth:
            game_map.smooth_tiles()


if __name__ == '__main__':
     main()
