import libtcodpy as libtcod

def handle_keys(key):
    moveX = 0
    moveY = 0
    
    up_p = False
    down_p = False
    left_p = False
    right_p = False

    # Movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        up_p = True
        moveY = moveY - 1
    if libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        down_p = True
        moveY = moveY + 1
    if libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        left_p = True
        moveX = moveX - 1
    if libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        right_p = True
        moveX = moveX + 1
    if (up_p or down_p or left_p or right_p):
        return {'move': (moveX, moveY)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}
    elif key.vk == libtcod.KEY_SPACE:
        return {'smooth': True}

    # No key was pressed
    return {}