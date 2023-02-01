# coding=utf-8
"""Textures and transformations in 2D"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys, os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica.gpu_shape import GPUShape, SIZE_IN_BYTES
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
from PIL import Image
import random 

__author__ = "Daniel Calderon"
__license__ = "MIT"


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.leftClickOn = False
        self.theta = 0.0
        self.mousePos = (0.0, 0.0)
        self.actual_sprite = 1
        self.x = 0.0
def cursor_pos_callback(window, x, y):
    global controller
    controller.mousePos = (x,y)


###################################################################################################
        # Agregamos dos nuevas variables a nuestro controlador
        
###################################################################################################


# global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

#############################################################################################
    # Agregamos dos nuevas teclas para interactuar
    elif key == glfw.KEY_RIGHT:
        controller.x += 0.05
        controller.actual_sprite = (controller.actual_sprite + 1)%10
    
    elif key == glfw.KEY_LEFT:
        controller.x -= 0.05
        controller.actual_sprite = (controller.actual_sprite - 1)%10
#############################################################################################

    else:
        print('Unknown key')


if __name__ == "__main__":
    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Ejercicio 4 Tomas Rivas", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.SimpleTextureTransformShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

######################################################################################################
   
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    spritesDirectory = os.path.join(thisFolderPath, "Sprites")
    spritePath = os.path.join(spritesDirectory, "FONDO.png")

    texture1 = es.textureSimpleSetup(
        spritePath, GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    spritesDirectory = os.path.join(thisFolderPath, "Sprites")
    spritePath = os.path.join(spritesDirectory, "LLUVIA.png")

    texture2 = es.textureSimpleSetup(
        spritePath, GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)


#######################################################################################################
    
    # Creating shapes on GPU memory

    # Creamos una lista para guardar todas las gpu shapes necesarias
    gpus = []
    gpus1 = []
    gpus2 = []
    # Definimos donde se encuentra la textura
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    spritesDirectory = os.path.join(thisFolderPath, "Sprites")
    spritePath = os.path.join(spritesDirectory, "sprites.png")

    texture = es.textureSimpleSetup(
            spritePath, GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    # Creamos una gpushape por cada frame de textura
    for i in range(10):
        gpuKnight = GPUShape().initBuffers()
        pipeline.setupVAO(gpuKnight)

        shapeKnight = bs.createTextureQuad(i/10,(i + 1)/10,0,1)

        gpuKnight.texture = texture

        gpuKnight.fillBuffers(shapeKnight.vertices, shapeKnight.indices, GL_STATIC_DRAW)

        gpus.append(gpuKnight)

    for i in range(10):
        gpufon = GPUShape().initBuffers()
        pipeline.setupVAO(gpufon)

        shapefon = bs.createTextureQuad(i/10-0.24,((i + 1)/10)+0.24,0,1)

        gpufon.texture = texture1

        gpufon.fillBuffers(shapefon.vertices, shapefon.indices, GL_STATIC_DRAW)

        gpus1.append(gpufon)
    for i in range(10):
        gpullu = GPUShape().initBuffers()
        pipeline.setupVAO(gpullu)

        shapellu = bs.createTextureQuad(-1+i*0.2,1+i*0.2,-1,1+i*0.2)

        gpullu.texture = texture2

        gpullu.fillBuffers(shapellu.vertices, shapellu.indices, GL_STATIC_DRAW)

        gpus2.append(gpullu)

#######################################################################################################    

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing the shapes
        theta = glfw.get_time()
##############################################################################################################################

        # Le entregamos al vertex shader la matriz de transformación
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.uniformScale(2)
        ]))

        pipeline.drawCall(gpus1[controller.actual_sprite])

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(-0.2, -0.65, 0),
            tr.uniformScale(0.5)
        ]))

        # Dibujamos la figura
        pipeline.drawCall(gpus[controller.actual_sprite])
        mousePosX = 2 * (controller.mousePos[0] - width/2) / width
        mousePosY = 2 * (height/2 - controller.mousePos[1]) / height
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(mousePosX, mousePosY, 0),
            tr.uniformScale(2)
        ]))

        # Dibujamos la figura
        pipeline.drawCall(gpus2[int((theta*10)%10)])
##############################################################################################################################

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuKnight.clear()

    glfw.terminate()
