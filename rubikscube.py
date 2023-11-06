import copy
import time
from math import cos, sin
import numpy as np
import pygame

pygame.init()


class Rubicube3D:
    def __init__(self):
        self.faces = []

        self.points = [np.matrix([-1, -1, 1]),
                       np.matrix([1, -1, 1]),
                       np.matrix([1, 1, 1]),
                       np.matrix([-1, 1, 1]),
                       np.matrix([-1, -1, -1]),
                       np.matrix([1, -1, -1]),
                       np.matrix([1, 1, -1]),
                       np.matrix([-1, 1, -1])
                       ]

        for count_ in range(6):
            self.faces.append([[count_ for i in range(3)] for j in range(3)])

        self.faces_pos_3D = [[5, 4, 7, 6],  # blue
                             [4, 0, 3, 7],  # yellow
                             [3, 2, 6, 7],  # orange
                             [1, 5, 6, 2],  # green
                             [0, 1, 2, 3],  # red
                             [4, 5, 1, 0],  # violet
                            ]

        self.colors = {0: (255, 0, 0),
                       1: (0, 255, 0),
                       2: (0, 0, 255),
                       3: (255, 255, 0),
                       4: (255, 0, 255),
                       5: (255, 128, 0)
                       }

        self.orientation = [0, 0, 0]



    def draw3D(self, win):
        rot_points_3D = self.apply_rotation_3D(self.orientation)

        rot_points = copy.deepcopy(rot_points_3D)

        projection_matrix = np.matrix([
            [1, 0, 0],
            [0, 1, 0]
        ])

        for i, point in enumerate(rot_points):
            rot_points[i] = np.dot(projection_matrix, point)

        for i, face in enumerate(self.faces_pos_3D):

            # calculer la normale de la face
            v0, v1, v2, v3 = [rot_points_3D[face[0]], rot_points_3D[face[1]], rot_points_3D[face[2]],
                              rot_points_3D[face[3]]]

            v0 = np.array(v0).flatten()
            v1 = np.array(v1).flatten()
            v2 = np.array(v2).flatten()

            u = v1 - v0
            v = v2 - v0
            normal = np.cross(u, v)


            if normal[2] > 0:

                # diviser la face en 9 carres
                for i_ in range(3):
                    for j in range(3):
                        # Calculez les coins du carre
                        x0 = rot_points[face[0]] + (rot_points[face[1]] - rot_points[face[0]]) * (i_ / 3) + (
                                    rot_points[face[3]] - rot_points[face[0]]) * (j / 3)
                        x1 = rot_points[face[0]] + (rot_points[face[1]] - rot_points[face[0]]) * ((i_ + 1) / 3) + (
                                    rot_points[face[3]] - rot_points[face[0]]) * (j / 3)
                        x2 = rot_points[face[0]] + (rot_points[face[1]] - rot_points[face[0]]) * ((i_ + 1) / 3) + (
                                    rot_points[face[3]] - rot_points[face[0]]) * ((j + 1) / 3)
                        x3 = rot_points[face[0]] + (rot_points[face[1]] - rot_points[face[0]]) * (i_ / 3) + (
                                    rot_points[face[3]] - rot_points[face[0]]) * ((j + 1) / 3)


                        # dessiner le carre

                        pygame.draw.polygon(win, self.colors[self.faces[i][j][i_]],
                                            (
                                                (x0[0, 0] * 100 + 450, x0[1, 0] * 100 + 450),
                                                (x1[0, 0] * 100 + 450, x1[1, 0] * 100 + 450),
                                                (x2[0, 0] * 100 + 450, x2[1, 0] * 100 + 450),
                                                (x3[0, 0] * 100 + 450, x3[1, 0] * 100 + 450)
                                            )
                                            )

                        # dessiner les contours du carre
                        contour_color = (0, 0, 0)
                        pygame.draw.line(win, contour_color, (x0[0, 0] * 100 + 450, x0[1, 0] * 100 + 450),
                                         (x1[0, 0] * 100 + 450, x1[1, 0] * 100 + 450))
                        pygame.draw.line(win, contour_color, (x1[0, 0] * 100 + 450, x1[1, 0] * 100 + 450),
                                            (x2[0, 0] * 100 + 450, x2[1, 0] * 100 + 450))
                        pygame.draw.line(win, contour_color, (x2[0, 0] * 100 + 450, x2[1, 0] * 100 + 450),
                                            (x3[0, 0] * 100 + 450, x3[1, 0] * 100 + 450))
                        pygame.draw.line(win, contour_color, (x3[0, 0] * 100 + 450, x3[1, 0] * 100 + 450),
                                            (x0[0, 0] * 100 + 450, x0[1, 0] * 100 + 450))

    def apply_rotation_3D(self, rotation):
        rotation_z = np.matrix([
            [cos(rotation[2]), -sin(rotation[2]), 0],
            [sin(rotation[2]), cos(rotation[2]), 0],
            [0, 0, 1]
        ])

        rotation_y = np.matrix([
            [cos(rotation[1]), 0, sin(rotation[1])],
            [0, 1, 0],
            [-sin(rotation[1]), 0, cos(rotation[1])]
        ])

        rotation_x = np.matrix([
            [1, 0, 0],
            [0, cos(rotation[0]), -sin(rotation[0])],
            [0, sin(rotation[0]), cos(rotation[0])]
        ])

        rot_points = [[x, x, x] for x in range(len(self.points))]
        for i, point in enumerate(self.points):
            rot = np.dot(rotation_y, point.reshape((3, 1)))
            rot = np.dot(rotation_z, rot)
            rot = np.dot(rotation_x, rot)

            rot_points[i] = rot
        return rot_points

    def turn_face(self, face):
        saved_cube = copy.deepcopy(self.faces)
        if face != 5 and face != 4 and face != 1:
            for i in range(3):
                for j in range(3):
                    self.faces[face][i][j] = saved_cube[face][j][2 - i]
        else:
            for i in range(3):
                for j in range(3):
                    self.faces[face][j][2 - i] = saved_cube[face][i][j]

        if face == 2:
            self.turn_top(0)
        elif face == 5:
            self.turn_top(2)
        elif face == 0:
            self.turn_line(0)
        elif face == 4:
            self.turn_line(2)
        elif face == 1:
            self.turn_columns(0)
        elif face == 3:
            self.turn_columns(2)

    def turn_line(self, line):
        saved_cube = copy.deepcopy(self.faces)
        line_turns = [1, 2, 3, 5]

        for i in range(4):
            for j in range(3):
                if i % 2 == 0:
                    if i == 2:
                        self.faces[line_turns[i]][j][2-line] = saved_cube[line_turns[i - 1]][2-line][j]
                    else:
                        self.faces[line_turns[i]][j][line] = saved_cube[line_turns[i - 1]][line][j]
                else:
                    if i == 1:
                        self.faces[line_turns[i]][2-line][j] = saved_cube[line_turns[i - 1]][j][line]
                    else:
                        self.faces[line_turns[i]][line][j] = saved_cube[line_turns[i - 1]][j][2-line]


    def turn_columns(self, columns):

        saved_cube = copy.deepcopy(self.faces)
        column_turns = [0, 2, 4, 5]

        for i in reversed(range(4)):
            for j in reversed(range(3)):
                if not i == 0:
                    if not i == 1:
                        self.faces[column_turns[i]][j][columns] = saved_cube[column_turns[i - 1]][j][columns]
                    else:
                        self.faces[column_turns[i]][j][columns] = saved_cube[column_turns[i - 1]][j][2-columns]
                else:
                    self.faces[column_turns[i]][j][2-columns] = saved_cube[column_turns[3]][j][columns]


    def turn_top(self, top):
        saved_cube = copy.deepcopy(self.faces)
        top_turns = [0, 3, 4, 1]

        for i in reversed(range(4)):
            for j in reversed(range(3)):
                self.faces[top_turns[i]][2-top][j] = saved_cube[top_turns[i - 1]][2-top][j]




