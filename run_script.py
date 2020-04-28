from argparse import ArgumentParser
from os import listdir, makedirs
from os.path import isfile, join, exists
from tqdm import tqdm
from inv_processing import (detect_lines_symbols,
                            constr_rows,
                            constr_blocks,
                            detect_table)
from scripts import draw_predictions

def create_folders(image_name):
    folders = [f'inv_processing/data',
               f'results',
               f'results/{image_name}',
               f'results/{image_name}/binary',
               f'results/{image_name}/text',
               f'results/{image_name}/lines',
               f'data_not_in_table']
    for folder in folders:
        if not exists(folder):
            makedirs(folder)

def main():
    # image_name = 'image_test'
    # image_path = f'{image_name}.jpg'
    # create_folders(image_name)

    draw_predictions.main()

if __name__ == "__main__":
    main()
