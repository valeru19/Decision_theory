import numpy as np
import matplotlib.pyplot as plt

# Определяем функцию, её первую и вторую производные
def f(x):
    return np.exp(x) + 1 / x

def f_prime(x):
    return np.exp(x) - 1 / (x**2)

def f_double_prime(x):
    return np.exp(x) + 2 / (x**3)

# Основная функция поиска экстремума методом касательных
def tangent_method(x0, epsilon=1e-6):
    iter_count = 0
    x_values = [x0]

    x_prev = x0

    while True:
        f_prime_x = f_prime(x_prev)
        f_double_prime_x = f_double_prime(x_prev)

        # Проверяем, что вторая производная положительна
        if f_double_prime_x <= 0:
            raise ValueError("Вторая производная должна быть положительной для выпуклой функции!")

        # Обновляем значение x по методу Ньютона (касательных)
        x_next = x_prev - f_prime_x / f_double_prime_x

        # Линейная аппроксимация p_{k-1}(x)
        p_current = f(x_prev) + f_prime_x * (x_next - x_prev)

        # Условие остановки
        if abs(f(x_next) - p_current) < epsilon:
            break

        # Обновляем значения для следующей итерации
        x_values.append(x_next)
        x_prev = x_next
        iter_count += 1

    return x_next, f(x_next), iter_count, x_values

# Пример использования метода
x0 = 0.5  # Начальная точка
extremum_x, extremum_f, iter_count, x_values = tangent_method(x0)

print(f"Экстремум находится в точке x = {extremum_x}")
print(f"Значение функции в экстремуме: f(x) = {extremum_f}")
print(f"Количество итераций: {iter_count}")

# Построим график функции и покажем точки итераций
x_vals = np.linspace(0.1, 2, 400)
f_vals = f(x_vals)

plt.plot(x_vals, f_vals, label='f(x) = e^x + 1/x', color='blue')

# Отметим точки, полученные на итерациях
for i, x_val in enumerate(x_values):
    plt.scatter(x_val, f(x_val), color='red', zorder=5)
    plt.text(x_val, f(x_val), f'x_{i}', fontsize=12)

plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.title('График функции и точки итераций метода касательных')
plt.grid(True)
plt.show()
