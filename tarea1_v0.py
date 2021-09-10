import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import sys

__author__ = "Ivan Sipiran"
__license__ = "MIT"

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4

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
    
    return numpy.array(circle, dtype = numpy.float32)
#Funcion que genera el tablero, donde x sera el largo y ancho del tablero y retorna su bs.Shape
def crear_tablero(x):
    #Se crea inicialmente un gran cuadrado blanco sobre el cual se dibujara
    tablero=[
        #positions       #colors
         -x/2, -x/2, 0.0,  1.0, 1.0, 1.0,
          x/2, -x/2, 0.0,  1.0, 1.0, 1.0,
          x/2,  x/2, 0.0,  1.0, 1.0, 1.0,

          x/2,  x/2, 0.0,  1.0, 1.0, 1.0,
         -x/2, x/2, 0.0,  1.0, 1.0, 1.0,
         -x/2, -x/2, 0.0,  1.0, 1.0, 1.0,]
    frac=x/8
    i=0
    x_position=1
    y_position=0
    #Ciclo en el que se crean los cuadrados negros
    while i<32:
        if i%4==0:
            if i==0:
                None
            else:
                y_position+=1
                x_position=1
        if y_position%2!=0:
            x_position-=1
            tablero.extend([
             -x/2 + frac*y_position, -x/2 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
             -x/2+ frac*y_position, -x/2 + x/8 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
            -x/2 + x/8+ frac*y_position, -x/2 + x/8 + frac*x_position, 0.0,  0.0, 0.0, 0.0,

            -x/2 + x/8+ frac*y_position, -x/2 + x/8 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
            -x/2 + x/8+ frac*y_position, -x/2 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
            -x/2 + frac*y_position, -x/2 + frac*x_position, 0.0,  0.0, 0.0, 0.0])
            x_position+=3

        if y_position%2 == 0:
             tablero.extend([
             -x/2 + frac*y_position, -x/2 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
             -x/2+ frac*y_position, -x/2 + x/8 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
            -x/2 + x/8+ frac*y_position, -x/2 + x/8 + frac*x_position, 0.0,  0.0, 0.0, 0.0,

            -x/2 + x/8+ frac*y_position, -x/2 + x/8 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
            -x/2 + x/8+ frac*y_position, -x/2 + frac*x_position, 0.0,  0.0, 0.0, 0.0,
            -x/2 + frac*y_position, -x/2 + frac*x_position, 0.0,  0.0, 0.0, 0.0])
             x_position+=2
        i+=1
    return numpy.array(tablero, dtype = numpy.float32)

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Tarea 1", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    dama = crear_dama(0.5,0.0, 0.0, 1.0, 0.0, 0.2)
    tablero=crear_tablero(1.0)
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

    # Each shape must be attached to a Vertex Buffer Object (VBO)
   

    vboTablero=glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vboTablero)
    glUseProgram(shaderProgram)
    glClear(GL_COLOR_BUFFER_BIT)
    glBufferData(GL_ARRAY_BUFFER, len(tablero) * SIZE_IN_BYTES, tablero, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vboTablero)

    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)
    glDrawArrays(GL_TRIANGLES, 0, int(len(tablero)/6))
    glfw.swap_buffers(window)
    
    # Waiting to close the window
    while not glfw.window_should_close(window):

        # Getting events from GLFW
        glfw.poll_events()
        
    glfw.terminate()