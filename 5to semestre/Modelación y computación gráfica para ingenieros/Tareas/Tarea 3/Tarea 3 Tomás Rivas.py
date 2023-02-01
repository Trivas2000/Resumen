# coding=utf-8
"""Tarea 3"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath
from operator import add

__author__ = "Ivan Sipiran"
__license__ = "MIT"

#Tarea 3 Modelación y computación grafica
#Alumno Tomás Rivas
#Rut 20.592.350-0
#Por favor leer el readme adjunto


#Las nuevas variables guardan:
#CarChangeX: el cambio que se está generando en la posición X del auto
#CarChangeZ: el cambio que se está generando en la posición Z del auto
#CarChangeAngle: el cambio que se está generando en el angulo del auto con respecto al eje Y
#CarAngle: El angulo actual del auto con respecto al eje Y
#CarZ: La posición actual del auto en Z
#CarX: La posición actual del auto en X


class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.viewPos = np.array([12,12,12])
        self.at = np.array([0,0,0])
        self.camUp = np.array([0, 1, 0])
        self.distance = 20
        self.CarChangeX = 0
        self.CarChangeZ = 0
        self.CarAngleChange = 0
        self.CarAngle = 0
        self.CarZ=0
        self.CarX=0
        
        
controller = Controller()

def setPlot(texPipeline, axisPipeline, lightPipeline):
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    glUseProgram(axisPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "lightPosition"), 5, 5, 5)
    
    glUniform1ui(glGetUniformLocation(lightPipeline.shaderProgram, "shininess"), 1000)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "constantAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "linearAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

def setView(texPipeline, axisPipeline, lightPipeline,view):
    
    glUseProgram(axisPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1], controller.viewPos[2])
    

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
    
    
def createOFFShape(pipeline, filename, r,g, b):
    shape = readOFF(getAssetPath(filename), (r, g, b))
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape

def readOFF(filename, color):
    vertices = []
    normals= []
    faces = []

    with open(filename, 'r') as file:
        line = file.readline().strip()
        assert line=="OFF"

        line = file.readline().strip()
        aux = line.split(' ')

        numVertices = int(aux[0])
        numFaces = int(aux[1])

        for i in range(numVertices):
            aux = file.readline().strip().split(' ')
            vertices += [float(coord) for coord in aux[0:]]
        
        vertices = np.asarray(vertices)
        vertices = np.reshape(vertices, (numVertices, 3))
        print(f'Vertices shape: {vertices.shape}')

        normals = np.zeros((numVertices,3), dtype=np.float32)
        print(f'Normals shape: {normals.shape}')

        for i in range(numFaces):
            aux = file.readline().strip().split(' ')
            aux = [int(index) for index in aux[0:]]
            faces += [aux[1:]]
            
            vecA = [vertices[aux[2]][0] - vertices[aux[1]][0], vertices[aux[2]][1] - vertices[aux[1]][1], vertices[aux[2]][2] - vertices[aux[1]][2]]
            vecB = [vertices[aux[3]][0] - vertices[aux[2]][0], vertices[aux[3]][1] - vertices[aux[2]][1], vertices[aux[3]][2] - vertices[aux[2]][2]]

            res = np.cross(vecA, vecB)
            normals[aux[1]][0] += res[0]  
            normals[aux[1]][1] += res[1]  
            normals[aux[1]][2] += res[2]  

            normals[aux[2]][0] += res[0]  
            normals[aux[2]][1] += res[1]  
            normals[aux[2]][2] += res[2]  

            normals[aux[3]][0] += res[0]  
            normals[aux[3]][1] += res[1]  
            normals[aux[3]][2] += res[2]  
        #print(faces)
        norms = np.linalg.norm(normals,axis=1)
        normals = normals/norms[:,None]

        color = np.asarray(color)
        color = np.tile(color, (numVertices, 1))

        vertexData = np.concatenate((vertices, color), axis=1)
        vertexData = np.concatenate((vertexData, normals), axis=1)

        print(vertexData.shape)

        indices = []
        vertexDataF = []
        index = 0

        for face in faces:
            vertex = vertexData[face[0],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[1],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[2],:]
            vertexDataF += vertex.tolist()
            
            indices += [index, index + 1, index + 2]
            index += 3        



        return bs.Shape(vertexDataF, indices)

def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape

def createTexturedArc(d):
    vertices = [d, 0.0, 0.0, 0.0, 0.0,
                d+1.0, 0.0, 0.0, 1.0, 0.0]
    
    currentIndex1 = 0
    currentIndex2 = 1

    indices = []

    cont = 1
    cont2 = 1

    for angle in range(4, 185, 5):
        angle = np.radians(angle)
        rot = tr.rotationY(angle)
        p1 = rot.dot(np.array([[d],[0],[0],[1]]))
        p2 = rot.dot(np.array([[d+1],[0],[0],[1]]))

        p1 = np.squeeze(p1)
        p2 = np.squeeze(p2)
        
        vertices.extend([p2[0], p2[1], p2[2], 1.0, cont/4])
        vertices.extend([p1[0], p1[1], p1[2], 0.0, cont/4])
        
        indices.extend([currentIndex1, currentIndex2, currentIndex2+1])
        indices.extend([currentIndex2+1, currentIndex2+2, currentIndex1])

        if cont > 4:
            cont = 0


        vertices.extend([p1[0], p1[1], p1[2], 0.0, cont/4])
        vertices.extend([p2[0], p2[1], p2[2], 1.0, cont/4])

        currentIndex1 = currentIndex1 + 4
        currentIndex2 = currentIndex2 + 4
        cont2 = cont2 + 1
        cont = cont + 1

    return bs.Shape(vertices, indices)

def createTiledFloor(dim):
    vert = np.array([[-0.5,0.5,0.5,-0.5],[-0.5,-0.5,0.5,0.5],[0.0,0.0,0.0,0.0],[1.0,1.0,1.0,1.0]], np.float32)
    rot = tr.rotationX(-np.pi/2)
    vert = rot.dot(vert)

    indices = [
         0, 1, 2,
         2, 3, 0]

    vertFinal = []
    indexFinal = []
    cont = 0

    for i in range(-dim,dim,1):
        for j in range(-dim,dim,1):
            tra = tr.translate(i,0.0,j)
            newVert = tra.dot(vert)

            v = newVert[:,0][:-1]
            vertFinal.extend([v[0], v[1], v[2], 0, 1])
            v = newVert[:,1][:-1]
            vertFinal.extend([v[0], v[1], v[2], 1, 1])
            v = newVert[:,2][:-1]
            vertFinal.extend([v[0], v[1], v[2], 1, 0])
            v = newVert[:,3][:-1]
            vertFinal.extend([v[0], v[1], v[2], 0, 0])
            
            ind = [elem + cont for elem in indices]
            indexFinal.extend(ind)
            cont = cont + 4

    return bs.Shape(vertFinal, indexFinal)

#Le agregamos 2 parámetros que representen el índice de la Wall texture y el roof texture; esto se hace sumando 
#una versión str del índice.
def createHouse(pipeline,wallIndex,roofIndex):

    #Creamos las figuras de base con sus respectivas texturas
    wallBaseShape = createGPUShape(pipeline, bs.createTextureQuad(1.0, 1.0))
    wallBaseShape.texture = es.textureSimpleSetup(
        getAssetPath("wall"+str(wallIndex)+".jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)

    roofBaseShape = createGPUShape(pipeline, bs.createTextureQuad(1.0, 1.0))
    roofBaseShape.texture = es.textureSimpleSetup(
        getAssetPath("roof"+str(roofIndex)+".jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)
    

    #Wall es el nodo base, y los 3 siguientes son sus rotaciones para completar las 
    # 4 paredes, estos los agrupamos en un nodo walls

    wall = sg.SceneGraphNode('wall')
    wall.transform = tr.translate(0.0,0.0,0.5)
    wall.childs += [wallBaseShape]

    wall_1 = sg.SceneGraphNode('wall_1')
    wall_1.transform = tr.rotationY(np.pi/2)
    wall_1.childs += [wall]

    wall_2 = sg.SceneGraphNode('wall_2')
    wall_2.transform = tr.rotationY(np.pi)
    wall_2.childs += [wall]

    wall_3 = sg.SceneGraphNode('wall_3')
    wall_3.transform = tr.rotationY(np.pi*3/2)
    wall_3.childs += [wall]

    walls = sg.SceneGraphNode('walls')
    walls.childs+=[wall]
    walls.childs+=[wall_1]
    walls.childs+=[wall_2]
    walls.childs+=[wall_3]

    #Roof es el nodo base del techo, a partir de este generamos 2 piezas rotadas que harán 
    #la parte superior del techo identificadas con Top y 2 laterales identificadas con side que
    #tapan los huecos entre el techo y las paredes. Todo esto agrupado en completeRoof.
    roof = sg.SceneGraphNode('roof')    
    roof.childs += [roofBaseShape]

    roofTop_1 = sg.SceneGraphNode('RoofTop_1')
    roofTop_1.transform = tr.matmul([tr.translate(0.0,0.7,-0.3),tr.rotationX(np.pi/4)])
    roofTop_1.childs += [roof]

    roofTop_2 = sg.SceneGraphNode('RoofTop_2')
    roofTop_2.transform = tr.matmul([tr.translate(0.0,0.7,0.3),tr.rotationX(-np.pi/4)])
    roofTop_2.childs += [roof]

    roofSide_1 = sg.SceneGraphNode('RoofSide_1')
    roofSide_1.transform = tr.matmul([tr.uniformScale(0.7),tr.translate(0.7,0.71,0),tr.rotationX(-np.pi/4),tr.rotationY(np.pi/2)])
    roofSide_1.childs += [roof]

    roofSide_2 = sg.SceneGraphNode('RoofSide_2')
    roofSide_2.transform = tr.matmul([tr.uniformScale(0.7),tr.translate(-0.7,0.71,0),tr.rotationX(-np.pi/4),tr.rotationY(np.pi/2)])
    roofSide_2.childs += [roof]


    completeRoof = sg.SceneGraphNode('completeRoof')    
    completeRoof.childs += [roofTop_1]
    completeRoof.childs += [roofTop_2]
    completeRoof.childs += [roofSide_1]
    completeRoof.childs += [roofSide_2]

    #Finalmente house es walls con complete roofs y retornamos este nodo.
    house = sg.SceneGraphNode('house')
    house.transform = tr.translate(0,0.2,0)
    house.childs+=[walls]
    house.childs+=[completeRoof]
    

    return house

# Le agregamos el parámetro length que representa cuantos cuadrados unidos formaran el Wall 
# y texture que es el nombre de la textura a usar.

def createWall(pipeline,length,texture):
    #Creamos la figura de base
    wallBase = createGPUShape(pipeline, bs.createTextureQuad(1.0, 1.0))
    wallBase.texture = es.textureSimpleSetup(
        getAssetPath(texture), GL_REPEAT, GL_REPEAT, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)

    #Final Wall es el nodo que retornaremos y con un for vamos agregándole nodos de Wall 
    # rotados para ensamblarse y trasladados para que no se solapen, finalmente retornamos finalWall
    finalWall=sg.SceneGraphNode('finalWall')
    for i in range(length):
        wall=sg.SceneGraphNode("wall"+str(i))
        wall.transform=tr.matmul([tr.translate(0,0,1*i),tr.rotationY(np.pi/2)])
        wall.childs+=[wallBase]
        finalWall.childs+=[wall]
    return finalWall


# TAREA3: Esta función crea un grafo de escena especial para el auto.
def createCarScene(pipeline):
    chasis = createOFFShape(pipeline, 'alfa2.off', 1.0, 0.0, 0.0)
    wheel = createOFFShape(pipeline, 'wheel.off', 0.0, 0.0, 0.0)

    scale = 2.0
    rotatingWheelNode = sg.SceneGraphNode('rotatingWheel')
    rotatingWheelNode.childs += [wheel]

    chasisNode = sg.SceneGraphNode('chasis')
    chasisNode.transform = tr.uniformScale(scale)
    chasisNode.childs += [chasis]

    wheel1Node = sg.SceneGraphNode('wheel1')
    wheel1Node.transform = tr.matmul([tr.uniformScale(scale),tr.translate(0.056390,0.037409,0.091705)])
    wheel1Node.childs += [rotatingWheelNode]

    wheel2Node = sg.SceneGraphNode('wheel2')
    wheel2Node.transform = tr.matmul([tr.uniformScale(scale),tr.translate(-0.060390,0.037409,-0.091705)])
    wheel2Node.childs += [rotatingWheelNode]

    wheel3Node = sg.SceneGraphNode('wheel3')
    wheel3Node.transform = tr.matmul([tr.uniformScale(scale),tr.translate(-0.056390,0.037409,0.091705)])
    wheel3Node.childs += [rotatingWheelNode]

    wheel4Node = sg.SceneGraphNode('wheel4')
    wheel4Node.transform = tr.matmul([tr.uniformScale(scale),tr.translate(0.066090,0.037409,-0.091705)])
    wheel4Node.childs += [rotatingWheelNode]


    car1 = sg.SceneGraphNode('car1')
    car1.transform = tr.rotationY(np.pi)
    car1.childs += [chasisNode]
    car1.childs += [wheel1Node]
    car1.childs += [wheel2Node]
    car1.childs += [wheel3Node]
    car1.childs += [wheel4Node]

    scene = sg.SceneGraphNode('system')
    scene.childs += [car1]

    return scene

# TAREA3: Esta función crea toda la escena estática y texturada de esta aplicación.
# Por ahora ya están implementadas: la pista y el terreno
# En esta función debes incorporar las casas y muros alrededor de la pista

def createStaticScene(pipeline):

    #Creamos la figura base de sky para hacer el cielo
    skyBaseShape = createGPUShape(pipeline, bs.createTextureQuad(1.0, 1.0))
    skyBaseShape.texture = es.textureSimpleSetup(
        getAssetPath("sky horizon.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)
    
    roadBaseShape = createGPUShape(pipeline, bs.createTextureQuad(1.0, 1.0))
    roadBaseShape.texture = es.textureSimpleSetup(
        getAssetPath("Road_001_basecolor.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)

    sandBaseShape = createGPUShape(pipeline, createTiledFloor(50))
    sandBaseShape.texture = es.textureSimpleSetup(
        getAssetPath("Sand 002_COLOR.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)

    arcShape = createGPUShape(pipeline, createTexturedArc(1.5))
    arcShape.texture = roadBaseShape.texture
    
    roadBaseNode = sg.SceneGraphNode('plane')
    roadBaseNode.transform = tr.rotationX(-np.pi/2)
    roadBaseNode.childs += [roadBaseShape]

    arcNode = sg.SceneGraphNode('arc')
    arcNode.childs += [arcShape]

    sandNode = sg.SceneGraphNode('sand')
    sandNode.transform = tr.translate(0.0,-0.1,0.0)
    sandNode.childs += [sandBaseShape]

    linearSector = sg.SceneGraphNode('linearSector')
        
    for i in range(10):
        node = sg.SceneGraphNode('road'+str(i)+'_ls')
        node.transform = tr.translate(0.0,0.0,-1.0*i)
        node.childs += [roadBaseNode]
        linearSector.childs += [node]

    linearSectorLeft = sg.SceneGraphNode('lsLeft')
    linearSectorLeft.transform = tr.translate(-2.0, 0.0, 5.0)
    linearSectorLeft.childs += [linearSector]

    linearSectorRight = sg.SceneGraphNode('lsRight')
    linearSectorRight.transform = tr.translate(2.0, 0.0, 5.0)
    linearSectorRight.childs += [linearSector]

    arcTop = sg.SceneGraphNode('arcTop')
    arcTop.transform = tr.translate(0.0,0.0,-4.5)
    arcTop.childs += [arcNode]

    arcBottom = sg.SceneGraphNode('arcBottom')
    arcBottom.transform = tr.matmul([tr.translate(0.0,0.0,5.5), tr.rotationY(np.pi)])
    arcBottom.childs += [arcNode]
    
    #Creamos 3 casas diferentes con distintos índices para diferentes diseños y las juntamos en houses
    house1=createHouse(pipeline,3,2)

    house2=createHouse(pipeline,4,1)
    house2.transform=tr.matmul([house2.transform,tr.translate(0,0,3)])

    house3=createHouse(pipeline,2,3)
    house3.transform=tr.matmul([house3.transform,tr.translate(0,0,-3)])

    house4=createHouse(pipeline,1,4)
    house4.transform=tr.matmul([house3.transform,tr.translate(5,0,0)])

    house5=createHouse(pipeline,5,5)
    house5.transform=tr.matmul([house3.transform,tr.translate(-5,0,6)])

    houses = sg.SceneGraphNode('houses')
    houses.childs += [house1]
    houses.childs += [house2]
    houses.childs += [house3]
    houses.childs += [house4]
    houses.childs += [house5]

    #Creamos un muro base y a partir de este 4 muros rectos que rodeen la pista de carreras, los agrupamos en walls
    wall=createWall(pipeline,11,"wall5.jpg")
    wall.transform=tr.matmul([wall.transform,tr.translate(0,-0.2,-4.5)])

    wall1=sg.SceneGraphNode('wall1')
    wall1.transform=tr.translate(2.5,0,0)
    wall1.childs+=[wall]
    
    wall2=sg.SceneGraphNode('wall2')
    wall2.transform=tr.translate(-2.5,0,0)
    wall2.childs+=[wall]

    wall3=sg.SceneGraphNode('wall3')
    wall3.transform=tr.translate(1.5,0,0)
    wall3.childs+=[wall]
    
    wall4=sg.SceneGraphNode('wall4')
    wall4.transform=tr.translate(-1.5,0,0)
    wall4.childs+=[wall]

    walls=sg.SceneGraphNode('walls')
    walls.childs+=[wall1]
    walls.childs+=[wall2]
    walls.childs+=[wall3]
    walls.childs+=[wall4]
    
    #Creamos 4 sky para hacer los 4 bordes tal como los muros en la parte de house y 
    #los agrupamos en el nodo sky
    sky1 = sg.SceneGraphNode('sky1')
    sky1.transform= tr.matmul([tr.uniformScale(100),tr.translate(0,0.1,-0.5)])
    sky1.childs+=[skyBaseShape]

    sky2 = sg.SceneGraphNode('sky2')
    sky2.transform= tr.rotationY(np.pi/2)
    sky2.childs+=[sky1]

    sky3 = sg.SceneGraphNode('sky3')
    sky3.transform= tr.rotationY(np.pi)
    sky3.childs+=[sky1]

    sky4 = sg.SceneGraphNode('sky4')
    sky4.transform= tr.rotationY(np.pi*3/2)
    sky4.childs+=[sky1]

    sky = sg.SceneGraphNode('sky')
    sky.childs+=[sky1]
    sky.childs+=[sky2]
    sky.childs+=[sky3]
    sky.childs+=[sky4]

    #Creamos la base del pasto reutilizando la función createWall, pero tendremos que rotar 
    # la figura para que este en la orientación del piso.
    baseGrass=createWall(pipeline,14,"grass_texture.jpg")
    
    grass1= sg.SceneGraphNode('grass1')
    grass1.transform= tr.matmul([tr.translate(0,-0.02,-6.3),tr.rotationZ(np.pi/2)])
    grass1.childs+=[baseGrass]

    grass2= sg.SceneGraphNode('grass2')
    grass2.transform= tr.matmul([tr.translate(1,-0.02,-6),tr.rotationZ(np.pi/2)])
    grass2.childs+=[baseGrass]

    grass3= sg.SceneGraphNode('grass3')
    grass3.transform= tr.matmul([tr.translate(-1,-0.02,-6),tr.rotationZ(np.pi/2)])
    grass3.childs+=[baseGrass]

    #Unimos los 3 grass que conforman el piso en un nodo grass
    grass = sg.SceneGraphNode('grass')
    grass.childs+=[grass1]
    grass.childs+=[grass2]
    grass.childs+=[grass3]
    
    #Juntamos todo en el nodo scene
    scene = sg.SceneGraphNode('system')
    scene.childs += [linearSectorLeft]
    scene.childs += [linearSectorRight]
    scene.childs += [arcTop]
    scene.childs += [arcBottom]
    scene.childs += [sandNode]
    scene.childs += [houses]
    scene.childs += [sky]
    scene.childs += [walls]
    scene.childs += [grass]
    
    return scene


if __name__ == "__main__":

        # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 800
    height = 800
    title = "Tarea 3 Tomas Rivas"
    window = glfw.create_window(width, height, title, None, None)
   
    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    axisPipeline = es.SimpleModelViewProjectionShaderProgram()
    texPipeline = es.SimpleTextureModelViewProjectionShaderProgram()
    lightPipeline = ls.SimpleGouraudShaderProgram()
    
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
    dibujo = createStaticScene(texPipeline)
    car =createCarScene(lightPipeline)

    setPlot(texPipeline, axisPipeline,lightPipeline)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)
    #Definimos los valores iniciales de la cámara y el auto, initial position es 
    # una transformación que se usara 1 sola vez para llevar al auto a su lugar y counter 
    # se encarga de esto.

    controller.viewPos=np.array([2.0, 1,9])
    controller.at=np.array([2.0, -0.037409,5])
    view = tr.lookAt(controller.viewPos,controller.at,controller.camUp)

    controller.CarX=2
    controller.CarZ=5
    initialPosition=tr.translate(2.0, -0.037409, 5.0)
    counter=1

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

        #En W modificamos el cambio del auto con respecto al eje z y su posición considerando el ángulo.
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            controller.CarChangeZ = (-0.015)

            controller.CarZ-=0.015*np.cos(controller.CarAngle)
            controller.CarX-=0.015*np.sin(controller.CarAngle)

        #Este else se encarga de frenar el auto cuando no se está apretando w   
        else:
            if(controller.CarChangeZ < 0):
                controller.CarChangeZ = max(controller.CarChangeZ-0.0001, 0)

        #Para S aplicamos lo mismo que W solo que con un valor menor para que retroceda mas lento y en la condición que 
        # no esté apretado W para que tenga prioridad si estamos avanzando el auto
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS and not glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            controller.CarChangeZ = (0.005)
            controller.CarZ+=0.005*np.cos(controller.CarAngle)
            controller.CarX+=0.005*np.sin(controller.CarAngle)
            controller.viewPos[2]+=(0.005)
            
        else:
            if(controller.CarChangeZ > 0):
                controller.CarChangeZ = max(controller.CarChangeZ-0.0001, 0)

        #Para A le damos un ángulo de cambio positivo y actualizamos el CarAngle    
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            controller.CarAngleChange=+0.004
            controller.CarAngle+=controller.CarAngleChange
       
        
        #Para D le damos un ángulo de cambio negativo y actualizamos el CarAngle    
        elif glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            controller.CarAngleChange=-0.004
            controller.CarAngle+=controller.CarAngleChange

        #Si no usamos ni A ni D que el ángulo de giro sea 0
        else:
            controller.CarAngleChange=0

        #Cambiamos el viewpos en función de la posición del auto, esto se usando coordenadas polares, 
        # por otro el lado el at siempre apuntara al auto. Redefinimos view. 
        controller.viewPos=np.array([controller.CarX+4*np.sin(controller.CarAngle),1,controller.CarZ+4*np.cos(controller.CarAngle)])
        controller.at=np.array([controller.CarX,-0.037409,controller.CarZ])
        view = tr.lookAt(controller.viewPos,controller.at,controller.camUp)
        

        setView(texPipeline, axisPipeline, lightPipeline,view)

        #NOTA: Aquí dibujas tu objeto de escena
        glUseProgram(texPipeline.shaderProgram)
        sg.drawSceneGraphNode(dibujo, texPipeline, "model")

        glUseProgram(lightPipeline.shaderProgram)

        # Redefinimos la transformación del auto de manera acumulativa usando la transformación previa. 
        # Es importante aquí que primero rotamos en Y; y que la transformación initialPosition solo 
        # funciona 1 vez y luego toma el valor tr.translate(0,0,0). Además trasladamos en base a los 
        # cambios previamente definidos en X y Z. Otra forma de poder haber hecho esto hubiera sido 
        # con CarX y CarZ pero en ese caso tendríamos que obviar la transformación que estaba hecha 
        # antes de este punto.
        car.transform=tr.matmul([car.transform,tr.translate(controller.CarChangeX,0,controller.CarChangeZ),initialPosition,tr.rotationY(controller.CarAngleChange)])
        sg.drawSceneGraphNode(car, lightPipeline, "model")

        #Código para que la transformación inicial funcione 1 sola vez
        if counter==1:
            initialPosition=tr.translate(0,0,0)
            counter-=1

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    dibujo.clear()
    

    glfw.terminate()