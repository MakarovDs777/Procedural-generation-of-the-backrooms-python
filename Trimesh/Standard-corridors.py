import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os

# Функция для генерации 3D-поля с ровными коридорами
def generate_corridors(room_width, room_height, room_depth):
    points = []
    for _ in range(10):
        x = np.random.randint(10, room_width - 10)
        y = np.random.randint(10, room_height - 10)
        points.append([x, y])

    vertices = []
    faces = []

    for i in range(len(points) - 1):
        dx = points[i+1][0] - points[i][0]
        dy = points[i+1][1] - points[i][1]
        length = max(abs(dx), abs(dy))

        if abs(dx) > abs(dy):
            # Учитываем размеры комнаты
            x1 = max(0, points[i][0])
            x2 = min(room_width, points[i][0] + length)
            y1 = max(0, points[i][1])
            y2 = min(room_height, points[i][1] + 2)

            # Создаем коридор от потолка до пола
            z1 = 0
            z2 = room_depth

            vertices.extend([
                [x1, y1, z1],
                [x2, y1, z1],
                [x2, y2, z1],
                [x1, y2, z1],
                [x1, y1, z2],
                [x2, y1, z2],
                [x2, y2, z2],
                [x1, y2, z2]
            ])
            faces.extend([
                [i*8, i*8+1, i*8+2, i*8+3],
                [i*8+4, i*8+5, i*8+6, i*8+7],
                [i*8, i*8+1, i*8+5, i*8+4],
                [i*8+1, i*8+2, i*8+6, i*8+5],
                [i*8+2, i*8+3, i*8+7, i*8+6],
                [i*8+3, i*8, i*8+4, i*8+7]
            ])
        else:
            # Учитываем размеры комнаты
            x1 = max(0, points[i][0])
            x2 = min(room_width, points[i][0] + 2)
            y1 = max(0, points[i][1])
            y2 = min(room_height, points[i][1] + length)

            # Создаем коридор от потолка до пола
            z1 = 0
            z2 = room_depth

            vertices.extend([
                [x1, y1, z1],
                [x2, y1, z1],
                [x2, y2, z1],
                [x1, y2, z1],
                [x1, y1, z2],
                [x2, y1, z2],
                [x2, y2, z2],
                [x1, y2, z2]
            ])
            faces.extend([
                [i*8, i*8+1, i*8+2, i*8+3],
                [i*8+4, i*8+5, i*8+6, i*8+7],
                [i*8, i*8+1, i*8+5, i*8+4],
                [i*8+1, i*8+2, i*8+6, i*8+5],
                [i*8+2, i*8+3, i*8+7, i*8+6],
                [i*8+3, i*8, i*8+4, i*8+7]
            ])

    mesh = trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))
    return mesh

# Функция для генерации комнаты с дырками
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

# Генерация 3D-поля с коридорами
corridors = generate_corridors(100, 100, 10)

# Генерация комнаты с дырками
room = generate_room_with_holes(100, 100, 10, 100)

# Объединение мешей
combined_mesh = trimesh.util.concatenate([corridors, room])

# Сохранение объединенного меша в OBJ файл
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "combined.obj")
combined_mesh.export(filename)
print(f"Model saved as {filename}")

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.add_collection3d(combined_mesh)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_zlim(0, 10)
plt.show()
