from OpenGL.GL import *
import numpy as np
import grafica.transformations as tr
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

#TAREA4: Esta función ejemplifica cómo podemos crear luces para nuestra escena. En este caso creamos 2 luces con diferentes 
# parámetros
spotlightsPool = dict()
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
    width = 800
    height = 800
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



#TAREA4: modificamos esta función para poder configurar todas las luces del pool
def setPlot(texPipeline, axisPipeline, lightPipeline):
    width = 800
    height = 800
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