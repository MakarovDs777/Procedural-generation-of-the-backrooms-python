import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import measure
from scipy.spatial import Delaunay
import os

def generate_delaunay_field(shape, num_cubes, distance):
    array = np.zeros(shape, dtype=float)

    points = []
    for i in range(num_cubes):
        x = (i % 2) * distance + distance // 2
        y = ((i // 2) % 2) * distance + distance // 2
        z = (i // 4) * distance + distance // 2
        if x < shape[0] and y < shape[1] and z < shape[2]:
            points.append([x, y, z])  # Генерируем кубы на фиксированной высоте
            generate_cube(array, (x, y, z), 5)

    for i in range(len(points) - 1):
        dx = points[i+1][0] - points[i][0]
        dy = points[i+1][1] - points[i][1]
        dz = points[i+1][2] - points[i][2]
        length = max(abs(dx), abs(dy), abs(dz))

        if abs(dx) > abs(dy) and abs(dx) > abs(dz):
            for j in range(abs(dx)):
                new_x = int(points[i][0] + j * np.sign(dx))
                new_y = points[i][1]
                new_z = points[i][2]
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                    array[new_x, new_y, new_z] = 1.0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            for m in range(-2, 3):
                                x1, y1, z1 = new_x + k, new_y + l, new_z + m
                                if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                    array[x1, y1, z1] = 1.0
            for j in range(abs(dz)):
                new_x = new_x
                new_y = new_y
                new_z = int(points[i][2] + j * np.sign(dz))
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                    array[new_x, new_y, new_z] = 1.0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            for m in range(-2, 3):
                                x1, y1, z1 = new_x + k, new_y + l, new_z + m
                                if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                    array[x1, y1, z1] = 1.0
        elif abs(dy) > abs(dx) and abs(dy) > abs(dz):
            for j in range(abs(dy)):
                new_x = points[i][0]
                new_y = int(points[i][1] + j * np.sign(dy))
                new_z = points[i][2]
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                    array[new_x, new_y, new_z] = 1.0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            for m in range(-2, 3):
                                x1, y1, z1 = new_x + k, new_y + l, new_z + m
                                if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                    array[x1, y1, z1] = 1.0
            for j in range(abs(dz)):
                new_x = new_x
                new_y = new_y
                new_z = int(points[i][2] + j * np.sign(dz))
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                    array[new_x, new_y, new_z] = 1.0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            for m in range(-2, 3):
                                x1, y1, z1 = new_x + k, new_y + l, new_z + m
                                if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                    array[x1, y1, z1] = 1.0
        else:
            for j in range(abs(dz)):
                new_x = points[i][0]
                new_y = points[i][1]
                new_z = int(points[i][2] + j * np.sign(dz))
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                    array[new_x, new_y, new_z] = 1.0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            for m in range(-2, 3):
                                x1, y1, z1 = new_x + k, new_y + l, new_z + m
                                if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                    array[x1, y1, z1] = 1.0

    for i in range(len(points)):
        x, y, z = points[i]
        if 0 <= x < shape[0] and 0 <= y < shape[1] and 0 <= z < shape[2]:
            for j in range(shape[0]):
                new_x = j
                new_y = y
                new_z = z
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                    array[new_x, new_y, new_z] = 1.0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            for m in range(-2, 3):
                                x1, y1, z1 = new_x + k, new_y + l, new_z + m
                                if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                    array[x1, y1, z1] = 1.0
            for j in range(shape[1]):
                new_x = x
                new_y = j
                new_z = z
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                    array[new_x, new_y, new_z] = 1.0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            for m in range(-2, 3):
                                x1, y1, z1 = new_x + k, new_y + l, new_z + m
                                if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                    array[x1, y1, z1] = 1.0
            for j in range(shape[2]):
                new_x = x
                new_y = y
                new_z = j
                if 0 <= new_x < shape[0] and 0 <= new_y < shape[1] and 0 <= new_z < shape[2]:
                    array[new_x, new_y, new_z] = 1.0
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            for m in range(-2, 3):
                                x1, y1, z1 = new_x + k, new_y + l, new_z + m
                                if 0 <= x1 < shape[0] and 0 <= y1 < shape[1] and 0 <= z1 < shape[2]:
                                    array[x1, y1, z1] = 1.0

    return array

def generate_cube(array, point, size):
    x, y, z = int(point[0]), int(point[1]), int(point[2])
    for i in range(-size, size+1):
        for j in range(-size, size+1):
            for k in range(-size, size+1):
                new_x, new_y, new_z = x + i, y + j, z + k
                if 0 <= new_x < array.shape[0] and 0 <= new_y < array.shape[1] and 0 <= new_z < array.shape[2]:
                    array[new_x, new_y, new_z] = 1.0

shape = (128, 128, 128) 
num_cubes = 60
distance = 20  

delaunay_field = generate_delaunay_field(shape, num_cubes, distance)

verts, faces, _, _ = measure.marching_cubes(delaunay_field, level=0.5)

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "delaunay.obj")
with open(filename, "w") as f:
    for j, vert in enumerate(verts):
        f.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")
    for face in faces:
        f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
print(f"Model saved as {filename}")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], color='blue', alpha=0.5)
plt.show()
