# coding=utf-8
"""Tarea 4"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path

from numpy.typing import _128Bit
from examples.ex_curve_demo import evalCurve
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath
import collisions as cl
from auxiliarT4 import *
from operator import add
from funciones_luces import *

#Este código está basado en el código de Valentina Aguilar.

__author__ = "Valentina Aguilar  - Ivan Sipiran"


#ALUMNO: Tomás Rivas
#Rut: 20.592.350-0

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = False
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




#TAREA 5 Ahora acepta el parámetro view para que tengamos más control sobre cómo se setea la vista BONUS
def setView(texPipeline, axisPipeline, lightPipeline,viewSetter):
    #la idea de usar coordenadas esfericas para la camara fue extraida del auxiliar 6
    #como el auto reposa en el plano XZ, no sera necesaria la coordenada Y esferica.
    view=viewSetter

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
    title = "Tarea 5 Tomas Rivas"
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
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    
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
    

    collision_list = cl.AABBList(mvpPipeline, [0,1,0]) # Objeto que almacena los AABB del entorno

     # TAREA 5
   #Aquí se generan las colisiones de los objetos, hay 5 objetos que almacenan las hitboxes:
   #collisions_player: Almacena el hitbox del jugador (El auto que controlamos)  con un color rojo
   #collision_list.objects: Almacena los hitboxes de todos los objetos inanimados con los que queremos chocar, esto incluye las casas y las paredes que se realizan a través de for. Son de color verde
   #collisions_automatic_car: Hitbox del auto automático que es de color azul
   #collisionsSlowTrack y collisionsFastTrack: Contienen los hitbox del slow track y el fast track respectivamente con color morado.

    for x in range(1,9):
        p = sg.findPosition(dibujo, "wall"+str(x)).reshape(1,4)[0][0:3] 
        collision_list.objects += [cl.AABB(p,  0.1, 0.4, 2.5)]   

    for x in range(1,11):
        p = sg.findPosition(dibujo, "house"+str(x)).reshape(1,4)[0][0:3] 
        collision_list.objects += [cl.AABB(p, 0.5, 0.5, 0.5)]  

    collisionsFastTrack = cl.AABBList(mvpPipeline, [0.4, 0.1, 0.5])
    p1 = sg.findPosition(dibujo, 'fastTrack')
    p1[2]+=2  #El +2 es para re ajustar una parte del hitbox que no calza con la textura
    p1.reshape(1,4)[0][0:3] 
    collisionsFastTrack.objects += [cl.AABB(p1,  0.4, 0.1, 2.5)]      

    collisionsSlowTrack = cl.AABBList(mvpPipeline, [0.4, 0.1, 0.5])
    p2 = sg.findPosition(dibujo, "slowTrack")
    p2[2]+=2 #El +2 es para re ajustar una parte del hitbox que no calza con la textura
    p2.reshape(1,4)[0][0:3] 
    collisionsSlowTrack.objects += [cl.AABB(p2,  0.4, 0.1, 2.5)]    

    collisions_player = cl.AABBList(mvpPipeline, [1, 0, 0]) 
    CarPos=[2+coord_X,0.1,5+coord_Z]
    player = cl.AABB(CarPos, 0.2, 0.3, 0.2)            
    collisions_player.objects += [player]

    collisions_automatic_car = cl.AABBList(mvpPipeline, [0, 0, 1]) 
    AutomaticCarPos=[FinalBezier[step,0],FinalBezier[step,1],FinalBezier[step,2]]
    automatic = cl.AABB(AutomaticCarPos, 0.2, 0.3, 0.2)             
    collisions_automatic_car.objects += [automatic]    

    gpuSky=createSkyBox(texPipeline)
    while not glfw.window_should_close(window):
        #### BONUS #####

        #Aquí variamos el valor speed dependiendo de si está en contacto con alguna de las 2 pistas, esto hace que el auto vaya a
        #mayor o menor velocidad. Si no está en contacto con ninguna toma un valor default.
        if collisions_player.check_overlap(collisionsFastTrack):
            speed=3
        elif collisions_player.check_overlap(collisionsSlowTrack):
            speed=0.75
        else:
            speed=1.5

        Xesf = controller.r * np.sin(controller.cameraPhiAngle)*np.cos(controller.cameraThetaAngle) #coordenada X esferica
        Zesf = controller.r * np.sin(controller.cameraPhiAngle)*np.sin(controller.cameraThetaAngle) #coordenada Y esferica

        viewPos = np.array([controller.X-Xesf,0.5,controller.Z-Zesf])
        view = tr.lookAt(
                viewPos, #eye
                np.array([controller.X,controller.Y,controller.Z]),     #at
                np.array([0, 1, 0])   #up
            )
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

        CurrentCarPos=[coord_X+2,-0.037409,coord_Z+5]
        CurrentCamPos=[controller.X,controller.Z]
        #TAREA4: Se manejan las teclas de la animación
        #ir hacia adelante 
        if(glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
            controller.X -= 1.7*speed * dt * np.sin(angulo) #avanza la camara
            controller.Z -= 1.7*speed * dt * np.cos(angulo) #avanza la camara
            coord_X -= 1.7*speed * dt * np.sin(angulo) #avanza el auto
            coord_Z -= 1.7*speed * dt * np.cos(angulo) #avanza el auto

        #ir hacia atras
        if(glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
            controller.X += speed * dt * np.sin(angulo) #retrocede la camara
            controller.Z += speed * dt * np.cos(angulo) #retrocede la cmara
            coord_X += speed * dt * np.sin(angulo) #retrocede el auto
            coord_Z += speed * dt * np.cos(angulo) #retrocede el auto

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
        setView(texPipeline, axisPipeline, lightPipeline,view)
        setPlot(texPipeline, axisPipeline,lightPipeline)

        if controller.showAxis:
            #Dibujo de los hitboxes
            glUseProgram(axisPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            axisPipeline.drawCall(gpuAxis, GL_LINES)
            collision_list.drawBoundingBoxes(mvpPipeline)
            collisions_player.drawBoundingBoxes(mvpPipeline)
            collisions_automatic_car.drawBoundingBoxes(mvpPipeline)
            collisionsFastTrack.drawBoundingBoxes(mvpPipeline)
            collisionsSlowTrack.drawBoundingBoxes(mvpPipeline)
        #NOTA: Aquí dibujas tu objeto de escena
        glUseProgram(texPipeline.shaderProgram)
        sg.drawSceneGraphNode(dibujo, texPipeline, "model")
        
        glUseProgram(lightPipeline.shaderProgram)
        #Aquí generamos el candidato a la siguiente posición y lo almacenamos.
        
        CandidateCarPos=[coord_X+2,-0.037409,coord_Z+5]
        player.set_pos(CandidateCarPos)

        #Revisamos las colisiones tanto con los objetos inanimados como con el auto automatico
        
        if not collisions_player.check_overlap(collision_list) and not collisions_player.check_overlap(collisions_automatic_car):
            
            #Si no hay choque se realiza el movimiento
            
            CurrentCarPos = CandidateCarPos
        else:
            #Si hay un choque nos fijamos en qué dirección es para anular el movimiento en esa dirección.
            direction=collisions_player.collide_and_slide(collision_list)+collisions_player.collide_and_slide(collisions_automatic_car)
            if direction[0]==1:
                coord_X=(CurrentCarPos[0]-2)
                controller.X=CurrentCamPos[0]
            if direction[2]==1:
                coord_Z=(CurrentCarPos[2]-5)
                controller.Z=CurrentCamPos[1]

            player.set_pos(CurrentCarPos)
    
        #aqui se mueve el auto
        sg.drawSceneGraphNode(car, lightPipeline, "model")
        Auto = sg.findNode(car,'system-car')
        Auto.transform = tr.matmul([tr.translate(CurrentCarPos[0],CurrentCarPos[1],CurrentCarPos[2]),tr.rotationY(np.pi+angulo),tr.rotationY(-np.pi),tr.translate(-2,0.037409,-5)])
        #transformación que hace que el auto se ponga en el origen, para luego trasladarlo al punto (2.0, −0.037409, 5.0) para despés poder moverlo.

        #Dibujamos el auto que se mueve automáticamente, para los step entre [1000,2000] y [3000,4000] le agregamos una rotación 
        # para que el auto gire mientras toma la curva. Los step se reinician a
        # 0 al llegar a 4000 y la traslación se hace según el step en el que se encuentre. Finalmente aumentamos el step en 1 en cada iteración.
        sg.drawSceneGraphNode(automaticCar, lightPipeline, "model")
        Automatico = sg.findNode(automaticCar,'system-car')
        if ((step>=1000 and step<=2000) or (step>=3000 and step<=4000)) and not collisions_player.check_overlap(collisions_automatic_car):
            AutomaticAngle-=np.pi/1000 
        Automatico.transform = tr.matmul([tr.translate(FinalBezier[step,0],FinalBezier[step,1],FinalBezier[step,2]),tr.rotationY(AutomaticAngle),tr.rotationY(-np.pi),tr.translate(-2,0.037409,-5)])
        automatic.set_pos([FinalBezier[step,0],FinalBezier[step,1],FinalBezier[step,2]])
        if not collisions_player.check_overlap(collisions_automatic_car):
            step+=1
        if step==4000:
            step=0

        ############# BONUS ##################  Aquí reseteamos la view para que el skybox sea inalcanzable, luego dibujamos el skybox
        view[0:3,3] = 0
        setView(texPipeline, axisPipeline, lightPipeline,view)
        glUseProgram(texPipeline.shaderProgram)
        sg.drawSceneGraphNode(gpuSky, texPipeline, "model")
        # Once the render is done, buffers  are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    dibujo.clear()
    

    glfw.terminate()