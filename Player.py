from lin_alg import vector_from_yaw_pitch
import numpy as np

class Player:

    def __init__(self, color, position = [0,0,0], yaw=0, pitch=0):
        self.color = color
        self.position = position # [i] gl cs
        self.yaw = yaw
        self.pitch = pitch


    def looking_vector(self) -> list:
        """generates the vector of the players looking direction

        Returns:
            list: the looking vector
        """
        return vector_from_yaw_pitch(self.yaw, self.pitch)
    

    def move_to(self, x=None, y=None, z=None) -> None:
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


    def move(self, speed) -> None:
        """moves the player (not relative to its yaw)

        Args:
            speed (list of 3): the vector to move
        """
        self.position = np.add(self.position, speed)


    def rotate(self, yaw=None, pitch=None) -> None:
        """adds the yaw/pitch

        Args:
            yaw (float, optional): yaw to add. Defaults to None.
            pitch (float, optional): pitch to add. Defaults to None.
        """
        if yaw:
            self.yaw += yaw
        if pitch:
            self.pitch += pitch

    def serialize(self) -> str:
        """serializes the player

        Returns:
            str: the serialized player
        """
        return serialize_field(self.position[0], 10) + serialize_field(self.position[1], 10) + serialize_field(self.position[2], 10)\
               + serialize_field(self.yaw, 10) + serialize_field(self.pitch, 10) + self.color


def deserialize_player(serialized) -> Player:
    """ deserializes a player

    Args:
        serialized (str): the serialized player

    Returns:
        Player: the player
    """
    length = 10
    try:
        return Player(serialized[5*length:], [float(serialized[:length]), float(serialized[length:2*length]), float(serialized[2*length:3*length])]
                  , float(serialized[3*length:4*length]), float(serialized[4*length:5*length]))
    except Exception as e:
        print(e)
        print("invlaid input!, player")

def deserialize_new_player(serialized) -> Player:
    """desirilizes the starting player from the server connection

    Args:
        serialized (str): the starting player serialized

    Returns:
        Player: starting player
    """
    try:
        length = 10
        return Player(serialized[3*length:], [float(serialized[:length]), float(serialized[length:2*length]), float(serialized[2*length:3*length])])
    except Exception as e:
        print(e)
        print("invalid input!, new player")

def serialize_field(field, length) -> str:
    """serializes a field

    Args:
        field (any): the value to serialize
        length (int): the wanted length for the field

    Returns:
        str: _description_
    """
    return str(field).zfill(length)[:length]
