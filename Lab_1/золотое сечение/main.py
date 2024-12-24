import numpy as np
import matplotlib.pyplot as plt


# Определяем целевую функцию F(x)
def F(x):
    return np.exp(x) + 1 / x


# Первая производная функции F'(x)
def F_derivative(x):
    return np.exp(x) - 1 / (x ** 2)


# Вторая производная функции F''(x)
def F_2derivative(x):
    return np.exp(x) + 2 / (x ** 3)


# Метод золотого сечения
def golden_section_search(a, b, eps=1e-6):
    phi = 1.618
    iter_count = 0
    x_values = []

    x1 = b - (b - a) / phi
    x2 = a + (b - a) / phi

    while abs(b - a) > eps:
        if F(x1) < F(x2):
            b = x2
            x2 = x1
            x1 = b - (b - a) / phi
        else:
            a = x1
            x1 = x2
            x2 = a + (b - a) / phi

        x_values.append((a + b) / 2)
        iter_count += 1

    x_min = (a + b) / 2
    return x_min, F(x_min), iter_count, x_values


# Метод касательных
def tangent_method(a, b, eps=1e-6):
    i = 0
    xm = 0
    x_values = []

    while abs(b - a) > eps:
        xm = (a * F_derivative(a) - b * F_derivative(b) - F(a) + F(b)) / (F_derivative(a) - F_derivative(b))
        x_values.append(xm)

        if F_derivative(xm) > 0:
            b = xm
        else:
            a = xm
        i += 1

    return xm, F(xm), i, x_values


# Метод Ньютона
def newton(x0, eps=1e-6):
    xk = x0
    iter = 0
    x_values = [xk]

    while True:
        iter += 1
        df1 = F_derivative(xk)
        d2f1 = F_2derivative(xk)

        if d2f1 == 0:
            print("Вторая производная равна нулю, метод Ньютона не может быть применен.")
            return None, None, iter, x_values

        xk_1 = xk - (df1 / d2f1)
        x_values.append(xk_1)

        if abs(xk_1 - xk) < eps:
            break

        xk = xk_1

    return xk_1, F(xk_1), iter, x_values


# Функция для построения графиков
def plot_results(a, b, golden_result, tangent_result, newton_result):
    x = np.linspace(0.1, 1.5, 500)
    y = F(x)

    plt.figure(figsize=(12, 8))

    # График функции F(x)
    plt.plot(x, y, label="F(x) = exp(x) + 1 / x", color='blue')

    # Точки минимума для каждого метода
    plt.plot(golden_result[0], golden_result[1], 'ro', label="Минимум (метод золотого сечения)")
    plt.plot(tangent_result[0], tangent_result[1], 'go', label="Минимум (метод касательных)")
    plt.plot(newton_result[0], newton_result[1], 'bo', label="Минимум (метод Ньютона)")

    # Итерации
    plt.plot(golden_result[3], [F(x) for x in golden_result[3]], 'r--', label="Итерации (метод золотого сечения)")
    plt.plot(tangent_result[3], [F(x) for x in tangent_result[3]], 'g--', label="Итерации (метод касательных)")
    plt.plot(newton_result[3], [F(x) for x in newton_result[3]], 'b--', label="Итерации (метод Ньютона)")

    plt.xlabel("x")
    plt.ylabel("F(x)")
    plt.title("Поиск минимума функции F(x) различными методами")
    plt.legend()
    plt.grid()
    plt.show()


# Основная часть программы
if __name__ == "__main__":
    a = 0.1
    b = 1
    initial_x = 0.5

    print("Метод золотого сечения:")
    x_min_gs, y_min_gs, iter_gs, x_vals_gs = golden_section_search(a, b)
    print('X min (golden section): ', x_min_gs)
    print('Y min (golden section): ', y_min_gs)
    print('Количество итераций (golden section): ', iter_gs)

    print("\nМетод касательных:")
    x_min_sec, y_min_sec, iter_sec, x_vals_sec = tangent_method(a, b)
    print('X min (tangent method): ', x_min_sec)
    print('Y min (tangent method): ', y_min_sec)
    print('Количество итераций (tangent method): ', iter_sec)

    print("\nМетод Ньютона:")
    x_min_newton, y_min_newton, iter_newton, x_vals_newton = newton(initial_x)
    print('X min (Newton method): ', x_min_newton)
    print('Y min (Newton method): ', y_min_newton)
    print('Количество итераций (Newton method): ', iter_newton)

    # Построение графиков
    plot_results(a, b, (x_min_gs, y_min_gs, iter_gs, x_vals_gs),
                 (x_min_sec, y_min_sec, iter_sec, x_vals_sec),
                 (x_min_newton, y_min_newton, iter_newton, x_vals_newton))
