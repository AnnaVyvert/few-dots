import random
from tkinter import *
# import Tkinter as tk
import math
import copy
from config import consts
from storage import data

root = Tk()

init_title = "few-dots, score: " + str(data["eaten"]) + ', bombs: ' + str(data["n_bombs"])
root.title(init_title)
# root.iconbitmap("ico.ico")
photo = PhotoImage(file="assets/ico.png")
root.iconphoto(False, photo)

move_positions = []
food_positions = []
enemy_positions = []
bomb_positions = []
bomb_init_positions = []
right_positions = []


# реакция на клик левой кнопкой мыши
def on_left_mouse_click(event):
    if not data["game_is_over"]:
        x, y = event.x, event.y
        global move_positions
        move_positions = [x, y]
        canvas.delete("move" + str(data['n_move']))
        data['n_move'] += 1
        create_circle(x, y, 4, fill="green", outline="#282828", width=2, tags='move' + str(data['n_move']))
        data["fix_position"] = data["position"]


def on_right_mouse_click(event):
    x, y = event.x, event.y
    if data['n_bombs'] > 0:
        bomb_positions.append([data['position'][0], data['position'][1]])
        right_positions.append([x, y])
        create_circle(data['position'][0], data['position'][1], 10, fill="violet", outline="#282828", width=4,
                      tags='bomb' + str(data['n_bomb']))
        data['n_bombs'] -= 1
        data['n_bomb'] += 1
        root.title("few-dots, score: " + str(data["eaten"]) + ', bombs: ' + str(data["n_bombs"]))
    if data['game_is_over']:
        restart(0)

def create_food():
    x = random.randint(0, consts['canvas_width'])
    y = random.randint(0, consts['canvas_height'])
    food_positions.append([x, y])
    create_circle(x, y, consts['circle_radius'], fill="yellow", outline="#282828", width=4,
                  tags='food' + str(data['n_food']))
    data['n_food'] += 1


def create_bomb():
    x = random.randint(0, consts['canvas_width'])
    y = random.randint(0, consts['canvas_height'])
    bomb_init_positions.append([x, y])
    create_circle(x, y, 10, fill="pink", outline="#282828", width=4,
                  tags='bomb_init' + str(data['n_bomb_init']))
    data['n_bomb_init'] += 1


def create_enemy():
    x = consts['canvas_width'] * random.randint(0, 1)
    y = consts['canvas_height'] * random.randint(0, 1)
    enemy_positions.append([x, y])
    create_circle(x, y, consts['circle_radius'], fill="red", outline="#282828", width=4,
                  tags='enemy' + str(data['n_enemy']))
    data['n_enemy'] += 1


def move_enemies():
    hunter_position = data['position']
    try:
        for i in range(len(enemy_positions)):
            e = enemy_positions[i]
            if e[0] is None or e[1] is None: continue
            fixed_hunter_position = copy.copy(e)
            e_speed = (data['speed'] - 2) + math.cos((data['counter'] % 1000) / 318 - math.pi) + 1
            move_dot(e, fixed_hunter_position, hunter_position, e_speed)
    except Exception as e:
        # print(1, e)
        pass


def collapse_bombs():
    # print(enemy_positions, bomb_positions)
    for i in range(len(enemy_positions)):
        for j in range(len(bomb_positions)):
            e = enemy_positions[i]
            e2 = bomb_positions[j]
            if e[0] is None or e[1] is None: continue
            if e2[0] is None or e2[1] is None: continue
            collapse_condition = e2[0] - consts['circle_radius'] < e[0] < e2[0] + consts['circle_radius'] and \
                                 e2[1] - consts['circle_radius'] < \
                                 e[1] < e2[1] + consts['circle_radius']
            if collapse_condition:
                canvas.delete("bomb" + str(j))
                e[0], e[1] = None, None
                e2[0], e2[1] = None, None


def create_circle(x, y, r, **kwargs):
    return canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)


# create_circle = _create_circle

