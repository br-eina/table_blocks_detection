import numpy as np
import cv2
# from PIL import Image
# import sys
import json
# import math
import copy
# import random
import pickle
# import utils
# from filenames import img_name
import os
import argparse

def show_image(image):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", image)
    cv2.waitKey(0)

def save_image(image, filename):
    cv2.imwrite(filename, image)

def write_to_json(stats, filename):
    data = []
    for ind, stat in enumerate(stats):
        data.append({
            'x': stat[0],
            'y': stat[1],
            'w': stat[2],
            'h': stat[3],
            'A': stat[4]
        })
    with open(filename, 'wb') as outfile:
    # store the data as binary data stream
        pickle.dump(data, outfile)

def gray_image(image):
    NUM_CHANNELS = 3
    if len(image.shape) == NUM_CHANNELS:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def threshold_image(image):
    gray = gray_image(image)
    thresh_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh_image
    