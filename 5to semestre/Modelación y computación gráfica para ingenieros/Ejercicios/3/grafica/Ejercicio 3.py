# coding=utf-8
"""Drawing 4 shapes with different transformations"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr
import math
__author__ = "Daniel Calderon"
__license__ = "MIT"
glfw.init()


# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    else:
        print('Unknown key')


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Displaying multiple shapes - Modern OpenGL", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)
    class Shape:
        def __init__(self, vertices, indices, textureFileName=None):
            self.vertices = vertices
            self.indices = indices
            self.textureFileName = textureFileName

    def createContorno(RA,R,G,B):

        vertices = []
        indices = []

        dtheta = 2 * math.pi / 200

        for i in range(0,200):
            theta = i * dtheta
            if i==199:
                vertices += [
                RA * math.cos(theta), RA * math.sin(theta), 0,
                    R,G,B]

                indices += [0,i]
            else:
                vertices += [
                    RA* math.cos(theta), RA * math.sin(theta), 0,
                        R,G,B]

                indices += [i, i+1]
    

    # The final triangle connects back to the second vertex
        

        return Shape(vertices, indices)
    def Orbitas(RA,R1,G1,B1,R2,G2,B2):

        vertices = []
        indices = []

        dtheta = 2 * math.pi / 200

        for i in range(0,200):
            theta = i * dtheta
            if i==199:
                vertices += [
                RA * math.cos(theta), RA * math.sin(theta), 0,
                    R2,G2,B2]

                indices += [0,i]
            else:
                if i%10>5:
                
                    vertices += [
                    RA* math.cos(theta), RA * math.sin(theta), 0,
                        R1,G1,B1]    
                else:       
                    vertices += [
                    RA* math.cos(theta), RA * math.sin(theta), 0,
                        R2,G2,B2]
                indices += [i, i+1]
        return Shape(vertices, indices)
    # Creating shapes on GPU memory
    shapeSol = bs.createCircle(40,1,1,0)
    gpuSol = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSol)
    gpuSol.fillBuffers(shapeSol.vertices, shapeSol.indices, GL_STATIC_DRAW)

    shapeTierra = bs.createCircle(40,0,0,1)
    gpuTierra = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTierra)
    gpuTierra.fillBuffers(shapeTierra.vertices, shapeTierra.indices, GL_STATIC_DRAW)

    shapeLuna = bs.createCircle(40,0.8,0.8,0.8)
    gpuLuna = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuLuna)
    gpuLuna.fillBuffers(shapeLuna.vertices, shapeLuna.indices, GL_STATIC_DRAW)

    shapeCont1 = createContorno(0.29,1,1,0)
    gpuCont1= es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCont1)
    gpuCont1.fillBuffers(shapeCont1.vertices, shapeCont1.indices, GL_STATIC_DRAW)

    shapeCont2 = createContorno(0.17,0,0,1)
    gpuCont2= es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCont2)
    gpuCont2.fillBuffers(shapeCont2.vertices, shapeCont2.indices, GL_STATIC_DRAW)

    shapeOrb = Orbitas(0.7,1,1,1,0,0,0)
    gpuOrb= es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuOrb)
    gpuOrb.fillBuffers(shapeOrb.vertices, shapeOrb.indices, GL_STATIC_DRAW)

    shapeOrb2 = Orbitas(0.3,1,1,1,0,0,0)
    gpuOrb2= es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuOrb2)
    gpuOrb2.fillBuffers(shapeOrb2.vertices, shapeOrb2.indices, GL_STATIC_DRAW)
    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Using the time as the theta parameter
        theta = glfw.get_time()

        # Sol
        triangleTransform = tr.matmul([
            tr.translate(0, 0, 0),
            tr.uniformScale(0.55)
        ])

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform)

        pipeline.drawCall(gpuSol)

        # Tierra
        triangleTransform2 = tr.matmul([
            tr.translate(0, 0, 0),
            tr.translate(np.cos(theta)*0.7, np.sin(theta)*0.7, 0),
            tr.uniformScale(0.3)
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, triangleTransform2)
        pipeline.drawCall(gpuTierra)

        # Luna
        quadTransform = tr.matmul([
         tr.translate(0,0,0),   
         tr.translate(np.cos(theta)*0.7+np.cos(2*theta)*0.3, np.sin(theta)*0.7+np.sin(2*theta)*0.3, 0),  
            tr.uniformScale(0.15)
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, quadTransform)
        pipeline.drawCall(gpuLuna)

        #Orbitas
        quadTransform = tr.matmul([
         tr.translate(0,0,0),
            
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, quadTransform)
        pipeline.drawCall(gpuCont1,GL_LINES)
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
    
        quadTransform = tr.matmul([
         tr.translate(0,0,0),
         tr.translate(np.cos(theta)*0.7, np.sin(theta)*0.7, 0)     
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, quadTransform)
        pipeline.drawCall(gpuCont2,GL_LINES)

        quadTransform = tr.matmul([
         tr.translate(0,0,0),
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, quadTransform)
        pipeline.drawCall(gpuOrb,GL_LINES)

        quadTransform = tr.matmul([
         tr.translate(0,0,0),
         tr.translate(np.cos(theta)*0.7, np.sin(theta)*0.7, 0),
        ])
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, quadTransform)
        pipeline.drawCall(gpuOrb2,GL_LINES)
        glfw.swap_buffers(window)

        



    # freeing GPU memory
    gpuQuad.clear()
    
    glfw.terminate()