def get_bomb():
    hunter_position = data['position']
    for i in range(len(bomb_init_positions)):
        e = bomb_init_positions[i]
        if e[0] is None or e[1] is None: continue
        collapse_condition = e[0] - consts['circle_radius'] < hunter_position[0] < e[0] + consts['circle_radius'] and e[
            1] - consts['circle_radius'] < \
                             hunter_position[1] < e[1] + consts['circle_radius']
        if collapse_condition:
            canvas.delete("bomb_init" + str(i))
            e[0], e[1] = None, None
            # data["n_bomb_init"] += 1
            data['n_bombs'] += 1
            root.title("few-dots, score: " + str(data["eaten"]) + ', bombs: ' + str(data["n_bombs"]))


def update():
    cx, cy = data['circle_location']
    c_vx, c_vy = data['circle_velocity']  # вытаскиваем теперь еще и скорость
    # mx, my = data['mouse']
    mx = data['position'][0]
    my = data['position'][1]

    # тут ничего не меняем
    vx = mx - cx
    vy = my - cy
    length = math.sqrt(vx ** 2 + vy ** 2)
    vx /= length
    vy /= length

    # тут теперь пересчитываем c_vx и c_vy
    c_vx += vx * data['speed']
    c_vy += vy * data['speed']

    # тормозящий момент
    c_vx -= c_vx * 0.2
    c_vy -= c_vy * 0.2

    # сдвигаем cx и cy на c_vx и c_vy
    cx += c_vx
    cy += c_vy

    # фиксируем координаты и скорость кружка в data
    data['circle_velocity'] = (c_vx, c_vy)
    data['circle_location'] = (cx, cy)


def hunter_move():
    hunter_position = data['position']
    fixed_hunter_position = copy.copy(data["fix_position"])
    try:
        move_dot(hunter_position, fixed_hunter_position, move_positions, data['speed'])
    except Exception as e:
        # print(2, e)
        pass


def move_dot(source_dot_position, fixed_dot_position, move_position, speed):
    index = interact_axis(source_dot_position, move_position)
    index2 = 1 if index == 0 else 0
    direction = right_direction(fixed_dot_position, move_position, index)
    source_dot_position[index] += direction * speed
    if index == 0:
        source_dot_position[index2] = line_y(fixed_dot_position, move_position, source_dot_position[index])
    else:
        source_dot_position[index2] = line_x(fixed_dot_position, move_position, source_dot_position[index])
    # print(hunter_position, move_position)
    # data['position'] = source_dot_position


def check_hunter_collapse():
    hunter_position = data['position']
    for i in range(len(food_positions)):
        e = food_positions[i]
        if e[0] is None or e[1] is None: continue
        collapse_condition = e[0] - consts['circle_radius'] < hunter_position[0] < e[0] + consts['circle_radius'] and e[
            1] - consts['circle_radius'] < \
                             hunter_position[1] < e[1] + consts['circle_radius']
        if collapse_condition:
            canvas.delete("food" + str(i))
            e[0], e[1] = None, None
            data["eaten"] += 1
            root.title("few-dots, score: " + str(data["eaten"]) + ', bombs: ' + str(data["n_bombs"]))
            # data['position'] = e
            # data['fix_position'] = e


def round_move():
    hunter_position = data['position']
    try:
        e = copy.copy(move_positions)
        collapse_condition = e[0] - consts['distance4capture'] < hunter_position[0] < e[0] + consts[
            'distance4capture'] and e[1] - consts['distance4capture'] < hunter_position[
                                 1] < e[1] + consts['distance4capture']
        if collapse_condition:
            data['position'] = e
            data['fix_position'] = e
    except Exception as e:
        # print(3, e)
        pass


def enemy_collapse():
    hunter_position = data['position']
    for i in range(len(enemy_positions)):
        e = enemy_positions[i]
        if e[0] is None or e[1] is None: continue
        collapse_condition = hunter_position[0] - consts['circle_radius'] < e[0] < hunter_position[0] + consts[
            'circle_radius'] and \
                             hunter_position[1] - consts['circle_radius'] < \
                             e[1] < hunter_position[1] + consts['circle_radius']
        if collapse_condition:
            data["game_is_over"] = True


