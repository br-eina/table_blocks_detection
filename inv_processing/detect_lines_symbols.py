import numpy as np
import cv2
from copy import deepcopy as copy
import pickle
from inv_processing import utils, cc_utils

def display_labels(labels, retval, indexes_to_remove, thresh, image_name):
    full_mask = thresh[:]
    full_mask = 0
    for label in range(1, retval):
        if label not in indexes_to_remove:
            mask = np.array(labels, dtype=np.uint8)
            mask[labels == label] = 255
            mask[labels != label] = 0
            full_mask = full_mask + mask
    if not full_mask.any():
        full_mask = thresh[:]
        full_mask[0:thresh.shape[0], 0:thresh.shape[1]] = 0
    utils.save_image(full_mask, "results/{0}/binary/{0}_lines_full.jpg".format(image_name))
    return full_mask

def detect_lines(stats, avg_height):
    stats_copy = copy(stats)
    indexes_to_remove = []
    for ind, stat in enumerate(stats_copy[:]):
        # 100 (50) - previous
        # Не таблицы и линии:
        # Если ширина меньше чем 30 высот и высота меньше чем 5 средних высот
        if stat[2] < 30 * stat[3] and stat[3] < 4 * avg_height:
            stats.remove(stat)
            indexes_to_remove.append(ind + 1)
    return stats, indexes_to_remove

def isolate_lines(src, structuring_element):
    cv2.erode(src, structuring_element, src, (-1, -1)) # makes white spots smaller
    cv2.dilate(src, structuring_element, src, (-1, -1)) # makes white spots bigger

def save_data(image, stats, all_text_stats, stats_lines, dil_lines_stats,
              vert_lines_stats, hor_lines_stats, avg_height, image_name):
    # TODO: temporary data
    # TODO: CC class
    # Save data
    cc_utils.dump_stats(image_name, all_text_stats,
                        cc_type='text')
    cc_utils.dump_stats(image_name, stats_lines,
                        cc_type='lines')
    cc_utils.dump_stats(image_name, vert_lines_stats,
                        cc_type='vert_lines')
    cc_utils.dump_stats(image_name, hor_lines_stats,
                        cc_type='hor_lines')
    cc_utils.dump_stats(image_name, dil_lines_stats,
                        cc_type='dil_lines')
    # Save debug images
    cc_utils.save_bboxes(image, image_name,
                         stats, cc_type='all_CC')
    cc_utils.save_bboxes(image, image_name,
                         vert_lines_stats, cc_type='lines_vert')
    cc_utils.save_bboxes(image, image_name,
                         hor_lines_stats, cc_type='lines_hor')
    cc_utils.save_bboxes(image, image_name,
                         stats_lines, cc_type='lines')
    cc_utils.save_bboxes(image, image_name,
                         all_text_stats, cc_type='all_text')
    cc_utils.save_bboxes(image, image_name,
                         dil_lines_stats, cc_type='dil_lines')
    # Write avg_height to file
    with open("inv_processing/data/data_avg_h_{0}.data".format(image_name), 'wb') as outfile:
        # store the data as binary data stream
        pickle.dump(avg_height, outfile)


