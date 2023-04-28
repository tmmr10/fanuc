# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import os
import socket
import Queue

#=====================================================================

width = 1024
height = 768
threshold = 70

host = "192.168.125.10"
port = 59002
addr = (host, port)
BUFFER_SIZE = 1024
PACKET_SIZE = 5

z_paint = 0
z_move = -5

# Kalibrierungs-Punkte
xk1 = -90.0
yk1 = -90.0
xk2 = 90.0
yk2 = 90.0

# Home-Punkt
xh = 10
yh = -150
zh = -45

#=====================================================================
def loadConfig():

    if os.path.isfile("findPoints.conf"):
        with open("findPoints.conf", "r") as configFile:
            data = configFile.readlines()
            for line in data:
                line = ''.join(line.split()) #entferne moegliche whitespaces
                if line.startswith("x0"):
                    line = line.replace("x0=", "")
                    x0 = float(line)
                elif line.startswith("y0"):
                    line = line.replace("y0=", "")
                    y0 = float(line)
                elif line.startswith("fx"):
                    line = line.replace("fx=", "")
                    fx = float(line)
                elif line.startswith("fy"):
                    line = line.replace("fy=", "")
                    fy = float(line)
                else:
                    print("Check findPoints.conf")
    else:
        print("No findPoints.conf found.")
        
    return (x0, y0, fx, fy)

            #print("x: "+str(x0)+"y: "+str(y0)+"fx: "+str(fx)+"fy: "+str(fy))
#=====================================================================

def writeConfig(x0, y0, fx, fy):
    with open("findPoints.conf", "w") as configFile:
        configFile.write("x0 = "+str(x0)+"\ny0 = "+str(y0)+"\nfx = "+str(fx)+"\nfy = "+str(fy)+"\n")

#=====================================================================

def calibrate(camera):
    # TODO fix format
    global coordList
    coordList = list()

    coordList.append([xk1,yk1, z_move])
    coordList.append([xk1,yk1, z_paint])
    coordList.append([xk1,yk1, z_move])
    
    coordList.append([xk2,yk2, z_move])
    coordList.append([xk2,yk2, z_paint])
    coordList.append([xk2,yk2, z_move])
    
    coordList.append([xh, yh, zh])
    
    sendToRobot(coordList)

    binary = takePicture(camera)
    pointList = floodfill(binary)
    print("Anzahl Punkte = 2?: "+ str(len(pointList)))

    dx = xk2-xk1
    dy = yk2-yk1

    kx1 = pointList[0][0]
    ky1 = pointList[0][1]

    kx2 = pointList[1][0]
    ky2 = pointList[1][1]

    print(pointList)

    dkx = kx2 -kx1
    dky = ky2 -ky1

    fx = dkx/dx
    fy = dky/dy

    x0 = kx1+(dkx/2)
    y0 = ky1+(dky/2)
    
    print("fx: "+str(fx)+" fy: "+str(fy))
    print("x0: "+str(x0)+" y0: "+str(y0))

    writeConfig(x0, y0, fx, fy)

#=====================================================================
def calibratePen(direction):
    global coordList
    if(direction == "zzero"):
        coordList = list()
        coordList.append([xk1,yk1, z_paint])
    elif(direction == "home"):
        coordList = list()
        coordList.append([xh, yh, zh])
    sendToRobot(coordList)
#=====================================================================


def fillList(image, x, y, pixelList):
    q = Queue.Queue()
    q.put((x,y))

    while not q.empty():
        point = q.get()
        x = point[0]
        y = point[1]

        if image.item((y,x)) == 255:
            pixelList.append([x,y])
            image.itemset((y,x), 0)

            if x > 0:
                q.put((x-1, y))
            if x < width-1:
                q.put((x+1, y))
            if y > 0:
                q.put((x, y-1))
            if y < height-1:
                q.put((x, y+1))

#=====================================================================

