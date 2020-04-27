"""Convert pdf to jpg"""
import os
from argparse import ArgumentParser
from pdf2image import convert_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError,
                                  PDFPageCountError,
                                  PDFSyntaxError)
from tqdm import tqdm
from PIL import Image
from inv_processing.utils import create_folders

_INPUT_FOLDER = '1C pdf/'
_OUTPUT_FOLDER = 'docs/'

def parsing():
    """Parsing arguments from cmd"""
    parser = ArgumentParser(description='Convert pdf to jpg')
    parser.add_argument('--input', metavar='INPUT_FOLDER', default=_INPUT_FOLDER, type=str,
                        help='Path of the input folder with pdf files (default: "1C pdf/")')
    parser.add_argument('--output', metavar='OUTPUT_FOLDER', default=_OUTPUT_FOLDER, type=str,
                        help='Path of the output folder with jpg files (default: "docs/")')
    args = parser.parse_args()
    return args.input, args.output

def main():
    """Launch pdf to jpg convertion"""
    pdf_folder, img_folder = parsing()
    create_folders(img_folder)

    owd = os.getcwd()
    os.chdir(pdf_folder)
    filenames = os.listdir()
    os.chdir(owd)

    print(f'{len(filenames)} PDFs to process: \n')

    pbar = tqdm(filenames)
    for ind_pdf, pdf_path in enumerate(pbar):
        pbar.set_description(f'Processind PDF #{ind_pdf+1}')
        pbar.leave = True
        images_in_pdf = convert_from_path(pdf_folder+pdf_path)
        if len(str(ind_pdf)) == 1:
            index = f'000{ind_pdf}'
        elif len(str(ind_pdf)) == 2:
            index = f'00{ind_pdf}'
        elif len(str(ind_pdf)) == 3:
            index = f'0{ind_pdf}'
        else:
            index = f'{ind_pdf}'
        for image in images_in_pdf:
            image.save(img_folder+f'inv-{index}.jpg')

if __name__ == "__main__":
    main()
