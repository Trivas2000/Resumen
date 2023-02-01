# coding=utf-8
"""Tarea 2, Carro 13"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path

from numpy.matrixlib import mat
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath

__author__ = "Ivan Sipiran"
__license__ = "MIT"

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.viewPos = np.array([10,10,10])
        self.camUp = np.array([0, 1, 0])
        self.distance = 10


controller = Controller()

def setPlot(pipeline, mvpPipeline):
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 5, 5, 5)
    
    glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 1000)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

def setView(pipeline, mvpPipeline):
    view = tr.lookAt(
            controller.viewPos,
            np.array([0,0,0]),
            controller.camUp
        )

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1], controller.viewPos[2])
    

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
    
    elif key == glfw.KEY_1:
        controller.viewPos = np.array([controller.distance,controller.distance,controller.distance]) #Vista diagonal 1
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_2:
        controller.viewPos = np.array([0,0,controller.distance]) #Vista frontal
        controller.camUp = np.array([0,1,0])

    elif key == glfw.KEY_3:
        controller.viewPos = np.array([controller.distance,0,controller.distance]) #Vista lateral
        controller.camUp = np.array([0,1,0])

    elif key == glfw.KEY_4:
        controller.viewPos = np.array([0,controller.distance,0]) #Vista superior
        controller.camUp = np.array([1,0,0])
    
    elif key == glfw.KEY_5:
        controller.viewPos = np.array([controller.distance,controller.distance,-controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_6:
        controller.viewPos = np.array([-controller.distance,controller.distance,-controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_7:
        controller.viewPos = np.array([-controller.distance,controller.distance,controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    else:
        print('Unknown key')

def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape

#Copiaremos el modelo 13 de los carros(Camioneta Azul)
def createScene(pipeline):

    cuboazul = createGPUShape(pipeline, bs.createColorCubeTarea2(0,0,1))
    cubonegro = createGPUShape(pipeline, bs.createColorCubeTarea2(0,0,0))
    cuboverde = createGPUShape(pipeline, bs.createColorCubeTarea2(0,0.6,0.3))
    cuborojo = createGPUShape(pipeline, bs.createColorCubeTarea2(1,0,0))
    figllanta = createGPUShape(pipeline, bs.createColorCylinderTarea2(0,0,0))
    figdisco = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.5,0.5,0.5))
    cubogrisclaro = createGPUShape(pipeline, bs.createColorCubeTarea2(0.4,0.4,0.4))
    cubogrisoscuro = createGPUShape(pipeline, bs.createColorCubeTarea2(0.2,0.2,0.2))
    cubonaranja = createGPUShape(pipeline, bs.createColorCubeTarea2(1,0.5,0))

    #CUERPO PRINCIPAL

    cuerpod = sg.SceneGraphNode('cuerpod')
    cuerpod.transform = tr.matmul([tr.scale(1.65,0.7,1.8),tr.translate(0.8,0.9,0)])
    cuerpod.childs += [cuboazul]

    luzrojadelantera = sg.SceneGraphNode('lusrojad')
    luzrojadelantera.transform = tr.matmul([tr.scale(0.2,0.1,1.801),tr.translate(12,7,0)])
    luzrojadelantera.childs += [cuborojo]

    
    patentesup = sg.SceneGraphNode('patentesup')
    patentesup.transform = tr.matmul([tr.scale(0.3,0.4,1.7),tr.translate(9,1.8,0)])
    patentesup.childs += [cubogrisclaro]

    patenteinf = sg.SceneGraphNode('patenteinf')
    patenteinf.transform = tr.matmul([tr.scale(0.3,0.2,1.7),tr.translate(9.2,1.3,0)])
    patenteinf.childs += [cubogrisoscuro]

    luznaranjad = sg.SceneGraphNode('luznaranjad')
    luznaranjad.transform = tr.matmul([tr.scale(0.1,0.07,0.2),tr.translate(30,3,6)])
    luznaranjad.childs += [cubonaranja]

    luznaranjai = sg.SceneGraphNode('luznaranjai')
    luznaranjai.transform = tr.matmul([tr.scale(0.1,0.07,0.2),tr.translate(30,3,-6)])
    luznaranjai.childs += [cubonaranja]

    focod = sg.SceneGraphNode('focod')
    focod.transform = tr.matmul([tr.scale(0.2,0.2,0.2),tr.translate(14.2,3.7,6.2),tr.rotationZ(-np.pi/2)])
    focod.childs += [figdisco]

    focoi = sg.SceneGraphNode('focoi')
    focoi.transform = tr.matmul([tr.scale(0.2,0.2,0.2),tr.translate(14.2,3.7,-6.2),tr.rotationZ(-np.pi/2)])
    focoi.childs += [figdisco]

    patentenegra = sg.SceneGraphNode('patentenegra')
    patentenegra.transform = tr.matmul([tr.scale(0.3,0.35,0.92),tr.translate(9.01,1.8,0)])
    patentenegra.childs += [cubonegro]

    chevrolet1 = sg.SceneGraphNode('chevrolet1')
    chevrolet1.transform = tr.matmul([tr.scale(0.075,0.05,0.15),tr.translate(39.2,14,0)])
    chevrolet1.childs += [cubonaranja]

    chevrolet2 = sg.SceneGraphNode('chevrolet2')
    chevrolet2.transform = tr.matmul([tr.scale(0.075,0.05,0.075),tr.translate(39.2,14.7,0)])
    chevrolet2.childs += [cubonaranja]

    chevrolet3 = sg.SceneGraphNode('chevrolet3')
    chevrolet3.transform = tr.matmul([tr.scale(0.075,0.05,0.075),tr.translate(39.2,13.3,0)])
    chevrolet3.childs += [cubonaranja]

    patente = sg.SceneGraphNode('patente')
    patente.childs += [patentesup]
    patente.childs += [patenteinf]
    patente.childs += [luznaranjad]
    patente.childs += [luznaranjai]
    patente.childs += [focod]
    patente.childs += [focoi]
    patente.childs += [patentenegra]
    patente.childs += [chevrolet1]
    patente.childs += [chevrolet2]
    patente.childs += [chevrolet3]
    


    cuerpodelantero = sg.SceneGraphNode('cuerpod')
    cuerpodelantero.childs += [cuerpod]
    cuerpodelantero.childs += [luzrojadelantera]
    cuerpodelantero.childs += [patente]


    #MALETA
    puertatrasera = sg.SceneGraphNode('puertatrasera')
    puertatrasera.transform = tr.matmul([tr.scale(0.1,0.7,1.8),tr.translate(-36,0.9,0)])
    puertatrasera.childs += [cuboazul]

    puertalateral = sg.SceneGraphNode('puertalateral')
    puertalateral.transform = tr.scale(1.65,0.7,0.1)
    puertalateral.childs += [cuboazul]

    puertalateralizq = sg.SceneGraphNode('puertalateralizq')
    puertalateralizq.transform = tr.translate(-1.9,0.63,-1.7)
    puertalateralizq.childs += [puertalateral]

    puertalateralder = sg.SceneGraphNode('puertalateralder')
    puertalateralder.transform = tr.translate(-1.9,0.63,1.7)
    puertalateralder.childs += [puertalateral]

    bordesmaleta = sg.SceneGraphNode('bordesmaleta')
    bordesmaleta.childs += [puertalateralder,puertalateralizq,puertatrasera]

    base = sg.SceneGraphNode('base')
    base.transform = tr.matmul([tr.scale(1.8,0.3,1.79),tr.translate(-1,0.9,0)])
    base.childs += [cuboverde]

    interiorlargod= sg.SceneGraphNode('interiorlargod')
    interiorlargod.transform = tr.matmul([tr.translate(-1.9,0.63,1.6),tr.scale(1.63,0.7,0.05)])
    interiorlargod.childs += [cuboverde]

    interiorlargoi= sg.SceneGraphNode('interiorlargoi')
    interiorlargoi.transform = tr.matmul([tr.translate(-1.9,0.63,-1.6),tr.scale(1.63,0.7,0.05)])
    interiorlargoi.childs += [cuboverde]

    interiorcortoad= sg.SceneGraphNode('interiorcortoad')
    interiorcortoad.transform = tr.matmul([tr.scale(0.08,0.7,1.78),tr.translate(-44,0.9,0)])
    interiorcortoad.childs += [cuboverde]

    interiorcortoat= sg.SceneGraphNode('interiorcortoat')
    interiorcortoat.transform = tr.matmul([tr.scale(0.08,0.7,1.78),tr.translate(-3.8,0.88,0)])
    interiorcortoat.childs += [cuboverde]

    interior= sg.SceneGraphNode('interior')
    interior.childs += [interiorcortoad,interiorcortoat,interiorlargoi,interiorlargod]

    parachoquearriba= sg.SceneGraphNode('parachoquearriba')
    parachoquearriba.transform = tr.matmul([tr.scale(0.08,0.1,1.4),tr.translate(-46,8,0)])
    parachoquearriba.childs += [cubogrisoscuro]

    parachoqueabajo= sg.SceneGraphNode('parachoqueabajo')
    parachoqueabajo.transform = tr.matmul([tr.scale(0.08,0.3,1.67),tr.translate(-46,0,0)])
    parachoqueabajo.childs += [cubogrisoscuro]


    marcofoco= sg.SceneGraphNode('marcofoco')
    marcofoco.transform = tr.matmul([tr.scale(0.08,0.3,0.15),tr.translate(-46.1,0,0)])
    marcofoco.childs += [cubogrisclaro]

    luzfoco= sg.SceneGraphNode('luzfoco')
    luzfoco.transform = tr.matmul([tr.scale(0.08,0.22,0.1),tr.translate(-46.2,0,0)])
    luzfoco.childs += [cuborojo]

    luzizq= sg.SceneGraphNode('luzizq')
    luzizq.transform = tr.translate(0,0.7,-1.5)
    luzizq.childs += [marcofoco,luzfoco]

    luzder= sg.SceneGraphNode('luzder')
    luzder.transform = tr.translate(0,0.7,1.5)
    luzder.childs += [marcofoco,luzfoco]

    rojalateralder = sg.SceneGraphNode('rojalateralder')
    rojalateralder.transform = tr.matmul([tr.scale(0.2,0.1,0.1),tr.translate(-16,7,-17.1)])
    rojalateralder.childs += [cuborojo]

    rojalateralizq = sg.SceneGraphNode('rojalateralizq')
    rojalateralizq.transform = tr.matmul([tr.scale(0.2,0.1,0.1),tr.translate(-16,7,17.1)])
    rojalateralizq.childs += [cuborojo]

    detallesmaleta= sg.SceneGraphNode('detallesmaleta')
    detallesmaleta.childs += [parachoquearriba]
    detallesmaleta.childs += [parachoqueabajo]
    detallesmaleta.childs += [luzizq]
    detallesmaleta.childs += [luzder]
    detallesmaleta.childs += [rojalateralder]
    detallesmaleta.childs += [rojalateralizq]
    
    #CREANDO LA RUEDA
    llanta = sg.SceneGraphNode('llanta')
    llanta.transform= tr.matmul([tr.rotationZ(np.pi/2),tr.rotationX(np.pi/2),tr.scale(1,0.2,1)])
    llanta.childs += [figllanta]
    disco = sg.SceneGraphNode('disco')
    disco.transform= tr.matmul([tr.rotationZ(np.pi/2),tr.rotationX(np.pi/2),tr.scale(0.65,0.22,0.65)])
    disco.childs += [figdisco]

    ruedamaleta= sg.SceneGraphNode('ruedamaleta')
    ruedamaleta.transform = tr.matmul([tr.translate(-0.9,1.3,1.4),tr.uniformScale(0.5)])
    ruedamaleta.childs += [disco,llanta]

    maleta = sg.SceneGraphNode('maleta')
    maleta.childs += [base]
    maleta.childs += [bordesmaleta]
    maleta.childs += [interior]
    maleta.childs += [ruedamaleta]
    maleta.childs += [detallesmaleta]

    

    cuerpo = sg.SceneGraphNode('cuerpo')#Finalizamos el cuerpo principal
    cuerpo.childs += [cuerpodelantero]
    cuerpo.childs += [maleta]
    cuerpo.childs += [luzrojadelantera]
    
    

    #HACIENDO LAS 4 RUEDAS(El objeto ruedas esta creado de la parte anterior)
    rueda1 = sg.SceneGraphNode('rueda1')
    rueda1.transform=tr.matmul([tr.translate(2.1,-0.2,1.8),tr.uniformScale(0.5)])
    rueda1.childs += [disco,llanta]

    rueda2 = sg.SceneGraphNode('rueda1')
    rueda2.transform=tr.matmul([tr.translate(2.1,-0.2,-1.8),tr.uniformScale(0.5)])
    rueda2.childs += [disco,llanta]

    rueda3 = sg.SceneGraphNode('rueda1')
    rueda3.transform=tr.matmul([tr.translate(-1.5,-0.2,1.8),tr.uniformScale(0.5)])
    rueda3.childs += [disco,llanta]

    rueda4 = sg.SceneGraphNode('rueda1')
    rueda4.transform=tr.matmul([tr.translate(-1.5,-0.2,-1.8),tr.uniformScale(0.5)])
    rueda4.childs += [disco,llanta]

    ruedas = sg.SceneGraphNode('ruedas')
    ruedas.childs += [rueda1]
    ruedas.childs += [rueda2]
    ruedas.childs += [rueda3]
    ruedas.childs += [rueda4]

    #CAPOT(La parte superior de la camioneta)
    capot1 = sg.SceneGraphNode('capot1')
    capot1.transform = tr.matmul([tr.scale(0.7,0.6,1.8),tr.translate(0,0.9,0)])
    capot1.childs += [cuboazul]

    capot2 = sg.SceneGraphNode('capot2')
    capot2.transform = tr.matmul([tr.scale(0.7,0.7,1.8),tr.translate(0.695,0.25,0),tr.rotationZ(0.6)])
    capot2.childs += [cuboazul]

    ventanas1= sg.SceneGraphNode('ventanas1')
    ventanas1.transform = tr.matmul([tr.scale(0.7,0.6,1.8),tr.translate(0,0.9,0)])
    ventanas1.childs += [cubonegro]

    ventanas2= sg.SceneGraphNode('ventanas2')
    ventanas2.transform = tr.matmul([tr.scale(0.7,0.7,1.8),tr.translate(0.695,0.25,0),tr.rotationZ(0.6)])
    ventanas2.childs += [cubonegro]
    
    ventanas3= sg.SceneGraphNode('ventanas3')
    ventanas3.transform = tr.matmul([tr.scale(0.7,0.7,1.6),tr.translate(1.15,0.25,0),tr.rotationZ(0.6)])
    ventanas3.childs += [cubonegro]

    ventanas4= sg.SceneGraphNode('ventanas4')
    ventanas4.transform = tr.matmul([tr.scale(0.7,0.6,1.44),tr.translate(-0.55,0.9,-0.1)])
    ventanas4.childs += [cubonegro]

    ventanas= sg.SceneGraphNode('ventanas')
    ventanas.transform = tr.matmul([tr.translate(0.1,0.05,0),tr.uniformScale(0.75),tr.scale(1,1,1.35)])
    ventanas.childs += [ventanas1]
    ventanas.childs += [ventanas2]
    ventanas.childs += [ventanas3]  
    ventanas.childs += [ventanas4]  

    capot = sg.SceneGraphNode('capot')
    capot.transform = tr.matmul([tr.translate(0.35,1,0),tr.scale(0.8,1,0.97)])
    capot.childs += [capot1]
    capot.childs += [capot2]
    capot.childs += [ventanas]

    scene = sg.SceneGraphNode('auto')#Teminamos ensamblando todas las partes
    scene.transform = tr.translate(0.3,0,0)
    scene.childs += [cuerpo]
    scene.childs += [ruedas]
    scene.childs += [capot]
    return scene

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800
    title = "Tarea 2"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    pipeline = ls.SimpleGouraudShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    cpuAxis = bs.createAxis(7)
    gpuAxis = es.GPUShape().initBuffers()
    mvpPipeline.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    #NOTA: Aqui creas un objeto con tu escena
    dibujo = createScene(pipeline)

    setPlot(pipeline, mvpPipeline)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        setView(pipeline, mvpPipeline)

        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawCall(gpuAxis, GL_LINES)

        #NOTA: Aquí dibujas tu objeto de escena
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(dibujo, pipeline, "model")
        

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    dibujo.clear()
    

    glfw.terminate()