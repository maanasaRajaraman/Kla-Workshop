# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 08:01:50 2023

@author: maana
"""
import json
from PIL import Image
import cv2
import os
import csv

def detail(inputJFile):
    #function to read die dimentions
    dataL = json.loads(inputJFile)
    w = dataL["die"]["width"]
    h = dataL["die"]["height"]
    nRow = dataL["die"]["rows"]
    nClns = dataL["die"]["columns"]
    strWidth = dataL["street_width"]
    return w, h, strWidth, nRow, nClns
        
def careArea(inputJFile):
    #function to read care areas
    dataList = json.loads(inputJFile)
    careAreas = []    
    for i in dataList["care_areas"]:
        topLeft = (i["top_left"]["x"], i["top_left"]["y"])
        bottomRight = (i["bottom_right"]["x"], i["bottom_right"]["y"])
        careAreas.append((topLeft, bottomRight))
    
    return careAreas

def eclZone(inputJFile):
    #function to read exclusion zones
    dataList = json.loads(inputJFile)
    eclZ = []
    for i in dataList["exclusion_zones"]:
        topLeft = (i["top_left"]["x"], i["top_left"]["y"])
        bottomRight = (i["bottom_right"]["x"], i["bottom_right"]["y"])
        eclZ.append((topLeft, bottomRight))
    return eclZ

def frameNumber(img):
    #to calculate freame index/number
    '''fname=img.split("/")[-1]
    print(fname)
    frameNo=fname.split("_")
    print(frameNo)
    frameNo=frameNo[2]
    return frameNo
    '''
    frameName=os.path.splitext(img)[0]
    f=frameName.split('_')
    frameNo=f[-1]
    frameNo = int(frameNo.lstrip("0"))
    return frameNo
    

def loadpng(imageFile):
    png=Image.open(imageFile)
    return png
    #IEO error if not able to open ?
    
def diePosition(dIndex, dW, dH, strW):
   #calculate die position
    xStart= (dIndex % strW) * dW
    yStart=(dIndex // strW) * dW
    xEnd= xStart+dW
    yEnd= yStart+dW
    
    diePos=[xStart, yStart, xEnd, yEnd]
    return diePos

def areasInsideDie(careArea, exclZone, dIndex):
    #returns care area and exclusion zone inside particular die
    caD=careArea[dIndex]
    
    if dIndex in exclZone:
        exlZ=exclZone[dIndex]
    else:
        exlZ=None
    return caD, exlZ

def insideArea(i, j, area):
    topLeft, bottomRight = area
    x1, y1 = topLeft
    x2, y2 = bottomRight
    return x1 <= i <= x2 and y1 >= j >= y2

def defectFound(image, i, j):
    px=image.getpixel((i,j))
    r,g,b=px
    if r+g+b != 255+255+255:
        return True
    else:
        return False

def detectionFunction(wafer, diePos, cArea, ecZ):
    #to find defect location
    foundDefect=[]
    #here diePos=[xStart, yStart, xEnd, yEnd]
    dp=diePos
    for j in range(dp[1], dp[3]):
        for i in range(dp[0], dp[2]):
            if insideArea(i,j,cArea):
                if ecZ!=None:
                    if not insideArea(i, j, ecZ):
                        if defectFound(wafer, i, j):
                            foundDefect.append((i,j))
    return foundDefect

def defectPos(defect, pos):
    defectPos=(defect[0]+ pos[0], defect[1]+pos[1] )
    return defectPos

def anomalyDetection(inputf, imageList):
    finalAnomaly=[]
    
    dWidth, dHeight, strWidhth, row, cln = detail(inputJson)
    careAreai = careArea(inputJson)
    exclusionZones = eclZone(inputJson)
    print(dWidth, dHeight, strWidhth, row, cln)
    print(careAreai)
    for i in imageList:
        frameNum=frameNumber(i)
        waferImg=loadpng(i)
        for die in range(row*cln):
            pos=diePosition(die, dWidth, dHeight, strWidhth)
            ca, ez =areasInsideDie(careAreai, exclusionZones, die)
            print(ca, ez)
            defects=detectionFunction(waferImg, pos, ca, ez)
            for d in defects:
                dloc=defectPos(d, pos)
                anomaly= [die, dloc[0], dloc[1]]
                finalAnomaly.append(anomaly)
    return finalAnomaly
              
            
def anomalyFn(defects, csvFile):
    with open(csvFile, 'w', newline='') as csvF:
        writer = csv.writer(csvF)
        for defect in defects:
            index, i, j = defect
            writer.writerow([index, i, j])
    
with open("input.json", "r") as file:
    inputJson = file.read()

'''
dWidth, dHeight, strWidhth = detail(inputJson)
careArea = careArea(inputJson)
exclusionZones = eclZone(inputJson)
'''

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        #img = cv2.imread(os.path.join(folder,filename))
        img=filename
        if img is not None:
            images.append(img)
    return images

imgPathList=load_images_from_folder("images")
print(imgPathList)

final=anomalyDetection("input.json", imgPathList)

anomalyFn(final, "final.csv")
   