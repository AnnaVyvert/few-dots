import random
from tkinter import *
# import Tkinter as tk
import math
import copy

root = Tk()

root.title("the thing, score: " + str(0))

canvas_width = 500
canvas_height = 500
food_tick_create = 100
enemy_tick_create = 250
circle_radius = 10
to_move = 4
move_positions = []
food_positions = []
enemy_positions = []


# реакция на клик левой кнопкой мыши
def on_left_mouse_click(event):
    if not data["game_is_over"]:
        x, y = event.x, event.y
        move_positions.append([x, y])
        print(x, y)
        canvas.delete("move" + str(data['n_move']))
        data['n_move'] += 1
        canvas.create_circle(x, y, 4, fill="green", outline="#282828", width=2, tags='move' + str(data['n_move']))
        data["fix_position"] = data["position"]


def create_food():
    x = random.randint(0, canvas_width)
    y = random.randint(0, canvas_height)
    food_positions.append([x, y])
    canvas.create_circle(x, y, circle_radius, fill="yellow", outline="#282828", width=4,
                         tags='food' + str(data['n_food']))
    data['n_food'] += 1
    print(food_positions)
    # print(f' {x}, {y}')


def create_enemy():
    x = random.randint(0, canvas_width * random.randint(0, 1))
    y = random.randint(0, canvas_height * random.randint(0, 1))
    x, y = abs(x), abs(y)
    enemy_positions.append([x, y])
    canvas.create_circle(x, y, circle_radius, fill="red", outline="#282828", width=4,
                         tags='enemy' + str(data['n_enemy']))
    data['n_enemy'] += 1


def move_enemies():
    hunter_position = data['position']
    try:
        for i in range(len(enemy_positions)):
            e = enemy_positions[i]
            fixed_hunter_position = copy.copy(e)
            move_position = hunter_position
            index = interact_axis(e, move_position)
            index2 = 1 if index == 0 else 0
            e_speed = (data['speed'] - 2) + math.cos((data['counter'] % 1000) / 318 - math.pi) + 1
            # print('speed: ', e_speed)
            direction = right_direction(e, move_position, index)
            e[index] += direction * e_speed
            # print(fixed_hunter_position, move_position, e[index])
            if index == 0:
                e[index2] = line_y(fixed_hunter_position, move_position, e[index])
            else:
                e[index2] = line_x(fixed_hunter_position, move_position, e[index])
    except Exception as e:
        print(e)


def field_borders():
    hunter_position = data['position']
    if 0 > hunter_position[0] > canvas_width:
        hunter_position[0] = canvas_width / 2
    if 0 > hunter_position[1] > canvas_width:
        hunter_position[1] = canvas_height / 2


# реакция на клик правой кнопкой мыши
def on_right_mouse_click(event):
    x, y = event.x, event.y
    print(f'Правая: {x}, {y}')


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle = _create_circle

data = {
    "game_is_over": False,
    "counter": 0,
    "mouse": (0, 0),
    "position": [canvas_width / 2, canvas_height / 2],
    "fix_position": [canvas_width / 2, canvas_height / 2],
    "circle_location": (250, 100),
    "circle_velocity": (0, 0),  # добавили вектор скорости кружочка
    "speed": 3,  # снизим скорость чуток
    "n_move": -1,
    "n_food": 0,
    "n_enemy": 0,
    "eaten": 0,
}


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
        move_position = move_positions[data['n_move']]
        index = interact_axis(hunter_position, move_position)
        index2 = 1 if index == 0 else 0
        # direction = -1 if hunter_position[0] > move_position[0] else 1
        # direction = -1 if hunter_position[1] > move_position[1] else 1
        direction = right_direction(fixed_hunter_position, move_position, index)
        # if direction * hunter_position[0] < move_position[0]:
        hunter_position[index] += direction * data['speed']
        if index == 0:
            hunter_position[index2] = line_y(fixed_hunter_position, move_position, hunter_position[index])
        else:
            hunter_position[index2] = line_x(fixed_hunter_position, move_position, hunter_position[index])
        # print(hunter_position, move_position)
        data['position'] = hunter_position
    except:
        pass


def check_hunter_collapse():
    hunter_position = data['position']
    for i in range(len(food_positions)):
        e = food_positions[i]
        if e[0] is None or e[1] is None: continue
        collapse_condition = e[0] - circle_radius < hunter_position[0] < e[0] + circle_radius and e[1] - circle_radius < \
                             hunter_position[1] < e[1] + circle_radius
        if collapse_condition:
            canvas.delete("food" + str(i))
            e[0], e[1] = None, None
            data["eaten"] += 1
            root.title("the thing, score: " + str(data["eaten"]))
            # data['position'] = e
            # data['fix_position'] = e


def round_move():
    hunter_position = data['position']
    try:
        e = copy.copy(move_positions[data['n_move']])
        collapse_condition = e[0] - to_move < hunter_position[0] < e[0] + to_move and e[1] - to_move < hunter_position[
            1] < e[1] + to_move
        if collapse_condition:
            data['position'] = e
            data['fix_position'] = e
    except:
        pass


def enemy_collapse():
    hunter_position = data['position']
    for i in range(len(enemy_positions)):
        e = enemy_positions[i]
        if e[0] is None or e[1] is None: continue
        collapse_condition = hunter_position[0] - circle_radius < e[0] < hunter_position[0] + circle_radius and \
                             hunter_position[1] - circle_radius < \
                             e[1] < hunter_position[1] + circle_radius
        if collapse_condition:
            data["game_is_over"] = True


def on_tick():
    update()  # обновляем положение объектов на канве
    if data['counter'] % food_tick_create == 0:
        create_food()

    if data['counter'] % enemy_tick_create == 0:
        create_enemy()

    hunter_move()
    move_enemies()
    check_hunter_collapse()
    enemy_collapse()
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
    # x, y = data['mouse']
    x = data['position'][0]
    y = data['position'][1]
    try:
        for i in range(len(enemy_positions)):
            e = enemy_positions[i]
            canvas.create_circle(e[0], e[1], circle_radius, fill="red", outline="#282828", width=4,
                                 tags='enemy' + str(i))
    except:
        pass
    # рисуем кружок
    if not data["game_is_over"]:
        canvas.create_circle(x, y, circle_radius, fill="orange", outline="#282828", width=4, tags='hunter')


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
    # return p1[axis] > p2[axis]


def to_the_up(self):
    data['position'][1] -= data['speed']

def to_the_left(self):
    data['position'][0] -= data['speed']

def to_the_low(self):
    data['position'][1] += data['speed']

def to_the_right(self):
    data['position'][0] += data['speed']


def restart(event):
    root.title("the thing, score: " + str(0))
    data["game_is_over"] = False



canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="#111")
canvas.pack()
canvas.focus_set()
canvas.bind('<Button-1>', on_left_mouse_click)
canvas.bind('<Key-w>', to_the_up)
canvas.bind('<Key-a>', to_the_left)
canvas.bind('<Key-s>', to_the_low)
canvas.bind('<Key-d>', to_the_right)
canvas.bind('<Key-r>', restart)

on_tick()

root.mainloop()
