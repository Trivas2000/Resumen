"""P5) [Efectos con Shaders] Realice un par de shaders, donde el primero solo dibuje los píxeles con un tono verde
 y el segundo represente un modo atardecer. Además agregue la funcionalidad de que se puedan alternar entre los shaders
apretando teclas. Con [Q] activa el primer efecto, y con [W] activa el segundo ejemplo"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from gpu_shape import GPUShape, SIZE_IN_BYTES

# A class to store the application control
class Controller:
    fillPolygon = True
    effect1 = False
    effect2 = False


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

    elif key == glfw.KEY_A:
        controller.effect1 = not controller.effect1

    elif key == glfw.KEY_B:
        controller.effect2 = not controller.effect2

    else:
        print('Unknown key')
    
# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices

class SimpleShaderProgram:

    def __init__(self):

        vertex_shader = """
            #version 130

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                gl_Position = vec4(position, 1.0f);
                newColor = color;
            }
            """

        fragment_shader = """
            #version 130
            in vec3 newColor;

            out vec4 outColor;
            void main()
            {
                outColor = vec4(newColor, 1.0f);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color specification => 3*4 + 3*4 = 24 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

class GreenShaderProgram:

    def __init__(self):

        vertex_shader = """
            #version 130

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                gl_Position = vec4(position, 1.0f);
                newColor = color;
            }
            """

        fragment_shader = """
            #version 130
            in vec3 newColor;

            out vec4 outColor;
            void main()
            {
                vec3 finalColor = newColor;
                if (newColor.g == 1 && newColor.b ==1 )
                {
                    finalColor = vec3(newColor.r*1, 0, newColor.b*1);
                }
                if (newColor.g > 0.39 || newColor.b <0.6 )
                {
                    finalColor = vec3(newColor.r, 0, newColor.b);
                }
                outColor = vec4(finalColor, 1.0f);
                if (newColor.g ==1 && newColor.b <0.6 )
                {
                    finalColor = vec3(0,0,0);
                }
                outColor = vec4(finalColor, 1.0f);
                if (newColor.r ==1 && newColor.g==1 )
                {
                    finalColor = vec3(1,1,1);
                }
                outColor = vec4(finalColor, 1.0f);
                
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color specification => 3*4 + 3*4 = 24 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

class SunsetShaderProgram:

    def __init__(self):

        vertex_shader = """
            #version 130

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                
                newColor = color;
                if ((newColor.r ==1 && newColor.g==1)||(newColor.r ==0 && newColor.g==0&&newColor.b>0.5) )
                {
                   vec3 posfinal = vec3(position[0]-0.5,position[1],position[2]);
                gl_Position = vec4(posfinal, 1.0f);
                }
                else
                {
                   vec3 posfinal = vec3(position[0],position[1],position[2]);
                gl_Position = vec4(posfinal, 1.0f);
                }
                
            }
            """

        fragment_shader = """
            #version 130
            in vec3 newColor;

            out vec4 outColor;
            void main()
            {   
                vec3 finalColor = vec3((newColor.r) , newColor.g , newColor.b);
                outColor = vec4(finalColor, 1.0f);
            }
            """

        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    def setupVAO(self, gpuShape):

        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        # 3d vertices + rgb color specification => 3*4 + 3*4 = 24 bytes
        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        # Unbinding current vao
        glBindVertexArray(0)


    def drawCall(self, gpuShape, mode=GL_TRIANGLES):
        assert isinstance(gpuShape, GPUShape)

        # Binding the VAO and executing the draw call
        glBindVertexArray(gpuShape.vao)
        glDrawElements(mode, gpuShape.size, GL_UNSIGNED_INT, None)

        # Unbind the current VAO
        glBindVertexArray(0)

def create_sky(y0, y1):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -1.0, y0, 0.0,  0.0, 1.0, 1.0,
         1.0, y0, 0.0,  0.0, 1.0, 1.0,
         1.0, y1, 0.0,  0.8, 1.0, 1.0,
        -1.0, y1, 0.0,  0.8, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)

def create_land(y0, y1):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
        -1.0, y0, 0.0,  0.0, 1, 0.5,
         1.0, y0, 0.0,  0.0, 1, 0.5,
         1.0, y1, 0.0,  0.2, 0.4, 0,
        -1.0, y1, 0.0,  0.2, 0.4, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                2, 3, 0]

    return Shape(vertices, indices)

def create_sun():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions                           colors
       0.4,0.9,0,1,1,0,
       0.6,0.9,0,1,1,0,
       0.6,0.7,0,1,1,0,
       0.4,0.7,0,1,1,0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices =  [0, 1, 3,
                1, 3, 2
                ]

    return Shape(vertices, indices)
def create_rio():

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions                           colors
    0.2,0,0,0,0,1,
    0.4,0,0,0,0,1,
    0.2,-0.5,0,0,0,1,
    0.4,-0.5,0,0,0,1,
    0.5,-0.5,0,0,0,1,
    0.3,-1,0,0,0,0.6,
    0.5,-1,0,0,0,0.6,
    0.3,-0.5,0,0,0,1,
    0.4,-0.4,0,0,0,1,
    0.3,-0.6,0,0,0,1
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices =  [0,1,2,
                1,2,3,
                7,4,5,
                4,5,6,
                2,9,7,
                3,8,4
                ]

    return Shape(vertices, indices)

def create_mont(x0, y0, width, height):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions        colors
         x0, y0, 0.0,  0.3, 0.15, 0.1,
         x0 + width*0.8, y0, 0.0,  0.3, 0.15, 0.1,
         x0 + width*0.4, y0 + height, 0.0,  0.6, 0.31, 0.17,
         x0+width*1.6, y0, 0.0,  0.3, 0.15, 0.1,
         x0 + width*1.2, y0 + height, 0.0,  0.6, 0.31, 0.17,
         x0+width*2.4, y0, 0.0,  0.3, 0.15, 0.1,
         x0 + width*2, y0 + height, 0.0,  0.6, 0.31, 0.17,
         x0+width*3.2, y0, 0.0,  0.3, 0.15, 0.1,
         x0 + width*2.8, y0 + height, 0.0,  0.6, 0.31, 0.17]


    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2,
                1, 4, 3,
                3,6,5,
                5,7,8 ]

    return Shape(vertices, indices)

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800

    window = glfw.create_window(width, height, "P5: Efectos con shaders", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    # Creating our shader program and telling OpenGL to use it
    simplePipeline = SimpleShaderProgram()
    greenPipeline = GreenShaderProgram()
    sunsetPipeline = SunsetShaderProgram()

    # Creating shapes on GPU memory
    sky_shape = create_sky(y0=0, y1=1.0)
    gpu_sky = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_sky)
    greenPipeline.setupVAO(gpu_sky)
    sunsetPipeline.setupVAO(gpu_sky)
    gpu_sky.fillBuffers(sky_shape.vertices, sky_shape.indices, GL_STATIC_DRAW)

    land_shape = create_land(y0=0, y1=-1)
    gpu_land = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_land)
    greenPipeline.setupVAO(gpu_land)
    sunsetPipeline.setupVAO(gpu_land)
    gpu_land.fillBuffers(land_shape.vertices, land_shape.indices, GL_STATIC_DRAW)

    sun_shape = create_sun()
    gpu_sun = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_sun)
    greenPipeline.setupVAO(gpu_sun)
    sunsetPipeline.setupVAO(gpu_sun)
    gpu_sun.fillBuffers(sun_shape.vertices, sun_shape.indices, GL_STATIC_DRAW)

    mont1_shape = create_mont(x0=-1, y0=0, width=0.6, height=0.4)
    gpu_mont1 = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_mont1)
    greenPipeline.setupVAO(gpu_mont1)
    sunsetPipeline.setupVAO(gpu_mont1)
    gpu_mont1.fillBuffers(mont1_shape.vertices, mont1_shape.indices, GL_STATIC_DRAW)
    
    rio_shape = create_rio()
    gpu_rio = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_rio)
    greenPipeline.setupVAO(gpu_rio)
    sunsetPipeline.setupVAO(gpu_rio)
    gpu_rio.fillBuffers(rio_shape.vertices, rio_shape.indices, GL_STATIC_DRAW)
    # Setting up the clear screen color
    glClearColor(0.2, 0.2, 0.2, 1.0)

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

        if (controller.effect1):
            glUseProgram(greenPipeline.shaderProgram)
            greenPipeline.drawCall(gpu_sky)
            greenPipeline.drawCall(gpu_land)
            greenPipeline.drawCall(gpu_sun)
            greenPipeline.drawCall(gpu_rio)
            greenPipeline.drawCall(gpu_mont1)
        elif (controller.effect2):
            glUseProgram(sunsetPipeline.shaderProgram)
            sunsetPipeline.drawCall(gpu_sky)
            sunsetPipeline.drawCall(gpu_land)
            greenPipeline.drawCall(gpu_sun)
            greenPipeline.drawCall(gpu_rio)
            sunsetPipeline.drawCall(gpu_mont1)
        else:
            glUseProgram(simplePipeline.shaderProgram)
            simplePipeline.drawCall(gpu_sky)
            simplePipeline.drawCall(gpu_land)
            greenPipeline.drawCall(gpu_sun)
            greenPipeline.drawCall(gpu_rio)
            simplePipeline.drawCall(gpu_mont1)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpu_sky.clear()
    glfw.terminate()