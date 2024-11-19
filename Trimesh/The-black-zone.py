import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def generate_room(x, z):
    room_size = np.random.randint(5, 15)
    room_height = np.random.randint(5, 10)
    vertices = np.array([
        [0, 0, 0],
        [room_size, 0, 0],
        [room_size, room_size, 0],
        [0, room_size, 0],
        [0, 0, room_height],
        [room_size, 0, room_height],
        [room_size, room_size, room_height],
        [0, room_size, room_height]
    ])
    faces = np.array([
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [2, 3, 7, 6],
        [3, 0, 4, 7]
    ])
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.vertices += [x, 0, z]
    return mesh

def generate_corridor(x, z, length, direction):
    corridor_width = 2
    corridor_height = 2
    vertices = np.array([
        [0, -corridor_width/2, 0],
        [length, -corridor_width/2, 0],
        [length, corridor_width/2, 0],
        [0, corridor_width/2, 0],
        [0, -corridor_width/2, corridor_height],
        [length, -corridor_width/2, corridor_height],
        [length, corridor_width/2, corridor_height],
        [0, corridor_width/2, corridor_height]
    ])
    faces = np.array([
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [2, 3, 7, 6],
        [3, 0, 4, 7]
    ])
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.vertices += [x, 0, z]
    rotation_matrix = np.array([
        [np.cos(direction), -np.sin(direction), 0],
        [np.sin(direction), np.cos(direction), 0],
        [0, 0, 1]
    ])
    mesh.vertices = (rotation_matrix @ mesh.vertices.T).T
    return mesh

# Генерация комнат и коридоров
meshes = []
for _ in range(10):
    x = np.random.randint(-50, 50)
    z = np.random.randint(-50, 50)
    room = generate_room(x, z)
    meshes.append(room)
    if np.random.rand() < 0.5:
        corridor_length = np.random.randint(5, 20)
        corridor_direction = np.random.uniform(0, np.pi)
        corridor = generate_corridor(x, z, corridor_length, corridor_direction)
        meshes.append(corridor)
    if np.random.rand() < 0.5:
        x2 = x + np.random.randint(-10, 10)
        z2 = z + np.random.randint(-10, 10)
        room2 = generate_room(x2, z2)
        meshes.append(room2)
        corridor_length = np.sqrt((x - x2)**2 + (z - z2)**2)
        corridor_direction = np.arctan2(z2 - z, x2 - x)
        corridor = generate_corridor(x, z, corridor_length, corridor_direction)
        meshes.append(corridor)

# Сохранение модели
mesh = trimesh.util.concatenate(meshes)
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "model.obj")
mesh.export(filename)
print(f"Model saved as {filename}")

# Визуализация модели
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], color='r', alpha=0.5)
for face in mesh.faces:
    v1, v2, v3 = mesh.vertices[face]
    ax.plot3D([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]], 'r', alpha=0.5)
    ax.plot3D([v2[0], v3[0]], [v2[1], v3[1]], [v2[2], v3[2]], 'r', alpha=0.5)
    ax.plot3D([v3[0], v1[0]], [v3[1], v1[1]], [v3[2], v1[2]], 'r', alpha=0.5)
plt.show()
