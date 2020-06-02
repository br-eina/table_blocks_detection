import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import json_normalize
from os import listdir
from os.path import isfile, join

import pickle

from sklearn.model_selection import cross_val_score, StratifiedKFold, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import itertools
import seaborn as sns
import joblib

def clean_label(x):
    return x.split('"')[3]

def remove_ext(x):
    return x.partition('.')[0]

def area(a, b):  # returns None if rectangles don't intersect
    a_x_min, b_x_min = a['x'], b['x']
    a_x_max, b_x_max = a['x'] + a['w'], b['x'] + b['w']
    a_y_min, b_y_min = a['y'], b['y']
    a_y_max, b_y_max = a['y'] + a['h'], b['y'] + b['h']

    dx = min(a_x_max, b_x_max) - max(a_x_min, b_x_min)
    dy = min(a_y_max, b_y_max) - max(a_y_min, b_y_min)
    if dx >= 0 and dy >= 0:
        return dx * dy
    return None

def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.05 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")


    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()

def dataset_construction():
    # Load annotation:
    path_ann = 'annotator/annotations/annotation.csv'
    df_ann = pd.read_csv(path_ann)

    # Удаляем ненужные колонки:
    col_to_drop = [1, 2, 3, 4]
    df_ann.drop(df_ann.columns[col_to_drop], axis=1, inplace=True)
    df_ann.rename(columns={'region_attributes': 'label'}, inplace=True)

    df_ann['label'] = df_ann['label'].apply(clean_label)

    df_attr = json_normalize(df_ann['region_shape_attributes'].map(eval))
    df_attr.drop('name', axis=1, inplace=True)

    df_ann.drop('region_shape_attributes', axis=1, inplace=True)
    df_ann['x'] = df_attr['x'].astype(int)
    df_ann['y'] = df_attr['y'].astype(int)
    df_ann['w'] = df_attr['width'].astype(int)
    df_ann['h'] = df_attr['height'].astype(int)
    df_ann['filename'] = df_ann['filename'].apply(remove_ext)

    path_images = 'docs/'
    image_names = [f[:-4] for f in listdir(path_images) if isfile(join(path_images, f))]
    image_names.sort()

    # Mark blocks with annotated labels:
    df_blocks = pd.DataFrame(columns=['filename', 'img_h', 'img_w',
                                  'x', 'y', 'w', 'h', 'chars', 'in_table', 'label'])
    for image_name in image_names:
        path_block = f'data_not_in_table/blocks_non_table_{image_name}.data'

        with open(path_block, 'rb') as f:
            text_blocks = pickle.load(f)

        df_ann_dict = df_ann.loc[df_ann['filename'] == f'{image_name}'].to_dict(orient='records')

        for ann in df_ann_dict:
            for ind, block in enumerate(text_blocks):
                if area(block, ann) >= 10:
                    text_blocks[ind]['label'] = ann['label']
                text_blocks[ind]['filename'] = ann['filename']

        for i in range(len(text_blocks)):
            if 'label' not in text_blocks[i]:
                text_blocks[i]['label'] = 'misc'
        df_one_doc_blocks = pd.DataFrame(text_blocks)
        df_blocks = pd.concat([df_blocks, df_one_doc_blocks], sort=False)

    path_csv_blocks = 'labeled_nontable_blocks.csv'
    df_blocks.to_csv(path_csv_blocks, index=False)
    return df_blocks

