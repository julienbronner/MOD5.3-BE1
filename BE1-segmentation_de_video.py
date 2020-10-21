# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 08:24:53 2020

@author: julbr
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Construct a VideoReader object associated with the sample file.

vidObj = cv2.VideoCapture('Pub_C+_176_144.mp4')

# Determine the height and width of the frames.
if not vidObj.isOpened(): 
	  print("Error opening video stream or file")

else: 

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
      if count >= 50:
          break

Red = []
Green = []
Blue = []

for i in range(50):
    r, g, b = 0, 0, 0
    for j in range(vidHeight):
        for k in range(vidWidth):
            r += Mat[i][j][k][0]
            g += Mat[i][j][k][1]
            b += Mat[i][j][k][2]
    Red.append(r)
    Green.append(g)
    Blue.append(b)
    
plt.hist([Red, Green, Blue], bins = [x for x in range(0, 50)], color = ['red', 'green', 'blue'],
         label = ['Red', 'Green', 'Blue']) # bar est le defaut
plt.ylabel('Amount')
plt.xlabel('Frame')
plt.legend()