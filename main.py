"""Start document"""
from argparse import ArgumentParser
from os import listdir, makedirs
from os.path import isfile, join, exists
from tqdm import tqdm
from inv_processing import (detect_lines_symbols,
                            constr_rows,
                            constr_blocks,
                            detect_table)
from inv_processing.utils import create_folders


_DEF_FOLDER = 'docs/'

def parsing():
    """Parsing arguments from cmd"""
    parser = ArgumentParser(description='Detect chars, textblocks and tables on invoice images')
    parser.add_argument('--sel', metavar='SELECTION_TYPE', default='folder', type=str,
                        help='Type "files" to select files (default: folder).')
    parser.add_argument('--fol', metavar='FOLDER_PATH', default=_DEF_FOLDER, type=str,
                        help='Path of the folder (default: "docs/").')
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

def main():
    """Launch invoice processing"""
    folders_init = ['inv_processing/data',
                    'results',
                    'data_not_in_table']
    create_folders(*folders_init)
    img_names, folder_path = parsing()
    print(f'{len(img_names)} images to process: \n')
    pbar = tqdm(img_names)
    for ind_img, image_name in enumerate(pbar):
        pbar.set_description(f'Image #{ind_img+1}: {image_name}')
        # Create folders for debugging
        folders_debug = [f'results/{image_name}',
                         f'results/{image_name}/binary',
                         f'results/{image_name}/text',
                         f'results/{image_name}/lines',
                         f'results/{image_name}/rows',
                         f'results/{image_name}/table_debug']
        create_folders(*folders_debug)
        image_path = f'{folder_path + image_name}.jpg'
        # Script sequence
        detect_lines_symbols.main(image_name, image_path)
        constr_rows.main(image_name, image_path)
        constr_blocks.main(image_name, image_path)
        detect_table.main(image_name, image_path)

if __name__ == "__main__":
    main()
