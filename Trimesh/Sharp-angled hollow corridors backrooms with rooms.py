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

    return cube

# Функция для создания комнаты
def create_room():
    room_size = 5
    room = trimesh.creation.box(extents=(room_size, room_size, room_size))
    return room

# Функция для объединения коридоров и комнат в лабиринт
def create_labyrinth(num_corridors, num_rooms):
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

    for _ in range(num_rooms):
        room = create_room()
        room.apply_translation([random.uniform(-10, 10), random.uniform(-10, 10), 0])
        labyrinth = labyrinth.union(room)

    return labyrinth

# Создание лабиринта коридоров и комнат
num_corridors = 10
num_rooms = 5
labyrinth = create_labyrinth(num_corridors, num_rooms)

# Сохранение лабиринта в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Сохранение лабиринта в OBJ файл
filename = os.path.join(desktop_path, "labyrinth.obj")
labyrinth.export(filename)
print(f"Model saved as {filename}")

# Визуализация лабиринта
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(labyrinth.vertices[:, 0], labyrinth.vertices[:, 1], labyrinth.vertices[:, 2], color='r', alpha=0.5)
plt.show()
