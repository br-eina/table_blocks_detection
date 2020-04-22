import numpy as np
import cv2
import json
import copy
import random
from collections import Counter
import pickle
import csv
import os
import argparse
import pandas as pd

def show_image(image):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", image)
    cv2.waitKey(0)

def save_image(image, filename):
    cv2.imwrite(filename, image)

def show_image_symbols_not_in_table(image, symbols_not_in_table):
    image_to_show = image.copy()
    for element in symbols_not_in_table:
        p_1 = (element['x'], element['y'])
        p_2 = (element['x'] + element['w'], element['y'] + element['h'])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 2)
    show_image(image_to_show)

# image_name = 'schet_opl-23'

# # image_path = "docs/{0}.jpg".format(image_name)
# image_path = "categories/___/{0}.jpg".format(image_name)

# image = cv2.imread(image_path)

# # Load symbols not in table
# with open("data/symbols_not_in_table_{0}.data".format(image_name), 'rb') as filehandle:
#     # read the data as binary data stream
#     symbols_not_in_table = pickle.load(filehandle)

# # show_image_symbols_not_in_table(image, symbols_not_in_table)

# # print(symbols_not_in_table)
# path_annotations = '/content/drive/My Drive/datasets/docs_text_blocks_tables.csv'
# df_textblocks = pd.read_csv(path_textblocks)



test = [
    {'x': 123, 'y': 1212},
    {'x': 121221, 'y': 21}
]

with open("test.data", 'wb') as f:
    pickle.dump(test, f)

# Load text_blocks elem
with open('categories/___/data/blocks_not_in_table_schet_fact-01.data', 'rb') as filehandle:
    # read the data as binary data stream
    text_blocks_rows = pickle.load(filehandle)

print()


