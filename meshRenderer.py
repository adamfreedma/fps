from objects import *
from OpenGL.GL import *
import numpy as np
from LinAlg import *
from OpenGL.GLU import *
import objects


def mesh_all(looking):
    mesh(objects.world, looking)
    mesh(objects.players, looking)


def mesh(object_list, looking):
    glBegin(GL_QUADS)
    for obj in object_list:
        for face in obj.faces:
            # ? does open gl lighting implement this
            color = obj.color
            face_norm = convert_object_to_gl_cs(plane_normal([obj.verticies[index] for index in face]))
            # changing the brightness by the projection of the planes norm
            color = [np.linalg.norm(np.cross(face_norm, looking)) * c for c in color]
            for vertex in face:
                glColor3fv(color)
                glVertex3fv(obj.verticies[vertex])
    glEnd()


def draw_line(p1, p2, color):
    glBegin(GL_LINES);
    glColor3fv(color)
    glVertex2fv(p1);
    glVertex2fv(p2);
    glEnd();
