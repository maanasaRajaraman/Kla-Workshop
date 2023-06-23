# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 08:01:50 2023

@author: maana
"""

import json
from PIL import Image
import cv2
import os

def detail(inputJFile):
    #function to read die dimentions
    dataL = json.loads(inputJFile)
    w = dataL["die"]["width"]
    h = dataL["die"]["height"]
    nRow = dataL["die"]["rows"]
    nClns = dataL["die"]["columns"]
    strWidth = dataL["street_width"]
    return w, h, strWidth
        
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
    fname=img.split("/")[-1]
    frameNo=fname.split("_").split(".")[0]
    return frameNo

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        #img = cv2.imread(os.path.join(folder,filename))
        img=filename
        if img is not None:
            images.append(img)
    return images

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


def detection(wafer, diePos, cArea, ecZ):
    foundDefect=[]
    #diePos=[xStart, yStart, xEnd, yEnd]
    dp=diePos
    for j in range(dp[1], dp[3]):
        for i in range(dp[0], dp[2]):
            if insideArea(i,j,cArea):
                if not insideArea(i, j, ecZ):
                    if defectiveFound(wafer, i, j):
                        foundDefect.append((i,j))

def insideArea(i, j, area):
    topLeft, bottomRight = area
    x1, y1 = topLeft
    x2, y2 = bottomRight
    return x1 <= x <= x2 and y1 >= y >= y2

    
with open("input.json", "r") as file:
    inputJson = file.read()
dWidth, dHeight, strWidhth = detail(inputJson)
careArea = careArea(inputJson)
exclusionZones = eclZone(inputJson)

imgPathList=load_images_from_folder("images")

for i in imgPathList:
    waferImg=loadpng(i)
    
    

def isWithinArea(x, y, area):
    topLeft, bottomRight = area
    x1, y1 = topLeft
    x2, y2 = bottomRight
    return x1 <= x <= x2 and y1 >= y >= y2

def isDefective(waferImage, x, y):
    # Perform defect detection logic on the pixel (example: check color intensity, etc.)
    return False  # Replace with your defect detection logic


