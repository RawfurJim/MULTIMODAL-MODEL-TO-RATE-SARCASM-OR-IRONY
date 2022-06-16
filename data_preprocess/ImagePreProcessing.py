# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:29:31 2021

@author: SHIKHAR TIWARI
"""
# Importing necessary libraries

import cv2 as cv       
# OpenCV(cv2) is the open-source library for the computer vision,
# machine learning, and image processing. It plays a major role 
# in real-time operation on images or videos. It helps to process
# images and videos to identify objects, faces, specific patterns etc. 


import numpy as np
# Numpy, is a python library. On integrating it with OpenCV it become capable of 
# processing the OpenCV array structure for analysis. 
# For example: To identify image pattern and its various features we use Numpy 
# array and perform mathematical operations on these features.


import os
# This module in python provides functions to interact with operating system.
# For example: To move files across the directories, listing out files and directories,
# deleting directory or files and many more.


######################################################################################################################################################################################################################################################

src=r'D:\Part1'                                                                # source directory.
dst=r'D:\Image_Dataset'                                                        # destination directory.
srcfiles=os.listdir(src)                                                       # files/Images in source directory.
dstfiles=os.listdir(dst)                                                       # files/Images in destination directory.
os.chdir(src)                                                                  # changes the current working directory to source directory.

                                                                               # Now the source directory becomes a current working directory so that we can access the images stored in it.

i=1                                                                            # i is initialised to save the processed images with unique number that is, to keep the track of which image corresponds to which red comment box. Its value increases by 1 everytime the below 'for' loop runs.

                                                                               # The srcfiles is a list of all the images stored in source directory, the 'for' loop iterates over the srcfiles.

for photo in srcfiles:
    photopath=os.path.join(src, photo)  
    img=cv.imread(photopath,cv.IMREAD_UNCHANGED)                               # Loads an image from specified path(photopath). 
    img1=img.copy()                               
    img2=img.copy()                                                            # Creates 2 copies of the same image.
    
                                                                               # By defaut OpenCV loads image in BGR color format.   
 
    hsv=cv.cvtColor(img, cv.COLOR_BGR2HSV)                                     # Converts image from BGR TO HSV.
                                                                               # In HSV, it is more easier to represent a color than BGR color-space.
                                                                               # It allows to identify a particular color using a single value, the hue, instead of three values. 
                                             
                                                                               # Since the image contains red colored comment box, the aim is to detect and crop out the red box from the image.                                             
                                                                               # The red color, in OpenCV, has the hue values approximately in the range of 0 to 10 and 160 to 180.                                           

    lower_range = np.array([0, 100, 100], dtype=np.uint8)                      # The lower range is the minimum shade of red that will be detected.
    upper_range = np.array([2.5, 255, 255], dtype=np.uint8)                    # The upper range is the maximum shade of red that will be detected.
    mask1 = cv.inRange(hsv, lower_range, upper_range)                          # Creates mask1 for the image. It returns a specific area of image, containing the red color that are between the lower and upper range.

    lower_range = np.array([160, 100, 100], dtype=np.uint8)
    upper_range = np.array([179, 255, 255], dtype=np.uint8)                    # Similarily for the hue values between 160-180, created mask2
    mask2 = cv.inRange(hsv, lower_range, upper_range)
    
    
    mask=cv.add(mask1,mask2)                                                   # Combines both the masks
    ret, threshold=cv.threshold(mask, 240, 255, 0)                             # Applies threshold to remove artifacts (pixels with values other than the [range:240-255] are set to 0)
    contours, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)  # It returns a list of detected contours. 
                                                                                          # Contours is a curve joining all the continuous points (along the boundary), having same color 
    
    
    largestcontour = sorted(contours, key=lambda c: cv.contourArea(c), reverse=True)      # Returns a list of all the detected contours in descending order of their areas

                                                                               # In almost all the images the largest contour is of red box. Keeping that in mind, I selected only the contour having largest enclosed area for my further processing 


    for c in largestcontour[:1]:                                               # Takes the contour having largest area. 
        if cv.contourArea(c)>14274:                                            # Contour area should be greater than 14274 to proceed futher. If not, the loop breaks at this point and next image is loaded.
                                                                               # It has been found by hit and trial method, that contours with area greater than 14274 always corresponds to red box.
            
            cv.drawContours(img,[c], 0, (0,255,0), 3)                          # Draws a green colored contour onto the original image. It accuratly overlaps the Red Box. 
            (x,y,w,h) = cv.boundingRect(c)                                     # Calculates the coordinates of overlapping contour which is also the coordinates of the Red Box.
            
            CmntBox_roi=img1[y:y+h,x:(x+w)]                                    # Cropping out the Red comment box from the original image
            image_roi=cv.rectangle(img2, (x,y),(x+w,y+h),(255,255,255),-1)     # Filling up the cropped out area of image with the white color
            
            image_path='D:\Image_Dataset'                                      # Folder path where image will be stored
            CmntBoxpath='D:\Redbox_Dataset'                                    # Folder path where red box will be stored
            
                                                                               # Now, in some cases the image is composed of only the white pixels which is of no use and should be removed.
                                                                               # So using 'if-else' statement these images are moved to 'Exception' folder and
                                                                               # rest of the images and red boxes are successfully stored in their respective folders as mentioned below.      
            if np.mean(image_roi)>=240:
                cv.imwrite(os.path.join('D:\Exception', 'exception{}.png'.format(i)),image_roi)
            else:
                cv.imwrite(os.path.join(image_path, 'Image{}.png'.format(i)),image_roi)
                cv.imwrite(os.path.join(CmntBoxpath, 'CmntBox{}.png'.format(i)),CmntBox_roi)
            i=i+1        

####################################################################################################################################################################################################################################################### 


