# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 08:24:53 2020

@author: julbr
"""
import cv2
import numpy as np

# Construct a VideoReader object associated with the sample file.

vidObj = cv2.VideoCapture('Pub_C+_176_144.mp4')

# Determine the height and width of the frames.
if (vidObj.isOpened()== False): 
	  print("Error opening video stream or file")

if vidObj.isOpened(): 

    nb_frames = int(vidObj.get(7))
    vidWidth  = int(vidObj.get(3))
    vidHeight = int(vidObj.get(4))

    print('Largeur : ', vidWidth, ' ; Hauteur : ', vidHeight, " ; Nb d'images : ", nb_frames)

# Create a Python movie structure array, Mat.
Mat = np.zeros((nb_frames, vidHeight, vidWidth, 3))

success,image = vidObj.read()
count = 0
success = True
while success:
  success,image = vidObj.read()
  Mat[count] = image         # save each frame into Mat
  count += 1
