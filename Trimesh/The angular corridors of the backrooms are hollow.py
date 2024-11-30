import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os
import random

# Функция для создания случайного коридора
def create_corridor():
    # Создание основного куба с размерами коридора
    corridor_length = 10
    corridor_width = 2
    corridor_height = 2
    cube = trimesh.creation.box(extents=(corridor_length, corridor_width, corridor_height))

    # Размеры отверстий
    hole_size_x = [1.0, 1.0, 1.0]  # Отверстия по оси X

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

    return cube

# Функция для объединения коридоров в лабиринт
def create_labyrinth(num_corridors):
    labyrinth = None
    for _ in range(num_corridors):
        corridor = create_corridor()
        if labyrinth is None:
            labyrinth = corridor
        else:
            corridor.apply_translation([random.uniform(-5, 5), random.uniform(-5, 5), 0])
            rotation_matrix = trimesh.transformations.rotation_matrix(np.pi/2, [0, 0, 1])
            if random.random() < 0.5:
                corridor.apply_transform(rotation_matrix)
            labyrinth = labyrinth.union(corridor)
    return labyrinth

# Создание лабиринта коридоров
num_corridors = 10
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
