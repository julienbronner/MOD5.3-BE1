# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 12:07:34 2020

@author: Loïc
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

##### Fonctions #####
#%%
def Get_Image_colour(vidObj, limit, vidWidth, vidHeight):
    # On stocke les images (info rgb par pixel) dans un np.array
    Red = []
    Green = []
    Blue = []
    
    success,image = vidObj.read()
    count = 0
    success = True
    
    while count < limit :
        success,image = vidObj.read()
        if success:
            Red.append(np.sum(image[:,:,2])/(vidWidth*vidHeight))      # L'ordre d'OpenCV n'est pas RGB mais BGR
            Green.append(np.sum(image[:,:,1])/(vidWidth*vidHeight))
            Blue.append(np.sum(image[:,:,0])/(vidWidth*vidHeight))
            count += 1
        else :
            break
    return Red, Green, Blue
#%%
def Get_Image_greyscale(vidObj, limit, vidWidth, vidHeight):
    # On stocke les images (info rgb par pixel) dans un np.array
    Grey = []
    
    success,image = vidObj.read()
    count = 0
    success = True
    
    while count < limit :
        success,image = vidObj.read()
        if success:
            Grey.append(np.sum(image[:,:,0]*0.11 +
                              image[:,:,1]*0.59 +
                              image[:,:,2]*0.3)/(vidWidth*vidHeight))
            count += 1
        else :
            break
    return Grey
#%%
def Get_Image_colour_split(vidObj, limit, vidWidth, vidHeight, split = 1):
    # On stocke les images (info rgb par pixel) dans un np.array
    Red_split = np.zeros([0, split**2])
    Green_split = np.zeros([0, split**2])
    Blue_split = np.zeros([0, split**2])
    success,image = vidObj.read()
    count = 0
    success = True
    
    while count < limit :
        success,image = vidObj.read()
        Red = []
        Green = []
        Blue = []
        for i in range(split):
            for j in range(split):
                if success:
                    Red.append(np.sum(image[int(i*vidWidth/split):int((i+1)*vidWidth/split),
                                            int(j*vidHeight/split):int((j+1)*vidHeight/split),2]
                                      )/(vidWidth*vidHeight/split**2))      # L'ordre d'OpenCV n'est pas RGB mais BGR
                    Green.append(np.sum(image[int(i*vidWidth/split):int((i+1)*vidWidth/split),
                                              int(j*vidHeight/split):int((j+1)*vidHeight/split),1]
                                        )/(vidWidth*vidHeight/split**2))
                    Blue.append(np.sum(image[int(i*vidWidth/split):int((i+1)*vidWidth/split),
                                             int(j*vidHeight/split):int((j+1)*vidHeight/split),0]
                                       )/(vidWidth*vidHeight/split**2))
                else :
                    break
        if len(Red) == split**2:
            Red_split = np.append(Red_split, [Red], axis = 0)
            Green_split = np.append(Green_split, [Green], axis = 0)
            Blue_split = np.append(Blue_split, [Blue], axis = 0)
        count += 1
    return Red_split, Green_split, Blue_split
#%%
def Get_Image_greyscale_split(vidObj, limit, vidWidth, vidHeight):
    # On stocke les images (info rgb par pixel) dans un np.array
    Grey_split = np.zeros([0, split**2])
    
    success,image = vidObj.read()
    count = 0
    success = True
    
    while count < limit :
        success,image = vidObj.read()
        Grey = []
        for i in range(split):
            for j in range(split):
                if success:
                    Grey.append(np.sum(image[int(i*vidWidth/split):
                                             int((i+1)*vidWidth/split),
                                             int(j*vidHeight/split):
                                             int((j+1)*vidHeight/split),0]*0.11 +
                                       image[int(i*vidWidth/split):
                                             int((i+1)*vidWidth/split),
                                             int(j*vidHeight/split):
                                             int((j+1)*vidHeight/split),1]*0.59 +
                                       image[int(i*vidWidth/split):
                                             int((i+1)*vidWidth/split),
                                             int(j*vidHeight/split):
                                             int((j+1)*vidHeight/split),2]*0.3)
                                /(vidWidth*vidHeight/split**2))   
                else :
                    break
        if len(Grey) == split**2:
            Grey_split = np.append(Grey_split, [Grey], axis = 0)
        count += 1
    return Grey_split
