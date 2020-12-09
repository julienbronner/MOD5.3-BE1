# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 09:56:49 2020

@author: julbr
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

vidObj = cv2.VideoCapture('D:/julbr/Documents/ecole/ECL/3A/MOD 5.3 Analyse de données/BE1_Traitement_et_analyse_des_données_visuelles_et_sonores 2020-21/MOD5.3-BE1/Pub_C+_176_144_cut.mp4')
nb_frames = int(vidObj.get(7)) # On mesure le nombre d'image de la vidéo
vidWidth  = int(vidObj.get(3)) # Nb de pixels en largeur
vidHeight = int(vidObj.get(4)) # En hauteur
fps = int(vidObj.get(cv2.CAP_PROP_FPS)) # On mesure le nombre d'image par seconde
print('Largeur :', vidWidth, '; Hauteur :', vidHeight, "; Nb d'images :", nb_frames, "; fps :", fps)
cercle_dilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))

success,image1 = vidObj.read()
count = 1
image_grey1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image_dilate1 = cv2.dilate(cv2.Canny(image_grey1, 50,250), cercle_dilate)
liste_valeur = []

#image_contour  = cv2.Canny(image_grey1, 100,200)
#print(image_grey1)
#plt.figure()
#plt.imshow(image_grey1, cmap = plt.get_cmap('gray'))
#print(image_contour)
#plt.figure()
#plt.imshow(image_contour, cmap = plt.get_cmap('gray'))
#print(image_dilate1)
#plt.figure()
#plt.imshow(image_dilate1, cmap = plt.get_cmap('gray'))

while count < nb_frames :
    success,image2 = vidObj.read()
    if success:
        image_grey2=cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        image_dilate2 = cv2.dilate(cv2.Canny(image_grey2,100,200), cercle_dilate)
#        critere1=np.minimum(image_dilate1,image_dilate2)
#        critere2=image_dilate1-critere1
#        critere3=image_dilate2-critere1
#        moyenne_critere = math.sqrt((sum(sum(critere2))/sum(sum(image_dilate1))) * (sum(sum(critere3))/sum(sum(image_dilate2)))) / (sum(sum(critere1))/ ((sum(sum(image_dilate1))+sum(sum(image_dilate2))))/2)
        m1=np.minimum(image_dilate1,image_dilate2)
        m2=image_dilate1-m1
        m3=image_dilate2-m1
        moyenne_critere = math.sqrt((sum(sum(m2))/sum(sum(image_dilate1))) * (sum(sum(m3))/sum(sum(image_dilate2)))) / (sum(sum(m1))/ ((sum(sum(image_dilate1))+sum(sum(image_dilate2))))/2) 
    
#        print( sum(sum(critere2)), sum(sum(critere3)))
#        moyenne_critere = sum(sum(critere2))
        liste_valeur.append( moyenne_critere)
        image_dilate1 = image_dilate2
        image_grey1 = image_grey2
        count += 1
#        plt.figure()
#        plt.imshow(critere2, cmap = plt.get_cmap('gray'))
    else :
        break

plt.figure(6)
plt.plot(liste_valeur)
plt.show()