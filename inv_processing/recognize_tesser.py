import os
from os import listdir, makedirs
from os.path import isfile, join
from inv_processing.utils import create_folders

def main(image_name):
    create_folders(f'tesser_data/{image_name}/recognized')
    folder_path = f'tesser_data/{image_name}'
    label_images = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

    doc_id_images = [image for image in label_images if image.startswith('doc_id')]
    info_images = [image for image in label_images if image.startswith('info')]
    total_images = [image for image in label_images if image.startswith('total')]
    verif_images = [image for image in label_images if image.startswith('verif')]

    # CMD commands:
    owd = os.getcwd()
    os.chdir('Tesseract-OCR')

    for images in (doc_id_images, info_images, total_images, verif_images):
        if images:
            for image in images:
                cmd = f"tesseract E:\__PR\docs\\table_blocks_detection\\tesser_data\{image_name}\{image} E:\__PR\docs\\table_blocks_detection\\tesser_data\{image_name}\\recognized\{image.split('.')[0]} -l rus --psm 6"
                os.system(f'cmd /c {cmd}')

    os.chdir(owd)

    # Read recognized txt and accumulate info:
    txt_folder = f'tesser_data/{image_name}/recognized'
    txt_files = [f for f in listdir(txt_folder) if isfile(join(txt_folder, f))]

    doc_id_txts = [txt_file for txt_file in txt_files if txt_file.startswith('doc_id')]
    info_txts = [txt_file for txt_file in txt_files if txt_file.startswith('info')]
    total_txts = [txt_file for txt_file in txt_files if txt_file.startswith('total')]
    verif_txts = [txt_file for txt_file in txt_files if txt_file.startswith('verif')]

    for txts in (doc_id_txts, info_txts, total_txts, verif_txts):
        if txts:
            full_filename = txts[0].split('-')[0]
            with open(f'{txt_folder}/full_{full_filename}.txt', 'w', encoding='utf-8') as w:
                for txt in txts:
                    with open(f'{txt_folder}/{txt}', encoding='utf-8') as f:
                        for line in f:
                            w.write(line)

        # with open(f'{txt_folder}/info_full.txt', 'w') as f:
        #     f.write(info_text)

