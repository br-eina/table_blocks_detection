import csv
import pickle
from os import listdir
from os.path import isfile, join
import pandas as pd
from ast import literal_eval
import numpy as np

path_images = 'categories/___/'
image_names = [f[:-4] for f in listdir(path_images) if isfile(join(path_images, f))]

# name = image_names[0]
# print(name.partition('-'))

path_ann = 'annotator/annotations/large_blocks.csv'
df = pd.read_csv(path_ann)
print(df.head())








# # Textblocks:
# with open("blocks_nr.csv", mode='w', newline='') as file:
#     writer = csv.writer(file, delimiter=',')

#     headers = ['filename', 'x', 'y', 'w', 'h']
#     writer.writerow(headers)

#     for image_name in image_names:
#         with open('categories/___/data/blocks_not_in_table_{}.data'.format(image_name), 'rb') as f:
#             text_blocks = pickle.load(f)

#             for block in text_blocks:
#                 data = [image_name, block['x'], block['y'], block['w'], block['h']]
#                 writer.writerow(data)


