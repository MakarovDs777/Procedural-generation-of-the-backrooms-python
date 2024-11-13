import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
import os

# Функция для генерации 3D-поля с коридорами
def generate_delaunay_field(shape):
    array = np.zeros(shape, dtype=float)

    # Генерация точек для коридоров
    points = []
    for _ in range(50):  # 50 коридоров
        x = np.random.randint(10, shape[0] - 10)
        y = np.random.randint(10, shape[1] - 10)
        z = shape[2] // 3  # Генерируем точки на фиксированной высоте
        points.append([x, y, z])

    points2 = []
    for _ in range(50):  # 50 коридоров
        x = np.random.randint(10, shape[0] - 10)
        y = np.random.randint(10, shape[1] - 10)
        z = 2 * shape[2] // 3  # Генерируем точки на фиксированной высоте
        points2.append([x, y, z])

    points3 = []
    for _ in range(50):  # 50 коридоров
        x = np.random.randint(10, shape[0] - 10)
        y = np.random.randint(10, shape[1] - 10)
        z = shape[2] // 6  # Генерируем точки на фиксированной высоте
        points3.append([x, y, z])

    # Генерация коридоров между точками
    for i in range(len(points) - 1):
        start_point = points[i]
        end_point = points[i + 1]

        # Горизонтальный коридор
        for new_x in range(min(start_point[0], end_point[0]), max(start_point[0], end_point[0]) + 1):
            new_y = start_point[1]
            new_z = start_point[2]

            # Делаем коридоры высокими и широкими
            for height_offset in range(-1, 5):  # Высота коридоров
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1]:
                    array[new_x, new_y, new_z + height_offset] = 1.0
                    for k in range(-2, 3):  # Ширина по x и y
                        for l in range(-2, 3):
                            if 0 <= new_x + k < shape[0] and 0 <= new_y + l < shape[1]:
                                array[new_x + k, new_y + l, new_z + height_offset] = 1.0

        # Вертикальный коридор
        for new_y in range(min(start_point[1], end_point[1]), max(start_point[1], end_point[1]) + 1):
            new_x = end_point[0]
            new_z = end_point[2]

            # Делаем коридоры высокими и широкими
            for height_offset in range(-1, 5):  # Высота коридоров
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1]:
                    array[new_x, new_y, new_z + height_offset] = 1.0
                    for k in range(-2, 3):  # Ширина по x и y
                        for l in range(-2, 3):
                            if 0 <= new_x + k < shape[0]:
                                array[new_x + k, new_y + l, new_z + height_offset] = 1.0

    for i in range(len(points2) - 1):
        start_point = points2[i]
        end_point = points2[i + 1]

        # Горизонтальный коридор
        for new_x in range(min(start_point[0], end_point[0]), max(start_point[0], end_point[0]) + 1):
            new_y = start_point[1]
            new_z = start_point[2]

            # Делаем коридоры высокими и широкими
            for height_offset in range(-1, 5):  # Высота коридоров
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1]:
                    array[new_x, new_y, new_z + height_offset] = 1.0
                    for k in range(-2, 3):  # Ширина по x и y
                        for l in range(-2, 3):
                            if 0 <= new_x + k < shape[0] and 0 <= new_y + l < shape[1]:
                                array[new_x + k, new_y + l, new_z + height_offset] = 1.0

        # Вертикальный коридор
        for new_y in range(min(start_point[1], end_point[1]), max(start_point[1], end_point[1]) + 1):
            new_x = end_point[0]
            new_z = end_point[2]

            # Делаем коридоры высокими и широкими
            for height_offset in range(-1, 5):  # Высота коридоров
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1]:
                    array[new_x, new_y, new_z + height_offset] = 1.0
                    for k in range(-2, 3):  # Ширина по x и y
                        for l in range(-2, 3):
                            if 0 <= new_x + k < shape[0] and 0 <= new_y + l < shape[1]:
                                array[new_x + k, new_y + l, new_z + height_offset] = 1.0

    for i in range(len(points3) - 1):
        start_point = points3[i]
        end_point = points3[i + 1]

        # Горизонтальный коридор
        for new_x in range(min(start_point[0], end_point[0]), max(start_point[0], end_point[0]) + 1):
            new_y = start_point[1]
            new_z = start_point[2]

            # Делаем коридоры высокими и широкими
            for height_offset in range(-1, 5):  # Высота коридоров
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1]:
                    array[new_x, new_y, new_z + height_offset] = 1.0
                    for k in range(-2, 3):  # Ширина по x и y
                        for l in range(-2, 3):
                            if 0 <= new_x + k < shape[0] and 0 <= new_y + l < shape[1]:
                                array[new_x + k, new_y + l, new_z + height_offset] = 1.0

        # Вертикальный коридор
        for new_y in range(min(start_point[1], end_point[1]), max(start_point[1], end_point[1]) + 1):
            new_x = end_point[0]
            new_z = end_point[2]

            # Делаем коридоры высокими и широкими
            for height_offset in range(-1, 5):  # Высота коридоров
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1]:
                    array[new_x, new_y, new_z + height_offset] = 1.0
                    for k in range(-2, 3):  # Ширина по x и y
                        for l in range(-2, 3):
                            if 0 <= new_x + k < shape[0] and 0 <= new_y + l < shape[1]:
                                array[new_x + k, new_y + l, new_z + height_offset] = 1.0

    # Добавление соединений между уровнями
    for i in range(len(points)):
        start_point = points[i]
        end_point = points2[i]
        for new_z in range(min(start_point[2], end_point[2]), max(start_point[2], end_point[2]) + 1):
            if 0 <= start_point[0] < shape[0] and 0 <= start_point[1] < shape[1]:
                for height_offset in range(-1, 5):  # Высота коридоров
                    array[start_point[0], start_point[1], new_z + height_offset] = 1.0
                    for k in range(-2, 3):  # Ширина по x и y
                        for l in range(-2, 3):
                            if 0 <= start_point[0] + k < shape[0] and 0 <= start_point[1] + l < shape[1]:
                                array[start_point[0] + k, start_point[1] + l, new_z + height_offset] = 1.0

    for i in range(len(points2)):
        start_point = points2[i]
        end_point = points3[i]
        for new_z in range(min(start_point[2], end_point[2]), max(start_point[2], end_point[2]) + 1):
            if 0 <= start_point[0] < shape[0] and 0 <= start_point[1] < shape[1]:
                for height_offset in range(-1, 5):  # Высота коридоров
                    array[start_point[0], start_point[1], new_z + height_offset] = 1.0
                    for k in range(-2, 3):  # Ширина по x и y
                        for l in range(-2, 3):
                            if 0 <= start_point[0] + k < shape[0] and 0 <= start_point[1] + l < shape[1]:
                                array[start_point[0] + k, start_point[1] + l, new_z + height_offset] = 1.0

    return array

# Параметры
shape = (128, 128, 128)  # Размеры 3D массива

# Генерация 3D-поля с коридорами
delaunay_field = generate_delaunay_field(shape)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(delaunay_field, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "delaunay.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], color='r', alpha=0.5)
plt.show()
