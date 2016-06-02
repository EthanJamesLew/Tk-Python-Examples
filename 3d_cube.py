import numpy as np
import math as mt
import tkinter as tk
import time

##Prototype--not complete or clean

class HomoCoord(np.ndarray):
    def __init__(self, *args, **kargs):
        self = self.ifTranspose()
        if self.shape[1] > 1 and self.shape[0] > 1:
            raise ValueError

        self.nonHomo = self.getCoord()

    def ifTranspose(self):
        if self.shape[1] > 1:
            self = self.transpose()
        return self

    def getCoord(self):
        self = self.ifTranspose()
        
        temp = []
        for i in range(0, self.shape[0] -1):
            temp.append(float(self[i][0])/self[self.shape[0]-1][0])
        return np.array([temp]).transpose()
        
    def __new__(cls, a):
        obj = np.asarray(a).view(cls)
        return obj

class Cube():
    def __init__(self, height):
        self.points = [[1.0]]
        self.vertices = []
        self.height = height

        self.Vertices2d = []

        self.addDim()
        self.addDim()
        self.addDim()
        self.makeVertices3d()
        self.makeVertices2d()

    def addDim(self):
        temp = []
        for i in self.points:
            temp.append([self.height/2.] + i)
            temp.append([-self.height/2.] + i)
        self.points = temp

    def makeVertices3d(self):
        self.vertices = []
        for i in self.points:
            self.vertices.append(HomoCoord(np.array([i]).transpose()))

    def transform3d(self, mat):
        temp = []
        for i in self.vertices:
            a =  HomoCoord(np.array(mat*i))
            temp.append(a)
        self.vertices = temp
        self.makeVertices2d()

    def rotZ(self, rad):
        self.transform3d(np.matrix([[mt.cos(rad),-mt.sin(rad),0,0],[mt.sin(rad),mt.cos(rad),0,0],[0,0,1.,0],[0,0,0,1.]]))

    def rotY(self, rad):
        self.transform3d(np.matrix([[mt.cos(rad),0,mt.sin(rad),0],[0,1.0,0,0],[-mt.sin(rad),0,mt.cos(rad),0],[0,0,0,1.]]))

    def rotX(self, rad):
        self.transform3d(np.matrix([[1.,0,0,0],[0,mt.cos(rad),-mt.sin(rad),0],[0,mt.sin(rad),mt.cos(rad),0],[0,0,0,1.]]))

    def makeVertices2d(self):
        self.Vertices2d = []
        camera = np.matrix([[1.,0,0,0],[0,1.,0,0],[0,0,0,0],[0,0,-.1,1.]])
        for i in self.vertices:
            a = HomoCoord(np.array(camera*i))
            self.Vertices2d.append(a.getCoord())

root = tk.Tk()
canvas = tk.Canvas(root, width=700, height=700, borderwidth=0, highlightthickness=0, bg="black")
frame = tk.Frame(root)
frame.grid(row=1,column=0)
canvas.grid(row=1,column=1)

Label1=tk.Label(frame, text="Rot X")
outlineScale = tk.Scale(frame, from_=0, to=3.14, orient=tk.HORIZONTAL, resolution=0.001)
Label1.pack(side = tk.BOTTOM)
outlineScale.pack(side = tk.BOTTOM)

Label12=tk.Label(frame, text="Rot Y")
outlineScale2 = tk.Scale(frame, from_=0, to=3.14, orient=tk.HORIZONTAL, resolution=0.001)
Label12.pack(side = tk.BOTTOM)
outlineScale2.pack(side = tk.BOTTOM)

Label13=tk.Label(frame, text="Rot Z")
outlineScale3 = tk.Scale(frame, from_=0, to=3.14, orient=tk.HORIZONTAL, resolution=0.001)
Label13.pack(side = tk.BOTTOM)
outlineScale3.pack(side = tk.BOTTOM)


coord = HomoCoord(np.array([[4],[5],[6]]))
cube = Cube(5)


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs) 
    
tk.Canvas.create_circle = _create_circle

def drawEdge(x, y):
    canvas.create_line(50*cube.Vertices2d[x-1][0][0]+350, 50*cube.Vertices2d[x-1][1][0]+350, 50*cube.Vertices2d[y-1][0][0]+350, 50*cube.Vertices2d[y-1][1][0]+350, fill="blue", width=2)

def drawEdges():
    drawEdge(1,2)
    drawEdge(1,3)
    drawEdge(5,1)
    drawEdge(6,5)
    drawEdge(2,6)
    drawEdge(2,4)
    drawEdge(6,8)
    drawEdge(7,5)
    drawEdge(8,7)
    drawEdge(7,3)
    drawEdge(4,8)
    drawEdge(3,4)


    
count = 0
drawEdges()
for i in cube.Vertices2d:
    count += 1
    canvas.create_circle(50*i[0][0]+350, 50*i[1][0]+350, 6, fill="blue", outline="#DDD", width=2)
    canvas.create_text(50*i[0][0]+350, 50*i[1][0]+350+20, text=str(count),fill = 'red', font=("Purisa", 12))

tk.Canvas.create_circle = _create_circle

rot = 0
update = 0
fps = 0
b = 0.00001
data = range(256) # 0..255
grays = (tuple(map(lambda v: "#%02x%02x%02x" % (v, v, v), data)))
points = []
for i in cube.Vertices2d:
    points.append((i[0][0],i[1][0]))
while(True):
    update += 1
    a = time.time()
    #time.sleep(1/420.)
    rot += 0.004 *(333.0/(1/b))
    cube.rotX(rot + outlineScale.get())
    cube.rotY(rot + outlineScale2.get())
    cube.rotZ(rot + outlineScale3.get())
    cube.makeVertices3d()
    canvas.delete("all")

    k = 0
    for j in points:
        k += 1
        ind = abs(int((k/len(points))*len(grays))-1)
        canvas.create_circle(50*j[0]+350, 50*j[1]+350, 1, fill=grays[ind],width=0)
    k = 0
    drawEdges()
    count = 0

    for i in cube.Vertices2d:
        count += 1
        points.append((i[0][0],i[1][0]))
        canvas.create_circle(50*i[0][0]+350, 50*i[1][0]+350, 6, fill="blue", outline="#DDD", width=2)
        canvas.create_text(50*i[0][0]+350, 50*i[1][0]+350+20, text=str(count),fill = 'red', font=("Purisa", 12))

    canvas.create_text(60, 675, text=str(fps)+ " fps",fill = 'red', font=("Purisa", 15))
    b = time.time() - a
    if update > 60:
        update = 0
        fps = int(1/b)
    if len(points) > 500:
        points = points[-500:]
    canvas.update()
