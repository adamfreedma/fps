from copy import copy
import numpy as np
import LinAlg


class Object:
    
    def __init__(self, faces, vertices, edges, color=[1, 1, 1]):
        # [i] object cs
        self.faces = faces
        self.vertices = vertices
        self.edges = edges
        self.color = color
        
    def move(self, vector):
        self.vertices = [np.add(vertex, vector) for vertex in self.verticies]
#  [i] object cs => (f,l,u)
#  [i] gl cs => (r,u,b)


colors = {"black": [0, 0, 0], "green": [0, 1, 0], "red": [1, 0, 0], "blue": [0, 0, 1]}

brown = (0.43, 0.3, 0.21)
gray = (0.4, 0.4, 0.4)

# [i] object cs
# *all boxes vertices*
b1_vertices_vector3 = [
    [5,-20,-1],
    [5,-20,1],
    [5,10,-1],
    [5,10,1],
    [25,-20,-1],
    [25,-20,1],
    [25,10,-1],
    [25,10,1],
]

b2_vertices_vector3 = [
    [5,5,-1],
    [5,5,1],
    [5,10,-1],
    [5,10,1],
    [-20,5,-1],
    [-20,5,1],
    [-20,10,-1],
    [-20,10,1],
]

a1_vertices_vector3 = [
    [-5,0,-1],
    [-5,0,1],
    [-5,-5,-1],
    [-5,-5,1],
    [-35,0,-1],
    [-35,0,1],
    [-35,-5,-1],
    [-35,-5,1],
]

a2_vertices_vector3 = [
    [-15,-5,-1],
    [-15,-5,1],
    [-15,-15,-1],
    [-15,-15,1],
    [-35,-5,-1],
    [-35,-5,1],
    [-35,-15,-1],
    [-35,-15,1],
]

c_vertices_vector3 = [
    [25,20,-1],
    [25,20,1],
    [25,40,-1],
    [25,40,1],
    [5,20,-1],
    [5,20,1],
    [5,40,-1],
    [5,40,1],
]

d_vertices_vector3 = [
    [0,40,-1],
    [0,40,1],
    [0,30,-1],
    [0,30,1],
    [-20,40,-1],
    [-20,40,1],
    [-20,30,-1],
    [-20,30,1],
]

e_vertices_vector3 = [
    [0,25,-1],
    [0,25,1],
    [0,15,-1],
    [0,15,1],
    [-20,25,-1],
    [-20,25,1],
    [-20,15,-1],
    [-20,15,1],
]


f_vertices_vector3 = [
    [0,-10,-1],
    [0,-10,1],
    [0,-15,-1],
    [0,-15,1],
    [-5,-10,-1],
    [-5,-10,1],
    [-5,-15,-1],
    [-5,-15,1],
]

w1_vertices_vector3 = [
    [-15,-25,-1],
    [-15,-25,1],
    [-15,-26,-1],
    [-15,-26,1],
    [-30,-25,-1],
    [-30,-25,1],
    [-30,-26,-1],
    [-30,-26,1],
]

w2_vertices_vector3 = [
    [-10,-10,-1],
    [-10,-10,1],
    [-10,-26,-1],
    [-10,-26,1],
    [-11,-10,-1],
    [-11,-10,1],
    [-11,-26,-1],
    [-11,-26,1],
]

w3_vertices_vector3 = [
    [25,-25,-1],
    [25,-25,1],
    [25,-26,-1],
    [25,-26,1],
    [0,-25,-1],
    [0,-25,1],
    [0,-26,-1],
    [0,-26,1],
]


wt_vertices_vector3 = [
    [30,50,-1],
    [30,50,1],
    [30,-31,-1],
    [30,-31,1],
    [31,50,-1],
    [31,50,1],
    [31,-31,-1],
    [31,-31,1],
]

