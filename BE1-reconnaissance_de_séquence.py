# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 12:07:34 2020

@author: Loïc
"""

import cv2
import pysift
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
def Get_Image_colour_split(vidObj, limit, vidWidth, vidHeight):
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
def Get_sequences(seuil_noir):
    Sequences = []
    # On répèrtorie les cut détectés par des grandes variations de chaque couleurs
    seq = []
    for i in range(len(Grey)) :
        if Grey[i] > seuil_noir :
            seq.append(i)
        else :
            if len(seq) > 1 :
                Sequences.append(seq)
            seq = []     
    return Sequences
#%%
def Get_max_lum(sequence):
    for i in sequence :
        G = np.array(Grey)
        G = G[sequence]
        max_lum = np.argsort(G)[-1]
    frame = np.where(Grey == G[max_lum])[0][0]
    print('Maximum de luminosité de ', G[max_lum], ' à la frame', frame)
    sift = cv2.SIFT_create()
    kp = sift.detect(Grey[frame],None)
    img=cv2.drawKeypoints(Grey[frame],kp,img)
    cv2.imwrite('sift_keypoints.jpg',img)
    return max_lum, G[max_lum]
        
#%%

#%% Lecture de la vidéo

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
    
#%% Quantification des couleurs et affichage potentiel
    
    GreyScale = True
    displayEvo = False
    Split = False
    split = 3
    
    if Split :
        if GreyScale :
            Grey_split = Get_Image_greyscale_split(vidObj, limit, vidWidth, vidHeight)
            if displayEvo :
                fig, axs = plt.subplots(split, split)
                Xrange = [x for x in range(min(limit, nb_frames-3))]
                for i in range(split):
                    for j in range(split):
                        axs[i, j].plot(Xrange, Grey_split[:,i+j*2], label = "Niveaux de gris", color = 'grey')
                        #plt.savefig('Evolution des niveaux de gris - split ' + str(split)+ '.png', dpi=300)
        else :
            Red_split, Green_split, Blue_split = Get_Image_colour_split(vidObj, limit, vidWidth, vidHeight)
            if displayEvo :
                fig, axs = plt.subplots(split, split)
                Xrange = [x for x in range(min(limit, nb_frames-3))]
                for i in range(split):
                    for j in range(split):
                        axs[i, j].plot(Xrange, Red_split[:,i+j*2], label = "Rouge", color = 'red')
                        axs[i, j].plot(Xrange, Green_split[:,i+j*2], label = "Vert", color = 'green')
                        axs[i, j].plot(Xrange, Blue_split[:,i+j*2], label = "Bleu", color = 'blue')
                        #plt.savefig('Evolution des couleurs - split ' + str(split)+ '.png', dpi=300)
    else :
        if GreyScale :
            Grey = Get_Image_greyscale(vidObj, limit, vidWidth, vidHeight)
            if displayEvo :
                Xrange = [x for x in range(min(limit, nb_frames-3))]
                plt.plot(Xrange, Grey, label = "Niveaux de gris", color = 'grey')
                plt.xlabel("Images")
                plt.ylabel("Quantification de l'intensité des couleurs")
                plt.legend()
                # plt.savefig('Visualisation du seuil de détection des noirs.png', dpi=300)
        else :
            Red, Green, Blue = Get_Image_colour(vidObj, limit, vidWidth, vidHeight)
            if displayEvo :
                Xrange = [x for x in range(min(limit, nb_frames-3))]
                plt.plot(Xrange, Red, label = "Rouge", color = 'red')
                plt.plot(Xrange, Green, label = "Vert", color = 'green')
                plt.plot(Xrange, Blue, label = "Bleu", color = 'blue')
                plt.xlabel("Images")
                plt.ylabel("Quantification de l'intensité des couleurs")
                plt.legend()
                # plt.savefig('Visualisation du seuil de détection des noirs.png', dpi=300)
                    
#%% Découpage des séquences
    #Grey = Get_Image_greyscale(vidObj, limit, vidWidth, vidHeight)
    seuil_noir = 3.9
    Sequences = Get_sequences(seuil_noir)
    Sequences = np.delete(Sequences, 0, 0)
    for i in Sequences :
        print(i[0], i[-1])
    for seq in Sequences :
        Get_max_lum(seq)

#%% Choix des images

    