import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os
import random
from scipy.spatial.transform import Rotation as R

def create_hole(position, size):
    """Создает куб в форме отверстия."""
    hole = trimesh.creation.box(extents=size)
    hole.vertices += position
    return hole

def generate_cube_with_corridor_and_room():
    # Создание куба
    cube = trimesh.creation.box(extents=(12, 4, 12))

    # Размеры коридора
    corridor_size = (1.0, 1.0, 1.0)  # Размеры коридора по осям (X, Y, Z)

    # Определяем позицию коридора
    corridor_position = [1, 2, -8]  # Коридор идет вверх

    # Создание коридора и вычитание из куба
    corridor = create_hole(corridor_position, corridor_size)
    cube = cube.difference(corridor)

    # Генерация комнаты, которая будет соединяться с коридором
    room = trimesh.creation.box(extents=(30, 2, 1.5))  # Размеры комнаты
    room_position = [10.0, -1.0, 0.0]  # Позиция комнаты (размещаем над кубом)
    room.vertices += room_position

    # Объединение куба и комнаты
    combined_mesh = cube.union(room)

    return combined_mesh

def generate_multiple_copies(mesh, num_copies):
    multiple_meshes = []
    for _ in range(num_copies):
        copy_mesh = mesh.copy()
        # Вращение меша на случайный угол в 90 градусов
        angle = random.choice([0, 90, 180, 270])  # углы в градусах
        rotation = R.from_euler('y', angle, degrees=True)
        transform = rotation.as_matrix()
        # Добавляем строку и столбец к матрице преобразования
        transform = np.vstack((transform, [0, 0, 0]))
        transform = np.hstack((transform, [[0], [0], [0], [1]]))
        copy_mesh = copy_mesh.apply_transform(transform)
        # Перемещение меша на случайную позицию
        copy_mesh.vertices += [random.uniform(-20, 30), 1, random.uniform(-20, 30)]
        multiple_meshes.append(copy_mesh)
    return multiple_meshes

def main():
    # Генерация куба с коридором и комнатой
    mesh = generate_cube_with_corridor_and_room()

    # Генерация множества копий
    multiple_meshes = generate_multiple_copies(mesh, 10)

    # Объединение копий в одну структуру
    combined_mesh = multiple_meshes[0]
    for i in range(1, len(multiple_meshes)):
        combined_mesh = combined_mesh.union(multiple_meshes[i])

    # Сохранение в OBJ файл
    desktop_path = os.path.expanduser("~")
    filename = os.path.join(desktop_path, "Desktop", "multiple_copies.obj")
    combined_mesh.export(filename)
    print(f"Файл сохранен как {filename}")

    # Визуализация
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(combined_mesh.vertices[:, 0], combined_mesh.vertices[:, 1], combined_mesh.vertices[:, 2], color='r', alpha=0.5)
    plt.show()

if __name__ == "__main__":
    main()
