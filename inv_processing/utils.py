"""Provides high-level support for CV algorithms and image processing."""
import cv2

def show_image(image):
    """Visualize image in the floating window.

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

def grayscale_image(image):
    """Grayscale the image.

    Args:
        image (np.array): image to grayscale

    Returns:
        gray_image (np.array): grayscaled image

    """
    num_channels = 3
    if len(image.shape) == num_channels:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def threshold_image(image):
    """Threshold the image (OTSU).

    Args:
        image (np.array): image to threshold

    Returns:
        thresh_image (np.array): thresholded image

    """
    gray = grayscale_image(image)
    thresh_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh_image
