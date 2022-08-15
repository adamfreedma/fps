# Online first person shooter

online multiplayer game made in python using sockets for networking, pygame and opengl for 3D rendering.

---
### To play the project:

Clone the respository and keep the server directory on the server, and client directories on the clients.

box_gen.py is just a script to easily generate axis-aligned boxes in the
format of the code, it is not a part of the game files.

**To connect to the server change on all clients the ip in "client.py", row 23:**
```
connection = Connection("127.0.0.1", 1729)
````
Change 127.0.0.1 to the ip of the server.

## Requirements:
You will need to install pygame, pyopengl, and numpy.

you could install them using pip:
```
pip install pygame
pip install pyopengl
pip install numpy
````

---
