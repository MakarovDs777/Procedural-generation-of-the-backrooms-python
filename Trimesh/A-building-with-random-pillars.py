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

    # Генерируем дырки внутри комнаты
    for _ in range(num_holes):
        # Выбираем случайную позицию на верхней стороне
        x = np.random.randint(0, width - 2)  # оставляем 2 единицы для ширины дырки
        y = np.random.randint(0, depth - 2)  # оставляем 2 единицы для глубины дырки

        # Генерируем дырку, которая проходит от потолка к потолку по уровню
        if x > 0 and x < width and y > 0 and y < depth:
            cube_verts = np.array([
                [x - 1, 0, y - 1],
                [x + 1, 0, y - 1],
                [x + 1, 0, y + 1],
                [x - 1, 0, y + 1],
                [x - 1, height, y - 1],
                [x + 1, height, y - 1],
                [x + 1, height, y + 1],
                [x - 1, height, y + 1]
            ])

            cube_faces = np.array([
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
            ])

            # Добавляем вершины и грани куба в общий список
            vertices.extend(cube_verts.tolist())
            faces.extend(cube_faces + len(vertices) - 8)

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