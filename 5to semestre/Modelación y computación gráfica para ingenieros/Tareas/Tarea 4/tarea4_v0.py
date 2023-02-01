# coding=utf-8
"""Tarea 4"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
from examples.ex_curve_demo import evalCurve
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath
from auxiliarT4 import *
from operator import add

#Este código está basado en el código de Valentina Aguilar.

__author__ = "Valentina Aguilar  - Ivan Sipiran"


#ALUMNO: Tomás Rivas
#Rut: 20.592.350-0

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.X = 2.0 #posicion X de donde esta el auto
        self.Y = -0.037409 #posicion Y de donde esta el auto
        self.Z = 5.0 #posicion Z de donde esta el auto
        #lo siguiente se creo para poder usar coordenadas esfericas
        self.cameraPhiAngle = -np.pi/4 #inclinacion de la camara 
        self.cameraThetaAngle = np.pi/2 #rotacion con respecto al eje y
        self.r = 2 #radio
        ### BONUS #### 
        self.lights=1 #Valor que cambiamos para activar/desactivar las luces

#TAREA4: Esta clase contiene todos los parámetros de una luz Spotlight. Sirve principalmente para tener
# un orden sobre los atributos de las luces
class Spotlight:
    def __init__(self):
        self.ambient = np.array([0,0,0])
        self.diffuse = np.array([0,0,0])
        self.specular = np.array([0,0,0])
        self.constant = 0
        self.linear = 0
        self.quadratic = 0
        self.position = np.array([0,0,0])
        self.direction = np.array([0,0,0])
        self.cutOff = 0
        self.outerCutOff = 0

controller = Controller()

#TAREA4: aquí se crea el pool de luces spotlight (como un diccionario)
spotlightsPool = dict()

#TAREA4: Esta función ejemplifica cómo podemos crear luces para nuestra escena. En este caso creamos 2 luces con diferentes 
# parámetros

def setLights(CarPos,LightPointer, AutomaticCarPos, AutomaticPointer,multiplier,switch):
    #TAREA4: Primera luz spotlight
    spot1 = Spotlight()
    spot1.ambient = np.array([0.0, 0.0, 0.0])
    spot1.diffuse = np.array([1.0, 1.0, 1.0])
    spot1.specular = np.array([1.0, 1.0, 1.0])
    spot1.constant = 1.0
    spot1.linear = 0.09
    spot1.quadratic = 0.032
    spot1.position = np.array([2, 5, 0]) #TAREA4: esta ubicada en esta posición
    spot1.direction = np.array([0, -1, 0]) #TAREA4: está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
    spot1.cutOff = np.cos(np.radians(12.5)) #TAREA4: corte del ángulo para la luz
    spot1.outerCutOff = np.cos(np.radians(45)) #TAREA4: la apertura permitida de la luz es de 45°
                                                #mientras más alto es este ángulo, más se difumina su efecto
    
    spotlightsPool['spot1'] = spot1 #TAREA4: almacenamos la luz en el diccionario, con una clave única

    #TAREA4: Segunda luz spotlight
    spot2 = Spotlight()
    spot2.ambient = np.array([0.0, 0, 0.0])
    spot2.diffuse = np.array([1.0, 1.0, 1.0])
    spot2.specular = np.array([1.0, 1.0, 1.0])
    spot2.constant = 1.0
    spot2.linear = 0.09
    spot2.quadratic = 0.032
    spot2.position = np.array([-2, 5, 0]) #TAREA4: Está ubicada en esta posición
    spot2.direction = np.array([0, -1, 0]) #TAREA4: también apunta hacia abajo
    spot2.cutOff = np.cos(np.radians(12.5))
    spot2.outerCutOff = np.cos(np.radians(15)) #TAREA4: Esta luz tiene menos apertura, por eso es más focalizada
    spotlightsPool['spot2'] = spot2 #TAREA4: almacenamos la luz en el diccionario


    #En esta sección están las luces que cree yo, son 5 más por lo que modifique la cantidad de luces 
    # spotlight a 7 en los shaders. La 3 y 4 corresponden a los focos del auto controlado manualmente; la 5 y la 6 a 
    # los focos del auto que se mueve automáticamente y la 7 define la luz ambiental para el ciclo dia/noche.

### Variables: ### 

    # CarPos: Posición del auto controlado

    # LightPointer: Un punto justo al frente del auto controlado para usar como referencia al calcular la dirección 
    # de las luces 

    # AutomaticCarPos: La posición del auto automático
    
    # AutomaticPointer: Lo mismo que el LightPointer pero para el auto automatico

###################  Focos auto manual  ###################
    
    #Tomando como base algunos valores de las luces del foco más acotado, creamos estas luces que 
    # se diferencian por la posición y dirección en la que apuntan.

    spot3 = Spotlight()
    spot3.ambient = np.array([0.0, 0, 0.0])
    spot3.diffuse = switch*np.array([1,1,1])
    spot3.specular = switch*np.array([1,1,1])
    spot3.constant = 1
    spot3.linear = 0.09
    spot3.quadratic = 0.032

    #Usamos como base la posición del auto, y luego corremos levemente la luz en el eje X y Z dependiendo del ángulo. La manera en la que varía la calcule sacando el producto 
    # cruz entre el vector Up y el puntero de la luz lo que da un vector en el eje X del auto. 
    spot3.position = np.array(CarPos) 
    spot3.position[0]-=0.05*LightPointer[2]
    spot3.position[2]+=0.05*LightPointer[0]

    #De igual manera tomamos como base el puntero inicial de la luz y lo desplazamos.
    spot3.direction = np.array(LightPointer)
    spot3.direction[0]-=0.05*LightPointer[2]
    spot3.direction[2]+=0.05*LightPointer[0] 
    spot3.cutOff = np.cos(np.radians(12.5))
    spot3.outerCutOff = np.cos(np.radians(15)) 
    spotlightsPool['spot3'] = spot3 


    #La 4ta luz es igual a la 3era pero con signos opuestos en las variaciones. Así completamos la luz izquierda y derecha
    spot4 = Spotlight()
    spot4.ambient = np.array([0.0, 0, 0.0])
    spot4.diffuse = switch*np.array([1,1,1])
    spot4.specular = switch*np.array([1,1,1])
    spot4.constant = 1
    spot4.linear = 0.09
    spot4.quadratic = 0.032
    spot4.position = np.array(CarPos) 
    spot4.position[0]+=0.05 *LightPointer[2]
    spot4.position[2]-=0.05 *LightPointer[0]
    spot4.direction = np.array(LightPointer) 
    spot4.direction[0]+=0.05 *LightPointer[2]
    spot4.direction[2]-=0.05 *LightPointer[0]
    spot4.cutOff = np.cos(np.radians(12.5))
    spot4.outerCutOff = np.cos(np.radians(15)) 
    spotlightsPool['spot4'] = spot4 

###################  Focos auto automatico  ###################

    #La 5ta y 6 luz siguen los mismos procesos de las anteriores pero ahora con la posición y apuntado del auto que se mueve automáticamente.

    spot5 = Spotlight() 
    spot5.ambient = np.array([0.0, 0, 0.0])
    spot5.diffuse = np.array([1.0, 1.0, 1.0])
    spot5.specular = np.array([1.0, 1.0, 1.0])
    spot5.constant = 1.0
    spot5.linear = 0.09
    spot5.quadratic = 0.032
    spot5.position = np.array(AutomaticCarPos) 
    spot5.position[0]-=0.05*AutomaticPointer[2]
    spot5.position[2]+=0.05*AutomaticPointer[0]
    spot5.direction = np.array(AutomaticPointer)
    spot5.direction[0]-=0.05*AutomaticPointer[2]
    spot5.direction[2]+=0.05*AutomaticPointer[0] 
    spot5.cutOff = np.cos(np.radians(12.5))
    spot5.outerCutOff = np.cos(np.radians(15)) 
    spotlightsPool['spot5'] = spot5 

    spot6 = Spotlight()
    spot6.ambient = np.array([0.0, 0, 0.0])
    spot6.diffuse = np.array([1,1,1])
    spot6.specular = np.array([1,1,1])
    spot6.constant = 1.0
    spot6.linear = 0.09
    spot6.quadratic = 0.032
    spot6.position = np.array(AutomaticCarPos)
    spot6.position[0]+=0.05*AutomaticPointer[2]
    spot6.position[2]-=0.05*AutomaticPointer[0]
    spot6.direction = np.array(AutomaticPointer)
    spot6.direction[0]+=0.05*AutomaticPointer[2]
    spot6.direction[2]-=0.05*AutomaticPointer[0] 
    spot6.cutOff = np.cos(np.radians(12.5))
    spot6.outerCutOff = np.cos(np.radians(15))
    spotlightsPool['spot6'] = spot6 

#####   BONUS  ######

    #Aquí defino la luz que se encarga de manejar el ciclo día/noche. Esta luz solo tiene una componente ambiental que se calcula como 1 por el multiplier 
    # para los 3 componentes. El cálculo del multiplier está hecho fuera de la función por lo que aquí únicamente nos preocupamos de la multiplicación y 
    # de agregar la luz al diccionario.

    spot7 = Spotlight()
    spot7.ambient = multiplier*np.array([1, 1, 1])
    spotlightsPool['spot7'] = spot7 

#TAREA4: modificamos esta función para poder configurar todas las luces del pool
def setPlot(texPipeline, axisPipeline, lightPipeline):
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100) #el primer parametro se cambia a 60 para que se vea más escena

    glUseProgram(axisPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    #TAREA4: Como tenemos 2 shaders con múltiples luces, tenemos que enviar toda esa información a cada shader
    #TAREA4: Primero al shader de color
    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    #TAREA4: Enviamos la información de la luz puntual y del material
    #TAREA4: La luz puntual está desactivada por defecto (ya que su componente ambiente es 0.0, 0.0, 0.0), pero pueden usarla
    # para añadir más realismo a la escena
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].position"), 5, 5, 5)

    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "material.shininess"), 32)

    #TAREA4: Aprovechamos que las luces spotlight están almacenadas en el diccionario para mandarlas al shader
    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "linear"), 0.09)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "quadratic"), 0.032)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)

    #TAREA4: Ahora repetimos todo el proceso para el shader de texturas con mútiples luces
    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    

    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].position"), 5, 5, 5)

    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "material.shininess"), 32)

    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "linear"), 0.09)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "quadratic"), 0.032)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)

#TAREA4: Esta función controla la cámara
def setView(texPipeline, axisPipeline, lightPipeline):
    #la idea de usar coordenadas esfericas para la camara fue extraida del auxiliar 6
    #como el auto reposa en el plano XZ, no sera necesaria la coordenada Y esferica.
    Xesf = controller.r * np.sin(controller.cameraPhiAngle)*np.cos(controller.cameraThetaAngle) #coordenada X esferica
    Zesf = controller.r * np.sin(controller.cameraPhiAngle)*np.sin(controller.cameraThetaAngle) #coordenada Y esferica

    viewPos = np.array([controller.X-Xesf,0.5,controller.Z-Zesf])
    view = tr.lookAt(
            viewPos, #eye
            np.array([controller.X,controller.Y,controller.Z]),     #at
            np.array([0, 1, 0])   #up
        )

    glUseProgram(axisPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])

    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    
    

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    ### BONUS ####


    elif key == glfw.KEY_ENTER:
        if controller.lights==1:
            controller.lights=0
        else:
            controller.lights=1
    
    
if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800
    title = "Tarea 4"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    #TAREA4: Se usan los shaders de múltiples luces
    axisPipeline = es.SimpleModelViewProjectionShaderProgram()
    texPipeline = ls.MultipleLightTexturePhongShaderProgram()
    lightPipeline = ls.MultipleLightPhongShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(axisPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    cpuAxis = bs.createAxis(7)
    gpuAxis = es.GPUShape().initBuffers()
    axisPipeline.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    #NOTA: Aqui creas un objeto con tu escena
    #TAREA4: Se cargan las texturas y se configuran las luces
    loadTextures()
    
    dibujo = createStaticScene(texPipeline)
    car = createCarScene(lightPipeline)

###### Creamos otro auto que será el que se moverá automáticamente. #######
    automaticCar=createCarScene(lightPipeline)
    
    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

 
#######  CURVAS y parametros iniciales###########

    #La función estándar para crear una matriz de bezier que será la que ocupare para las curvas
    def bezierMatrix(P0, P1, P2, P3):
        
        G = np.concatenate((P0, P1, P2, P3), axis=1)

        Mb = np.array([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]])
    
        return np.matmul(G, Mb)

    t0 = glfw.get_time()
    coord_X = 0 
    coord_Z = 0
    angulo = 0
 
    step=0 #Paso de la curva, parte en 0
    AutomaticAngle=np.pi #Angulo del auto automático, parte en pi
    
    #Los puntos que usamos para las curvas de Bezier,  hay un dibujo en la carpeta de un boceto que use donde está más o menos la posición de cada punto.
    P0=np.array([[-2,-0.037409,5.5]]).T
    P1=np.array([[-2,-0.037409,-4.5]]).T
    P2=np.array([[-2,-0.037409,-7]]).T
    P3=np.array([[2,-0.037409,-7]]).T
    P4=np.array([[2,-0.037409,-4.5]]).T
    P5=np.array([[2,-0.037409,5.5]]).T
    P6=np.array([[2,-0.037409,8]]).T
    P7=np.array([[-2,-0.037409,8]]).T

    #La primera y la tercera curva representan las partes rectas de la pista, y la segunda y cuarta las partes curvas. Cada curva tiene 1000 puntos y las concatenamos en una curva final de 4000 puntos.
    curvaBezier1 =bezierMatrix(P0,P0,P1,P1)
    Bezier1= evalCurve(curvaBezier1,1000)

    curvaBezier2 =bezierMatrix(P1,P2,P3,P4)
    Bezier2= evalCurve(curvaBezier2,1000)

    curvaBezier3 =bezierMatrix(P4,P4,P5,P5)
    Bezier3= evalCurve(curvaBezier3,1000)

    curvaBezier4 =bezierMatrix(P5,P6,P7,P0)
    Bezier4= evalCurve(curvaBezier4,1000)

    FinalBezier = np.concatenate((Bezier1,Bezier2,Bezier3,Bezier4), axis=0)
    t=0
    
    while not glfw.window_should_close(window):

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        #Se obtiene una diferencia de tiempo con respecto a la iteracion anterior.
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        #Calculamos CarPos con los valores en X y Z pero al valor de Y le ponemos 0.1 para que este mas levantada.
        CarPos=[2+coord_X,0.1,5+coord_Z]

        #Calculamos los valores del puntero de luz de manera casi idéntica a la posición de la vista
        Xesf = controller.r * np.sin(controller.cameraPhiAngle)*np.cos(controller.cameraThetaAngle) 
        Zesf = controller.r * np.sin(controller.cameraPhiAngle)*np.sin(controller.cameraThetaAngle)
        LightPointer=[Xesf,0,Zesf]

        #Realizamos el mismo proceso para el auto-matico
        AutomaticCarPos=[FinalBezier[step,0],0.1,FinalBezier[step,2]]
        PointX = controller.r * np.sin(controller.cameraPhiAngle)*np.cos(-np.pi/2-AutomaticAngle) 
        PointZ = controller.r * np.sin(controller.cameraPhiAngle)*np.sin(-np.pi/2-AutomaticAngle)
        AutomaticPointer=[PointX,0,PointZ]

        # BONUS #

        #Aquí defino como varía el multiplicador de la luz ambiental, lo hará según el tiempo dentro de una función seno para hacerlo cíclico. 
        # El /6 define que tan rápido son los ciclos, considero que con 6 queda a una velocidad razonable para apreciar el día/noche y la transición. 
        # Finalmente el max es para que no se llegue a 0 porque causaría que los objetos quedaran completamente negros.

        timeChanger=max(np.sin(t1/6),0.0000001)


        setLights(CarPos,LightPointer,AutomaticCarPos,AutomaticPointer,timeChanger,controller.lights)

        #TAREA4: Se manejan las teclas de la animación
        #ir hacia adelante 
        if(glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
            controller.X -= 1.5 * dt * np.sin(angulo) #avanza la camara
            controller.Z -= 1.5 * dt * np.cos(angulo) #avanza la camara
            coord_X -= 1.5 * dt * np.sin(angulo) #avanza el auto
            coord_Z -= 1.5 * dt * np.cos(angulo) #avanza el auto

        #ir hacia atras
        if(glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
            controller.X += 1.5 * dt * np.sin(angulo) #retrocede la camara
            controller.Z += 1.5 * dt * np.cos(angulo) #retrocede la cmara
            coord_X += 1.5 * dt * np.sin(angulo) #retrocede el auto
            coord_Z += 1.5 * dt * np.cos(angulo) #retrocede el auto

        #ir hacia la izquierda
        if(glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
            controller.cameraThetaAngle -= dt  #camara se gira a la izquierda
            angulo += dt #auto gira a la izquierda

        #ir hacia la derecha
        if(glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
            controller.cameraThetaAngle += dt #camara se gira a la derecha
            angulo -= dt #auto gira a la derecha

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        #TAREA4: Ojo aquí! Se configura la cámara y el dibujo en cada iteración. Esto es porque necesitamos que en cada iteración
        # las luces de los faros de los carros se actualicen en posición y dirección
        setView(texPipeline, axisPipeline, lightPipeline)
        setPlot(texPipeline, axisPipeline,lightPipeline)

        if controller.showAxis:
            glUseProgram(axisPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            axisPipeline.drawCall(gpuAxis, GL_LINES)

        #NOTA: Aquí dibujas tu objeto de escena
        glUseProgram(texPipeline.shaderProgram)
        sg.drawSceneGraphNode(dibujo, texPipeline, "model")
        
        glUseProgram(lightPipeline.shaderProgram)



        
        #aqui se mueve el auto
        sg.drawSceneGraphNode(car, lightPipeline, "model")
        Auto = sg.findNode(car,'system-car')
        Auto.transform = tr.matmul([tr.translate(coord_X+2,-0.037409,coord_Z+5),tr.rotationY(np.pi+angulo),tr.rotationY(-np.pi),tr.translate(-2,0.037409,-5)])
        #transformación que hace que el auto se ponga en el origen, para luego trasladarlo al punto (2.0, −0.037409, 5.0) para despés poder moverlo.

        #Dibujamos el auto que se mueve automáticamente, para los step entre [1000,2000] y [3000,4000] le agregamos una rotación 
        # para que el auto gire mientras toma la curva. Los step se reinician a
        # 0 al llegar a 4000 y la traslación se hace según el step en el que se encuentre. Finalmente aumentamos el step en 1 en cada iteración.
        sg.drawSceneGraphNode(automaticCar, lightPipeline, "model")
        Automatico = sg.findNode(automaticCar,'system-car')
        if (step>=1000 and step<=2000) or (step>=3000 and step<=4000):
            AutomaticAngle-=np.pi/1000 
        Automatico.transform = tr.matmul([tr.translate(FinalBezier[step,0],FinalBezier[step,1],FinalBezier[step,2]),tr.rotationY(AutomaticAngle),tr.rotationY(-np.pi),tr.translate(-2,0.037409,-5)])
        step+=1
        if step==4000:
            step=0

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    dibujo.clear()
    

    glfw.terminate()