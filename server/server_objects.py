from copy import copy
import numpy as np
import lin_alg


class Object:

    def __init__(self, faces, vertices, edges, color=[1, 1, 1]):
        # [i] object cs
        self.faces = faces
        self.vertices = vertices
        self.edges = edges
        self.color = color

    def move(self, vector) -> None:
        """moves the object

        Args:
            vector (list of 3): the vector to add to the objects position
        """
        self.vertices = [np.add(vertex, vector) for vertex in self.verticies]


#  [i] object cs => (f,l,u)
#  [i] gl cs => (r,u,b)


colors = {"black": [0, 0, 0], "green": [0, 1, 0], "red": [1, 0, 0], "blue": [0, 0, 1]}
# [i] object cs
cube_vertices_vector3 = [
    [1.0000, 1.0000, 1.0000],
    [1.0000, 1.0000, -1.0000],
    [1.0000, -1.0000, 1.0000],
    [1.0000, -1.0000, -1.0000],
    [-1.0000, 1.0000, 1.0000],
    [-1.0000, 1.0000, -1.0000],
    [-1.0000, -1.0000, 1.0000],
    [-1.0000, -1.0000, -1.0000]]
# [i] object cs
cube_edges_vector2 = [
    [5, 7],
    [1, 5],
    [0, 1],
    [7, 6],
    [2, 3],
    [4, 5],
    [2, 6],
    [0, 2],
    [7, 3],
    [6, 4],
    [4, 0],
    [3, 1],
]
# [i] object cs
cube_faces_vector4 = [
    [0, 4, 6, 2],
    [3, 2, 6, 7],
    [7, 6, 4, 5],
    [5, 1, 3, 7],
    [1, 0, 2, 3],
    [5, 4, 0, 1],
]
# [i] object cs
floor_vertices_vector3 = [
    [100.0000, 100.0000, -2.0000],
    [100.0000, 100.0000, -3.0000],
    [100.0000, -100.0000, -2.0000],
    [100.0000, -100.0000, -3.0000],
    [-100.0000, 100.0000, -2.0000],
    [-100.0000, 100.0000, -3.0000],
    [-100.0000, -100.0000, -2.0000],
    [-100.0000, -100.0000, -3.0000], ]
# [i] object cs
floor_edges_vector2 = [
    [5, 7],
    [1, 5],
    [0, 1],
    [7, 6],
    [2, 3],
    [4, 5],
    [2, 6],
    [0, 2],
    [7, 3],
    [6, 4],
    [4, 0],
    [3, 1],
]
# [i] object cs
floor_faces_vector4 = [
    [0, 4, 6, 2],
    [3, 2, 6, 7],
    [7, 6, 4, 5],
    [5, 1, 3, 7],
    [1, 0, 2, 3],
    [5, 4, 0, 1],
]
# [i] object cs
player_template_vertices_vector3 = [
    [0.5000, 0.50000, 1.000],
    [0.5000, 0.5000, -1.000],
    [0.5000, -0.5000, 1.000],
    [0.5000, -0.5000, -1.000],
    [-0.5000, 0.5000, 1.000],
    [-0.5000, 0.5000, -1.000],
    [-0.5000, -0.5000, 1.000],
    [-0.5000, -0.5000, -1.000], ]
# [i] object cs
player_template_edges_vector2 = [
    [5, 7],
    [1, 5],
    [0, 1],
    [7, 6],
    [2, 3],
    [4, 5],
    [2, 6],
    [0, 2],
    [7, 3],
    [6, 4],
    [4, 0],
    [3, 1],
]
# [i] object cs
player_template_faces_vector4 = [
    [0, 4, 6, 2],
    [3, 2, 6, 7],
    [7, 6, 4, 5],
    [5, 1, 3, 7],
    [1, 0, 2, 3],
    [5, 4, 0, 1],
]
# [i] object cs
players = {}
# [i] object cs
world = [Object(cube_faces_vector4, cube_vertices_vector3, cube_edges_vector2),
         Object(floor_faces_vector4, floor_vertices_vector3, floor_edges_vector2, [0.3, 0.3, 0.3])]


def create_player(color, position, is_gl_cs=True) -> None:
    """adds a player to the player object list

    Args:
        color (str): player color
        position (list of 3): player position
        is_gl_cs (bool, optional): is the position in gl cs. Defaults to True.
    """
    try:
        if is_gl_cs:
            position = lin_alg.convert_gl_to_object_cs(position)

        # [i] position - object cs
        players[color] = (Object(copy(player_template_faces_vector4),
                                [np.add(vertex, position) for vertex in player_template_vertices_vector3],
                                copy(player_template_edges_vector2), colors[color]))
    except Exception as e:
        print(color, position, "create player")

def line_world_intersection(pos, vector, color) -> float:
    """checks the intersection of a bullet with the world

    Args:
        pos (list of 3 - gl cs): starting position of the shooter
        vector (list of 3 - gl cs): bullet direction vector

    Returns:
        float: distance from targetwd
    """
    # [i] pos and vector in gl cs
    min_distance = np.Inf
    object_hit = None
    # testing for each face for each object
    for obj in players.values():
        if colors[color] != obj.color:
            # [i] obj in object cs
            for face in obj.faces:
                # [i] plane converted to gl cs
                plane = [lin_alg.convert_object_to_gl_cs(obj.vertices[index]) for index in face]
                # calculating intersection
                intersection = lin_alg.line_plane_distance(plane, pos, vector)
                # reassigning the object hit if its the closest one and its hit
                if intersection > 0 and intersection < min_distance:
                    min_distance = intersection
                    object_hit = obj
    object_color = None
    # returning the color of the player hit
    if object_hit:
        object_color = [key for key, val in colors.items() if  val == object_hit.color][0]
    return object_color
