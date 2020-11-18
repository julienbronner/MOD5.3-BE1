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

def video_to_greyscale(vidObj):
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
    
def filtrage_geo_video_v1(video_greyscale, masque_filtrage):
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

def filtrage_geo_video_v2(video_greyscale, masque_filtrage, seuil_bord, seuil_comparaison):
    """
    seuil_bord entre 0 et 255
    seuil_comparaison entre 0 et 100, % de pixel du bord en commun
    """
    (nb_frames, Height, Width) = np.shape(video_greyscale)
    #video_filtree = np.zeros((nb_frames, vidHeight, vidWidth))
    video_bord = np.zeros((nb_frames, Height, Width))
    pad_filtrage = (np.shape(masque_filtrage)[0] - 1) // 2
    matrice_unite = np.ones((5,5))
    pad_unite = (np.shape(matrice_unite)[0] - 1) // 2
    #print(np.shape(masque_filtrage))
    liste_coupure = []
    liste_coupure_verite = [52,142,163,187,200,221,248,256,268,307,485,526]
    
    #out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), nb_frames, (Width,Height), False)
    
    for frame in range(nb_frames):
        # Partie detection de bord
        frame_greyscale = video_greyscale[frame]
        frame_greyscale = cv2.copyMakeBorder(frame_greyscale, pad_filtrage, pad_filtrage, pad_filtrage, pad_filtrage, cv2.BORDER_REPLICATE)
        frame_filtree = np.zeros((Height, Width))
        for i in range(pad_filtrage,Height+pad_filtrage):
            for j in range(pad_filtrage,Width+pad_filtrage):
                sous_matrice = frame_greyscale[i-pad_filtrage:i+pad_filtrage+1, j-pad_filtrage:j+pad_filtrage+1]
                frame_filtree[i-pad_filtrage,j-pad_filtrage] = sum(sum(sous_matrice* masque_filtrage))
        frame_filtree = rescale_intensity(frame_filtree, in_range=(0, 255))
        frame_filtree = (frame_filtree * 255).astype("uint8")
        # video_filtree[frame] = frame_filtree
        
        # Partie elargissement bord
        frame_bord = np.zeros((Height+pad_unite*2, Width+pad_unite*2))
        frame_filtree = cv2.copyMakeBorder(frame_filtree, pad_unite, pad_unite, pad_unite, pad_unite, cv2.BORDER_REPLICATE)
        for i in range(pad_unite, Height+pad_unite):
            for j in range(pad_unite, Width+pad_unite):
                if frame_filtree[i,j] > seuil_bord :
                    frame_bord[i-pad_unite:i+pad_unite+1, j-pad_unite:j+pad_unite+1] = 255*matrice_unite #image_filtree[i,j]*matrice_unite
                else : 
                    frame_bord[i, j] = 0
        video_bord[frame] = frame_bord[pad_unite:-pad_unite, pad_unite:-pad_unite]
        
        #out.write(video_bord[frame])
        #cv2.imshow('frame',video_bord[frame])


        # Partie comparaison bord avec l'image précédente
        if frame >0: # on evite la première frame parce qu'on ne peut la comparer a rien
            nombre_pixel_bord_commun = 0
            for i in range(len(video_bord[0])):
                for j in range(len(video_bord[0][0])):
                    if ((video_bord[frame,i,j]==255) and (video_bord[frame-1,i,j]==255)):
                        nombre_pixel_bord_commun+=1
#            nombre_pixel_bord_commun = sum(sum(video_bord[frame]==video_bord[frame-1]))
            fraction_commune = 100*nombre_pixel_bord_commun/(Height*Width)
            if (frame%100 == 0) or (frame in liste_coupure_verite):
                print(f"Frame : {frame} ; Nbr de pixel en commun : {nombre_pixel_bord_commun} ; Fraction de pixel commun : {round(fraction_commune,2)}")
                cv2.imwrite(f'frame_{frame-2}.png', video_bord[frame-2])
                cv2.imwrite(f'frame_{frame-1}.png', video_bord[frame-1])
            if fraction_commune < seuil_comparaison:
                liste_coupure.append(frame)
    return liste_coupure

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
    pad = (np.shape(matrice_unite)[0] - 1) // 2
    image_bord = np.zeros((Height+pad*2, Width+pad*2))
    image_filtree = cv2.copyMakeBorder(image_filtree, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    for i in range(pad, Height+pad):
        for j in range(pad, Width+pad):
            if image_filtree[i,j] > seuil :
                image_bord[i-pad:i+pad+1, j-pad:j+pad+1] = 255*matrice_unite #image_filtree[i,j]*matrice_unite
            else : 
                image_bord[i, j] = 0
    return image_bord



#%% Main
vidObj = cv2.VideoCapture('D:/julbr/Documents/ecole/ECL/3A/MOD 5.3 Analyse de données/BE1_Traitement_et_analyse_des_données_visuelles_et_sonores 2020-21/MOD5.3-BE1/Pub_C+_176_144_cut.mp4')
masque_base =np.array([[0,1,0],[1,-4,1],[0,1,0]])
masque_horizontal = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
masque_vertical = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])
image_path = "D:/julbr/Documents/ecole/ECL/3A/MOD 3.2 Deep Learning & IA/TD2/TD2_Apprentissage_Profond-fichiers/images/gorbeau.jpg"


#%% Test Vidéo
if not vidObj.isOpened(): 
    print("Erreur lors de l'ouverture du fichier video")

else:
    gray = video_to_greyscale(vidObj)
    print("Gray video")
#    plt.imshow(gray[1450], cmap = plt.get_cmap('gray'))
#    filtre = filtrage_geo_video_v1(gray, masque_base)
#    print("Filtrage")
#    plt.imshow(filtre[1450], cmap = plt.get_cmap('gray'))
    coupure = filtrage_geo_video_v2(gray, masque_base, 120, 5)
    print(coupure)

#%% Test image
#gray = image_to_greyscale(image_path)
#filtre = filtrage_geo_image(gray, masque_base)
#plt.imshow(filtre, cmap = plt.get_cmap('gray'))
#bord = elargissement_bord(filtre, 150)
#plt.imshow(bord, cmap = plt.get_cmap('gray'))