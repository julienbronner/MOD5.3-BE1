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
def Get_Image_colour(vidObj, limit, vidWidth, vidHeight, split = 1):
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
        for i in range(0, split):
            for j in range(0, split):
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
def Get_Image_greyscale(vidObj, limit, vidWidth, vidHeight):
    # On stocke les images (info rgb par pixel) dans un np.array
    Grey_split = np.zeros([1, split**2])
    
    success,image = vidObj.read()
    count = 0
    success = True
    
    while count < limit :
        success,image = vidObj.read()
        Grey = []
        for i in range(0, split):
            for j in range(0, split):
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
            if count == 0 :
                Grey_split[0] = Grey
            else :
                Grey_split = np.append(Grey_split, [Grey], axis = 0)
        count += 1
    return Grey_split
#%%
def Analyse_colour(Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split, seuil_cut, seuil_noir, cut):
    
    nb_f_pos =  [0 for i in range(split**2)]
    nb_f_neg =  [0 for i in range(split**2)]
    nb_erreur = [0 for i in range(split**2)]
    
    for j in range(0,split**2):
        Noir_split, Cut_split, RedCut_split, GreenCut_split, BlueCut_split = [], [], [], [], []
        for i in range(2,len(Red_split[:,j])):
            if np.abs(Red_split[i,j]-Red_split[i-1,j]) > seuil_cut:
                RedCut_split.append(i)
                # print("Coupure des rouges à la frame ", i+1)
            if np.abs(Green_split[i,j]-Green_split[i-1,j]) > seuil_cut:
                GreenCut_split.append(i)
            if np.abs(Blue_split[i,j]-Blue_split[i-1,j]) > seuil_cut:
                BlueCut_split.append(i)

        # Puis on considère que c'est un cut si les variations sont communes à chaque couleur
        for i in RedCut_split:
            # if i in GreenCut and i in BlueCut :
            if Red_split[i,j] < seuil_noir and Green_split[i,j] < seuil_noir and Blue_split[i,j] < seuil_noir :
                Noir_split.append(i+1)
            else :
                Cut_split.append(i+1)
                
                # print("Coupure à la frame ", i+1)
                # print("Red : ",Red[i], "; Green : ", Green[i], "; Blue : ", Blue[i])
                    
        # On compare à présent les résultats à la vérité sur terrain
        
        Noir_split = set(Noir_split)
        Cut_split = set(Cut_split)
        #print()
        #print('Cut :', sorted(Cut_split))
        #print('Noir :', sorted(Noir_split))

        if cut == True:
            nb_f_pos[j] = len(Cut_split.difference(Cut_verif))
            nb_f_neg[j] = len(Cut_verif.difference(Cut_split))
            print("CUT :", Cut_split[j])
            print("NOIR :", Noir_split[j])

        else :
            nb_f_pos[j] = len(Noir_split.difference(Noir_verif))
            nb_f_neg[j] = len(Noir_verif.difference(Noir_split))
            #print("CUT :", Cut_split[j])
            #print("NOIR :", Noir_split[j])
            
        nb_erreur[j] = nb_f_pos[j] + nb_f_neg[j]
        
    Nb_f_pos_split = np.append(Nb_f_pos_split, [nb_f_pos], axis = 0)
    Nb_f_neg_split = np.append(Nb_f_neg_split, [nb_f_neg], axis = 0)
    Nb_erreur_split = np.append(Nb_erreur_split, [nb_erreur], axis = 0)
    return Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split

