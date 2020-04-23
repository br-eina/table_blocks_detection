"""Provides high-level support for CV algorithms and image processing."""
import cv2
from inv_processing import utils

def display_centroids(image, centroids):
    """Display centroids for connected components.

    Args:
        image: (np.array): background image to draw centroids on
        centroids: (np.array): coordinates of centroids

    Returns:
        None

    """
    image_to_show = image.copy()
    for coord in centroids:
        cv2.circle(image_to_show, (int(coord[0]), int(coord[1])), 6, (0, 0, 255), -1)
    utils.show_image(image_to_show)
