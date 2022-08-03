# Online first person shooter

online multiplayer game made in python using sockets for networking, pygame and opengl for 3D rendering.

---
### To play the project:

#### _needed files_:

| File  | server | client |
| ------|:------:|:------:|
|LinAlg.py|&#9745;|&#9745;|
|Player.py|&#9745;|&#9745;|
|objects.py|&#9745;|&#9745;|
|client.py||&#9745;|
|connection.py||&#9745;|
|meshRenderer.py||&#9745;|
|server.py| &#9745;|        |
|server_objects.py|&#9745;|        |
|text.py||&#9745;|
|Rainshow.otf||&#9745;|
|instructions.PNG||&#9745;|
|screen.png||&#9745;|
|shot.wav||&#9745;|
|steps.wav||&#9745;|
|box_gen.py||        |

box_gen.py is just a script to easily generate axis-aligned boxes in the
format of the code, it is not a part of the game files.

**To connect to the server on all clients change the ip in "client.py", row 23:**
```
connection = Connection("127.0.0.1", 1729)
````
Change 127.0.0.1 to the ip of the server.

You will also need to install pygame, pyopencv, and numpy libraries.

---
