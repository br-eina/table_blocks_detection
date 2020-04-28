from inv_processing import utils
import cv2
import pandas as pd


def main():
    path_df = 'pred_blocks.csv'
    df = pd.read_csv(path_df)

    test_filenames = df['filename'].unique()
    for image_name in test_filenames:
        df_inv = df.loc[df['filename'] == image_name]

        row = df_inv.to_dict('records')

        image_path = f'docs/test/{image_name}.jpg'
        predict_folder = 'predictions'
        image = cv2.imread(image_path)

        utils.create_folders(predict_folder)
        utils.save_image(image, path=f'{predict_folder}/{image_name}.jpg')

        utils.bounding_boxes(image, image_name, pred=True, method='row', row=row,
                             path=f'{predict_folder}/{image_name}_pred.jpg')

if __name__ == "__main__":
    main()
