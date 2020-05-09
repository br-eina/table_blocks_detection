"""Draw predictions on the test images"""
import cv2
import pandas as pd
from inv_processing import utils

def main(element_type, prediction=True, folder_ender=""):
    """Read dataset with 'prediction' field and draw predictions on the images.

        Args:
            element_type (str): has to be either 'blocks' or 'symbols'.
            prediction (bool, optional): if True - draw bboxes for predictions, otherwise (False) for labels.
                Defaults to True.
            folder_ender (str, optional): ender of the folder (labels{folder_ender}).
                Defaults to empty string.

        Returns:
            None

    """
    path_df = f'pred_{element_type}.csv'
    df = pd.read_csv(path_df)

    test_filenames = df['filename'].unique()
    for image_name in test_filenames:
        df_inv = df.loc[df['filename'] == image_name]

        row = df_inv.to_dict('records')

        image_path = f'docs/test/{image_name}.jpg'
        if prediction:
            label_field = 'prediction'
            if element_type == 'blocks':
                folder = f'predictions{folder_ender}'
            else:
                folder = f'predictions{folder_ender}/symbols'
        else:
            label_field = 'label'
            if element_type == 'blocks':
                folder = f'labels{folder_ender}'
            else:
                folder = f'labels{folder_ender}/symbols'

        image = cv2.imread(image_path)

        utils.create_folders(folder)
        utils.save_image(image, path=f'{folder}/{image_name}.jpg')

        utils.bounding_boxes(image, image_name, label_field=label_field, method='row', row=row,
                             path=f'{folder}/{image_name}_pred.jpg')

if __name__ == "__main__":
    _ELEMENT_TYPE = 'blocks'
    main(_ELEMENT_TYPE)
