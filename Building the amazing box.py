from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
points_lst = []
adjust_speed = 1.0
blinking_flag = False
stop_flag = False
blink_cnt = 0

Above = 248
Below = -248
Right = 248
Left = -248

def convert_coordinate(x, y):
    a = x - (WINDOW_WIDTH / 2)
    b = (WINDOW_HEIGHT / 2) - y
    return a, b

def draw_boundary_define():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(Left, Above)
    glVertex2f(Right, Above)
    glVertex2f(Left, Below)
    glVertex2f(Right, Below)
    glVertex2f(Left, Above)
    glVertex2f(Left, Below)
    glVertex2f(Right, Above)
    glVertex2f(Right, Below)
    glEnd()

def draw_point():
    global blink_cnt
    
    visible_set = (blink_cnt % 60) < 30
    
    glPointSize(5)
    glBegin(GL_POINTS)
    
    for dots in points_lst:
        if blinking_flag and not visible_set:
            glColor3f(0.0, 0.0, 0.0)
        else:
            glColor3f(dots['color'][0], dots['color'][1], dots['color'][2])
        
        glVertex2f(dots['x'], dots['y'])
    
    glEnd()

def keyboard_listener(key, x, y):
    global stop_flag
    
    if key == b' ':
        stop_flag = not stop_flag
        if stop_flag:
            print("Animation is Stopped")
        else:
            print("Animation started Moving")
    glutPostRedisplay()        

def special_key_listener(key, x, y):
    global adjust_speed
    
    if stop_flag:
        print("Animation is stopped, Speed remains same.")
        return

    if key == GLUT_KEY_UP:
        adjust_speed *= 1.5
        print("Speed increased")
    elif key == GLUT_KEY_DOWN:
        adjust_speed /= 1.5
        print("Speed decreased")
    glutPostRedisplay()    

def mouse_listener(button, state, x, y):
    global blinking_flag
    
    if stop_flag:
        print("Animation is Stopped, mouse clicks disabled.")
        return
        
    if state == GLUT_DOWN:
        if button == GLUT_LEFT_BUTTON:
            blinking_flag = not blinking_flag
            if blinking_flag:
                print("Blinking ON")
            else:
                print("Blinking OFF")
        
        elif button == GLUT_RIGHT_BUTTON:
            ball_x, ball_y = convert_coordinate(x, y)
            
            create_points = {
                'x': ball_x,
                'y': ball_y,
                'dx': random.choice([-1, 1]),
                'dy': random.choice([-1, 1]),
                'color': [random.random(), random.random(), random.random()]
            }
            points_lst.append(create_points)
            print(f"New point created at ({ball_x}, {ball_y})")

def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -250, 250, 0, 1)
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    draw_boundary_define()
    draw_point()

    glutSwapBuffers()

def animate():
    global blink_cnt
    
    if stop_flag:
        glutPostRedisplay()
        return

    if blinking_flag:
        blink_cnt += 1

    for dots in points_lst:
        dots['x'] += dots['dx'] * adjust_speed
        dots['y'] += dots['dy'] * adjust_speed
        
        if dots['x'] > Right or dots['x'] < Left:
            dots['dx'] *= -1
        
        if dots['y'] > Above or dots['y'] < Below:
            dots['dy'] *= -1
            
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Project Task2")

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()

if __name__ == "__main__":
    main()   