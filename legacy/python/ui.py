# -*- coding: iso-8859-1 -*-
import Tkinter as tk
from Tkinter import *
from PIL import Image, ImageTk
import tkFont
import sched, time
import threading
import findPoints


# empty global variable for points from image
pointsList = list()
pointsListBackup = list()
clickedPointsList = list()
clickFlag = 0
calibratePen = "Calibrate Pen"
buttonList = list()

INFO_UEBERSCHRIFT = """
Anleitung zum Starten des FANUC-Roboters

"""
INFO_FANUC = """
 1 Licht über der Arbeitsfläche ausschalten
 2 Schutzkappe vom Stift am Roboter entfernen
 3 gewünschte Punkte auf das Whiteboard zeichnen
 
 4 Fanuc am Robotersteuerung im Handmodus starten
 5 Automatikmodus am TP starten:
    6 [Select] -> "nucberry" -> [Enter]
    7 Cursor in erste Zeile setzten
    8 per [Step] auf Einzelschritt umschalten (Symbol oben links: ->|->|)
    9 [Shift]+[FWD] -> warten bis Progamm wieder pausiert ist 
	(Roboter fährt Homeposition an)
    10 Einzelschritt wieder ausschalten
    11 Robotersteuerung auf Auto umschalten, TP auf Auto umschalten
    12 Cycle-Start Taste an Robotersteuerung drücken
"""

INFO_UI = """
 13 "Take Picture" klicken
    13.1 "Auto" klicken, um Punkte automatisch zu verbinden
   ODER
    13.2 Punkte per Hand verbinden
 14 "Move Robot" klicken, um den Roboter die Punkte anfahren zu lassen	   
"""

class FullScreenApp(object):   
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        
        height_button = 7
        width_button = 13
        
        show_img("default_infopicture.png", 1)
        
        f1 = tk.Frame(root)
        
        helv36 = tkFont.Font(family='Helvetica', size=17, weight=tkFont.BOLD)
        
        button_close = Button(f1, text="Close", font=helv36, width=width_button, height=height_button/2, command=close_click, bg="red")
        button_auto = Button(f1, text="Auto", font=helv36, width=width_button, height=height_button/2, command=clickRoboterAuto)
        button_picture = Button(f1, text="Take Picture", font=helv36,  width=width_button, height=height_button, command=picture_click)
        button_move = Button(f1, text="Move Robot", font=helv36, width=width_button, height=height_button, command=move_click)
        button_calibrate = Button(f1, text="Calibrate", font=helv36, width=width_button, height=height_button/2, command=kalibrieren_click)
        button_calibratePen = Button(f1, text="Calibrate Pen", font=helv36, width=width_button, height=height_button/2, command=kalibrierenPen_click)
        buttonList.append(button_calibratePen)
        
        f1.grid(row=0, column=1, sticky="nsew")
        button_close.grid(row=0, column=0 )
        button_picture.grid(row=1, column=0)
        button_auto.grid(row=2, column=0)
        button_move.grid(row=3, column=0)
        button_calibrate.grid(row=4, column=0)
        button_calibratePen.grid(row=5, column=0)
        
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
    
def kalibrieren_click():
    findPoints.calibrate(camera)
    
def kalibrierenPen_click():
    #global button_calibratePen
    global calibratePen
    button_calibratePen = buttonList[0]
    if(calibratePen == "Calibrate Pen"):
        button_calibratePen.config(text="Go Home")
        calibratePen = "Go Home"
        findPoints.calibratePen("zzero")
    elif(calibratePen == "Go Home"):
        button_calibratePen.config(text="Calibrate Pen")
        calibratePen = "Calibrate Pen"
        findPoints.calibratePen("home")
   
def picture_click():
    print "picture geklickt"
    canvas.delete("all")
    global pointsList
    pointsList = findPoints.run_image(camera)
    global pointsListBackup
    pointsListBackup = list(pointsList)
    del clickedPointsList[0:len(clickedPointsList)]
    show_img("output.png", 0)
    global clickFlag 
    clickFlag = 0
    
    
def move_click():
    print "move geklickt"
    if (len(clickedPointsList) > 1):
        findPoints.run_robot(clickedPointsList)
    else:
        findPoints.run_robot(pointsList)
    
    
def close_click():
    root.destroy()
    
    
def _create_circle(self, x, y, r, **kwargs):
    #print "create circle"
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle
  
