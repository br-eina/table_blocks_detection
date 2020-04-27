"""Numerate files in the folder"""
from argparse import ArgumentParser
import os
from tqdm import tqdm


_FOLDER = 'docs/'

def parsing():
    """Parsing arguments from cmd"""
    parser = ArgumentParser(description='Convert pdf to jpg')
    parser.add_argument('--folder', metavar='FOLDER', default=_FOLDER, type=str,
                        help='Path of the folder with files (default: "docs/")')
    args = parser.parse_args()
    return args.folder

def main():
    """Script for numerating files"""
    folder = parsing()
    os.chdir(folder)
    filenames = os.listdir()
    print(f'{len(filenames)} files to numerate: \n')

    pbar = tqdm(filenames)
    for ind_file, file_path in enumerate(pbar):
        pbar.set_description(f'Processind file #{ind_file+1}')
        pbar.leave = True

        # Define index of the file:
        if len(str(ind_file)) == 1:
            index = f'000{ind_file}'
        elif len(str(ind_file)) == 2:
            index = f'00{ind_file}'
        elif len(str(ind_file)) == 3:
            index = f'0{ind_file}'
        else:
            index = f'{ind_file}'

        filename = 'inv'
        ext = file_path.split('.')[1]

        os.rename(file_path, f'{filename}-{index}.{ext}')

if __name__ == "__main__":
    main()