def calcCentroid(pixelList):
    sumX = 0
    sumY = 0
    for i in pixelList:
        sumX = sumX + i[0]
        sumY = sumY + i[1]

    Xc = sumX/len(pixelList)
    Yc = sumY/len(pixelList)
    return [Xc,Yc]


#=====================================================================

def sendToRobot(coordList):
    # open socket to robot
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(addr)
    
    # initialize connection
    sock.send("move_via_piui")
    data = sock.recv(BUFFER_SIZE)
    if data != "ack":
        print "server failed to accept command move_via_piui"
        sock.close()
        return

    # send packets
    num_coord = 0
    data = ""
    for i in coordList:
        data += str(i[0])+"|"+str(i[1])+"|"+str(i[2])+"|L;"
        num_coord += 1
        
        
        if num_coord >= PACKET_SIZE:
            num_coord = 0
            sock.send(data)
            data = sock.recv(BUFFER_SIZE)
            if data != "ack":
                print "server failed to parse coords"
                sock.close()
                return
            
            data = ""
            
    if data != "":
        sock.send(data)
        data = sock.recv(BUFFER_SIZE)
        if data != "ack":
            print "server failed to parse coords"
            sock.close()
            return
    
    # send finished
    sock.send("finished")
    data = sock.recv(BUFFER_SIZE)
    if data != "ack":
        print "server failed to move robot"
      
    sock.close()

#=====================================================================

def convertKoord(x0, y0, fx, fy, x, y):
    xFanuc = round((x-x0)/fx,0)
    yFanuc = round((y-y0)/fy,0)
    return (xFanuc, yFanuc)

#=====================================================================

def pix2Coord(pointList):
    x0, y0, fx, fy = loadConfig()    
    coordList = list()
    
    # move over first point
    x = pointList[0][0]
    y = pointList[0][1]
    xFanuc, yFanuc = convertKoord(x0, y0, fx, fy, x, y)
    coordList.append([xFanuc,yFanuc, z_move])
    
    for i in pointList:
        x = i[0]
        y = i[1]
        xFanuc, yFanuc = convertKoord(x0, y0, fx, fy, x, y)
        coordList.append([xFanuc,yFanuc, z_paint])
        
    # move over last point
    x = pointList[len(pointList)-1][0]
    y = pointList[len(pointList)-1][1]
    xFanuc, yFanuc = convertKoord(x0, y0, fx, fy, x, y)
    coordList.append([xFanuc,yFanuc, z_move])
        
    coordList.append([xh, yh, zh])

    return coordList

#=====================================================================

def floodfill(binary):
    count = 0
    pointList = list()

    # floodfill pixels
    for x in range(0, width):
        for y in range(0, height):
            if binary.item((y, x)) == 255:
                pixelList = list() #Erzeuge Liste fuer gefundene Pixel
                count += 1
                fillList(binary, x, y, pixelList)
                pointList.append(calcCentroid(pixelList))

    print("number of points found: " + str(count))

    return pointList

#=====================================================================

def takePicture(camera):
    rawCapture = PiRGBArray(camera)

    # allow the camera to warmup
    time.sleep(0.1)

    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array
    # read mask from file
    mask = cv2.imread('mask.png',0)

    # write picture to file
    cv2.imwrite("output.png", img)

    # convtert to grayscale, filter threshold, apply mask
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    th, dst = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    binary = cv2.bitwise_and(dst, dst,mask = mask)

    # display the image on screen
    #cv2.imshow("Image", dst)

    return binary

#=====================================================================
# MAIN PROGRAM STARTS HERE
#=====================================================================

def init():
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (width, height)

    return camera

def run_image(camera):
    binary = takePicture(camera)

    pointList = floodfill(binary)

    return pointList

def run_robot(pointList):
    coordList = pix2Coord(pointList)
    nCoordList = len(coordList)

    if nCoordList>0:
        sendToRobot(coordList)
    else:
        print("list is empty")
