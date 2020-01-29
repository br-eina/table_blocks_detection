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
# from tesserocr import PyTessBaseAPI, PSM

# parser = argparse.ArgumentParser()
# parser.add_argument("--img", help="help_image_name")
# args = parser.parse_args()


from os import listdir
from os.path import isfile, join
mypath = "docs/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# print(onlyfiles)

new_list = []

for filename in onlyfiles:
    new = filename[:-4]
    new_list.append(new)


# with open('data/data_text_blocks_tables_inv-0001.data', 'rb') as filehandle:
#     text_blocks_rows = pickle.load(filehandle)




with open("features.csv", mode='w', newline='') as file:
    writer = csv.writer(file, delimiter= ',')

    headers = ['inv_numb', 'node', 'x', 'y', 'w', 'h', 'neighbors', 'in_table']
    writer.writerow(headers)
    for image_name in new_list:
        image_path = "docs/{0}.jpg".format(image_name)
        image = cv2.imread(image_path)

        min_resol = min(image.shape[0], image.shape[1])

        node_list = []

        if os.path.isfile('data/data_text_blocks_tables_{0}.data'.format(image_name)):

            with open('data/data_text_blocks_tables_{0}.data'.format(image_name), 'rb') as filehandle:
                # read the data as binary data stream
                text_blocks_rows = pickle.load(filehandle)
            
            for ind_row, row in enumerate(text_blocks_rows):
                for ind_block, block in enumerate(row):
                    node = (ind_row, ind_block)
                    node_list.append(node)

                    # with 

            

            for ind_row, row in enumerate(text_blocks_rows):
                for ind_block, block in enumerate(row):
                    node = (ind_row, ind_block)
                    neighbors = []

                    # Upper node
                    neighb_node = (ind_row - 1, ind_block)
                    if neighb_node in node_list:
                        neighb_block = text_blocks_rows[ind_row - 1][ind_block]
                        if (block['y'] - (neighb_block['y'] + neighb_block['h'])) < min_resol / 4:
                            neighbors.append(neighb_node)
                    
                    # Down node
                    neighb_node = (ind_row + 1, ind_block)
                    if neighb_node in node_list:
                        neighb_block = text_blocks_rows[ind_row + 1][ind_block]
                        if (neighb_block['y'] - (block['y'] + block['h'])) < min_resol / 4:
                            neighbors.append(neighb_node)

                    # Left node
                    neighb_node = (ind_row, ind_block - 1)
                    if neighb_node in node_list:
                        neighb_block = text_blocks_rows[ind_row][ind_block - 1]
                        if (block['x'] - (neighb_block['x'] + neighb_block['w'])) < min_resol / 4:
                            neighbors.append(neighb_node)

                    # Right node
                    neighb_node = (ind_row, ind_block + 1)
                    if neighb_node in node_list:
                        neighb_block = text_blocks_rows[ind_row][ind_block + 1]
                        if (neighb_block['x'] - (block['x'] + block['w'])) < min_resol / 4:
                            neighbors.append(neighb_node)


                    # node_list.append(node)

                    data = [image_name, node, block['x'], block['y'], block['w'], block['h'], neighbors, block['in_table']]
                    writer.writerow(data)


# print(node_list)