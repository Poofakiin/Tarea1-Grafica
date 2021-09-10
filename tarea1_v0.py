import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import sys

__author__ = "Benjamin Aguilar"
__license__ = "MIT"

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

#Function that generates an shape object that contains vertex and index of the board
def crear_tablero(x):
    #Vertices contains the vertex of a blank square, and indices contains the index of the same square.
    vertices=[
        #positions       #colors
        -x/2, -x/2, 0.0,  1.0, 1.0, 1.0,
         x/2, -x/2, 0.0,  1.0, 1.0, 1.0,
         x/2,  x/2, 0.0,  1.0, 1.0, 1.0,
         -x/2, x/2, 0.0,  1.0, 1.0, 1.0,]
    indices=[
        0, 1, 2,
        2, 3, 0]
    frac=x/8
    i=0
    x_position=1
    y_position=0
    multiplier=1
    #Cicle where the black squares are created
    while i<32:
        indice=multiplier*4
        #change of line in the board
        if i%4==0:
            if i==0:
                None
            else:
                y_position+=1
                x_position=1
        if y_position%2!=0:
            x_position-=1
            #we add the new vertex to the vertices array, the same goes the indexs
            vertices.extend([
            -x/2 + frac*y_position, -x/2 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
            -x/2 + frac*y_position, -x/2 + x/8 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
            -x/2 + x/8+ frac*y_position, -x/2 + x/8 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
            -x/2 + x/8+ frac*y_position, -x/2 + frac*x_position, 0.0,  0.0, 0.0, 0.0])
            indices.extend([indice, indice+1,indice+2,
                            indice+2,indice+3,indice])
            x_position+=3

        if y_position%2 == 0:
            #we add the new vertex to the vertices array, the same goes the indexs
            vertices.extend([
         -x/2 + frac*y_position, -x/2 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
             -x/2+ frac*y_position, -x/2 + x/8 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
            -x/2 + x/8+ frac*y_position, -x/2 + x/8 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
            -x/2 + x/8+ frac*y_position, -x/2 + frac*x_position, 0.0,  0.0, 0.0, 0.0])
            indices.extend([indice, indice+1,indice+2,
                            indice+2,indice+3,indice])
            x_position+=2
        i+=1
        multiplier+=1
    #the function return a shape object
    return bs.Shape(vertices,indices)

#Function that creates 1 single 'checker', it take x,y positions, r,g,b colors and radius, and returns an array with the vertex
def crear_dama(x,y,r,g,b,radius):
    
    circle = []
    for angle in range(0,360,10):
        circle.extend([x, y, 0.0, r, g, b])
        circle.extend([x+numpy.cos(numpy.radians(angle))*radius, 
                       y+numpy.sin(numpy.radians(angle))*radius, 
                       0.0, r, g, b])
        circle.extend([x+numpy.cos(numpy.radians(angle+10))*radius, 
                       y+numpy.sin(numpy.radians(angle+10))*radius, 
                       0.0, r, g, b])
    
    return circle
#Function that creates the total of 24 checkers. It returns a numpy array with the vertexs
def crear_damas_totales():
    damas=[]
    x_roj= (-0.4375)
    y_roj= (0.4375)
    radio= (0.0625)
    #Red checkers
    for i in range(12):
        #Change of line in the board
        if i%4==0:
            if i==0:
                None
            else:
                y_roj-=0.125
                x_roj=-0.4375
        if i>=4 and i<=7:
            x_roj+=0.125
            damas.extend(crear_dama(x_roj,y_roj,1,0,0,radio))
            x_roj+=0.125
            i+=1

        else:
            damas.extend(crear_dama(x_roj,y_roj,1,0,0,radio))
            x_roj+=0.25
            i+=1
        
    x_azul=-0.3125
    y_azul=-0.4375
    #Green checkers
    for i in range(12):
        #Change of line in the board
        if i%4==0:
            if i==0:
                None
            else:
                y_azul+=0.125
                x_azul=-0.3125

        if i>=4 and i<=7:
            x_azul-=0.125
            damas.extend(crear_dama(x_azul,y_azul,0,0,1,radio))
            x_azul+=0.375
            i+=1

        else:
            damas.extend(crear_dama(x_azul,y_azul,0,0,1,radio))
            x_azul+=0.25
            i+=1
        
    return numpy.array(damas, dtype = numpy.float32)

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        window= None
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Tarea 1", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)
    # Defining shaders for our pipeline
    vertex_shader = """
    #version 330
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
    #version 330
    in vec3 newColor;

    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """

    # Binding artificial vertex array object for validation
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))
    #We'll create the shapes on GPU with 2 diferents methods(they're the same), first we'll use easy_shaders.py functions to create board shape,
    #and then we'll use the gl defaults funcitons to create the checkers shape.


    # Creating board shape on GPU memory using easy_shaders
    pipeline=es.SimpleShaderProgram()
    glUseProgram(pipeline.shaderProgram) 
    shapeQuad = crear_tablero(1.0)
    gpuQuad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuQuad)
    gpuQuad.fillBuffers(shapeQuad.vertices, shapeQuad.indices, GL_STATIC_DRAW)

    ##########
    glClearColor(0.15, 0.15, 0.15, 1.0)

    #Creating checkers shapes on GPU memory
    damas = crear_damas_totales()
    vboDama = glGenBuffers(1)
    
    glBindBuffer(GL_ARRAY_BUFFER, vboDama)
    glBufferData(GL_ARRAY_BUFFER, len(damas) * SIZE_IN_BYTES, damas, GL_STATIC_DRAW)

    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.5,0.5, 0.5, 1.0)

    glClear(GL_COLOR_BUFFER_BIT)

    glBindBuffer(GL_ARRAY_BUFFER, vboDama)
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)
    
    # It renders a scene using the active shader program (pipeline) and the active VAO (shapes)
    

    # Moving our draw to the active color buffer
    glfw.swap_buffers(window)

    # Waiting to close the window
    while not glfw.window_should_close(window):

        # Getting events from GLFW
        glfw.poll_events()
        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Drawing the board
        pipeline.drawCall(gpuQuad)

        #Drawing the checkers
        glDrawArrays(GL_TRIANGLES, 0, int(len(damas)/6))


        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuQuad.clear()

    glfw.terminate()
