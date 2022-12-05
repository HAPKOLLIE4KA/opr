import tkinter as tk
from my_constants import *


def coor_trans_x(x):
    return cx + x * length_interval_x


def coor_trans_y(y):
    return cy + y * length_interval_y


def draw_axis(canvas: tk.Canvas):
    canvas.create_line(0, cy, CANVAS_W, cy)
    canvas.create_line(cx, 0, cx, CANVAS_H)

    for number in range(1, intervals):
        text = str(number - intervals // 2) if number - intervals // 2 != 0 else ""
        x = left_x + length_interval_x * number
        canvas.create_line(x, cy - 3, x, cy + 3)
        canvas.create_text(x, cy + 8,
                           text=text,
                           font=("", 7)
                           )

    for number in range(1, intervals):
        text = str(number - intervals // 2) if number - intervals // 2 != 0 else ""
        y = bottom_y - length_interval_y * number
        canvas.create_line(cx - 2, y, cx + 2, y)
        canvas.create_text(cx + 10, y,
                           text=text,
                           font=("", 7)
                           )


def begin_draw_canvas(canvas):  # просто удалить все, кроме первой строки
    draw_axis(canvas)


def generation_half_arrays(array):
    half_1 = []
    half_2 = []

    for coord in array:
        if coord["x"] <= cx:
            half_1 += [coord["x"], coord['y']]
        elif coord["x"] >= cx:
            half_2 += [coord["x"], coord['y']]
    return half_1, half_2


def draw_halfs(canvas, half_1, half_2):
    half_1_line, half_2_line = None, None
    if len(half_1) > 3:
        half_1_line = canvas.create_line(half_1, fill="blue", width=2)
    if len(half_2) > 3:
        half_2_line = canvas.create_line(half_2, fill="blue", width=2)

    return [half_1_line, half_2_line]


def delete_graph(canvas, array_lines):
    for line in array_lines: canvas.delete(line)


def calculation_half_arrays(func):
    lx_math = 1 - intervals // 2
    rx_math = intervals - 1 - intervals // 2
    lx_canv = left_x + length_interval_x
    array = []

    while lx_math <= rx_math:
        try:
            x = round(lx_canv, 2)
            y = round(cy - length_interval_y * func(lx_math), 2)
            if 0 <= x <= CANVAS_W and 0 <= y <= CANVAS_H:
                array += [{"x": x, "y": y}]
        except Exception:
            pass

        lx_math += diff
        lx_canv += diff * length_interval_x

    return array

def func_block(canvas, func):
    array = calculation_half_arrays(func)
    half_1, half_2 = generation_half_arrays(array)
    return draw_halfs(canvas, half_1, half_2)


def draw_root(canvas, root, func):
    x, y = cx + root * length_interval_x, cy + length_interval_y * func(root)
    return canvas.create_line(x - 1, y + 1,
                              x + 1, y + 1,
                              x + 1, y - 1,
                              x - 1, y - 1,
                              fill="red", width=5)


def draw_a_b(canvas, a, b, line1, line2):
    x_a, x_b = coor_trans_x(a), coor_trans_x(b)
    if (line1, line2) != (None, None):
        canvas.delete(line1)
        canvas.delete(line2)
    line1 = canvas.create_line(x_a, cy - 10, x_a, cy + 10, fill="red", width=2)
    line2 = canvas.create_line(x_b, cy - 10, x_b, cy + 10, fill="red", width=2)

    return line1, line2


def draw_point(canvas, x, point):
    if point is not None: canvas.delete(point)
    x = coor_trans_x(x)
    point = canvas.create_line(x - 1, cy + 1,
                               x + 1, cy + 1,
                               x + 1, cy - 1,
                               x - 1, cy - 1, fill="green", width=5)

    return point


def destroy_a_b(canvas, line1, line2):
    canvas.delete(line1)
    canvas.delete(line2)