window = pygame.display.set_mode((900, 900))

rubicube = Rubicube3D()

time_keys = time.time() * 1000
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
    window.fill((255, 255, 255))

    rubicube.draw3D(window)

    pygame.display.flip()
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        rubicube.orientation[0] -= 0.05
    if key[pygame.K_DOWN]:
        rubicube.orientation[0] += 0.05
    if key[pygame.K_LEFT]:
        rubicube.orientation[1] -= 0.05
    if key[pygame.K_RIGHT]:
        rubicube.orientation[1] += 0.05
    if key[pygame.K_n]:
        rubicube.orientation[2] += 0.05
    if key[pygame.K_b]:
        rubicube.orientation[2] -= 0.05

    if key[pygame.K_m]:
        rand = np.random.randint(0, 5)
        if np.random.randint(0, 2) == 0:
            rubicube.turn_face(rand)
        else:
            rand = np.random.randint(0, 3)

            if rand == 0:
                rubicube.turn_line(1)
            elif rand == 1:
                rubicube.turn_columns(1)
            elif rand == 2:
                rubicube.turn_top(1)


    if time.time() * 1000 - time_keys > 100:
        if key[pygame.K_r]:
            rubicube.faces = []
            for count in range(6):
                rubicube.faces.append([[count for i in range(3)] for j in range(3)])
        elif key[pygame.K_t]:
            rubicube.turn_face(0)
        elif key[pygame.K_y]:
            rubicube.turn_face(1)
        elif key[pygame.K_u]:
            rubicube.turn_face(2)
        elif key[pygame.K_i]:
            rubicube.turn_face(3)
        elif key[pygame.K_o]:
            rubicube.turn_face(4)
        elif key[pygame.K_p]:
            rubicube.turn_face(5)
        elif key[pygame.K_g]:
            rubicube.turn_line(1)
        elif key[pygame.K_h]:
            rubicube.turn_columns(1)
        elif key[pygame.K_j]:
            rubicube.turn_top(1)
        time_keys = time.time() * 1000


pygame.quit()
