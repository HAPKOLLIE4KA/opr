import math


def func1(x):
    return (x + 2) ** 2 - 3


def func2(x):
    return -x ** 2 + 5


def func3(x):
    return (x-4)**3 + 3


def enumeration_method(func, a, b, eps):
    h = 50
    root1, root2 = float("inf"), float("inf")
    a, b, root2, count = counting_mechanics(func, a, h, a, b)

    while abs(root1 - root2) > eps:
        h *= 2
        root1 = root2
        a, b, root2, count = counting_mechanics(func, a, h, a, b)
        if root2 == float("inf"):
            return None

    return root2, count


def counting_mechanics(func, x, h, a, b):
    length_h = (b - a) / h
    count = 0
    while x < b:
        count += 1
        try:
            if func(x) * func(x + length_h) <= 0:
                return x - length_h, x + length_h, x, count
        except Exception:
            pass
        x += length_h

    return None, None, float("inf"), count
