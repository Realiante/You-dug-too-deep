import resources


def __effect_key(maze, character, pos):
    character.can_exit = True
    maze.dirty = True


def __effect_win(maze, character, pos):
    character.win = True


def __effect_damage_light(maze, character, pos):
    character.take_damage(1)


def __effect_on_set_player(maze, character, pos):
    maze.player_pos = pos[1], pos[0]


def __effect_on_set_key(maze, character, pos):
    maze.key_pos = pos[1], pos[0]


def __effect_on_set_end(maze, character, pos):
    maze.end_pos = pos[1], pos[0]


# TODO: load this part of the script from file
# index dictionary
# [0] immutable collection of possible textures,
# [1] path cost modifier (0 is regular, >10 is considered impassable),
# [2] tile on step event (arguments: Maze, Character, pos(x:int , y:int)),
# [3] tile on set event (arguments: Maze, Character, pos(x:int , y:int))
# [4] is this a base tile? Base tiles will be ignored if attempt is made to load them after the first layer
# [5] is this tile unique? When second instance of this tile is encountered it will be ignored.
dictionary = {
    'f': (resources.load_img_dir("tex/floor"), 0, None, None, True, False),
    'start': (None, 0, None, __effect_on_set_player, False, True),
    'w': (resources.load_img_dir("tex/wall"), 999, None, None, True, False),
    'key': ((resources.load_img("tex/key.png"),), -3, __effect_key, __effect_on_set_key, False, True),
    'end': ((resources.load_img("tex/door.png"),), 0, __effect_win, __effect_on_set_end, False, True),
    'trap': ((resources.load_img("tex/trap.png"),), 2, __effect_damage_light, None, True, False)
}
