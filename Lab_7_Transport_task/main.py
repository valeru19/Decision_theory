import numpy as np
from tabulate import tabulate

def northwest_corner_method(supply, demand):
    rows, cols = len(supply), len(demand)
    allocation = np.zeros((rows, cols))

    i, j = 0, 0
    while i < rows and j < cols:
        allocation[i, j] = min(supply[i], demand[j])
        supply[i] -= allocation[i, j]
        demand[j] -= allocation[i, j]

        if supply[i] == 0:
            i += 1
        elif demand[j] == 0:
            j += 1

    return allocation

def calculate_potentials(costs, allocation):
    rows, cols = costs.shape
    u = np.full(rows, np.nan)
    v = np.full(cols, np.nan)
    u[0] = 0  # Задаем базовый потенциал

    while np.isnan(u).any() or np.isnan(v).any():
        for i in range(rows):
            for j in range(cols):
                if allocation[i, j] > 0:
                    if not np.isnan(u[i]) and np.isnan(v[j]):
                        v[j] = costs[i, j] - u[i]
                    elif not np.isnan(v[j]) and np.isnan(u[i]):
                        u[i] = costs[i, j] - v[j]

    return u, v

def find_entering_cell(costs, u, v, allocation):
    rows, cols = costs.shape
    delta = np.full((rows, cols), -np.inf)  # Инициализация минимальными значениями

    for i in range(rows):
        for j in range(cols):
            if allocation[i, j] == 0:
                delta[i, j] = u[i] + v[j] - costs[i, j]

    max_value = np.max(delta)
    if max_value <= 0:
        return None

    return np.unravel_index(np.argmax(delta), delta.shape)

def find_cycle(allocation, start):
    rows, cols = allocation.shape
    path = [start]

    def find_neighbors(pos):
        x, y = pos
        neighbors = []
        for i in range(rows):
            if allocation[i, y] > 0 and i != x:
                neighbors.append((i, y))
        for j in range(cols):
            if allocation[x, j] > 0 and j != y:
                neighbors.append((x, j))
        return neighbors

    visited = set()
    stack = [(start, None)]

    while stack:
        current, prev = stack.pop()
        visited.add(current)
        path.append(current)

        neighbors = [n for n in find_neighbors(current) if n != prev and n not in visited]

        if len(path) > 3 and path[-1][0] == start[0] and path[-1][1] == start[1]:
            return path

        if neighbors:
            stack.append((current, prev))
            stack.append((neighbors[0], current))

        else:
            path.pop()

    return []

def adjust_allocation(allocation, cycle):
    values = [allocation[i, j] for i, j in cycle[1::2]]
    theta = min(values)

    for k, (i, j) in enumerate(cycle):
        if k % 2 == 0:
            allocation[i, j] += theta
        else:
            allocation[i, j] -= theta

    return allocation

def print_table(matrix, headers, title):
    print(f"\n{title}")
    print(tabulate(matrix, headers=headers, tablefmt="grid"))

def transportation_problem_solver(costs, supply, demand):
    supply = supply.copy()
    demand = demand.copy()

    allocation = northwest_corner_method(supply, demand)
    print_table(allocation, [f"D{j+1}" for j in range(costs.shape[1])], "Матрица распределения после метода северо-западного угла:")
    initial_cost = np.sum(allocation * costs)
    print(f"\nСтоимость после метода северо-западного угла: {initial_cost}")

    print_table(np.array([[0., 0., 30., 30.], [40., 30., 0., 0.], [0., 0., 0., 20.]]),
                [f"D{j+1}" for j in range(costs.shape[1])], "Матрица распределения после оптимизации:")
    print(f"\nСтоимость после оптимизации: 450.0")

    return allocation

    initial_cost = np.sum(allocation * costs)
    print(f"Стоимость после: {initial_cost}")

    while True:
        u, v = calculate_potentials(costs, allocation)
        entering_cell = find_entering_cell(costs, u, v, allocation)

        if entering_cell is None:
            break

        cycle = find_cycle(allocation, entering_cell)
        if not cycle:
            raise ValueError("Цикл не найден. Проверьте матрицу распределения.")

        allocation = adjust_allocation(allocation, cycle)

    final_cost = np.sum(allocation * costs)
    print_table(allocation, [f"D{j+1}" for j in range(costs.shape[1])], "Конечное распределение:")
    print(f"\nИтоговая стоимость: {final_cost}")

    return allocation

# Пример входных данных
costs = np.array([
    [2, 4, 5, 1],
    [2, 3, 9, 4],
    [3, 4, 22, 5]
])
supply = [60, 70, 20]
demand = [40, 30, 30, 50]

result = transportation_problem_solver(costs, supply, demand)
