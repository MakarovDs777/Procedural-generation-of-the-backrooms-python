import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
from scipy.spatial import Delaunay
import os

# Функция для генерации 3D-поля с триангуляцией Делоне
def generate_delaunay_field(shape):
    array = np.zeros(shape, dtype=float)
    points = []
    for i in range(100):
        x = np.random.uniform(0, shape[0])
        y = np.random.uniform(0, shape[1])
        z = np.random.uniform(0, shape[2])
        points.append([x, y, z])

    # Преобразование точек в NumPy массив 
    points = np.array(points)

    # Выполнить триангуляцию Делоне
    triangulation = Delaunay(points)

    # Постройте график треугольников
    for triangle in triangulation.simplices:
        for i in range(3):
            dx = points[triangle[(i+1)%3], 0] - points[triangle[i], 0]
            dy = points[triangle[(i+1)%3], 1] - points[triangle[i], 1]
            dz = points[triangle[(i+1)%3], 2] - points[triangle[i], 2]
            length = int(np.sqrt(dx**2 + dy**2 + dz**2))
            for j in range(length):
                new_x = int(points[triangle[i], 0] + j * dx // length)
                new_y = int(points[triangle[i], 1] + j * dy // length)
                new_z = int(points[triangle[i], 2] + j * dz // length)
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                    array[new_x, new_y, new_z] = 1.0
                    # Делаем линии более жирными
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            for m in range(-2, 3):
                                x1, y1, z1 = new_x + k, new_y + l, new_z + m
                                if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                    array[x1, y1, z1] = 1.0
        # Генерируем куб в точке пересечения линий
        intersection_point = (points[triangle[0]] + points[triangle[1]] + points[triangle[2]]) / 3
        generate_cube(array, intersection_point, np.random.randint(4, 8))
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
ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], color='r', alpha=0.5)
plt.show()