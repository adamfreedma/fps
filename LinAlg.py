from math import *
import numpy as np
import objects

PLAYER_RADIUS = 0.2

# [i] planes needs to be defined in a clockwise/counter-clockwise order (vertices with consequitive indexes must be adjacent)
# [i] right handed coordinate system (x-right, y-up, z-back)

def world_collision_detection(new_pos):
    collision = False
    for object in objects.world:
        if AABB_collison(new_pos, object):
            collision = True
            break
    return collision


def AABB_collison(new_pos, object):
    object = np.array([convert_object_to_gl_cs(vertex) for vertex in object.vertices])
    box = [[x - PLAYER_RADIUS for x in object.min(0)], [x + PLAYER_RADIUS for x in object.max(0)]]
    return box[0][0] < new_pos[0] < box[1][0] and box[0][1] < new_pos[1] < box[1][1] and box[0][2] < new_pos[2] < box[1][2]

def plane_normal(plane):
    """finds the normal of the plane

    Args:
        plane (list of 4 vertices(list of 3)): the 4 points of the plane

    Returns:
        list of 3: the normal to the vector
    """
    normal_vector = np.cross(np.subtract(plane[1], plane[0]), np.subtract(plane[2], plane[0]))
    return [-x for x in normalize(normal_vector)]


def norm(vector):
    """finds the norm(vector) of the vector

    Args:
        vector (list): input vector

    Returns:
        float: the norm of the vector
    """
    return sqrt(sum(x ** 2 for x in vector))


def normalize(vector):
    """finds the unit vector of the given vector

    Args:
        vector (list): input vector

    Returns:
        list: the unit vector
    """
    vector_norm = norm(vector)
    vector = [x / vector_norm for x in vector]
    return vector

def line_world_intersection(pos, vector):
    """checks the intersection of a bullet with the world

    Args:
        pos (list of 3 - gl cs): starting position of the shooter
        vector (list of 3 - gl cs): bullet direction vector

    Returns:
        float: distance from target
    """
    # [i] pos and vector in gl cs
    min_distance = np.Inf
    object_hit = None
    for obj in objects.players.values():
        # [i] obj in object cs
        for face in obj.faces:
            # [i] plane converted to gl cs
            plane = [convert_object_to_gl_cs(obj.vertices[index]) for index in face]
            intersection = line_plane_distance(plane, pos ,vector)
            if intersection > 0 and intersection < min_distance:
                min_distance = intersection
                object_hit = obj

    for obj in objects.world:
        # [i] obj in object cs
        for face in obj.faces:
            # [i] plane converted to gl cs
            plane = [convert_object_to_gl_cs(obj.vertices[index]) for index in face]
            intersection = line_plane_distance(plane, pos ,vector)
            if intersection > 0 and intersection < min_distance:
                min_distance = intersection
                object_hit = obj
    
    return object_hit


def line_plane_distance(plane, pos, vector):
    """returns  the factor needed for the vector to hit the plane(0-1 direct hit, 1- INF will eventually hit(bullet hit))

    Args:
        plane (list of 4 vertices(list of 3) - gl cs): the plane to find intersection
        pos (list of 3 - gl cs):  the starting pos of the vector
        vector (list of 3 - gl cs): the direction of the vector

    Returns:
        float: the factor needed for a hit (-1 if the vector is perpendicular to the plane or it hits outside the segment)
    """
    EPSILON = 1e-6
    distance = -1
    # finding the "slope" between the plane and vector (not actual slope)
    normal_vector = plane_normal(plane)
    slope = np.dot(vector, normal_vector)
    # check if they are  perdendicular
    if abs(slope) > EPSILON:
        # calculating the factor
        distance = np.dot(np.subtract(plane[0], pos), normal_vector) / slope
        # checking if the intersection is within the segment
        if not point_in_plane_section(plane, np.add(pos, np.multiply(vector, distance))):
            distance = -1

    return distance


def convert_object_to_gl_cs(vector):
    """converts a list in object cs to gl cs

    Args:
        vector (list of 3 - object cs): input vector in object cs

    Returns:
        list of 3 - gl cs: list in gl cs
    """
    return [-vector[1],vector[2],-vector[0]]


def convert_gl_to_object_cs(vector):
    """converts a list in gl cs to object cs

    Args:
        vector (list of 3 - gl cs): input vector in gl cs

    Returns:
        list of 3 - object cs: list in object cs
    """
    return [-vector[2],-vector[0],vector[1]]


def point_in_plane_section(plane, point):
    """checks if a point is within a rectangle region of a plane

    Args:
        plane (list of 4 vertices(list of 3) - gl cs): plane segment
        point (list of 3 - gl cs): given point

    Returns:
        bool: is the point within the segment
    """
    right = normalize(np.subtract(plane[3], plane[2]))
    left = normalize(np.subtract(plane[1], plane[0]))
    top = normalize(np.subtract(plane[2], plane[1]))
    bottom = normalize(np.subtract(plane[0], plane[3]))

    p3_to_point = normalize(np.subtract(point, plane[3]))
    p2_to_point = normalize(np.subtract(point, plane[2]))
    p1_to_point = normalize(np.subtract(point, plane[1]))
    p0_to_point = normalize(np.subtract(point, plane[0]))
    
    
    return 0 < acos(np.dot(p2_to_point, right)) < pi/2 and 0 < acos(np.dot(p0_to_point, left)) < pi/2  and 0 < acos(np.dot(p1_to_point, top)) < pi/2 and 0 < acos(np.dot(p3_to_point, bottom)) < pi/2


def rotate_yaw(vector, yaw, is_degrees=True):
    """rotates the vector around the y axis (left / right)

    Args:
        vector (list of 3 - gl cs): the target vector
        yaw (flaot): the amount to rotate
        is_degrees (bool, optional): is the yaw input in degrees. Defaults to True.

    Returns:
        list of 3: rotated vector - gl cs
    """
    # converting angle units
    if is_degrees:
        yaw = radians(yaw)
        
    yaw_rotation_matrix = [[cos(yaw), 0, sin(yaw)], [0, 1, 0], [-sin(yaw), 0, cos(yaw)]]
    return np.dot(vector, yaw_rotation_matrix)


def vector_from_yaw_pitch(yaw, pitch, size=1, is_degrees=True):
    """generates a vector from its yaw and its relative pitch

    Args:
        yaw (float): input yaw
        pitch (_type_): input pitch
        size (float, optional): the norm of the vector. Defaults to 1.
        is_degrees (bool, optional): is the input angles in degrees. Defaults to True.

    Returns:
        list of 3: the vector generated from the yaw and pitch - gl cs
    """
    if is_degrees:
        yaw = radians(yaw)
        pitch = radians(pitch)
    
    vector = [0, sin(pitch) * size, 0]
    vector[0] = -sin(yaw) * cos(pitch) * size
    vector[2] = cos(yaw) * cos(pitch) * size
    return vector


def main():
    # plane = [[-1,1,0], [1,1,0], [1,-1,0], [-1,-1,0]]
    # pos = [-.9, .9, 1]
    # vector = [0, 0.09, -1]
    # print("line plane intersection:", line_plane_distance(plane, pos, vector))
    vector = [1,2,3]
    vector = convert_gl_to_object_cs(vector)
    vector = convert_object_to_gl_cs(vector)
    print(vector)


if __name__ == '__main__':
    main()
