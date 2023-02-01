
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from gpu_shape import GPUShape, SIZE_IN_BYTES
import transformations as tr
import basic_shapes as bs

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
    
    #Agregare 2 funciones adicionales asociadas a las teclas “A” Y “B” por lo que las agregamos al controlador:
    elif key == glfw.KEY_A:
        controller.effect1 = not controller.effect1

    elif key == glfw.KEY_B:
        controller.effect2 = not controller.effect2

    else:
        print('Unknown key')
    
class Shape:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices

    #En el simple shader agregue la multiplicación por la matriz transform a las posiciones.
class SimpleShaderProgram:

    def __init__(self):

        vertex_shader = """
            #version 130
            uniform mat4 transform;

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                gl_Position = transform * vec4(position, 1.0f);
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

#Aquí genero un segundo shader cuyo objetivo será que cuando apretemos la tecla “B” nos cambie 
# los colores a una temática de playa, es por eso que le e puesto beach como nombre. 
# Esto se hace con condiciones en los colores, en particular un cambio de que cuando sea negro 
# lo cambiemos por un color arena, y cuando sea una tonalidad de azul o rojo lo cambiemos por verde o rosado.

class BeachProgram:

    def __init__(self):

        vertex_shader = """
            #version 130
            uniform mat4 transform;

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                gl_Position = transform * vec4(position, 1.0f);
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
                if (newColor.r >0.01 && newColor.g <0.9 && newColor.b <0.9 )
                {
                    finalColor = vec3(0.2,1,0.2);
                }
                if (newColor.r == 0 && newColor.g == 0 && newColor.b ==0 )
                {
                    finalColor = vec3(1, 0.9,0.6);
                }
                outColor = vec4(finalColor, 1.0f);
                if (newColor.b >0.01 && newColor.g <0.9 && newColor.r <0.9 )
                {
                    finalColor = vec3(1,0.2,1);
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

#Para crear una dama aprovechamos la función createCircle de basic shapes y le 
# ponemos un N=600 pero dejamos los colores como parámetros para que sea sencillo generar damas de diferentes colores.
#(Siempre partirán en las coordenadas 0,0,0 pero con traslaciones las guiare hacia las posiciones necesarias.)

def create_dama(R,G,B):
    return bs.createCircle(600,R,G,B)

#La función para crear el tablero será un poco más compleja así que complementare con comentarios dentro de la función para explicar su funcionamiento. 
# En el principio partiré definiendo 4 vértices blancos en las esquinas para así generar con 2 triángulos un cuadrado blanco gigante que cubra todo.

def create_tablero():
    vertices = [
    #   positions        colors
        -1, 1, 0,       1, 1, 1,  #Vertice blanco esquina superior izquierda
         1, 1, 0,       1, 1, 1,   #Vertice blanco esquina superior derecha
        -1,-1, 0,       1, 1, 1,   #Vertice blanco esquina inferior izquierda
        1, -1, 0,       1, 1, 1]  #Vertice blanco esquina inferior derecha 

    #Esta lista de separadores representa las coordenadas donde quiero poner un vértice calculadas manualmente. 
    # Como las coordenadas que necesitamos son iguales en x e y esta lista vale para ambos y con un doble for que appende los índices, automatizamos el proceso.
         
    separadores=[-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1]
    for y in separadores:
        for x in separadores:
            vertices.append(x)
            vertices.append(y)
            vertices.append(0) #La La coordenada z es siempre 0
            vertices.append(0) #Los valores R,G y B serán siempre 0 ya que queremos crear vértices negros para los cuadrados restantes.
            vertices.append(0)
            vertices.append(0)

    indices = [0, 1, 2,
               1, 2, 3] #Estos índices iniciales generan el fondo blanco

    #Ahora creare 2 listas unas con los índices pares que tiene que tener la primera fila y otra con 
    # los impares que tiene que tener la segunda para generar todos los cuadrados negros. 
    # La idea es después iterar estas listas ya que si le sumamos 18 al vértice tenemos el que 
    # está 2 espacios hacia abajo y así poder generar todo el tablero. Tenemos que hacerlo 4 veces cada una para completar 
    # las 8 filas y para la primera tenemos que sumarle 0, la siguiente 18, después 36 y etc… Por lo que multiplicamos 18 por el 
    # índice de la fila que queremos más el valor inicial.     
          
    Pares=[5,14,15,
            5,6,15,
            7,8,17,
            16,17,7,
            9,10,19,
            18,19,9,
            11,12,21,
            11,21,20]
    impares=[22,23,13,
            13,14,23,
            24,25,15,
            15,16,25,
            17,27,26,
            17,18,27,
            19,20,29,
            19,29,28,]
    for x in [0,1,2,3]:
        for y in Pares:
            indices.append(y+18*x)             
    for x in [0,1,2,3]:
        for y in impares:
            indices.append(y+18*x)             

    return Shape(vertices, indices) #Finalmente retornamos la figura con sus vértices e índices.

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800

    window = glfw.create_window(width, height, "Tarea 1 Tomás Rivas", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    # Creamos los shader program
    simplePipeline = SimpleShaderProgram()
    beachPipeline = BeachProgram()

    # Creamos los objetos en la memoria GPU

    damaR_shape = create_dama(1,0,0) #Usamos  1,0,0 para que sea una dama roja
    gpu_damaR= GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_damaR)
    beachPipeline.setupVAO(gpu_damaR)
    gpu_damaR.fillBuffers(damaR_shape.vertices, damaR_shape.indices, GL_STATIC_DRAW)

    damaB_shape = create_dama(0,0,1) #Usamos  0,0,1 para que sea una dama azul
    gpu_damaB= GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_damaB)
    beachPipeline.setupVAO(gpu_damaB)
    gpu_damaB.fillBuffers(damaB_shape.vertices, damaB_shape.indices, GL_STATIC_DRAW)

    
    tablero_shape = create_tablero() #También creamos el tablero 
    gpu_tablero = GPUShape().initBuffers()
    simplePipeline.setupVAO(gpu_tablero)
    beachPipeline.setupVAO(gpu_tablero)
    gpu_tablero.fillBuffers(tablero_shape.vertices, tablero_shape.indices, GL_STATIC_DRAW)

   

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

        #Aquí los if, elif y else son para que corra el programa dependiendo del valor de los controladores, así podemos hacer que cambie la imagen al apretar “A” o “B”

        if (controller.effect1):

            #Para el primer caso cuando apretamos “A” solo habrá un drawCall para el tablero y así se podrá ver sin tener las damas encima, 
            #deje una matriz de transformación en caso de que uno quisiera escalarla o trasladarla pero para esta tarea esta con valores que no hacen ningún cambio.
            glUseProgram(simplePipeline.shaderProgram)

            glUniformMatrix4fv(glGetUniformLocation(simplePipeline.shaderProgram, "transform"), 1, GL_TRUE,
            np.matmul(tr.uniformScale(1),tr.translate(0,0,0))
            )
            simplePipeline.drawCall(gpu_tablero)
            
        #Ahora para cuando apretamos “B” (elif) o cuando no apretamos nada (else) el código será idéntico excepto por el shader usado, en el primer caso 
        # será del beach y en el otro será el simple. Para esto primero partiremos dibujando el tablero y después con un for que tiene los valores “y” de 
        # la primera y tercera fila, y un for con valores x correspondientes a las posiciones que deben tener en el tablero, generaremos damas
        #  y las trasladaremos a su posición correspondiente mediante un translate con el valor (x,y,0), y adicionalmente las escalaremos a un 0.2 para que quepan 
        # dentro de una casilla por lo que usamos matmul. Repetimos el proceso ahora con la segunda fila y sus valores correspondientes teniendo 
        # cuidado de usar damaR para que sean damas rojas. Después con otros for hacemos un proceso idéntico para las damas inferiores cambiando los valores de “y” y 
        # usando damaB para generar damas azules.

        elif (controller.effect2):
            glUseProgram(beachPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(beachPipeline.shaderProgram, "transform"), 1, GL_TRUE,
            np.matmul(tr.uniformScale(1),tr.translate(0,0,0))
            )
            simplePipeline.drawCall(gpu_tablero)
            
            for y in [0.875,0.375]:
                for x in [-0.875,-0.375,0.125,0.625]:
                    glUniformMatrix4fv(glGetUniformLocation(beachPipeline.shaderProgram, "transform"), 1, GL_TRUE,
                                        np.matmul(tr.translate(x,y,0),tr.uniformScale(0.2)))
                    simplePipeline.drawCall(gpu_damaR)

            for y in [0.625]:
                for x in [-0.625,-0.125,0.375,0.875]:
                    glUniformMatrix4fv(glGetUniformLocation(beachPipeline.shaderProgram, "transform"), 1, GL_TRUE,
                                        np.matmul(tr.translate(x,y,0),tr.uniformScale(0.2)))
                    simplePipeline.drawCall(gpu_damaR)

            for y in [-0.625]:
                for x in [-0.875,-0.375,0.125,0.625]:
                    glUniformMatrix4fv(glGetUniformLocation(beachPipeline.shaderProgram, "transform"), 1, GL_TRUE,
                                        np.matmul(tr.translate(x,y,0),tr.uniformScale(0.2)))
                    simplePipeline.drawCall(gpu_damaB)

            for y in [-0.875,-0.375]:
                for x in [-0.625,-0.125,0.375,0.875]:
                    glUniformMatrix4fv(glGetUniformLocation(beachPipeline.shaderProgram, "transform"), 1, GL_TRUE,
                                        np.matmul(tr.translate(x,y,0),tr.uniformScale(0.2)))
                    simplePipeline.drawCall(gpu_damaB)
        else:
            glUseProgram(simplePipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(simplePipeline.shaderProgram, "transform"), 1, GL_TRUE,
            np.matmul(tr.uniformScale(1),tr.translate(0,0,0))
            )
            simplePipeline.drawCall(gpu_tablero)

            for y in [0.875,0.375]:
                for x in [-0.875,-0.375,0.125,0.625]:
                    glUniformMatrix4fv(glGetUniformLocation(simplePipeline.shaderProgram, "transform"), 1, GL_TRUE,
                                        np.matmul(tr.translate(x,y,0),tr.uniformScale(0.2)))
                    simplePipeline.drawCall(gpu_damaR)

            for y in [0.625]:
                for x in [-0.625,-0.125,0.375,0.875]:
                    glUniformMatrix4fv(glGetUniformLocation(simplePipeline.shaderProgram, "transform"), 1, GL_TRUE,
                                        np.matmul(tr.translate(x,y,0),tr.uniformScale(0.2)))
                    simplePipeline.drawCall(gpu_damaR)

            for y in [-0.625]:
                for x in [-0.875,-0.375,0.125,0.625]:
                    glUniformMatrix4fv(glGetUniformLocation(simplePipeline.shaderProgram, "transform"), 1, GL_TRUE,
                                        np.matmul(tr.translate(x,y,0),tr.uniformScale(0.2)))
                    simplePipeline.drawCall(gpu_damaB)

            for y in [-0.875,-0.375]:
                for x in [-0.625,-0.125,0.375,0.875]:
                    glUniformMatrix4fv(glGetUniformLocation(simplePipeline.shaderProgram, "transform"), 1, GL_TRUE,
                                        np.matmul(tr.translate(x,y,0),tr.uniformScale(0.2)))
                    simplePipeline.drawCall(gpu_damaB)

        glfw.swap_buffers(window)
    glfw.terminate()