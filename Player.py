from LinAlg import vector_from_yaw_pitch
import numpy as np

class Player:

    def __init__(self, color, position = [0,0,0], yaw=0, pitch=0):
        self.color = color
        self.position = position # [i] gl cs
        self.yaw = yaw
        self.pitch = pitch


    def looking_vector(self):
        return vector_from_yaw_pitch(self.yaw, self.pitch)
    

    def move_to(self, x=None, y=None, z=None):
        """moves the Player

        Args:
            x (float, optional): x position to move to (postivie - right). Defaults to None.
            y (float, optional): y position to move to (positive - up). Defaults to None.
            z (float optional): z position to move to (positive - back). Defaults to None.
        """
        if x:
            self.position[0] = x
        if y:
            self.position[1] = y
        if z:
            self.position[2] = z


    def move(self, speed):
        self.position = np.add(self.position, speed)


    def rotate(self, yaw=None, pitch=None):
        if yaw:
            self.yaw += yaw
        if pitch:
            self.pitch += pitch

    def serialize(self):
        return serialize_var(self.position[0], 10) + serialize_var(self.position[1], 10) + serialize_var(self.position[2], 10)\
               + serialize_var(self.yaw, 10) + serialize_var(self.pitch, 10) + self.color


def deserialize_player(serialized):
    length = 10
    try:
        return Player(serialized[5*length:], [float(serialized[:length]), float(serialized[length:2*length]), float(serialized[2*length:3*length])]
                  , serialized[3*length:4*length], serialized[4*length:5*length])
    except Exception as e:
        print(e)
        print("invlaid input!, player")

def deserialize_new_player(serialized):
    try:
        length = 10
        return Player(serialized[3*length:], [float(serialized[:length]), float(serialized[length:2*length]), float(serialized[2*length:3*length])])
    except Exception as e:
        print(e)
        print("invalid input!, new player")

def serialize_var(var, length):
    return str(var).zfill(length)[:length]
