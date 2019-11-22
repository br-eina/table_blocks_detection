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