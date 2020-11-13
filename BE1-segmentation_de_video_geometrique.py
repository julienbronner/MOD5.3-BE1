# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 16:12:25 2020

@author: julbr
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.exposure import rescale_intensity

#%% Fonctions masque géométrique vidéo

def video_to_greyscale_video(vidObj):
    nb_frames = int(vidObj.get(7)) # On mesure le nombre d'image de la vidéo
    vidWidth  = int(vidObj.get(3)) # Nb de pixels en largeur
    vidHeight = int(vidObj.get(4)) # En hauteur
    fps = int(vidObj.get(cv2.CAP_PROP_FPS)) # On mesure le nombre d'image par seconde
    print('Largeur :', vidWidth, '; Hauteur :', vidHeight, "; Nb d'images :", nb_frames, "; fps :", fps)
    
    vid_greyscale = np.zeros((nb_frames, vidHeight, vidWidth))
    success,image = vidObj.read()
    count = 0
    success = True
    while count < nb_frames :
        success,image = vidObj.read()
        if success:
            vid_greyscale[count]=(image[:,:,0] + image[:,:,1] + image[:,:,2])/3
            count += 1
        else :
            break
    return vid_greyscale 
    
def filtrage_geo_video(video_greyscale, masque_filtrage):
    (nb_frames, vidHeight, vidWidth) = np.shape(video_greyscale)
    video_filtree = np.zeros((nb_frames, vidHeight-2, vidWidth-2))
    print(np.shape(masque_filtrage))
    for frame in range(nb_frames):
        for i in range(1,vidHeight-1):
            for j in range(1,vidWidth-1):
                sous_matrice = video_greyscale[frame, i-1:i+2, j-1:j+2]
                video_filtree[frame,i-1,j-1] = sum(sum(sous_matrice* masque_filtrage))
#    video_filtree = rescale_intensity(video_filtree, in_range=(0, 255))
#	video_filtree = (video_filtree * 255).astype("uint8")
    return video_filtree

#%% Fonctions masque géométrique image

def image_to_greyscale(image):
    image = cv2.imread(image)
    Height, Width  = np.shape(image)[:2] # Nb de pixels en largeur, hauteur
    print('Largeur :', Width, '; Hauteur :', Height)
    
    greyscale = np.zeros((Height, Width))
    greyscale=(image[:,:,0] + image[:,:,1] + image[:,:,2])/3
    print(np.shape(greyscale))
    return greyscale 
    
def filtrage_geo_image(image_greyscale, masque_filtrage):
    Height, Width = np.shape(image_greyscale)[:2]
    pad = (np.shape(masque_filtrage)[0] - 1) // 2
    print(pad)
    image_filtree = np.zeros((Height, Width))
    image_greyscale = cv2.copyMakeBorder(image_greyscale, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    for i in range(pad, Height+pad):
        for j in range(pad, Width+pad):
            sous_matrice = image_greyscale[i-pad:i+pad+1, j-pad:j+pad+1]
            image_filtree[i-pad,j-pad] = sum(sum(sous_matrice* masque_filtrage))
    image_filtree = rescale_intensity(image_filtree, in_range=(0, 255))
    image_filtree = (image_filtree * 255).astype("uint8")
    return image_filtree

def elargissement_bord(image_filtree,seuil): # fait un bord plus large et seuil pour etre soit blanc soit noir
    Height, Width = np.shape(image_filtree)
    matrice_unite = np.ones((5,5))
    image_bord = np.zeros((Height, Width))
    pad = (np.shape(matrice_unite)[0] - 1) // 2
    image_filtree = cv2.copyMakeBorder(image_filtree, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    for i in range(pad, Height+pad):
        for j in range(pad, Width+pad):
            if image_filtree[i,j] > seuil :
                image_bord[i-pad:i+pad+1, j-pad:j+pad+1] = 255*matrice_unite #image_filtree[i,j]*matrice_unite
            else : 
                image_bord[i, j] = 0
    return image_bord



#%% Main
vidObj = cv2.VideoCapture('D:/julbr/Documents/ecole/ECL/3A/MOD 5.3 Analyse de données/BE1_Traitement_et_analyse_des_données_visuelles_et_sonores 2020-21/MOD5.3-BE1/Pub_C+_176_144.mp4')
masque_base =np.array([[0,1,0],[1,-4,1],[0,1,0]])
masque_horizontal = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
masque_vertical = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])
image_path = "D:/julbr/Documents/ecole/ECL/3A/MOD 3.2 Deep Learning & IA/TD2/TD2_Apprentissage_Profond-fichiers/images/gorbeau.jpg"

#if not vidObj.isOpened(): 
#    print("Erreur lors de l'ouverture du fichier video")
#
#else:
#    gray = video_to_greyscale(vidObj)
#    print("Gray video")
#    plt.imshow(gray[1450], cmap = plt.get_cmap('gray'))
#    filtre = filtrage_geo_video(gray, masque_base)
#    print("Filtrage")
#    plt.imshow(filtre[1450], cmap = plt.get_cmap('gray'))
#    

gray = image_to_greyscale(image_path)
filtre = filtrage_geo_image(gray, masque_base)
plt.imshow(filtre, cmap = plt.get_cmap('gray'))
#bord = elargissement_bord(filtre, 150)
#plt.imshow(bord, cmap = plt.get_cmap('gray'))