def main():
    # Dataset preparation:
    fact_filenames = {'inv-0011', 'inv-0014', 'inv-0020', 'inv-0027', 'inv-0029',
                  'inv-0031', 'inv-0032', 'inv-0033', 'inv-0039', 'inv-0040',
                  'inv-0062', 'inv-0063', 'inv-0074', 'inv-0075', 'inv-0076',
                  'inv-0077', 'inv-0078', 'inv-0081', 'inv-0083', 'inv-0084',
                  'inv-0085', 'inv-0086', 'inv-0087', 'inv-0088', 'inv-0089',
                  'inv-0090', 'inv-0091', 'inv-0092', 'inv-0093', 'inv-0094',
                  'inv-0095', 'inv-0096', 'inv-0097', 'inv-0098', 'inv-0099',
                  'inv-0100', 'inv-0101', 'inv-0102'}
    path_csv_blocks = 'labeled_nontable_blocks.csv'
    df_blocks = pd.read_csv(path_csv_blocks)
    df_blocks['x_c'] = (df_blocks['x'] + df_blocks['w'] // 2) / df_blocks['img_w']
    df_blocks['y_c'] = (df_blocks['y'] + df_blocks['h'] // 2) / df_blocks['img_h']
    df_blocks['w'] = df_blocks['w'] / df_blocks['img_w']
    df_blocks['h'] = df_blocks['h'] / df_blocks['img_h']
    df_blocks.drop(columns=['img_h', 'img_w', 'x', 'y'], inplace=True)
    df_blocks.drop(df_blocks[df_blocks.filename == 'inv-0069'].index, inplace=True)
    # df_blocks = df_blocks.loc[df_blocks['filename'].isin(fact_filenames) == False]
    df_blocks['above_1'] = df_blocks['above_1'].astype('int64')
    df_blocks['between'] = df_blocks['between'].astype('int64')
    df_blocks['below_2'] = df_blocks['below_2'].astype('int64')

    # Construct test dataset:
    test_filenames = {'inv-0000', 'inv-0022', 'inv-0024', 'inv-0032', 'inv-0040',
                  'inv-0044', 'inv-0046', 'inv-0047', 'inv-0051', 'inv-0059',
                  'inv-0064', 'inv-0067', 'inv-0073', 'inv-0075',
                  'inv-0079', 'inv-0083', 'inv-0088', 'inv-0098', 'inv-0100',
                  'inv-0102', 'inv-0103', 'inv-0113'}
                  # inv-0069
    test_filenames = test_filenames - fact_filenames

    df_blocks_test = df_blocks.loc[df_blocks['filename'].isin(test_filenames)]
    df_blocks_train = df_blocks.loc[df_blocks['filename'].isin(test_filenames) == False]

    # Choose the numeric features:
    cols = []
    for i in df_blocks_train.columns:
        if (df_blocks_train[i].dtype == "float64") or (df_blocks_train[i].dtype == 'int64'):
            cols.append(i)
    print('Numeric features: ', cols)

    # Divide the dataset into the input and target
    X = df_blocks_train[cols].copy()
    y, uniques = pd.factorize(df_blocks_train['label'])

    # Test RF quality:
    rfc = RandomForestClassifier(max_depth=16, max_features=3, min_samples_leaf=1, random_state=42, n_jobs=-1)
    rfc.fit(X, y)

    # Choose the numeric features - test:
    cols = []
    for i in df_blocks_test.columns:
        if (df_blocks_test[i].dtype == "float64") or (df_blocks_test[i].dtype == 'int64'):
            cols.append(i)

    # Divide the dataset into the input and target
    X_test = df_blocks_test[cols].copy()
    y_test, uniques = pd.factorize(df_blocks_test['label'])

    prediction = rfc.predict(X_test)
    # conf_m = confusion_matrix(y_test, prediction, labels=[0, 1, 2, 3, 4])
    # plot_confusion_matrix(conf_m, target_names=['misc', 'doc_id', 'info', 'total', 'verif'])

    # label_encoding = {0: 'misc', 1: 'doc_id', 2: 'info', 3: 'total', 4: 'verif'}
    # df_blocks_test = df_blocks_test.assign(prediction=prediction)
    # df_blocks_test['prediction'] = df_blocks_test['prediction'].map(label_encoding)
    # print(df_blocks_test.head())
    joblib.dump(rfc, 'rf_blocks.joblib')