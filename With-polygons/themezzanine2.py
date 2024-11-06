import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
from scipy.interpolate import interp1d
import os

# Генерация изогнутой линии
def generate_curve():
    points = []
    for i in range(100):
        x = np.random.uniform(-10, 10)
        y = np.random.uniform(-10, 10)
        z = np.random.uniform(-10, 10)
        points.append([x, y, z])

    # Интерполяция
    t = np.linspace(0, 1, len(points))
    x = np.array([point[0] for point in points])
    y = np.array([point[1] for point in points])
    z = np.array([point[2] for point in points])

    x_interp = interp1d(t, x, kind='cubic')
    y_interp = interp1d(t, y, kind='cubic')
    z_interp = interp1d(t, z, kind='cubic')

    t_interp = np.linspace(0, 1, 1000)
    x_interp = x_interp(t_interp)
    y_interp = y_interp(t_interp)
    z_interp = z_interp(t_interp)

    return x_interp, y_interp, z_interp

# Генерация изосурфейса
def generate_surface(x, y, z):
    # Создание 3D массива
    array = np.zeros((64, 64, 64), dtype=float)

    # Создание трубчатой структуры
    for i in range(len(x)):
        x_idx = int((x[i] + 10) / 20 * 64)
        y_idx = int((y[i] + 10) / 20 * 64)
        z_idx = int((z[i] + 10) / 20 * 64)

        if 0 <= x_idx < 64 and 0 <= y_idx < 64 and 0 <= z_idx < 64:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    for dz in range(-2, 3):
                        if 0 <= x_idx + dx < 64 and 0 <= y_idx + dy < 64 and 0 <= z_idx + dz < 64:
                            array[x_idx + dx, y_idx + dy, z_idx + dz] = 1.0

    return array

# Параметры
shape = (64, 64, 64)  # Размеры 3D массива

# Генерация изогнутой линии
x, y, z = generate_curve()

# Генерация изосурфейса
surface = generate_surface(x, y, z)

# Создание изосурфейса
verts, faces, _, _ = measure.marching_cubes(surface, level=0.5)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "curve.obj")
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