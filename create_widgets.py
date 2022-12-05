import tkinter as tk
from my_constants import *
from graph import *
from method import *
import threading
import time


def update():
    win.update()


def create_check_button():
    int_var = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
    x = 30
    y = 60
    y_factor = 25
    tk.Label(win, text="Выберите функцию:").place(x=x, y=40)
    wfunc1 = tk.Checkbutton(win, text="(x + 2)^2 - 3 ", command=check, variable=int_var[0])
    wfunc2 = tk.Checkbutton(win, text="-x^2 + 5", command=check, variable=int_var[1])
    wfunc3 = tk.Checkbutton(win, text="(x-4)^3 + 3", command=check, variable=int_var[2])

    widgets_array = [wfunc1, wfunc2, wfunc3]

    for i in range(len(widgets_array)):
        widgets_array[i].place(x=x, y=y + y_factor * i)

    return widgets_array, int_var


def create_entry():
    x = 30
    y = 160
    y_factor = 25
    x_factor = 4
    l1 = tk.Label(win, text="Левая граница")
    left_border_entry = tk.Entry(win)
    l2 = tk.Label(win, text="Правая граница")
    right_border_entry = tk.Entry(win)
    l3 = tk.Label(win, text="Точность")
    eps_entry = tk.Entry(win)
    eps_entry.insert(0, "0.001")
    array = [[l1, left_border_entry], [l2, right_border_entry], [l3, eps_entry]]

    for i in range(len(array)):
        for j in range(2):
            array[i][j].place(x=x + x * x_factor * j, y=y + y_factor * i)

    return {
        "left": left_border_entry,
        "right": right_border_entry,
        "eps": eps_entry
    }


def create_result_text():
    x = 30
    y = 280
    result = tk.Label(win, text="Результат: ")
    result.place(x=x, y=y)

    text_result = tk.Label(win,
                           width=20,
                           borderwidth=1,
                           relief="solid",
                           text=" ",
                           anchor="w"
                           )
    text_result.place(x=x + 2, y=y + 20)

    return text_result


def create_calc_button():
    x = 120
    y = 240

    btn = tk.Button(win, text="Рассчитать", command=calculate_root_start)
    btn.place(x=x, y=y)
    return btn


def create_iteration_text():
    x = 30
    y = 220
    tk.Label(win, height=15, text="Количество обращений к функции:").place(x=x, y=y)
    text_iteration = tk.Label(win,
                              width=20,
                              borderwidth=1,
                              relief="solid",
                              text=" ",
                              anchor="w"
                              )
    text_iteration.place(x=32, y=345)
    return text_iteration


def create_result_func_in_root():
    x = 30
    y = 370
    tk.Label(win, text="Результат функции в корне:").place(x=x, y=y)
    text_result_func_in_root = tk.Label(win,
                                        width=20,
                                        borderwidth=1,
                                        relief="solid",
                                        text=" ",
                                        anchor="w"
                                        )
    text_result_func_in_root.place(x=32, y=390)
    return text_result_func_in_root


def create_header_text():
    text_header = tk.Label(win, width=100, height=15, text="Решение уравнений. Метод перебора", font=("", 13))
    text_header.place(x=10, y=-130)


def create_error_text():
    x = 30
    y = 450

    text_error = tk.Label(win,
                          width=30,
                          height=15,
                          text=" ",
                          anchor="n",
                          fg="red",
                          )
    text_error.place(x=x + 2, y=y + 20)

    return text_error


def create_canvas_frame():
    canvas_frame = tk.Frame(win,
                            borderwidth=1,
                            relief="solid",
                            height=CANVAS_H,
                            width=CANVAS_W
                            )

    canvas_frame.place(x=CANVASx0, y=CANVASy0)

    return canvas_frame


def create_canvas(canvas_frame):
    canvas_graph = tk.Canvas(canvas_frame,
                             width=CANVAS_W,
                             height=CANVAS_H,
                             )
    canvas_graph.pack()
    return canvas_graph


def create_win():
    win = tk.Tk()
    win.title("Метод перебора")
    win.geometry(f"{WIDTH}x{HIGHT}+200+30")
    win.resizable(False, False)
    return win


def copy_int_var():
    return [x.get() for x in int_var]


def switch_func():
    if int_var[0].get() == 1:
        return func1
    elif int_var[1].get() == 1:
        return func2
    elif int_var[2].get() == 1:
        return func3
    else:
        return None


