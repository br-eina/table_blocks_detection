import pandas as pd
from joblib import load
import cv2
from inv_processing import utils

def save_cropped_image(image, image_name, text_blocks, t=3):
    for ind, block in enumerate(text_blocks):
        x, y, h, w = block['x']-t, block['y']-t, block['h']+2*t, block['w']+2*t
        crop_img = image[y:y+h, x:x+w]
        crop_path = f"tesser_data/{image_name}/{block['prediction']}-{ind}.jpg"
        utils.save_image(crop_img, crop_path)

def main(image_name):
    model = load('rf_blocks.joblib')

    # Df preparation:
    path_csv_blocks = 'labeled_nontable_blocks.csv'
    df_blocks = pd.read_csv(path_csv_blocks)
    df_blocks = df_blocks.loc[df_blocks['filename'] == image_name]
    df_blocks['x_c'] = (df_blocks['x'] + df_blocks['w'] // 2) / df_blocks['img_w']
    df_blocks['y_c'] = (df_blocks['y'] + df_blocks['h'] // 2) / df_blocks['img_h']
    df_blocks['w'] = df_blocks['w'] / df_blocks['img_w']
    df_blocks['h'] = df_blocks['h'] / df_blocks['img_h']
    df_blocks.drop(columns=['img_h', 'img_w', 'x', 'y'], inplace=True)
    df_blocks['above_1'] = df_blocks['above_1'].astype('int64')
    df_blocks['between'] = df_blocks['between'].astype('int64')
    df_blocks['below_2'] = df_blocks['below_2'].astype('int64')

    # Choose the numeric features:
    cols = []
    for i in df_blocks.columns:
        if (df_blocks[i].dtype == "float64") or (df_blocks[i].dtype == 'int64'):
            cols.append(i)

    # Divide the dataset into the input and target
    X = df_blocks[cols].copy()
    # y, uniques = pd.factorize(df_blocks['label'])

    prediction = model.predict(X)

    label_encoding = {0: 'misc', 1: 'doc_id', 2: 'info', 3: 'total', 4: 'verif'}
    df_blocks = pd.read_csv(path_csv_blocks)
    df_blocks = df_blocks.loc[df_blocks['filename'] == image_name]
    df_blocks = df_blocks.assign(prediction=prediction)
    df_blocks['prediction'] = df_blocks['prediction'].map(label_encoding)

    image_path = f'docs/test/{image_name}.jpg'
    image = cv2.imread(image_path)

    row = df_blocks.to_dict('records')
    utils.bounding_boxes(image, image_name, method=row, row=row,
                         label_field='prediction', path=f'predictions/{image_name}_pred.jpg')

    # Create folders for tesseract:
    utils.create_folders('tesser_data', f'tesser_data/{image_name}')
    df_not_misc = df_blocks.loc[df_blocks['prediction'] != 'misc']
    blocks_doc_id = df_not_misc.loc[df_not_misc['prediction'] == 'doc_id'].to_dict(orient='records')
    blocks_info = df_not_misc.loc[df_not_misc['prediction'] == 'info'].to_dict(orient='records')
    blocks_total = df_not_misc.loc[df_not_misc['prediction'] == 'total'].to_dict(orient='records')
    blocks_verif = df_not_misc.loc[df_not_misc['prediction'] == 'verif'].to_dict(orient='records')

    # Crop image:
    if blocks_doc_id:
        save_cropped_image(image, image_name, blocks_doc_id)
    if blocks_info:
        save_cropped_image(image, image_name, blocks_info)
    if blocks_total:
        save_cropped_image(image, image_name, blocks_total)
    if blocks_verif:
        save_cropped_image(image, image_name, blocks_verif)