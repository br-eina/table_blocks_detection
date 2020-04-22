from pdf2image import convert_from_path
from pdf2image.exceptions import (PDFInfoNotInstalledError,
                                  PDFPageCountError,
                                  PDFSyntaxError)
import os
from tqdm import tqdm
from PIL import Image

def main():
    pdf_folder = '1C pdf/'
    img_folder = '1C img/'

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
        for ind_img, image in enumerate(images_in_pdf):
            image.save(img_folder+f'inv-{ind_pdf}-{ind_img}.jpg')

if __name__ == "__main__":
    main()