def check():
    global prev_var, global_func, global_lines_func, global_root_line
    if global_root_line is not None: canvas.delete(global_root_line)
    for i in range(len(int_var)):  # контроль выбора только одного чекбаттона
        if int_var[i].get() == prev_var[i] == 1:
            check_button_widgets[i].deselect()
            break
    prev_var = copy_int_var()

    global_func = switch_func()  # выбор функции

    if global_lines_func is not None:  # удаление старой функции из графика
        delete_graph(canvas, global_lines_func)
        global_lines_func = None

    if global_func is not None:  # отрисовка функции, если она выбрана
        global_lines_func = func_block(canvas, global_func)

    clear_result_iter()


def validation_widgets():
    flag = 1
    text = ''
    if global_func is None:
        text += "Не выбрана функция\n"
        flag = 0
    if entry_widgets['eps'].get() == '':
        text += "Не введена точность\n"
        flag = 0
    elif entry_widgets['eps'].get() != '':
        try:
            if float(entry_widgets['eps'].get()) < 0.0000000001:
                text += "Слишком низкая точноть\n"
                flag = 0
        except Exception:
            text += "Неверно введена точность\n"
            flag = 0

    if entry_widgets['left'].get() == '' or entry_widgets['right'].get() == '':
        text += "Не введены границы\n"
        flag = 0
    else:
        try:
            if float(entry_widgets['left'].get()) >= float(entry_widgets['right'].get()):
                text += "Неверно введены границы\n"
                flag = 0
        except:
            text += "В границах введите числа\n"
            flag = 0

    error_text.config(text=text)
    return flag


iter = 0


def enumeration_method(func, a, b, eps):
    if func(a) == 0:
        return a, 1
    elif func(b) == 0:
        return b, 1

    global iter
    iter = 0
    line1, line2 = draw_a_b(canvas, a, b, None, None)
    h = 5
    root1, root2 = float("inf"), float("inf")
    a, b, root2, count = counting_mechanics(func, a, h, a, b)

    while abs(root1 - root2) > eps:
        line1, line2 = draw_a_b(canvas, a, b, line1, line2)
        h *= 2
        root1 = root2
        a, b, root2, iter_func = counting_mechanics(func, a, h, a, b)
        count += iter_func
        if root2 == float("inf"):
            return None

    destroy_a_b(canvas, line1, line2)
    return root2, count


def counting_mechanics(func, x, h, a, b):
    global iter
    timer = 0.1 if abs(b - a) > 0.1 else 0
    length_h = (b - a) / h
    count = 0
    point = None
    while x < b:
        time.sleep(timer)
        count += 1
        iter += 1
        text_iteration.config(text=f"{iter}")
        point = draw_point(canvas, x, point)
        try:
            if func(x) * func(x + length_h) <= 0:
                canvas.delete(point)
                return x - length_h, x + length_h, x, count
        except Exception:
            pass
        x += length_h
    canvas.delete(point)
    return None, None, float("inf"), count


def clear_result_iter():
    text_result.config(text="")
    text_iteration.config(text="")
    text_result_func_in_root.config(text=f"")


def calculate_root_start():
    threading.Thread(target=calculate_root).start()


def calculate_root():
    global global_root_line, a, b
    clear_result_iter()
    if global_root_line is not None: canvas.delete(global_root_line)
    if not validation_widgets():
        return
    a, b, eps = float(entry_widgets["left"].get()), float(entry_widgets["right"].get()), float(
        entry_widgets["eps"].get())
    root, count = enumeration_method(global_func, a, b, eps)
    text_iteration.config(text=f"{count}")
    if root == float("inf"): text_result.config(text="Корня на отрезке нет"); return
    text_result.config(text=f"{root}")
    text_result_func_in_root.config(text=f"{global_func(root)}")
    global_root_line = draw_root(canvas, root, global_func)


win = create_win()
create_header_text()
text_iteration = create_iteration_text()
text_result_func_in_root = create_result_func_in_root()
check_button_widgets, int_var = create_check_button()
prev_var = copy_int_var()
entry_widgets = create_entry()
btn_calc = create_calc_button()
text_result = create_result_text()
canvas_frame = create_canvas_frame()
canvas = create_canvas(canvas_frame)
thread = None
error_text = create_error_text()
global_func = None
global_lines_func = None
global_root_line = None