wb1_vertices_vector3 = [
    [-30,50,-1],
    [-30,50,1],
    [-30,5,-1],
    [-30,5,1],
    [-31,50,-1],
    [-31,50,1],
    [-31,5,-1],
    [-31,5,1],
]
wb2_vertices_vector3 = [
    [-45,-31,-1],
    [-45,-31,1],
    [-45,5,-1],
    [-45,5,1],
    [-46,-31,-1],
    [-46,-31,1],
    [-46,5,-1],
    [-46,5,1],
]

wr_vertices_vector3 = [
    [30,-30,-1],
    [30,-30,1],
    [30,-31,-1],
    [30,-31,1],
    [-46,-30,-1],
    [-46,-30,1],
    [-46,-31,-1],
    [-46,-31,1],
]

wl1_vertices_vector3 = [
    [31, 50,-1],
    [31, 50,1],
    [31, 51,-1],
    [31, 51,1],
    [-31,50,-1],
    [-31,50,1],
    [-31,51,-1],
    [-31,51,1],
]

wl2_vertices_vector3 = [
    [-30,5,-1],
    [-30,5,1],
    [-30,4,-1],
    [-30,4,1],
    [-46,5,-1],
    [-46,5,1],
    [-46,4,-1],
    [-46,4,1],
]


# [i] object cs
edges_vector2 = [
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
faces_vector4 = [
    [0, 4, 6, 2],
    [3, 2, 6, 7],
    [7, 6, 4, 5],
    [5, 1, 3, 7],
    [1, 0, 2, 3],
    [5, 4, 0, 1],
    ]
# [i] object cs
floor_vertices_vector3 = [
    [100.0000, 100.0000, -1.0000],
    [100.0000, 100.0000, -2.0000],
    [100.0000, -100.0000, -1.0000],
    [100.0000, -100.0000, -2.0000],
    [-100.0000, 100.0000, -1.0000],
    [-100.0000, 100.0000, -2.0000],
    [-100.0000, -100.0000, -1.0000],
    [-100.0000, -100.0000, -2.0000],]

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
    [-0.5000, -0.5000, -1.000],]
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
world = [Object(faces_vector4, a1_vertices_vector3, edges_vector2, gray), 
         Object(faces_vector4, a2_vertices_vector3, edges_vector2, gray), 
         Object(faces_vector4, b1_vertices_vector3, edges_vector2, gray), 
         Object(faces_vector4, b2_vertices_vector3, edges_vector2, gray),
         Object(faces_vector4, c_vertices_vector3, edges_vector2, gray),
         Object(faces_vector4, d_vertices_vector3, edges_vector2, gray),
         Object(faces_vector4, e_vertices_vector3, edges_vector2, gray),
         Object(faces_vector4, f_vertices_vector3, edges_vector2, gray), 
         Object(faces_vector4, w1_vertices_vector3, edges_vector2, gray), 
         Object(faces_vector4, w2_vertices_vector3, edges_vector2, gray), 
         Object(faces_vector4, w3_vertices_vector3, edges_vector2, gray),
         Object(faces_vector4, wt_vertices_vector3, edges_vector2, gray),
         Object(faces_vector4, wb1_vertices_vector3, edges_vector2, gray),
         Object(faces_vector4, wb2_vertices_vector3, edges_vector2, gray),
         Object(faces_vector4, wr_vertices_vector3, edges_vector2, gray),
         Object(faces_vector4, wl1_vertices_vector3, edges_vector2, gray),
         Object(faces_vector4, wl2_vertices_vector3, edges_vector2, gray),
         Object(floor_faces_vector4, floor_vertices_vector3, floor_edges_vector2, brown),
]


def create_player(color, position, is_gl_cs=True):
    if is_gl_cs:
        position = LinAlg.convert_gl_to_object_cs(position)

    # [i] position - object cs
    players[color] = (Object(copy(player_template_faces_vector4), [np.add(vertex, position) for vertex in player_template_vertices_vector3], copy(player_template_edges_vector2), colors[color]))
