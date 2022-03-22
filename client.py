import pygame
from pygame.locals import *
from LinAlg import *
from Player import Player
from connection import Connection
import meshRenderer
from OpenGL.GL import *
from OpenGL.GLU import *
import objects
from time import time
import numpy as np
from random import randint

# making a connection with the server
connection = Connection("127.0.0.1", 1729)
# initialzing pygame to use opengl
pygame.init()
display = (1000, 1000)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# enables depth testing (making sure closer object are in the front of the screen)
glEnable(GL_DEPTH_TEST)
# enables lighting
glEnable(GL_LIGHTING)
# initializes the light source
glEnable(GL_LIGHT0)
# sets color to be seen from both back and front
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
# glShadeModel(GL_SMOOTH) inital value
# adding light sources to the light 0 
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])
# setting up camera
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0] / display[1]), 0.1, 150.0)

# TODO: change camera and player initialazing to using server given position
glMatrixMode(GL_MODELVIEW)
# [i] object cs
gluLookAt(0, -1e-10, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()
# [i] setting up player - gl cs
player1 = Player("black", [1e-10, 0, 0], yaw=90)
# init mouse movement and center mouse on screen
screen_center = screen.get_size()[0] // 2, screen.get_size()[1] // 2 
mouse_change = [0, 0]
pygame.mouse.set_pos(screen_center)

paused = False
run = True

speed = [0, 0, 0]
# global vars
PLAYER_RADIUS = 0.2
SENSETIVITY = 0.1
GRAVITY = 5
# initialzing mouse settings
pygame.mouse.set_pos(screen_center)
# pygame.mouse.set_visible(False) - in comment until crosshair is implemented

# *moving to the starting position given by the server*
# init the view matrix
glPushMatrix()
glLoadIdentity()
# getting the starting position
init_player = connection.connect()
# calculating needed movement
starting_movement = np.subtract(init_player.position, player1.position)
# moving the view
glTranslatef(*starting_movement)
# moving the player
starting_movement = rotate_yaw(starting_movement, player1.yaw)
player1.move(starting_movement)
player1.color = init_player.color
# moves the matrix
glMultMatrixf(viewMatrix)
# store the new matrixc
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

# apply view matrix
glPopMatrix()
glMultMatrixf(viewMatrix)

SPEED = 0.1

shots = []

delta_time = 1
prev_time = time()

while run:
    delta_time = time() - prev_time 
    
    # *updating players*
    # [i] update data in gl cs
    update_data = connection.update_data(player1)
    if update_data:
        for c, player in update_data.items():
            if c == player1.color:
                player1 = player
            else:
                objects.create_player(c, player.position)

    # getting actions
    for event in pygame.event.get():
        # checking for quits/ pauses
        if event.type == pygame.QUIT:
            run = False          
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused
                pygame.mouse.set_pos(screen_center)
            if event.key == pygame.K_c:
                objects.create_player("green", [randint(-10, 10), randint(-10, 10), 0], False)
        if event.type == pygame.MOUSEBUTTONDOWN:
            connection.send_shot(player1.color)
            # [i] both in gl cs
            hit_pos = line_world_intersection(player1.position, player1.looking_vector())
            shots.append((player1.position, hit_pos))
        if not paused:
            # getting the mosue movement
            if event.type == pygame.MOUSEMOTION:
                mouse_change = [event.pos[i] - screen_center[i] for i in range(2)]
            pygame.mouse.set_pos(screen_center)

    if not paused:
        
        print(player1.looking_vector())
        
        # get key presses
        key_presses = pygame.key.get_pressed()

        # init model view matrix
        glLoadIdentity()
        
        # apply the look up and down
        player1.rotate(pitch=-mouse_change[1] * SENSETIVITY)
        glRotatef(-player1.pitch, 1.0, 0.0, 0.0)
        
        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # saving up/down movement as it dosent reset every frame
        speed = [0, speed[1], 0]
        # calculate speed
        if key_presses[pygame.K_w]:
            speed[2] += SPEED * delta_time
        if key_presses[pygame.K_s]:
            speed[2] -= SPEED * delta_time
        if key_presses[pygame.K_d]:
            speed[0] -= SPEED * delta_time
        if key_presses[pygame.K_a]:
            speed[0] += SPEED * delta_time
        
        
        hit_wall = world_collision_detection(np.subtract(player1.position, rotate_yaw(speed,  player1.yaw + mouse_change[0] * SENSETIVITY)))
        if not hit_wall:
            # * apply the movement *
            glTranslatef(*speed)
        
        # apply the left and right rotation
        player1.rotate(yaw=mouse_change[0] * SENSETIVITY)
        glRotatef(mouse_change[0] * SENSETIVITY, 0.0, 1.0, 0.0)
        
        if not hit_wall:    
            # updating player position
            speed = rotate_yaw(speed, player1.yaw)
            player1.move(speed)

        # ! delete later
        # objects.world[0].move([0.1, 0 ,0])

        # moves the matrix
        glMultMatrixf(viewMatrix)
        # store the new matrixc
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
 
        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)
        # reapply light
        glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])
        # clearing the buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # adding game elements
        glPushMatrix()

        meshRenderer.mesh_all(player1.looking_vector())
        
        for shot in shots:
            meshRenderer.draw_line(np.add(convert_gl_to_object_cs(shot[0]), rotate_yaw([0,1,0], player1.yaw - 60)), convert_gl_to_object_cs(shot[1]), (1, 1, 1))
        shots = []

        pygame.display.flip()
        glPopMatrix()


pygame.quit()