def main(image_name, image_path):
    image = cv2.imread(image_path)

    # Threshold image
    thresh = utils.threshold_image(image)
    thresh = 255 - thresh
    binary_folder = f'results/{image_name}/binary'
    utils.save_image(thresh, path=f'{binary_folder}/{image_name}_binary.jpg')

    # Get connected components for whole binary image
    retval, labels, stats_np, _ = cv2.connectedComponentsWithStats(thresh, connectivity=8)

    # Get stats for text elements
    stats = stats_np[1:retval].tolist() # TODO: numpy array
    avg_height = cc_utils.mean_height(stats)
    text_el_stats = cc_utils.detect_text_elements(stats, avg_height)
    cc_utils.save_bboxes(image, image_name, text_el_stats,
                         cc_type='text_1', subfolder='text')

    # Get stats for lines and tables
    stats_copy_1 = copy(stats)
    stats_lines, indexes_to_remove_for_lines = detect_lines(stats_copy_1, avg_height)

    cc_utils.save_bboxes(image, image_name, stats_lines,
                         cc_type='detect_lines', subfolder='lines')

    # Save lines and tables mask
    full_lines_mask = display_labels(labels, retval, indexes_to_remove_for_lines, thresh, image_name)

    # Isolate horizontal and vertical lines using morphological operations
    # SCALE = 35
    scale = 50

    horizontal = full_lines_mask.copy()
    vertical = full_lines_mask.copy()

    horizontal_size = int(horizontal.shape[1] / scale)
    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT,
        (horizontal_size, 1))
    isolate_lines(horizontal, horizontal_structure)

    vertical_size = int(vertical.shape[0] / scale)
    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT,
        (1, vertical_size))
    isolate_lines(vertical, vertical_structure)

    # Get lines from morphological operations
    lines_mask = horizontal + vertical
    kernel = np.ones((3, 3), np.uint8)
    dilation_lines = cv2.dilate(lines_mask, kernel, iterations=1)

    # Get attached text elements from lines and tables:
    rem_elem_mask = full_lines_mask - dilation_lines
    utils.save_image(dilation_lines, "results/{0}/binary/{0}_lines_kernel_dilated.jpg".format(image_name))
    utils.save_image(rem_elem_mask, "results/{0}/binary/{0}_detached_elem.jpg".format(image_name))

    elem_image_path = "results/{0}/binary/{0}_detached_elem.jpg".format(image_name)
    elem_image = cv2.imread(elem_image_path)
    elem_gray_image = utils.grayscale_image(elem_image)
    _, thresh1 = cv2.threshold(elem_gray_image, 127, 255, cv2.THRESH_BINARY)

    # Connected components for remaining text elements:
    retval_rem, _, stats_np_rem, _ = cv2.connectedComponentsWithStats(thresh1, connectivity=8)
    stats_np_rem = stats_np_rem[1: retval_rem]
    stats_rem = stats_np_rem.tolist()
    stats_copy_rem = copy(stats_rem)

    # Detect text from these elements (might be lines from substraction)
    # remaining_text_el_stats = detect_text_for_rem(stats_copy_rem)
    remaining_text_el_stats = cc_utils.detect_text_elements(stats_copy_rem, avg_height)

    cc_utils.save_bboxes(image, image_name, remaining_text_el_stats,
                         cc_type='text_2', subfolder='text')

    # Combine all text elements
    all_text_stats = text_el_stats + remaining_text_el_stats

    # Connected components for dilated lines:
    retval_dil, _, stats_np_dil, _ = cv2.connectedComponentsWithStats(dilation_lines, connectivity=8)
    stats_np_dil = stats_np_dil[1: retval_dil]

    stats_dil = stats_np_dil.tolist()
    stats_copy_dil = copy(stats_dil)
    dil_lines_stats, _ = detect_lines(stats_copy_dil, avg_height)

    # Connected components for vertical lines:
    retval_vert, _, stats_np_vert, centroids_vert = cv2.connectedComponentsWithStats(vertical, connectivity=8)
    stats_np_vert = stats_np_vert[1: retval_vert]
    centroids_vert = centroids_vert[1:retval_vert]
    stats_vert = stats_np_vert.tolist()
    stats_copy_vert = copy(stats_vert)
    vert_lines_stats, _ = detect_lines(stats_copy_vert, avg_height)

    # Connected components for horizontal lines:
    retval_hor, _, stats_np_hor, centroids_hor = cv2.connectedComponentsWithStats(horizontal, connectivity=8)
    stats_np_hor = stats_np_hor[1: retval_hor]
    centroids_hor = centroids_hor[1:retval_hor]
    stats_hor = stats_np_hor.tolist()
    stats_copy_hor = copy(stats_hor)
    hor_lines_stats, _ = detect_lines(stats_copy_hor, avg_height)

    save_data(image, stats, all_text_stats, stats_lines, dil_lines_stats,
              vert_lines_stats, hor_lines_stats, avg_height, image_name)

if __name__ == "__main__":
    _IMAGE_NAME = "image_test"
    _IMAGE_PATH = "{}.jpg".format(_IMAGE_NAME)
    main(_IMAGE_NAME, _IMAGE_PATH)
    print(__name__)

