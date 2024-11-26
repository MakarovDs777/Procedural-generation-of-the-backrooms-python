import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import noise
import os
import sys
# Инициализация Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Инициализация камеры
gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
glTranslatef(0.0, 0.0, -30)
glRotatef(45, 1, 0, 0)  # Повернуть камеру на 45 градусов вокруг оси X

# Генерация шума
def generate_noise_2d(shape, x_offset, z_offset, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0):
    noise_map = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            noise_map[i][j] = noise.pnoise2((i + x_offset) / scale, (j + z_offset) / scale, octaves=octaves,
                                              persistence=persistence, lacunarity=lacunarity, repeatx=1024,
                                              repeaty=1024, base=42)
    return noise_map

# Создание террейна
def create_terrain(width, height, x_offset, z_offset):
    noise_map = generate_noise_2d((width, height), x_offset, z_offset)
    vertices = []
    for i in range(width):
        for j in range(height):
            x = i - width // 2
            z = j - height // 2
            y = noise_map[i][j] * 10
            vertices.append((x, y, z))
    return vertices

# Отрисовка террейна
def draw_terrain(vertices, width, height):
    glBegin(GL_TRIANGLES)
    for i in range(width - 1):
        for j in range(height - 1):
            glVertex3fv(vertices[i * height + j])
            glVertex3fv(vertices[(i + 1) * height + j])
            glVertex3fv(vertices[i * height + j + 1])

            glVertex3fv(vertices[(i + 1) * height + j])
            glVertex3fv(vertices[(i + 1) * height + j + 1])
            glVertex3fv(vertices[i * height + j + 1])
    glEnd()

# Отрисовка комнаты
def draw_room(width, height, depth):
    glBegin(GL_QUADS)
    # Пол
    glVertex3fv((-width/2, 0, -depth/2))
    glVertex3fv((width/2, 0, -depth/2))
    glVertex3fv((width/2, 0, depth/2))
    glVertex3fv((-width/2, 0, depth/2))

    # Потолок
    glVertex3fv((-width/2, height, -depth/2))
    glVertex3fv((width/2, height, -depth/2))
    glVertex3fv((width/2, height, depth/2))
    glVertex3fv((-width/2, height, depth/2))

    # Стены
    glVertex3fv((-width/2, 0, -depth/2))
    glVertex3fv((-width/2, height, -depth/2))
    glVertex3fv((-width/2, height, depth/2))
    glVertex3fv((-width/2, 0, depth/2))

    glVertex3fv((width/2, 0, -depth/2))
    glVertex3fv((width/2, height, -depth/2))
    glVertex3fv((width/2, height, depth/2))
    glVertex3fv((width/2, 0, depth/2))

    glVertex3fv((-width/2, 0, -depth/2))
    glVertex3fv((width/2, 0, -depth/2))
    glVertex3fv((width/2, height, -depth/2))
    glVertex3fv((-width/2, height, -depth/2))

    glVertex3fv((-width/2, 0, depth/2))
    glVertex3fv((width/2, 0, depth/2))
    glVertex3fv((width/2, height, depth/2))
    glVertex3fv((-width/2, height, depth/2))
    glEnd()
    
# Сохранение в OBJ файл
def save_to_obj(vertices, faces, filename):
    with open(filename, "w") as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")

# Основной цикл
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Сохранение на нажатие R
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                filename = os.path.join(desktop_path, "scene.obj")
                vertices = create_terrain(100, 100, 0, 0)
                terrain_faces = []
                for i in range(100 - 1):
                    for j in range(100 - 1):
                        terrain_faces.append([i * 100 + j, (i + 1) * 100 + j, i * 100 + j + 1])
                        terrain_faces.append([(i + 1) * 100 + j, (i + 1) * 100 + j + 1, i * 100 + j + 1])
                room_vertices = [
    [-50, 0, -50],
    [50, 0, -50],
    [50, 0, 50],
    [-50, 0, 50],
    [-50, 50, -50],
    [50, 50, -50],
    [50, 50, 50],
    [-50, 50, 50]
               ]
                room_faces = [
    [0, 1, 2],  # пол
    [0, 2, 3],
    [4, 5, 6],  # потолок
    [4, 6, 7],
    [0, 1, 5],  # стена 1
    [0, 5, 4],
    [1, 2, 6],  # стена 2
    [1, 6, 5],
    [2, 3, 7],  # стена 3
    [2, 7, 6],
    [3, 0, 4],  # стена 4
    [3, 4, 7]
                ]
                all_vertices = vertices + room_vertices
                all_faces = terrain_faces + [[x + len(vertices) for x in face] for face in room_faces]
                save_to_obj(all_vertices, all_faces, filename)
                print(f"Model saved as {filename}")

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
    glTranslatef(0.0, 0.0, -30)
    glRotatef(45, 1, 0, 0)  # Повернуть камеру на 45 градусов вокруг оси X

    # Отрисовка террейна
    vertices = create_terrain(100, 100, 0, 0)
    draw_terrain(vertices, 100, 100)

    # Отрисовка комнаты
    draw_room(100, 50, 100)

    pygame.display.flip()
    clock.tick(60)
