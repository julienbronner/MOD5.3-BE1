# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 12:07:34 2020

@author: Loïc
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

#%% Fonctions
def Get_Image_colour(vidObj, limit, vidWidth, vidHeight, split = 1):
    # On stocke les images (info rgb par pixel) dans un np.array
    Red_split = np.zeros([1, split**2])
    Green_split = np.zeros([1, split**2])
    Blue_split = np.zeros([1, split**2])
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
        #print(Red)
        if len(Red) == split**2:
            if count == 0 :
                Red_split[0] = Red
                Green_split[0] = Green
                Blue_split[0] = Blue
            else :
                Red_split = np.append(Red_split, [Red], axis = 0)
                Green_split = np.append(Green_split, [Green], axis = 0)
                Blue_split = np.append(Blue_split, [Blue], axis = 0)
        count += 1
    return Red_split, Green_split, Blue_split

def Get_Image_greyscale(vidObj, limit, vidWidth, vidHeight):
    # On stocke les images (info rgb par pixel) dans un np.array
    Grey_split = np.zeros([1, split**2])
    
    success,image = vidObj.read()
    count = 0
    success = True
    
    while count < limit :
        success,image = vidObj.read()
        for i in range(0, split):
            for j in range(0, split):
                if success:
                    Grey.append(np.sum(image[int(i*vidWidth/split):
                                             int((i+1)*vidWidth/split),
                                             int(j*vidHeight/split):
                                             int((j+1)*vidHeight/split),0]/3 +
                                       image[int(i*vidWidth/split):
                                             int((i+1)*vidWidth/split),
                                             int(j*vidHeight/split):
                                             int((j+1)*vidHeight/split),1]/3 +
                                           image[int(i*vidWidth/split):
                                             int((i+1)*vidWidth/split),
                                             int(j*vidHeight/split):
                                             int((j+1)*vidHeight/split),2]/3)
                                /(vidWidth*vidHeight/split**2))     
        else :
            break
        count += 1
    return Grey

def Analyse_colour(Nb_f_pos, Nb_f_neg, Nb_erreur, seuil_cut, seuil_noir, cut):
    Noir = []
    # On répèrtorie les cut détectés par des grandes variations de chaque couleurs
    RedCut_split = []
    GreenCut_split = []
    BlueCut_split = []
    
    RedCut = []
    GreenCut = []
    BlueCut = []
    
    for i in range(2,len(Red)):
        if np.abs(Red[i]-Red[i-1]) > seuil_cut:
            RedCut.append(i)
            # print("Coupure des rouges à la frame ", i+1)
        if np.abs(Green[i]-Green[i-1]) > seuil_cut:
            GreenCut.append(i)
        if np.abs(Blue[i]-Blue[i-1]) > seuil_cut:
            BlueCut.append(i)
        """
        if Red[i] < seuil_noir and Green[i] < seuil_noir and Blue[i] < seuil_noir :
            if len(Noir) == 0 or i > Noir[-1]+fps: # On considère qu'un plan noir dure moins de 0.5s
                Noir.append(i+1)
            # print("Plan noir à la frame ", i+1)
            # print("Red : ",Red[i], "; Green : ", Green[i], "; Blue : ", Blue[i])
        """
    # Puis on considère que c'est un cut si les variations sont communes à chaque couleur
    Cut = []
    for i in RedCut:
        # if i in GreenCut and i in BlueCut :
        if Red[i] < seuil_noir and Green[i] < seuil_noir and Blue[i] < seuil_noir :
            Noir.append(i+1)
        else :
            Cut.append(i+1)
            
            # print("Coupure à la frame ", i+1)
            # print("Red : ",Red[i], "; Green : ", Green[i], "; Blue : ", Blue[i])
                    
    # On compare à présent les résultats à la vérité sur terrain
    Noir = set(Noir)
    Cut = set(Cut)
    
    if len(Cut) == 0 :
        print("Erreur : seuil trop grand")
        return 0
    else:
        if cut == True:
            nb_f_pos = len(Cut.difference(Cut_verif))
            nb_f_neg = len(Cut_verif.difference(Cut))
            print("CUT :", Cut)
            print("NOIR :", Noir)

        else :
            nb_f_pos = len(Noir.difference(Noir_verif))
            nb_f_neg = len(Noir_verif.difference(Noir))
            print("CUT :", Cut)
            print("NOIR :", Noir)
            
        nb_erreur = nb_f_pos + nb_f_neg
        Nb_f_pos.append(nb_f_pos)
        Nb_f_neg.append(nb_f_neg)
        Nb_erreur.append(nb_erreur)
    
    return None