#%%
def Analyse_greyscale(Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split, seuil_cut, seuil_noir, cut):
    nb_f_pos =  [0 for i in range(split**2)]
    nb_f_neg =  [0 for i in range(split**2)]
    nb_erreur = [0 for i in range(split**2)]
    
    for j in range(0,split**2):
        Noir_split, Cut_split = [], []
        for i in range(2,len(Grey_split[:,j])):
            if np.abs(Grey_split[i,j]-Grey_split[i-1,j]) > seuil_cut:
                if Grey_split[i,j] < seuil_noir :
                    Noir_split.append(i+1)
                    #print("Noir à la frame ", i+1)
                else :
                    Cut_split.append(i+1)
                    #print("Coupure à la frame ", i+1)

        # On compare à présent les résultats à la vérité sur terrain
        Noir_split = set(Noir_split)
        Cut_split = set(Cut_split)
        print()
        print('Cut :', sorted(Cut_split))
        print('Noir :', sorted(Noir_split))
        """
        if len(Cut_split) == 0 :
            print("Erreur : seuil trop grand")
            return 0
        else:
        """
        if cut == True:
            nb_f_pos[j] = len(Cut_split.difference(Cut_verif))
            nb_f_neg[j] = len(Cut_verif.difference(Cut_split))
            #print("CUT :", Cut_split[j])
            #print("NOIR :", Noir_split[j])

        else :
            nb_f_pos[j] = len(Noir_split.difference(Noir_verif))
            nb_f_neg[j] = len(Noir_verif.difference(Noir_split))
            #print("CUT :", Cut_split[j])
            #print("NOIR :", Noir_split[j])
            
        nb_erreur[j] = nb_f_pos[j] + nb_f_neg[j]
            
    Nb_f_pos_split = np.append(Nb_f_pos_split, [nb_f_pos], axis = 0)
    Nb_f_neg_split = np.append(Nb_f_neg_split, [nb_f_neg], axis = 0)
    Nb_erreur_split = np.append(Nb_erreur_split, [nb_erreur], axis = 0)
    return Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split

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
    displayEvo = False
    split = 3
    cut = True

    if GreyScale :
        Grey_split = Get_Image_greyscale(vidObj, limit, vidWidth, vidHeight)
        if displayEvo :
            fig, axs = plt.subplots(split, split)
            Xrange = [x for x in range(0, min(limit, nb_frames-3))]
            for i in range(0, split):
                for j in range(0, split):
                    axs[i, j].plot(Xrange, Grey_split[:,i+j*2], label = "Niveaux de gris", color = 'grey')
            # plt.plot(Xrange, np.ones(len(Grey))*7.8, '-.', label  = 'Seuil de détection des noirs', color = 'black')
            # plt.xlabel("Images")
            # plt.ylabel("Quantification de l'intensité des gris")
            # plt.legend()
            # plt.savefig('Evolution des niveaux de gris.png', dpi=300)
    else :
        Red_split, Green_split, Blue_split = Get_Image_colour(vidObj, limit, vidWidth, vidHeight, split)
        if displayEvo :
            fig, axs = plt.subplots(split, split)
            Xrange = [x for x in range(0, min(limit, nb_frames-3))]
            for i in range(0, split):
                for j in range(0, split):
                    axs[i, j].plot(Xrange, Red_split[:,i+j*2], label = "Rouge", color = 'red')
                    axs[i, j].plot(Xrange, Green_split[:,i+j*2], label = "Vert", color = 'green')
                    axs[i, j].plot(Xrange, Blue_split[:,i+j*2], label = "Bleu", color = 'blue')
                    # plt.savefig('Evolution des niveaux de gris.png', dpi=300)
                    
#%% Détection des erreurs

    Nb_f_pos_split = np.zeros([0,split**2])
    Nb_f_neg_split = np.zeros([0,split**2])
    Nb_erreur_split = np.zeros([0,split**2])
    
    Nb_echa = 200
    Seuils = np.linspace(5, 50, Nb_echa)
    
    if cut :
        seuil_noir = 6
        for seuil_cut in Seuils:
            # print("Seuil cut :", seuil_cut)
            if GreyScale :
                Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split = Analyse_greyscale(Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split, seuil_cut, seuil_noir, cut)
            else :
                Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split = Analyse_colour(Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split, seuil_cut, seuil_noir, cut)
    else :
        seuil_cut = 15
        for seuil_noir in Seuils:
            # print("Seuil noir :", seuil_noir)
            if GreyScale :
                Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split = Analyse_greyscale(Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split, seuil_cut, seuil_noir, cut)
            else :
                Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split = Analyse_colour(Nb_f_pos_split, Nb_f_neg_split, Nb_erreur_split, seuil_cut, seuil_noir, cut)
            
    if not displayEvo : # Si on veut afficher les erreurs en fonction du seuil
        fig, axs = plt.subplots(split, split)
        for i in range(0, split):
            for j in range(0, split):
                axs[i, j].plot(Seuils, Nb_f_pos_split[:, i+j*2], label="Nombre de faux positifs", color = 'blue')
                axs[i, j].plot(Seuils, Nb_f_neg_split[:, i+j*2], label="Nombre de faux negatifs", color = 'red')
                axs[i, j].plot(Seuils, Nb_erreur_split[:, i+j*2], '--', label="Nombre d'erreurs", color = 'black')
                nb_erreur_min = min(Nb_erreur_split[:, i+j*2])
                indices = [k for k, err in enumerate(Nb_erreur_split[:, i+j*2]) if err == nb_erreur_min]
                print()
                print("Nb d'erreurs :", nb_erreur_min, "; pour un seuil de", Seuils[indices])
            """
            if cut :
                plt.savefig('Evolution_des_erreurs_en_fonction_du_seuil_de_détection_gris.png', dpi=300)
            else :
                plt.savefig('Evolution_des_erreurs_en_fonction_du_seuil_de_détection_de_noirs_gris.png', dpi=300)
            """