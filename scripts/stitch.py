#!/usr/bin/env python3
#
# stitch.py
#
# VERSION 1
#
# LAST EDIT: 09/14/2021
#
# Author: Laura Brancati, based on function found on: https://www.pyimagesearch.com/2018/12/17/image-stitching-with-opencv-and-python/
#
# Sitches images together that have overlapping areas. 
#
##############################################################################
# REQUIRED MODULES
##############################################################################
import os
import argparse
import cv2
import imutils
import numpy as np

##############################################################################
# FUNCTIONS
##############################################################################
def image_stitch(img_directory, output_path):
    img_dir = img_directory
    names = os.listdir(img_dir)

    #get all of the image file names from the directory and put them in a list
    images = []
    for name in names:
        img_path = os.path.join(img_dir, name)
        image = cv2.imread(img_path)
        images.append(image)

    #call stitch function and stitch images; status is 0 if succesfull
    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    stitcher.setPanoConfidenceThresh(.8)
    status, stitched = stitcher.stitch(images)

    if status==0:
        # create stitched image file
        cv2.imwrite(os.path.join(output_path+".jpg"), stitched)
        print("success!")
        
    else:
        print("status:", status)

##############################################################################
# MAIN
##############################################################################
if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="stitch images together that are in a directory")
    p.add_argument("-i", "--images", type=str, required=True,
	    help="path of input directory of images to stitch")
    p.add_argument("-o", "--output", type=str, required=True,
	    help="path to the output image")

    args = p.parse_args()
    
    #call function
    stitched = image_stitch(args.images, args.output)