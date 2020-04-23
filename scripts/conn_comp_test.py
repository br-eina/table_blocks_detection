import sys
sys.path.append(".")
from inv_processing import utils, cc_utils
import cv2

def main(image_name, image_path):
    image = cv2.imread(image_path)

    # Threshold image
    thresh = utils.threshold_image(image)
    thresh = 255 - thresh

    # Get connected components
    retval, labels, stats_np, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)

    cc_utils.display_centroids(image, centroids)


if __name__ == "__main__":
    _IMAGE_NAME = "cc_image_test"
    _IMAGE_PATH = "{}.jpg".format(_IMAGE_NAME)
    main(_IMAGE_NAME, _IMAGE_PATH)