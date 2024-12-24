import math as m
import matplotlib.pyplot as plt
import numpy as np
# Целевая функция
def f(x):
    try:
        exp_part = m.exp(x[0] ** 2 + x[1] ** 2)
    except OverflowError:
        exp_part = float('inf')  # Обработка переполнения
    exp_part = min(exp_part, 1e100)  # Ограничение значения экспоненты
    return exp_part + m.log(4 + x[1] ** 2)
# Градиент целевой функции
def grad_f(x):
    try:
        exp_part = m.exp(x[0] ** 2 + x[1] ** 2)
    except OverflowError:
        exp_part = float('inf')  # Обработка переполнения
    exp_part = min(exp_part, 1e100)  # Ограничение значения экспоненты
    x1 = 2 * x[0] * exp_part
    x2 = 2 * x[1] * exp_part + (2 * x[1]) / (4 + x[1] ** 2)
    # Нормализация градиента
    norm = m.sqrt(x1 ** 2 + x2 ** 2)
    if norm > 1e-10:  # Предотвращение деления на ноль
        x1 /= norm
        x2 /= norm
    return [x1, x2]
# Метод Хука-Дживса
def hook_jiws(x0, lamb, epsilon, alpha=1):
    xk = x0.copy()
    lamb0 = lamb
    iterations = 0
    traj = [xk.copy()]  # Траектория точек
    while lamb >= epsilon:
        iterations += 1
        p = 0
        elems = [xk]
        for i in range(len(xk)):
            temp_elems = []
            for elem in elems:
                x1 = elem.copy()
                x1[i] -= lamb
                x2 = elem.copy()
                x3 = elem.copy()
                x3[i] += lamb
                temp_elems.append(x1)
                temp_elems.append(x2)
                temp_elems.append(x3)
            elems = elems + temp_elems
            temp_elems.clear()
        elems = [list(t) for t in set(tuple(e) for e in elems)]
        elems.remove(xk)
        func_values = [f(elem) for elem in elems]
        min_f = min(func_values)
        min_x = elems[func_values.index(min_f)]
        f_x = f(xk)
        if round(min_f, 6) >= round(f_x, 6):
            p += 1
            lamb = lamb - (lamb0 / m.exp(p))
        else:
            xk = xk
            for i in range(len(min_x)):
                min_x[i] -= xk[i]
                min_x[i] *= alpha
                xk[i] += min_x[i]
            traj.append(xk.copy())
            p = 0
    return xk, f(xk), iterations, traj
# Градиентный спуск
def gradient_const(x0, lamb, epsilon):
    xk = x0.copy()
    xk_1 = xk.copy()
    iterations = 1
    traj = [xk.copy()]  # Траектория точек
    g = grad_f(xk)
    for i in range(len(xk)):
        xk_1[i] = xk[i] - g[i] * lamb
    while abs(f(xk_1) - f(xk)) >= epsilon:
        iterations += 1
        xk = xk_1.copy()
        g = grad_f(xk)
        for i in range(len(xk)):
            xk_1[i] = xk[i] - g[i] * lamb
        if f(xk_1) >= f(xk):
            lamb /= 2
        traj.append(xk.copy())
    return xk_1, f(xk_1), iterations, traj
# Построение графиков
def plot_trajectories(hook_traj, grad_traj, func_range=10):
    x = np.linspace(-func_range, func_range, 400)
    y = np.linspace(-func_range, func_range, 400)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[f([i, j]) for i, j in zip(x_row, y_row)] for x_row, y_row in zip(X, Y)])
    plt.contourf(X, Y, Z, levels=50, cmap='viridis')
    plt.colorbar(label="Уровень функции f(x)")
    hook_traj = np.array(hook_traj)
    grad_traj = np.array(grad_traj)
    plt.plot(hook_traj[:, 0], hook_traj[:, 1], 'ro-', label="Хук-Дживс")
    plt.plot(grad_traj[:, 0], grad_traj[:, 1], 'bo-', label="Градиентный спуск")
    plt.scatter(hook_traj[0, 0], hook_traj[0, 1], color='k', label="Начальная точка")
    plt.xlabel("x₁")
    plt.ylabel("x₂")
    plt.title("Траектории методов оптимизации")
    plt.legend()
    plt.grid()
    plt.show()
# Основной код
if __name__ == "__main__":
    x0 = [1, 2]  # Начальная точка
    lamb0 = 0.5  # Начальный шаг
    epsilon = 1e-6  # Точность
    print(f"Начальная точка: {x0}")
    print(f"Начальное значение функции: {f(x0)}")
    hook_res = hook_jiws(x0, lamb0, epsilon)
    grad_res = gradient_const(x0, lamb0, epsilon)
    print(
        f"Метод Хука-Дживса: точка минимума = {hook_res[0]}, значение функции = {hook_res[1]}, итерации = {hook_res[2]}")
    print(
        f"Градиентный спуск: точка минимума = {grad_res[0]}, значение функции = {grad_res[1]}, итерации = {grad_res[2]}")
    plot_trajectories(hook_res[3], grad_res[3], func_range=2)