def enemies_collapse():
    for i in range(len(enemy_positions)):
        for j in range(i + 1, len(enemy_positions)):
            e = enemy_positions[i]
            e2 = enemy_positions[j]
            if e[0] is None or e[1] is None: continue
            if e2[0] is None or e2[1] is None: continue
            collapse_condition = e2[0] - consts['circle_radius'] < e[0] < e2[0] + consts['circle_radius'] and \
                                 e2[1] - consts['circle_radius'] < \
                                 e[1] < e2[1] + consts['circle_radius']
            if collapse_condition:
                e[0] = consts['canvas_width'] * random.randint(0, 1)
                e[1] = consts['canvas_height'] * random.randint(0, 1)


def on_tick():
    update()  # обновляем положение объектов на канве
    if data['counter'] % consts['food_tick_create'] == 0:
        create_food()
    if data['counter'] % consts['bomb_tick_create'] == 0:
        create_bomb()
    if data['counter'] % consts['enemy_tick_create'] == 0:
        create_enemy()

    hunter_move()
    move_enemies()
    collapse_bombs()
    check_hunter_collapse()
    enemy_collapse()
    enemies_collapse()
    get_bomb()
    round_move()
    # field_borders()
    canvas.delete("hunter")
    for i in range(len(enemy_positions)):
        canvas.delete("enemy" + str(i))
    if data["game_is_over"]:
        canvas.delete("move" + str(data['n_move']))
    else:
        data['counter'] += 1  # увеличиваем счетчик итераций
        root.after(33, on_tick)  # перезапускаем счетчик
    draw_all()


def draw_all():
    x = data['position'][0]
    y = data['position'][1]
    try:
        for i in range(len(enemy_positions)):
            if enemy_positions[i][0] is None: continue
            e = enemy_positions[i]
            create_circle(e[0], e[1], consts['circle_radius'], fill="red", outline="#282828", width=4,
                          tags='enemy' + str(i))
    except Exception as e:
        # print(4, e)
        pass
    if not data["game_is_over"]:
        create_circle(x, y, consts['circle_radius'], fill="orange", outline="#282828", width=4, tags='hunter')


# def on_mouse_move(event):
#     data['mouse'] = (event.x, event.y)

def line_y(p1, p2, x):
    return (x - p1[0]) * (p2[1] - p1[1]) / (p2[0] - p1[0]) + p1[1]


def line_x(p1, p2, y):
    a = (p2[0] - p1[0]) / (p2[1] - p1[1])
    return p1[0] + y * a - p1[1] * a


def interact_axis(p1, p2):
    return 0 if abs(p2[0] - p1[0]) > abs(p2[1] - p1[1]) else 1


def right_direction(p1, p2, axis):
    return -1 if p1[axis] > p2[axis] else 1


def restart(event):
    if data["game_is_over"] is True:
        canvas.delete('all')
        root.title(init_title)
        data["game_is_over"] = False
        data["counter"] = 0
        data["mouse"] = (0, 0)
        data["position"] = [consts['canvas_width'] / 2, consts['canvas_height'] / 2]
        data["fix_position"] = [consts['canvas_width'] / 2, consts['canvas_height'] / 2]
        data["circle_location"] = (250, 100)
        data["circle_velocity"] = (0, 0)
        data["n_move"] = -1
        data["n_food"] = 0
        data["n_enemy"] = 0
        data["n_bomb_init"] = 0
        data["n_bomb"] = 0
        data["n_bombs"] = 1
        data["eaten"] = 0
        global move_positions, food_positions, enemy_positions, bomb_positions, bomb_init_positions
        move_positions, food_positions, enemy_positions, bomb_positions, bomb_init_positions = [], [], [], [], []
        on_tick()


canvas = Canvas(root, width=consts['canvas_width'], height=consts['canvas_height'], bg="#111")
canvas.pack()
canvas.focus_set()
canvas.bind('<Button-1>', on_left_mouse_click)
canvas.bind('<Button-3>', on_right_mouse_click)
canvas.bind('<Key-r>', restart)

on_tick()

root.mainloop()
