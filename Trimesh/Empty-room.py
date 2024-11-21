import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os

def generate_room_with_holes(width, height, depth, num_holes):
    # Определите вершины комнаты
    vertices = [
        [0, 0, 0],
        [width, 0, 0],
        [width, 0, depth],
        [0, 0, depth],
        [0, height, 0],
        [width, height, 0],
        [width, height, depth],
        [0, height, depth]
    ]

    # Определите грани комнаты
    faces = [
        [0, 1, 2],
        [0, 2, 3],
        [4, 5, 6],
        [4, 6, 7],
        [0, 1, 5],
        [0, 5, 4],
        [1, 2, 6],
        [1, 6, 5],
        [2, 3, 7],
        [2, 7, 6],
        [3, 0, 4],
        [3, 4, 7]
    ]

    mesh = trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))
    return mesh

# Генерация комнаты с дырками
room = generate_room_with_holes(100, 10, 100, 100)

# Сохранение изосурфейса в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "room_with_holes.obj")
room.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.add_collection3d(room)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_zlim(0, 10)
plt.show()
