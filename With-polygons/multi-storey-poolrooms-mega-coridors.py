import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
from scipy.spatial import Delaunay
import os

# Функция для генерации 3D-поля с триангуляцией Делоне
def generate_delaunay_field(shape):
    array = np.zeros(shape, dtype=float)

    # Генерация кубов на каждом уровне
    points = []
    for level in range(3):
        for _ in range(10):
            x = np.random.randint(10, shape[0] - 10)
            y = np.random.randint(10, shape[1] - 10)
            z = level * (shape[2] // 3) + np.random.randint(10, shape[2] // 3 - 10)
            points.append([x, y, z])
            generate_cube(array, (x, y, z), np.random.randint(4, 8))

    # Генерация линий между кубами на разных уровнях
    # Генерация коридоров между кубами
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            if points[i][2]!= points[j][2]:
                dx = points[i][0] - points[j][0]
                dy = points[i][1] - points[j][1]
                dz = points[i][2] - points[j][2]
                length = max(abs(dx), abs(dy), abs(dz))
                for k in range(int(length)):
                    if abs(dx) > abs(dy):
                        new_x = int(points[i][0] + k * dx // length)
                        new_y = points[i][1]
                    else:
                        new_x = points[i][0]
                        new_y = int(points[i][1] + k * dy // length)
                    new_z = points[i][2] + k * dz // length
                    if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                        array[new_x, new_y, new_z] = 1.0
                        for l in range(-2, 3):
                            for m in range(-2, 3):
                                x1, y1, z1 = new_x + l, new_y + m, new_z
                                if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                    array[x1, y1, z1] = 1.0

    return array

# Функция для генерации куба в заданной точке
def generate_cube(array, point, size):
    x, y, z = int(point[0]), int(point[1]), int(point[2])
    for i in range(-size, size+1):
        for j in range(-size, size+1):
            for k in range(-size, size+1):
                new_x, new_y, new_z = x + i, y + j, z + k
                if 0 <= new_x < array.shape[0] and 0 <= new_y < array.shape[1] and 0 <= new_z < array.shape[2]:
                    array[new_x, new_y, new_z] = 1.0

# Параметры
shape = (128, 128, 128)  # Размеры 3D массива

# Генерация 3D-поля с триангуляцией Делоне
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
ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], triangles=faces, cmap='viridis', alpha=0.5)
plt.show()