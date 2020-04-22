from argparse import ArgumentParser
from os import listdir, makedirs
from os.path import isfile, join, exists
from tqdm import tqdm
from inv_processing import (detect_lines_symbols,
                            constr_rows,
                            constr_blocks,
                            detect_table)

DEF_FOLDER = 'docs/'

def parsing():
    parser = ArgumentParser(description='Detect chars, textblocks and tables on invoice images')
    parser.add_argument('--sel', metavar='SELECTION_TYPE', default='folder', type=str,
                        help='Type "files" to select files (default: folder).')
    parser.add_argument('--fol', metavar='FOLDER_PATH', default=DEF_FOLDER, type=str,
                        help='Path of the folder (default: docs/).')
    parser.add_argument('--img', metavar='IMG_NAME', type=str, nargs='+',
                        help='Images to process. Type names without extension.')
    args = parser.parse_args()
    folder_path = args.fol
    img_names = []
    if args.sel == 'folder':
        files_in_folder = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
        img_names.extend([filename[:-4] for filename in files_in_folder])
    elif args.sel == 'files':
        img_names.extend(args.img)
    else:
        raise ValueError('SELECTION_TYPE must be "files" or "folder"')
    return img_names, folder_path

def create_folders(image_name):
    if not exists('results/{0}'.format(image_name)):
        makedirs('results/{0}'.format(image_name))
    if not exists('results/{0}/binary'.format(image_name)):
        makedirs('results/{0}/binary'.format(image_name))

def main():
    img_names, folder_path = parsing()
    print(f'{len(img_names)} images to process: \n')
    pbar = tqdm(img_names)
    for ind_img, image_name in enumerate(pbar):
        create_folders(image_name)
        image_path = f'{folder_path + image_name}.jpg'
        # Script sequence
        detect_lines_symbols.main(image_name, image_path)
        pbar.set_description(f'Image #{ind_img+1}: {image_name}')
        constr_rows.main(image_name, image_path)
        pbar.set_description(f'Image #{ind_img+1}: {image_name}')
        constr_blocks.main(image_name, image_path)
        pbar.set_description(f'Image #{ind_img+1}: {image_name}')
        detect_table.main(image_name, image_path)
        pbar.set_description(f'Image #{ind_img+1}: {image_name}')

if __name__ == "__main__":
    main()
