from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
rain_cnt = 230
speed_ofYcor = 5.0
multiplyRain = 0.0
multipyRainSpeed = 0.1
h_diagonal = 5.0
rain_lst = []
diagonal_rain = 0.0

sky_c = [0.0, 0.0, 0.0, 1.0]
sky_targetC = [0.0, 0.0, 0.0]
c_step = 0.002

cg = [0.5, 0.3, 0.0]
gc = [0.1, 0.9, 0.1]
hc = [0.95, 0.95, 0.85]
rc1 = [0.4, 0.0, 0.8]
dc = [0.1, 0.1, 1.0]
wc = [0.6, 0.8, 1.0]
rc2 = [0.4, 0.6, 1.0]

def draw_background():
    background_spread = 290.0
    
    glColor3f(sky_c[0], sky_c[1], sky_c[2])
    glBegin(GL_TRIANGLES)
    glVertex2f(0, background_spread)
    glVertex2f(500, background_spread)
    glVertex2f(500, 500)
    glVertex2f(0, background_spread)
    glVertex2f(500, 500)
    glVertex2f(0, 500)
    glEnd()

    glColor3f(cg[0], cg[1], cg[2])
    glBegin(GL_TRIANGLES)
    glVertex2f(0, 0)
    glVertex2f(500, 0)
    glVertex2f(500, background_spread)
    glVertex2f(0, 0)
    glVertex2f(500, background_spread)
    glVertex2f(0, background_spread)
    glEnd()

def draw_grass():
    green1 = [0.3, 1.0, 0.1]
    green2 = [0.1, 0.7, 0.1]
    
    glBegin(GL_TRIANGLES)
    grass_b = 25
    width_grass_b = 500 / grass_b
    
    for i in range(grass_b):
        baselineX = i * width_grass_b
        
        glColor3f(green1[0], green1[1], green1[2])
        glVertex2f(baselineX, 250)
        
        glColor3f(green1[0], green1[1], green1[2])
        glVertex2f(baselineX + width_grass_b, 250)
        
        glColor3f(green2[0], green2[1], green2[2])
        glVertex2f(baselineX + width_grass_b / 2, 280)
    
    glEnd()

def draw_house():
    glColor3f(hc[0], hc[1], hc[2])
    glBegin(GL_TRIANGLES)
    glVertex2f(150, 100)
    glVertex2f(350, 100)
    glVertex2f(350, 250)
    glVertex2f(150, 100)
    glVertex2f(350, 250)
    glVertex2f(150, 250)
    glEnd()

    glColor3f(rc1[0], rc1[1], rc1[2])
    glBegin(GL_TRIANGLES)
    glVertex2f(130, 250)
    glVertex2f(370, 250)
    glVertex2f(250, 320)
    glEnd()

    glColor3f(dc[0], dc[1], dc[2])
    glBegin(GL_TRIANGLES)
    glVertex2f(230, 100)
    glVertex2f(270, 100)
    glVertex2f(270, 180)
    glVertex2f(230, 100)
    glVertex2f(270, 180)
    glVertex2f(230, 180)
    glEnd()

    glPointSize(5)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    glVertex2f(260, 140)
    glEnd()

    draw_window(170, 150)
    draw_window(290, 150)

def draw_window(partX, partY):
    win_limit = 30
    
    glColor3f(wc[0], wc[1], wc[2])
    glBegin(GL_TRIANGLES)
    glVertex2f(partX, partY)
    glVertex2f(partX + win_limit, partY)
    glVertex2f(partX + win_limit, partY + win_limit)
    glVertex2f(partX, partY)
    glVertex2f(partX + win_limit, partY + win_limit)
    glVertex2f(partX, partY + win_limit)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(partX + win_limit / 2, partY)
    glVertex2f(partX + win_limit / 2, partY + win_limit)
    glVertex2f(partX, partY + win_limit / 2)
    glVertex2f(partX + win_limit, partY + win_limit / 2)
    glEnd()

def draw_rain():
    glLineWidth(1)
    glColor3f(rc2[0], rc2[1], rc2[2])
    glBegin(GL_LINES)
    for r in rain_lst:
        glVertex2f(r['x'], r['y'])
        glVertex2f(r['x'] + diagonal_rain * 4.0, r['y'] - 15.0)
    glEnd()

def keyboard_listener(key, x, y):
    global sky_targetC
    if key == b'd':
        sky_targetC = [0.9, 0.9, 0.9]
    elif key == b'n':
        sky_targetC = [0.0, 0.0, 0.0]
    glutPostRedisplay()    

def special_key_listener(key, x, y):
    global diagonal_rain
    if key == GLUT_KEY_LEFT:
        diagonal_rain = max(diagonal_rain - 0.2, -h_diagonal)
    elif key == GLUT_KEY_RIGHT:
        diagonal_rain = min(diagonal_rain + 0.2, h_diagonal)
    glutPostRedisplay()    

def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    draw_background()
    draw_grass()
    draw_house()
    draw_rain()
    glutSwapBuffers()

def animate():
    global sky_c, rain_lst, diagonal_rain

    diagonal = abs(diagonal_rain)
    speedofY = speed_ofYcor + diagonal * multipyRainSpeed
    ideal_rain_cnt = int(rain_cnt + diagonal * multiplyRain)

    if len(rain_lst) < ideal_rain_cnt:
        for _ in range(ideal_rain_cnt - len(rain_lst)):
            rain_lst.append({'x': random.randint(0, 500), 'y': random.randint(500, 600)})
    elif len(rain_lst) > ideal_rain_cnt:
        rain_lst = rain_lst[:ideal_rain_cnt]

    for d in rain_lst:
        d['y'] -= speedofY
        d['x'] += diagonal_rain * 2.0
        if d['y'] < 0:
            d['y'] = random.randint(500, 600)
            d['x'] = random.randint(0, 500)
        if d['x'] > 500: d['x'] = 0
        elif d['x'] < 0: d['x'] = 500

    for i in range(3):
        if abs(sky_c[i] - sky_targetC[i]) < c_step:
            sky_c[i] = sky_targetC[i]
        elif sky_c[i] < sky_targetC[i]:
            sky_c[i] += c_step
        elif sky_c[i] > sky_targetC[i]:
            sky_c[i] -= c_step

    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Raining House Project")
    
    for _ in range(rain_cnt):
        rain_lst.append({'x': random.randint(0, 500), 'y': random.randint(0, 500)})

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMainLoop()

if __name__ == "__main__":
    main()
    
    

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