from ast import walk
from tracemalloc import stop
from turtle import Screen
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
from text import Text


def game() -> None:
    """main loop
    """
    # making a connection with the server
    connection = Connection("127.0.0.1", 1729)
    # initialzing pygame to use opengl
    pygame.init()
    display = (1280, 960)
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

    glMatrixMode(GL_MODELVIEW)
    # [i] object cs
    gluLookAt(0, -1e-10, 0, 0, 0, 0, 0, 0, 1)
    view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()
    # [i] setting up player - gl cs
    player1 = Player("black", [1e-10, 0, 0], yaw=90)
    # init mouse movement and center mouse on screen
    screen_center = screen.get_size()[0] // 2, screen.get_size()[1] // 2
    mouse_change = [0, 0]
    pygame.mouse.set_pos(screen_center)

    paused = False
    run = True
    game_done = False

    velocity = [0, 0, 0]
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
    glMultMatrixf(view_matrix)
    # store the new matrixc
    view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    # apply view matrix
    glPopMatrix()
    glMultMatrixf(view_matrix)

    # global vars
    sensitivity = 0.1
    speed = 10

    shots = []

    prev_time = time()

    update_data = []

    walk_sound = pygame.mixer.Sound("steps.wav")

    while run and not game_done:
        delta_time = time() - prev_time
        prev_time = time()

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                connection.send_shot(player1.color)
                # [i] both in gl cs
                hit_pos = line_world_intersection(player1.position, player1.looking_vector())
                shots.append((player1.position, hit_pos))
                
                pygame.mixer.music.load("shot.wav")
                pygame.mixer.music.play(0)
                
            if not paused:
                # getting the mosue movement
                if event.type == pygame.MOUSEMOTION:
                    mouse_change = [event.pos[i] - screen_center[i] for i in range(2)]
                pygame.mouse.set_pos(screen_center)

        if not paused:
            # get key presses
            key_presses = pygame.key.get_pressed()

            # init model view matrix
            glLoadIdentity()

            # apply the look up and down
            player1.rotate(pitch=-mouse_change[1] * sensitivity)
            glRotatef(-player1.pitch, 1.0, 0.0, 0.0)

            # init the view matrix
            glPushMatrix()
            glLoadIdentity()

            # saving up/down movement as it dosen't reset every frame
            velocity = [0, velocity[1], 0]
            # calculate speed
            if key_presses[pygame.K_w]:
                velocity[2] += speed * delta_time
            if key_presses[pygame.K_s]:
                velocity[2] -= speed * delta_time
            if key_presses[pygame.K_d]:
                velocity[0] -= speed * delta_time
            if key_presses[pygame.K_a]:
                velocity[0] += speed * delta_time

            # *updating players*
            # [i] update data in gl cs
            objects.players = {}
            game_done, update_data = connection.update_data(player1)
            if update_data and not game_done:
                for c, player in update_data.items():
                    if c == player1.color:
                        movement = np.subtract(player.position, player1.position)
                        player1.move(movement)
                        movement = rotate_yaw(movement, -player1.yaw)
                        glTranslatef(*movement)
                    else:
                        objects.create_player(c, player.position)

            # *checking for wall hits*
            hit_wall = world_collision_detection(np.add(player1.position, rotate_yaw(
                velocity,  player1.yaw + mouse_change[0] * sensitivity)))
            if not hit_wall:
                # * apply the movement *
                glTranslatef(*velocity)

            if norm(velocity) > 0 and not hit_wall:
                pygame.mixer.Sound.play(walk_sound)
            else:
                pygame.mixer.Sound.stop(walk_sound)

            # apply the left and right rotation
            player1.rotate(yaw=mouse_change[0] * sensitivity)
            glRotatef(mouse_change[0] * sensitivity, 0.0, 1.0, 0.0)

            if not hit_wall:
                # updating player position
                velocity = rotate_yaw(velocity, player1.yaw)
                player1.move(velocity)

            # moves the matrix
            glMultMatrixf(view_matrix)
            # store the new matrix
            view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            # apply view matrix
            glPopMatrix()
            glMultMatrixf(view_matrix)
            # reapply light
            glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])
            # clearing the buffer
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # adding game elements
            glPushMatrix()

            meshRenderer.mesh_all(player1.looking_vector())
            # drawing shots
            for shot in shots:
                meshRenderer.draw_line(np.add(convert_gl_to_object_cs(shot[0]), convert_gl_to_object_cs(
                    rotate_yaw([-1, 0, 0], player1.yaw + 60))), convert_gl_to_object_cs(shot[1]), (1, 1, 0))
            shots = []
            # updating screen
            pygame.display.flip()
            glPopMatrix()
    
    pygame.quit()

    if game_done:
        display_results(update_data, player1.color)


def display_results(results, you_color) -> None:
    """makes a screen to display the results

    Args:
        results (dictionary of color -> points): the result of the games
        you_color (string): the color of the player
    """
    screen = pygame.display.set_mode([1280, 960])

    x = 1280 // 2
    y = 100
    for player, points in results.items():
        # replacing the color of the client with "you" to indicate its him
        if player == you_color:
            txt = "you" + ": " + points
        else:
            txt = player + ": " + points
        # displaying the text
        text = Text(txt, (x, y), [255 * player_color for player_color in objects.colors[player]])
        text.write(screen)
        # going down a line
        y += 100
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == QUIT or event.type == KEYDOWN:
            break


def instructions(screen: pygame.display) -> None:
    """displays instructions on screen

    Args:
        screen (pygame.display): the screen of the game
    """
    instructions_screen = pygame.image.load("instructions.png").convert_alpha()
    screen.blit(instructions_screen, (0, 0))
    pygame.display.flip()
    # exit when esc is pressed
    in_instructions = True
    while in_instructions:
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and 115 < mouse_pos[0] < 360 and 60 < mouse_pos[1] < 120:
            in_instructions = False
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                in_instructions = False
    start_screen = pygame.image.load("screen.png").convert_alpha()
    screen.blit(start_screen, (0, 0))
    pygame.display.flip()


def main() -> None:
    """main loop
    """
    screen = pygame.display.set_mode([1280, 960])
    start_screen = pygame.image.load("screen.png").convert_alpha()
    screen.blit(start_screen, (0, 0))
    pygame.display.flip()
    ready_to_play = False
    while not ready_to_play:
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if 560 < mouse_pos[0] < 720 and 390 < mouse_pos[1] < 440:
                ready_to_play = True
            if 430 < mouse_pos[0] < 830 and 550 < mouse_pos[1] < 600:
                instructions(screen)
            if pygame.mouse.get_pressed()[0] and 580 < mouse_pos[0] < 715 and 710 < mouse_pos[1] < 770:
                exit()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                exit()
    pygame.quit()
    game()
    main()


if __name__ == '__main__':
    main()