def Analyse_greyscale(Nb_f_pos, Nb_f_neg, Nb_erreur, seuil_cut, seuil_noir, cut):
    Noir = []
    Cut = []
    
    for i in range(2,len(Grey)):
        if np.abs(Grey[i]-Grey[i-1]) > seuil_cut:
            if Grey[i] < seuil_noir :
                Noir.append(i+1)
                # print("Noir à la frame ", i+1)
            else :
                Cut.append(i+1)
                # print("Coupure à la frame ", i+1)

    # On compare à présent les résultats à la vérité sur terrain
    Noir = set(Noir)
    Cut = set(Cut)
    
    if len(Cut) == 0 :
        print("Erreur : seuil trop grand")
        return 0
    else:
        if cut == True:
            nb_f_pos = len(Cut.difference(Cut_verif))
            nb_f_neg = len(Cut_verif.difference(Cut))
            print("CUT :", Cut)
            print("NOIR :", Noir)

        else :
            nb_f_pos = len(Noir.difference(Noir_verif))
            nb_f_neg = len(Noir_verif.difference(Noir))
            print("CUT :", Cut)
            print("NOIR :", Noir)
            
        nb_erreur = nb_f_pos + nb_f_neg
        Nb_f_pos.append(nb_f_pos)
        Nb_f_neg.append(nb_f_neg)
        Nb_erreur.append(nb_erreur)
    
    return None

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
        Grey = Get_Image_greyscale(vidObj, limit, vidWidth, vidHeight)
        if displayEvo :
            Xrange = [x for x in range(0, min(limit, nb_frames-3))]
            plt.plot(Xrange, Grey, label = "Niveaux de gris", color = 'grey')
            # plt.plot(Xrange, np.ones(len(Grey))*7.8, '-.', label  = 'Seuil de détection des noirs', color = 'black')
            plt.xlabel("Images")
            plt.ylabel("Quantification de l'intensité des gris")
            plt.legend()
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
                    # plt.plot(Xrange, np.ones(len(Blue))*7.8, '-.', label  = 'Seuil de détection des noirs', color = 'black')
                    # plt.xlabel("Images")
                    # plt.ylabel("Quantification de l'intensité des couleurs")
                    # plt.legend()
                    # plt.savefig('Evolution des niveaux de gris.png', dpi=300)

    Nb_f_pos = []
    Nb_f_neg = []
    Nb_erreur = []
    
    Nb_echa = 500
    Seuils = np.linspace(4, 15, Nb_echa)
    
    cut = True
    displayErr = False
    
    if cut :
        seuil_noir = 7.8
        for seuil_cut in Seuils:
            # print("Seuil cut :", seuil_cut)
            if GreyScale :
                Analyse_greyscale(Nb_f_pos, Nb_f_neg, Nb_erreur, seuil_cut, seuil_noir, cut)
            else :
                Analyse_colour(Nb_f_pos, Nb_f_neg, Nb_erreur, seuil_cut, seuil_noir, cut)
    else :
        seuil_cut = 11.5
        for seuil_noir in Seuils:
            # print("Seuil noir :", seuil_noir)
            if GreyScale :
                Analyse_greyscale(Nb_f_pos, Nb_f_neg, Nb_erreur, seuil_cut, seuil_noir, cut)
            else :
                Analyse_colour(Nb_f_pos, Nb_f_neg, Nb_erreur, seuil_cut, seuil_noir, cut)
            
    if displayErr :
        nb_erreur_min = min(Nb_erreur)
        indices = [i for i, err in enumerate(Nb_erreur) if err == nb_erreur_min]
        print()
        print("Nb d'erreurs :", nb_erreur_min, "; pour un seuil de", Seuils[indices])
        print()
        
        # print(min(Nb_f_pos_cut[Taux_echec_cut.index(min(Taux_echec_cut))] + Nb_f_neg_cut[Taux_echec_cut.index(min(Taux_echec_cut))]))
        plt.plot(Seuils, Nb_f_pos, label="Nombre de faux positifs", color = 'blue')
        plt.plot(Seuils, Nb_f_neg, label="Nombre de faux negatifs", color = 'red')
        plt.plot(Seuils, Nb_erreur, '--', label="Nombre d'erreurs", color = 'black')
        plt.xlabel("Seuil")
        plt.ylabel("Nombre d'erreur")
        plt.legend()
        """
        if cut :
            plt.savefig('Evolution_des_erreurs_en_fonction_du_seuil_de_détection_gris.png', dpi=300)
        else :
            plt.savefig('Evolution_des_erreurs_en_fonction_du_seuil_de_détection_de_noirs_gris.png', dpi=300)
        """