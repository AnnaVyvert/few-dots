from config import consts

data = {
    "game_is_over": False,
    "counter": 0,
    "mouse": (0, 0),
    "position": [consts['canvas_width'] / 2, consts['canvas_height'] / 2],
    "fix_position": [consts['canvas_width'] / 2, consts['canvas_height'] / 2],
    "circle_location": (250, 100),
    "circle_velocity": (0, 0),
    "speed": 3,
    "n_move": -1,
    "n_food": 0,
    "n_enemy": 0,
    "n_bomb_init": 0,
    "n_bomb": 0,
    "n_bombs": 1,
    "eaten": 0,
}