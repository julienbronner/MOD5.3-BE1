# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 08:24:53 2020

@author: julbr
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

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
    
    success,image = vidObj.read()
    count = 0
    success = True
    
    # Petit échantillon pour les tests
    limit = nb_frames
    
    # Liste des coupures réelles, afin de comparer nos résultats
    Cut_verif = [52, 142, 163, 187, 200, 221, 248, 256, 268, 307, 485, 526, 561, 582, 595, 615, 635, 664, 690, 705, 720, 746, 821, 853, 903, 956, 975, 998, 1027, 1062, 1099, 1120, 1144, 1177, 1220, 1255, 1293, 1335, 1367, 1444, 1582, 1655, 1735, 1812, 1871, 1895, 1909, 1960, 2016, 2106, 2147, 2184, 2243, 2487, 2526, 2617, 2688, 2775, 2808, 2829, 2858, 2881, 2917, 2934, 2962, 2978, 3011, 3086, 3179]
    Noir_verif = [42, 552, 812, 1573, 2007, 2766, 3277]
    
    while count < limit :
        success,image = vidObj.read()
        if success:
            Mat[count] = image         # save each frame into Mat
            Red.append(int(np.sum(image[:,:,0])))
            Green.append(int(np.sum(image[:,:,1])))
            Blue.append(int(np.sum(image[:,:,2])))
            count += 1
        else :
            break
    
    plt.plot([x for x in range(0, min(limit, nb_frames-3))], Red, color = 'red')
    plt.plot([x for x in range(0, min(limit, nb_frames-3))], Green, color = 'green')
    plt.plot([x for x in range(0, min(limit, nb_frames-3))], Blue, color = 'blue')
    
    # On répèrtorie les cut détectés par des grandes variations de chaque couleurs
    RedCut = [] 
    GreenCut = []
    BlueCut = []
    seuil = 3e5
    
    for i in range(2,len(Red)):
        if np.abs(Red[i]-Red[i-1]) > seuil:
            RedCut.append(i)
            # print("Coupure des rouges à la frame ", i+1)
        if np.abs(Green[i]-Green[i-1]) > seuil:
            GreenCut.append(i)
        if np.abs(Blue[i]-Blue[i-1]) > seuil:
            BlueCut.append(i)
    
    # Puis on considère que c'est un cut si les variations sont communes à chaque couleur
    Cut = []
    Noir = []
    for i in RedCut:
        if i in BlueCut:
            if i in GreenCut :
                Cut.append(i)
                if Red[i] < 0.2e6 and Green[i] < 0.2e6 and Blue[i] < 0.2e6 :
                    print("Plan noir à la frame ", i+1)
                    # print("Red : ",Red[i], "; Green : ", Green[i], "; Blue : ", Blue[i])
                else:
                    print("Coupure à la frame ", i+1)
                    # print("Red : ",Red[i], "; Green : ", Green[i], "; Blue : ", Blue[i])