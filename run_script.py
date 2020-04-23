from argparse import ArgumentParser
from os import listdir, makedirs
from os.path import isfile, join, exists
from tqdm import tqdm
from inv_processing import (detect_lines_symbols,
                            constr_rows,
                            constr_blocks,
                            detect_table)

def main():
    image_name = 'image_test'
    image_path = f'{image_name}.jpg'

    detect_lines_symbols.main(image_name, image_path)

if __name__ == "__main__":
    main()