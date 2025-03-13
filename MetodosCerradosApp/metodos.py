import math

def bisection(f, a, b, tol, max_iter=1000):
    if f(a) * f(b) >= 0:
        raise ValueError("No hay cambio de signo en el intervalo.")
    iterations = []
    for _ in range(max_iter):
        c = (a + b) / 2
        error = (b - a) / 2
        fc = f(c)
        iterations.append((a, b, c, fc))
        if fc == 0 or error < tol:
            return c, iterations
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    return c, iterations

def false_position(f, a, b, tol, max_iter=1000):
    if f(a) * f(b) >= 0:
        raise ValueError("No hay cambio de signo en el intervalo.")
    iterations = []
    for _ in range(max_iter):
        fa = f(a)
        fb = f(b)
        c = a - (fa * (b - a)) / (fb - fa)
        fc = f(c)
        iterations.append((a, b, c, fc))
        if abs(fc) < tol:
            return c, iterations
        if fa * fc < 0:
            b = c
        else:
            a = c
    return c, iterations

def velocity_function(m):
    g = 9.8
    c = 15
    t = 9
    try:
        term = 1 - math.exp(-(c/m) * t)
        return (g * m / c) * term - 35
    except ZeroDivisionError:
        return float('inf')