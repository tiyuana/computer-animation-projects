from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import numpy as np

width = 1000
height = 800

poligoni = []  # poligoni objekta
vrhovi = []  # vrhovi objekta
stocke = []  # pocetne tocke spline krivulje
krivulja = []  # tocke svakog segmenta spline krivulje
tangente = []  # parovi tocki svih tangenti

objekt_ime = sys.argv[1]
spline_ime = sys.argv[2]

def crtajKrivulju():
    global z_k
    glPushMatrix()
    glRotatef(-40, 1, 1, 0)
    glTranslatef(5, -15, 0)
    glBegin(GL_LINE_STRIP)
    if z_k == 0:
        z_k += 1
        for j in range(0, br_stocki - 3):
            for t in np.linspace(0, 1, broj_koraka):
                T = np.array([t * t * t, t * t, t, 1])
                B = 1 / 6 * np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
                R = np.array([stocke[j], stocke[j + 1], stocke[j + 2], stocke[j + 3]])

                TB = np.dot(T, B)
                TBR = np.dot(TB, R)
                krivulja.append(TBR)

    for k in krivulja:
        glVertex3fv(k)
    glEnd()
    glPopMatrix()


def crtajTangente():
    global z_t
    glPushMatrix()
    glRotatef(-40, 1, 1, 0)
    glTranslatef(5, -15, 0)
    # glColor3f(1,1,1)
    glBegin(GL_LINES)
    if z_t == 0:
        z_t += 1
        for j in range(0, br_stocki - 3):
            for t in np.linspace(0, 1, broj_koraka):
                R = np.array([stocke[j], stocke[j + 1], stocke[j + 2], stocke[j + 3]])

                # Tocka krivulje -> 1.tocka
                T = np.array([t * t * t, t * t, t, 1])
                B = 1 / 6 * np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
                TB = np.dot(T, B)
                TBR = np.dot(TB, R)

                # Vektor tangente -> 2. tocka (ciljna orijentacija)
                T2 = np.array([t * t, t, 1])
                B2 = 1 / 2 * np.array([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]])
                TB2 = np.dot(T2, B2)
                TBR2 = np.dot(TB2, R)

                tocka = TBR
                tocka2 = tocka + 0.6 * TBR2
                tangente.append([tocka, tocka2])

    for ta in range(0, len(tangente), 3):  # crtat svaku 3. tangentu, ne sve
        glVertex3fv(tangente[ta][0])
        glVertex3fv(tangente[ta][1])
    glEnd()
    glPopMatrix()


def draw():
    global i
    global t
    global counter

    glClear(GL_COLOR_BUFFER_BIT)
    glColor3d(0.0, 0.8, 1.0)

    crtajKrivulju()
    crtajTangente()

    #CRTANJE OBJEKTA

    glPushMatrix()
    glRotatef(-40, 1, 1, 0)
    glTranslatef(5, -15, 0)

    # TRANSLACIIJA
    T = np.array([t * t * t, t * t, t, 1])
    B = 1 / 6 * np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
    R = np.array([stocke[i - 1], stocke[i], stocke[i + 1], stocke[i + 2]])
    TB = np.dot(T, B)
    TBR = np.dot(TB, R)
    # TBR = krivulja[counter]

    glTranslatef(TBR[0], TBR[1], TBR[2])

    # IZRACUN ZA ROTACIJU
    T2 = np.array([t * t, t, 1])
    B2 = 1 / 2 * np.array([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]])
    TB2 = np.dot(T2, B2)
    TBR2 = np.dot(TB2, R)
    ciljna_orijentacija = TBR2
    # ciljna_orijentacija = tangente[counter][1]

    # ROTACIJA
    os_rotacije = np.cross(pocetna_orijentacija, ciljna_orijentacija)
    se = np.dot(pocetna_orijentacija, ciljna_orijentacija)
    s_aps = np.linalg.norm(pocetna_orijentacija)
    e_aps = np.linalg.norm(ciljna_orijentacija)
    kut = np.arccos(se / (s_aps * e_aps))
    kut = np.rad2deg(kut)
    glRotatef(kut, os_rotacije[0], os_rotacije[1], os_rotacije[2])

    # CRTANJE
    glColor3f(1, 1, 0)
    if objekt_ime == "teddy.obj":
        glScale(0.15, 0.15, 0.15)  # za teddya
    else:
        glScale(3, 3, 3)  # za kocku
    glBegin(GL_LINE_LOOP)  # GL_LINE_LOOP / GL_TRIANGLES
    for p in poligoni:
        glVertex3fv(np.array(vrhovi[p[0] - 1]))
        glVertex3fv(np.array(vrhovi[p[1] - 1]))
        glVertex3fv(np.array(vrhovi[p[2] - 1]))
    glEnd()
    glPopMatrix()

    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)


def animate(nesto):
    global t
    global i
    global counter

    if t < 1 and i <= (br_stocki - 3):
        t += 1 / broj_koraka
    elif (t > 1) and i < (br_stocki - 3):
        t = 0
        i += 1
    elif t < 1 and i == (br_stocki - 3):
        t += 1 / broj_koraka
    elif t > 1 and i == (br_stocki - 3):  # za vracanje putanje na pocetak krivulje
        t = 0
        i = 1

    glutPostRedisplay()
    glutTimerFunc(20, animate, 0)

#UCITAVANJE IZ DATOTEKE

with open(objekt_ime) as objekt:
    for obj in objekt:
        obj = obj.strip().split(" ")
        if obj[0] == "v":
            vrhovi.append([float(obj[1]), float(obj[2]), float(obj[3])])
        elif obj[0] == "f":
            poligoni.append([int(obj[1]), int(obj[2]), int(obj[3])])

with open(spline_ime) as spline:
    for spl in spline:
        spl = spl.strip().split(" ")
        stocke.append([int(y) for y in spl])
br_stocki = len(stocke)

#POMOCNE VARIJABLE

broj_koraka = 35
pocetna_orijentacija = np.array([0, 0, 1])
t = 0
i = 1
z_k = 0
z_t = 0
counter = 0


# glutInit()
glutInit(sys.argv)

glutInitWindowSize(width, height)
glutInitWindowPosition(112, 84)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow("1.labos iz animacije")

glutDisplayFunc(draw)
glutReshapeFunc(reshape)
glutTimerFunc(20, animate, 0)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(90.0, float(width) / float(height), 0.1, 100.0)
glOrtho(-5.0, 15.0, -6.0, 16.0, -5.0, 60.0)
glMatrixMode(GL_MODELVIEW)
glutMainLoop()
