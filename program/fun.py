import cv2 as cv
import numpy as np
import os
import json
import sys
import time


gornjaG = 250
donjaG = 730

def preprocesirajSliku(path):
    ekstenzija = path[(path.rfind(".")+1):]
    if ekstenzija!="png" and ekstenzija!="jpg":
        return
    image_good = cv.imread(path)
    image_good_s = cv.cvtColor(image_good,cv.COLOR_BGR2GRAY)
    image_good_b = cv.adaptiveThreshold(image_good_s,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,11,4)
    cv.imshow("Originalna slika",image_good)
    cv.imshow("Sivoskalirana slika",image_good_s)
    cv.imshow("Binarna slika",image_good_b)
    return image_good_b

def daLiJeVidljivostDobra(image):
    m, n = image.shape
    brojPixel = 0
    for i in range(gornjaG,donjaG):
        for j in range(n):
            if image[i][j] == 255:
                brojPixel+=1
    if brojPixel>111000:
        return True
    return False

def pokreni(path):
    image = preprocesirajSliku(path)
    org_image = cv.imread(path)
    if daLiJeVidljivostDobra(image)==True:
        cv.imshow("Dobra vidljivost",org_image)
    else:
        cv.imshow("Losa vidljivost",org_image)




#####Dodatno
def konverzijaBinarnaOpen(path1,path2):
    image_good = cv.imread(path1)
    image_good_s = cv.cvtColor(image_good,cv.COLOR_BGR2GRAY)
    image_good_b = cv.adaptiveThreshold(image_good_s,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,11,4)
    m, n = 2, 2

    numForFileName = path1.rfind("/")
    fileName = path1[(numForFileName+1):]
    cv.imwrite(path2+"//"+fileName,image_good_b)




def brojPiksela(path,pathFile):
    ekstenzija = path[(path.rfind(".")+1):]
    if ekstenzija!="png" and ekstenzija!="jpg":
        return
    image = cv.imread(path)
    m, n,_ = image.shape
    brojPixel = 0
    for i in range(gornjaG,donjaG):
        for j in range(n):
            if image[i][j][0] == 255:
                brojPixel+=1
    f = open(pathFile,"+a")
    f.write(path[(path.rfind("/")+1):]+": "+str(brojPixel)+"\n")
    d = {"ime":path[(path.rfind("/")+1):],"broj":brojPixel}
    return d

def obradaFolderSlike(path1,path2): 
    for file in os.listdir(path1):
        konverzijaBinarnaOpen(path1+"//"+file,path2)
def statistikaSlikaFolder(path):
    lista = []
    i = 1
    for file in os.listdir(path):
        print(i)
        d = brojPiksela(path+"//"+file,path+"//podaci_o_pikselima.txt")
        if d!=None:
            lista.append(d)
        i+=1
    str_json = json.dumps(lista)
    f = open(path+"//"+"podaci_o_pikselima.json","w")
    f.write(str_json)

    f = open(path+"//podaci_o_pikselima.json")
    lista = json.load(f)
    min = float("+inf")
    minIme = ""
    max = float("-inf")
    maxIme = ""
    avg = 0
    sum = 0
    count = 0
    for podatak in lista:
        ime, broj = podatak["ime"],podatak["broj"]
        if broj>max:
            max = broj
            maxIme = ime
        if broj<min:
            min = broj
            minIme = ime
        sum += broj
    avg = sum/len(lista) if len(lista)>0 else 0
    f = open(path+"//statistika.txt","w")
    f.write(f"Max, {maxIme}: {max}\nMin, {minIme}: {min}\nAvg {avg}\nSum {sum}")


def obradaFoldera(path1,path2):
    obradaFolderSlike(path1,path2)
    statistikaSlikaFolder(path2)




cv.waitKey(0)