#%%

#%%

#%% Main

# Construit un objet VideoReader associé au fichier audio.

vidObj = cv2.VideoCapture('C:/Users/Loïc/Documents/Centrale/Semestre 9/Traitement et analyse des données visuelles et sonores/BE1_Traitement_et_analyse_des_données_visuelles_et_sonores 2020-21/Pub_C+_176_144.mp4')

if not vidObj.isOpened(): 
	  print("Erreur lors de l'ouverture du fichier audio")

else: 

    nb_frames = int(vidObj.get(7)) # On mesure le nombre d'image de la vidéo
    vidWidth  = int(vidObj.get(3)) # Nb de pixels en largeur
    vidHeight = int(vidObj.get(4)) # En hauteur
    fps = int(vidObj.get(cv2.CAP_PROP_FPS)) # On mesure le nombre d'image par seconde

    # print('Largeur :', vidWidth, '; Hauteur :', vidHeight, "; Nb d'images :", nb_frames, "; fps :", fps)

    # Petit échantillon pour les tests
    limit = nb_frames
    # Set des coupures  et noirs réels, afin de comparer nos résultats
    Cut_verif = {52, 142, 163, 187, 200, 221, 248, 256, 268, 307, 485, 526, 561, 582, 595, 615, 635, 664, 690, 705, 720, 746, 821, 853, 903, 956, 975, 998, 1027, 1062, 1099, 1120, 1144, 1177, 1220, 1255, 1293, 1335, 1367, 1444, 1582, 1655, 1735, 1812, 1871, 1895, 1909, 1960, 2016, 2106, 2147, 2184, 2243, 2487, 2526, 2617, 2688, 2775, 2808, 2829, 2858, 2881, 2917, 2934, 2962, 2978, 3011, 3086, 3179}
    Noir_verif = {42, 552, 812, 1573, 2007, 2766, 3277}
    
    GreyScale = False
    displayEvo = True 
    split = 2
    
    if GreyScale :
        Grey_split = Get_Image_greyscale(vidObj, limit, vidWidth, vidHeight)
        if displayEvo :
            fig, axs = plt.subplots(split, split)
            Xrange = [x for x in range(min(limit, nb_frames-3))]
            for i in range(split):
                for j in range(split):
                    axs[i, j].plot(Xrange, Grey_split[:,i+j*2], label = "Niveaux de gris", color = 'grey')
            # plt.plot(Xrange, np.ones(len(Grey))*7.8, '-.', label  = 'Seuil de détection des noirs', color = 'black')
            # plt.xlabel("Images")
            # plt.ylabel("Quantification de l'intensité des gris")
            # plt.legend()
                    plt.savefig('Evolution des niveaux de gris - split ' + str(split)+ '.png', dpi=300)
    else :
        Red_split, Green_split, Blue_split = Get_Image_colour(vidObj, limit, vidWidth, vidHeight, split)
        if displayEvo :
            fig, axs = plt.subplots(split, split)
            Xrange = [x for x in range(min(limit, nb_frames-3))]
            for i in range(split):
                for j in range(split):
                    axs[i, j].plot(Xrange, Red_split[:,i+j*2], label = "Rouge", color = 'red')
                    axs[i, j].plot(Xrange, Green_split[:,i+j*2], label = "Vert", color = 'green')
                    axs[i, j].plot(Xrange, Blue_split[:,i+j*2], label = "Bleu", color = 'blue')
                    plt.savefig('Evolution des couleurs - split ' + str(split)+ '.png', dpi=300)
                    
#%% Détection des erreurs
          
