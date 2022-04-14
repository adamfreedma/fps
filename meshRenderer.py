from objects import *
from OpenGL.GL import *
import numpy as np
from LinAlg import *
from OpenGL.GLU import *
import objects


def mesh_all(looking) -> None:
    """rerenders all objects

    Args:
        looking (list of 3): the current vector of the players looking direction
    """
    mesh(objects.world, looking)
    mesh(objects.players.values(), looking)


def mesh(object_list, looking) -> None:
    """renders a list of objects

    Args:
        object_list (list of Object): the objects to render
        looking (list of 3): the current vector of the players looking direction
    """
    BRIGHTNESS = 2
    glBegin(GL_QUADS)
    for obj in object_list:
        for face in obj.faces:
            # ? does open gl lighting implement this
            color = obj.color
            face_norm = convert_object_to_gl_cs(plane_normal([obj.vertices[index] for index in face]))
            # changing the brightness by the projection of the planes norm
            brightness = 1 - (np.linalg.norm(np.cross(face_norm, looking)) / BRIGHTNESS)
            # making the floor bright no matter what
            if abs(face_norm[1]) == 1:
                brightness = 1
            # applying lighting
            color = [brightness * c for c in color]
            # drawing faces
            for vertex in face:
                glColor3fv(color)
                glVertex3fv(obj.vertices[vertex])
    glEnd()


def draw_line(p1, p2, color, width=5) -> None:
    """draws a line in the 3d plane

    Args:
        p1 (list of 3): point a
        p2 (list of 3): point b
        color (list of 3): the color of the line
        width (int, optional): draws a line between point a to b. Defaults to 5.
    """
    glLineWidth(width)
    glBegin(GL_LINES)
    glColor3fv(color)
    glVertex3fv(p1)
    glVertex3fv(p2)
    glEnd()
