#!/usr/bin/python3.3

import tkinter as tk
from tkinter import *
from random import randint
from math import *

__author__ = "Pavlo Manovi"
__copyright__ ="Copyright (C) 2013 Pavlo Manovi"
__license__ = "GPL v3+"

#Here we add methods to the tkinter library to handle circles and circle arcs.
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc

#Usage of create_circle method wrappers to create circle arcs.
#
#canvas.create_circle(100, 120, 50, fill="blue", outline="#DDD", width=4)
#canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=45, end=140)
#canvas.create_circle_arc(100, 120, 48, fill="green", outline="", start=275, end=305)
#canvas.create_circle_arc(100, 120, 45, style="arc", outline="white", width=6, start=270-25, end=270+25)
#canvas.create_circle(150, 40, 20, fill="#BBB", outline="")


class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()
        self.grid()
        self.maxNodeNumber = 20
        self.maxDistance = 50

    #Sets up and places all the widgets.
    def createWidgets(self):
        self.debug = tk.Button(self)
        self.debug["text"] = "Debug!\n(Print ObjectsXY)"
        self.debug["command"] = self.debugOutput
        self.debug["fg"] = "white"
        self.debug["bg"] = "black"
        self.debug.grid(row=0, column=1, sticky=N+S+E+W)

        self.draw = tk.Button(self)
        self.draw["text"] = "Debug Canvas"
        self.draw["command"] = self.drawCanvas
        self.draw.grid(row=1, column=1, sticky=N+S+E+W)

        self.randomNodes = tk.Button(self)
        self.randomNodes["text"] = "Randomize Nodes"
        self.randomNodes["command"] = self.randomNodeGen
        self.randomNodes.grid(row=2, column=1, sticky=N+S+E+W)
        
        #Max node entry
        self.maxNodes = tk.Entry(self)
        self.maxNodes.grid(row=1, column=0, sticky=E+W, padx=250)

        self.inputInfo = Label(self, text="Min: 5, Max: 49")
        self.inputInfo.grid(row=1, column=0, sticky=W)

        self.getMaxNodes = tk.Button(self)
        self.getMaxNodes["text"] = "Set Max Nodes"
        self.getMaxNodes["command"] = self.updateMaxNodes
        self.getMaxNodes.grid(row=1, column=0, sticky=E)

        #Max distance between nodes
        self.maxDist = tk.Entry(self)
        self.maxDist.grid(row=2, column=0, sticky=E+W, padx=250)

        self.inputInfo = Label(self, text="Min: 5, Max: 49")
        self.inputInfo.grid(row=2, column=0, sticky=W)

        self.getMaxDist = tk.Button(self)
        self.getMaxDist["text"] = "Set Max Distance"
        self.getMaxDist["command"] = self.updateMaxDistance
        self.getMaxDist.grid(row=2, column=0, sticky=E)

        self.canvas = Canvas(self, width=1000, height=500, bg="white")
        self.canvas.grid(row=0, column=0, sticky=E+S)


    #debug output stuff
    def debugOutput(self):
        print(self.objectsXY)
        print("Number of objects: " + str(len(self.objectsXY)))

    #grabs input from text entry
    def updateMaxNodes(self):
        self.maxNodeNumber = int(self.maxNodes.get())

    #grabs input from text entry for distance
    def updateMaxDistance(self):
        self.maxDistance = int(self.maxDist.get())


    #Canvas drawing test, this has no real use other than debugging
    def drawCanvas(self):
        self.canvas.create_line(0, 0, 1000, 500)
        self.canvas.create_line(0, 500, 1000, 0, fill="red", dash=(4, 4))
        self.canvas.create_rectangle(50, 25, 150, 75, fill="blue")


    #Checks to see if the randomly generated x,y coordinates will overlap
    #another already existing node
    def checkForOverlapping(self, x, y):
        self.returnVal = 0
        if len(self.canvas.find_overlapping(x+15, y+15, x-15, y-15)) >= 1:
            self.returnVal = 1
            return(self.returnVal)
        else:
            return(self.returnVal)


    #Generates a random node disribution
    def randomNodeGen(self):
        self.canvas.delete(ALL)

        rand = randint(4, self.maxNodeNumber)
        self.objectsXY = [[0 for i in range(2)] for j in range(rand+1)]

        x = randint(20, 980)
        y = randint(20, 480)

        self.canvas.create_circle(x, y, 20,
            fill="#FD3", outline="black")

        self.objectsXY[0][0] = x
        self.objectsXY[0][1] = y

        for i in range(rand):
            isOverlapping = 1
            while isOverlapping:
                x = randint(20, 980)
                y = randint(20, 480)
                isOverlapping = self.checkForOverlapping(x, y)

            self.objectsXY[i+1][0] = x
            self.objectsXY[i+1][1] = y

            self.canvas.create_circle(x,
                y, 8, fill="#DDD", outline="black")

        for i in range(rand+1):
            for j in range(rand+1):
                if j > 0:
                    dist = sqrt(pow(self.objectsXY[i][0] - self.objectsXY[j][0],2)
                        + pow(self.objectsXY[i][1] - self.objectsXY[j][1],2))
                    if dist < self.maxDistance:
                        self.canvas.create_line(self.objectsXY[j][0], self.objectsXY[j][1],
                            self.objectsXY[i][0], self.objectsXY[i][1], fill="blue", dash=(2, 4))
            

class DroveNode:
    def __init__(self):
        self.nodesInView = 0
        self.nodeIDsInView = [0 for i in range(20)]

def main():
    ds = App()

    ds.master.title("Drove Network Simulator")
    ds.master.maxsize(1200, 700)

    ds.mainloop()

if __name__=='__main__':
    main()
