# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 08:24:53 2020

@author: julbr
"""

import cv2

vidObj = cv2.VideoCapture('Pub_C+_176_144.mp4')
success,image = vidObj.read()
count = 0
print(success)
while success:
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidObj.read()
  #print('Read a new frame: ', success)
  count += 1
  

# pour les dimensions
if vidObj.isOpened(): 

    width  = vidObj.get(3) # float
    height = vidObj.get(4) # float

    print('width, height:', width, height)