def motion(event):
    if (clickFlag == 0):
        print "Click Flag:"
        print clickFlag
        x, y = event.x, event.y
        xImg = (x*(1/1.38))+290
        yImg = (y*(1/1.39))+85
        
        #print('{}, {}'.format(xImg, yImg))
        
        nextPoint = findNextPoint(xImg,yImg)
        xPoint = nextPoint[0]
        yPoint = nextPoint[1]
        
        clickedPointsList.append([xPoint,yPoint])
        print(clickedPointsList)
        xPoint = (xPoint-290)*1.38
        yPoint = (yPoint-85)*1.39
        canvas.create_circle(xPoint, yPoint, 2, fill="blue", outline="#DDD", width=2)
        listLength = len(clickedPointsList)
        if (listLength >1):
            xPoint0 = clickedPointsList[listLength-2][0]
            yPoint0 = clickedPointsList[listLength-2][1]
            #xPoint0 = (xPoint0*(1/1.38))+290
            #yPoint0 = (yPoint0*(1/1.39))+85
            xPoint0 = (xPoint0-290)*1.38
            yPoint0 = (yPoint0-85)*1.39
            print('{}, {}'.format(xPoint0, yPoint0))
            canvas.create_line(xPoint0, yPoint0, xPoint, yPoint,fill="black", width=2)
        print('{}, {}'.format(xPoint, yPoint))    
        
def findNextPoint(x,y): 
    index = findNextPointIndex(x,y)
    nextPoint = [-1,-1]
    if (index >-1):
        nextPoint[0] = pointsList[index][0]
        nextPoint[1] = pointsList[index][1]
    return nextPoint
    
def findNextPointAndDel(x,y): 
    index = findNextPointIndex(x,y)
    nextPoint = [-1,-1]
    if (index >-1):
        nextPoint[0] = pointsList[index][0]
        nextPoint[1] = pointsList[index][1]
    del pointsList[index];
    return nextPoint
    
def findNextPointIndex(x,y):
    length = sys.maxint
    index = -1
    counter = 0
    for i in pointsList:
        xP = i[0]
        yP = i[1]
        dX = abs(x-xP)
        dY = abs(y-yP)
        if (length > dX+dY):
            length = dX+dY
            index = counter
        counter = counter+1
    return index

    
def clickRoboterAuto():
    del clickedPointsList[0:len(clickedPointsList)]
    global clickFlag
    clickFlag = 1
    
    global pointsList
    pointsList = list(pointsListBackup)
    
    canvas.delete("all")
    show_img("output.png", 0)
    
    findNearNeighborPath()
    
#label = Label()
def show_img(picture, initial_call):

    #TODO Image aufnehmen
    image = Image.open(picture)
       #ScreenSize: 1024*768px
    height_image = 760
    width_image = 760
    height_button = 15
    width_button = 30
       
    half_the_width = image.size[0] / 2
    half_the_height = image.size[1] / 2
    img4 = image.crop((half_the_width - 220, half_the_height - 300, half_the_width + 330, half_the_height + 250))
    #Hoehe: 550px
    #Breite: 550px
        
    image = img4.resize((height_image, width_image), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
        
    #294,84   
    #535,535
    
    
    if(initial_call == 0): 
        canvas.image = photo #keep a reference
        canvas.bind("<Button-1>", motion)
        canvas.create_image(0, 0, image=photo, anchor = NW)
        for i in pointsList:
            xPoint = (i[0]-290)*1.38
            yPoint = (i[1]-85)*1.39
            canvas.create_circle(xPoint, yPoint, 3, fill="blue", outline="#DDD", width=3)
    else:
        canvas_id = canvas.create_text(10, 10, anchor="nw", text=INFO_UEBERSCHRIFT,  font=('Helvetica', 24))
        canvas_id = canvas.create_text(10, 100, anchor="nw", text=INFO_FANUC,  font=('Helvetica', 14))
        canvas_id = canvas.create_text(10, 450, anchor="nw", text=INFO_UI,  font=('Helvetica', 14))
    
    canvas.grid(row=0, column=0)
    
def findNearNeighborPath():
    if(len(pointsList) > 0):
        x1 = pointsList[0][0]
        y1 = pointsList[0][1]
        clickedPointsList.append([x1,y1])
        while (len(pointsList) > 0):
            nextPoint = findNextPointAndDel(x1,y1)
            xPoint = nextPoint[0]
            yPoint = nextPoint[1]
            clickedPointsList.append([xPoint,yPoint])
            xP1 = (xPoint-290)*1.38
            yP1 = (yPoint-85)*1.39
            xP2 = (x1-290)*1.38
            yP2 = (y1-85)*1.39
            
            canvas.create_line(xP1, yP1, xP2, yP2,fill="black", width=2)
            x1 = xPoint
            y1 = yPoint
    
    
    
root=tk.Tk()
root.geometry("1024x768")
root.attributes('-fullscreen', True)
canvas = tk.Canvas(root, width=760, height=760, borderwidth=0, highlightthickness=0, bg="white")

# init camera
camera = findPoints.init()

# start Window
app=FullScreenApp(root)
root.mainloop()