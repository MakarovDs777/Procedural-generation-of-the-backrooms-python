import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os
import random

# Функция для создания случайного коридора
def create_corridor(position):
    # Создание основного куба с размерами коридора
    corridor_length = 10
    corridor_width = 6
    corridor_height = 1 # высота коридора (3 этажа по 2)

    cube = trimesh.creation.box(extents=(corridor_length, corridor_width, corridor_height))

    # Размеры отверстий
    hole_size_x = [-1.0, 1.0, 1.0]  # Отверстия по оси X

    # Определяем позиции для столбов по оси X (по одному слева и справа)
    hole_positions_x = [
        [corridor_length / 2 - hole_size_x[0] / 2, 0, 0],  # столб слева
        [-corridor_length / 2 + hole_size_x[0] / 2, 0, 0],   # столб справа
    ]

    # Создание и вычитание столбов по оси X
    for pos in hole_positions_x:
        hole = trimesh.creation.box(extents=(1.0, 1.0, 1.0))
        hole.apply_translation(pos)
        cube = cube.difference(hole)

    cube.apply_translation(position)  # Перемещаем коридор в заданную позицию
    return cube

# Функция для создания вертикального коридора
def create_vertical_corridor(position):
    vertical_corridor = trimesh.creation.box(extents=(1.0, 1.0, 9.0))
    vertical_corridor.apply_translation(position)
    return vertical_corridor

# Функция для объединения коридоров в лабиринт
def create_labyrinth(num_corridors):
    labyrinth = None
    for i in range(num_corridors):
        height_offset = random.randint(0, 2)*2 # Смещение по высоте (0, 2 или 4)
        corridor = create_corridor([random.uniform(-5, 5), random.uniform(-5, 5), height_offset])
        if labyrinth is None:
            labyrinth = corridor
        else:
            labyrinth = labyrinth.union(corridor)

    # Создание вертикального коридора в центре
    vertical_corridor = create_vertical_corridor([0, 0, 0])  # Позиция (0, 0) и высота от 0 до 3
    labyrinth = labyrinth.union(vertical_corridor)

    return labyrinth

# Создание лабиринта коридоров
num_corridors = 5
labyrinth = create_labyrinth(num_corridors)

# Сохранение лабиринта в OBJ файл
desktop_path = os.path.expanduser("~")
filename = os.path.join(desktop_path, "Desktop", "labyrinth.obj")
labyrinth.export(filename)
print(f"Model saved as {filename}")

# Визуализация лабиринта
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(labyrinth.vertices[:, 0], labyrinth.vertices[:, 1], labyrinth.vertices[:, 2], color='r', alpha=0.5)
plt.show()
