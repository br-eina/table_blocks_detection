"""Provides high-level support for CV algorithms and image processing."""
import cv2

def show_image(image):
    """ Visualize image in the floating window.

    Args:
        image (np.array): image to visualize.

    Returns:
        None

    """
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", image)
    cv2.waitKey(0)

def save_image(image, filename):
    """Save image in the specialized folder.

    Args:
        image (np.array): image to save
        filename (str): image path

    Returns:
        None

    """
    cv2.imwrite(filename, image)
