import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
import os

# Функция для генерации 3D-поля с коридорами
def generate_field(shape):
    array = np.zeros(shape, dtype=float)

    # Генерация точек для коридоров
    points = []
    for _ in range(100):
        x = np.random.randint(10, shape[0] - 10)
        y = np.random.randint(10, shape[1] - 10)
        z = np.random.randint(10, shape[2] - 10)
        points.append([x, y, z])  # Генерируем точки

    # Генерация коридоров между точками
    for i in range(len(points) - 1):
        start_point = points[i]
        end_point = points[i + 1]

        # Горизонтальный или вертикальный коридор
        if abs(start_point[0] - end_point[0]) > abs(start_point[1] - end_point[1]) and abs(start_point[0] - end_point[0]) > abs(start_point[2] - end_point[2]):
            for new_x in range(min(start_point[0], end_point[0]), max(start_point[0], end_point[0]) + 1):
                new_y = start_point[1]
                new_z = start_point[2]
                array[new_x, new_y, new_z] = 1.0
                # Делаем коридоры более жирными
                for k in range(-2, 3):
                    for l in range(-2, 3):
                        for m in range(-2, 3):
                            x1, y1, z1 = new_x + k, new_y + l, new_z + m
                            if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                array[x1, y1, z1] = 1.0
        elif abs(start_point[1] - end_point[1]) > abs(start_point[0] - end_point[0]) and abs(start_point[1] - end_point[1]) > abs(start_point[2] - end_point[2]):
            for new_y in range(min(start_point[1], end_point[1]), max(start_point[1], end_point[1]) + 1):
                new_x = start_point[0]
                new_z = start_point[2]
                array[new_x, new_y, new_z] = 1.0
                # Делаем коридоры более жирными
                for k in range(-2, 3):
                    for l in range(-2, 3):
                        for m in range(-2, 3):
                            x1, y1, z1 = new_x + k, new_y + l, new_z + m
                            if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                array[x1, y1, z1] = 1.0
        else:
            for new_z in range(min(start_point[2], end_point[2]), max(start_point[2], end_point[2]) + 1):
                new_x = start_point[0]
                new_y = start_point[1]
                array[new_x, new_y, new_z] = 1.0
                # Делаем коридоры более жирными
                for k in range(-2, 3):
                    for l in range(-2, 3):
                        for m in range(-2, 3):
                            x1, y1, z1 = new_x + k, new_y + l, new_z + m
                            if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                array[x1, y1, z1] = 1.0

    return array

# Параметры
shape = (128, 128, 128)  # Размеры 3D массива

# Генерация 3D-поля с коридорами
field = generate_field(shape=(128, 128, 128))

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(field, level=0.5)

# Создание mesh с острыми углами
mesh = trimesh.Trimesh(vertices=verts, faces=faces)

# Сохранение mesh на рабочий стол
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "mesh.stl")
mesh.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], color='r', alpha=0.5)
plt.show()
