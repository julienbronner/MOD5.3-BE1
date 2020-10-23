# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 08:24:53 2020

@author: julbr
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Petit échantillon pour les tests

limit = 3000

# Construct a VideoReader object associated with the sample file.

vidObj = cv2.VideoCapture('C:/Users/Loïc/Documents/Centrale/Semestre 9/Traitement et analyse des données visuelles et sonores/BE1_Traitement_et_analyse_des_données_visuelles_et_sonores 2020-21/Pub_C+_176_144.mp4')

# Determine the height and width of the frames.
if not vidObj.isOpened(): 
	  print("Error opening video stream or file")

else: 

    nb_frames = int(vidObj.get(7))
    vidWidth  = int(vidObj.get(3))
    vidHeight = int(vidObj.get(4))
    fps = int(vidObj.get(cv2.CAP_PROP_FPS))

    print('Largeur : ', vidWidth, ' ; Hauteur : ', vidHeight, " ; Nb d'images : ", nb_frames)

    # Create a Python movie structure array, Mat.
    Mat = np.zeros((nb_frames, vidHeight, vidWidth, 3))
    Red = []
    Green = []
    Blue = []
    # Mat_Red = np.zeros((nb_frames, vidHeight, vidWidth))
    # Mat_Green = np.zeros((nb_frames, vidHeight, vidWidth))
    # Mat_Blue = np.zeros((nb_frames, vidHeight, vidWidth))
    
    success,image = vidObj.read()
    count = 0
    success = True
    while success:
        success,image = vidObj.read()
        Mat[count] = image         # save each frame into Mat
        Red.append(int(np.sum(image[:,:,0])))
        Green.append(int(np.sum(image[:,:,1])))
        Blue.append(int(np.sum(image[:,:,2])))
        count += 1
        if count >= limit:
            break
    
    plt.plot([x for x in range(0, limit)], Red, color = 'red')
    plt.plot([x for x in range(0, limit)], Green, color = 'green')
    plt.plot([x for x in range(0, limit)], Blue, color = 'blue')
    
    RedCut = []
    GreenCut = []
    BlueCut = []
    Cut = []
    
    for i in range(2,limit):
        if np.abs(Red[i]-Red[i-1]) > 1e5:
            RedCut.append(i)
            # print("Coupure à la frame ", i+1)
        if np.abs(Green[i]-Green[i-1]) > 1e5:
            GreenCut.append(i)
        if np.abs(Blue[i]-Blue[i-1]) > 1e5:
            BlueCut.append(i)
    
    for i in RedCut:
        if i in BlueCut:
            if i in GreenCut :
                Cut.append(i)
                if Red[i] < 500 or Green[i] < 500 or Blue[i] < 500 :
                    print("Plan noir à la frame ", i+1)
                else :
                    print("Coupure à la frame ", i+1)