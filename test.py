import numpy as np
import cv2 
from PIL import Image
import sys
import json
import math
import copy
import random
import itertools
from collections import Counter
import pickle
import matplotlib.pyplot as plt
import csv
# import pytesseract
import os
# import tesserocr
# from tesserocr import PyTessBaseAPI, PSM

import argparse

def save_image(image, filename):
    cv2.imwrite(filename, image)

# with open('gt_tables.txt') as json_file:
#     data = json.load(json_file)
#     # for p in data['people']:
#     #     print('Name: ' + p['name'])
#     #     print('Website: ' + p['website'])
#     #     print('From: ' + p['from'])
#     #     print('')

# print(data)

# from os import listdir
# from os.path import isfile, join
# mypath = "docs/"
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# print(onlyfiles)

# new_list = []

# for filename in onlyfiles:
#     new = filename[:-4]
#     new_list.append(new)

# print(new_list)

# with open("gt_tables.txt", "w+") as text_file:
#     for ind, image_name in enumerate(new_list):
#         string = '{} : '.format(image_name)
#         # string1 = "python code\detect_lines_symbols.py --img {0} & ".format(image_name)
#         # string2 = "python code\constr_rows.py --img {0} & ".format(image_name)
#         # string3 = "python code\constr_blocks.py --img {0} & ".format(image_name)
#         # if ind != len(new_list) - 1:
#         #     string4 = "python code\\detect_table.py --img {0} &".format(image_name)
#         # else:
#         #     string4 = "python code\\detect_table.py --img {0}".format(image_name)
#         # string = string1 + string2 + string3 + string4
#         print(string, file=text_file)










# # define an empty list
# gt_number_tables = []

# # open file and read the content in a list
# with open('gt_number_tables.txt', 'r') as filehandle:
#     for line in filehandle:
#         # remove linebreak which is the last character of the string
#         currentPlace = line[0]

#         # add item to the list
#         gt_number_tables.append(currentPlace)


# print(gt_number_tables)



image_name = "inv-0014"
binary_image_path = "results/{0}/binary/{0}_binary.jpg".format(image_name)
binary_image = cv2.imread(binary_image_path)
new_binary_image = 255 - binary_image


save_image(new_binary_image, "NEW+BINARY.jpg")











# image_name = "inv-0001"
# image_path = "docs/{0}.jpg".format(image_name)
# image = cv2.imread(image_path)

# binary_image_path = "results/{0}/binary/{0}_binary.jpg".format(image_name)
# binary_image = cv2.imread(binary_image_path)

# # Load text_blocks elem
# with open('data/data_text_blocks_{0}.data'.format(image_name), 'rb') as filehandle:
#     # read the data as binary data stream
#     text_blocks_rows = pickle.load(filehandle)



# with PyTessBaseAPI(path='C:/pr/table_blocks_detection/tessdata', lang='rus+eng', psm=PSM.SINGLE_BLOCK) as api:

#     for row in text_blocks_rows:
#         for text_block in row:
#             t = 3
#             y = text_block['y']
#             if y >= t:
#                 y = text_block['y'] - t
#             h = text_block['h'] + 2*t
#             x = text_block['x']
#             if x >= t:
#                 x = text_block['x'] - t
#             w = text_block['w'] + 2*t
#             cropped_image = binary_image[y:y+h, x:x+w].copy()

#             api.SetImageFile(cropped_image)
#             text = api.getUTF8Text()

#             print(text)
