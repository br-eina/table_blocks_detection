import numpy as np
import cv2
import copy
import pickle
from inv_processing import utils

def write_to_json(stats, filename):
    data = []
    for stat in stats:
        data.append({
            'x': stat[0],
            'y': stat[1],
            'w': stat[2],
            'h': stat[3],
            'A': stat[4]
        })
    with open(filename, 'wb') as outfile:
        pickle.dump(data, outfile)

def gray_image(image):
    num_channels = 3
    if len(image.shape) == num_channels:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def threshold_image(image):
    gray = gray_image(image)
    thresh_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh_image

def display_centroids(image, array):
    image_to_show = image.copy()
    for coord in array:
        cv2.circle(image_to_show, (int(coord[0]), int(coord[1])), 6, (0, 0, 255), -1)
    # show_image(image_to_show)
    utils.show_image(image_to_show)

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

def display_bbox(image, stats):
    image_to_show = image.copy()
    for stat in stats:
        p_1 = (stat[0], stat[1])
        p_2 = (stat[0] + stat[2], stat[1] + stat[3])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255))
    # show_image(image_to_show)
    utils.show_image(image_to_show)

def remove_small_objects(text_stats):
    for stat in text_stats[:]:
        if (stat[2] < 3 and stat[3] < 6 ) or (stat[3] < 3 and stat[2] < 6):
            text_stats.remove(stat)
    return text_stats

def detect_lines(stats, avg_height):
    indexes_to_remove = []
    for ind, stat in enumerate(stats[:]):
        # 100 (50) - previous
        if stat[2] < 30 * stat[3] and stat[3] < 5 * avg_height:
            stats.remove(stat)
            indexes_to_remove.append(ind + 1)
    return stats, indexes_to_remove

def average_height(stats):
    height_sum = 0
    for stat in stats:
        height_sum += stat[3]
    avg_height = height_sum // len(stats)
    return avg_height

def detect_text_elements(stats, avg_height):
    text_el_stats = []
    for stat in stats:
        # 4 (vo 2oy) and 10 (v 3ey)
        if stat[2] < 10 * stat[3] and (2 <= stat[3] <= avg_height * 3) and 8 <= stat[4] <= 1500:
            text_el_stats.append(stat)
    return text_el_stats

def isolate_lines(src, structuring_element):
    cv2.erode(src, structuring_element, src, (-1, -1)) # makes white spots smaller
    cv2.dilate(src, structuring_element, src, (-1, -1)) # makes white spots bigger

def detect_text_for_rem(stats):
    remaining_text = copy.deepcopy(stats)
    for stat in remaining_text[:]:
        if (
            (stat[2] <= 6 and stat[3] >= 4 * stat[2]) or
            (stat[3] <= 6 and stat[2] >= 4 * stat[3]) or
            stat[4] <= 15
        ):
            remaining_text.remove(stat)
    return remaining_text

def make_data_lines(stats_lines, image_name):
    write_to_json(stats_lines, "inv_processing/data/data_lines_{0}.data".format(image_name))

def make_data_text(all_text_stats, image_name):
    write_to_json(all_text_stats, "inv_processing/data/data_text_{0}.data".format(image_name))

def make_data_vert_lines(vert_lines_stats, image_name):
    write_to_json(vert_lines_stats, "inv_processing/data/data_vert_lines_{0}.data".format(image_name))

def make_data_hor_lines(hor_lines_stats, image_name):
    write_to_json(hor_lines_stats, "inv_processing/data/data_hor_lines_{0}.data".format(image_name))

def save_vert_lines(image, lines_elem, image_name):
    image_to_show = image.copy()
    for element in lines_elem:
        p_1 = (element[0], element[1])
        p_2 = (element[0] + element[2], element[1] + element[3])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 3)
    utils.save_image(image_to_show, "results/{0}/{0}_lines_vert.jpg".format(image_name))

def save_all_lines(image, lines_elem, image_name):
    image_to_show = image.copy()
    for element in lines_elem:
        p_1 = (element[0], element[1])
        p_2 = (element[0] + element[2], element[1] + element[3])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 3)
    utils.save_image(image_to_show, "results/{0}/{0}_lines.jpg".format(image_name))

def save_hor_lines(image, lines_elem, image_name):
    image_to_show = image.copy()
    for element in lines_elem:
        p_1 = (element[0], element[1])
        p_2 = (element[0] + element[2], element[1] + element[3])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 3)
    utils.save_image(image_to_show, "results/{0}/{0}_lines_hor.jpg".format(image_name))


def save_data(image, thresh, all_text_stats, stats_lines,
              vert_lines_stats, hor_lines_stats, avg_height, image_name):
    utils.save_image(thresh, "results/{0}/binary/{0}_binary.jpg".format(image_name))
    make_data_text(all_text_stats, image_name)
    make_data_lines(stats_lines, image_name)
    make_data_vert_lines(vert_lines_stats, image_name)
    make_data_hor_lines(hor_lines_stats, image_name)
    save_vert_lines(image, vert_lines_stats, image_name)
    save_hor_lines(image, hor_lines_stats, image_name)
    save_all_lines(image, stats_lines, image_name)
    # Write avg_height to file
    with open("inv_processing/data/data_avg_h_{0}.data".format(image_name), 'wb') as outfile:
        # store the data as binary data stream
        pickle.dump(avg_height, outfile)


def main(image_name, image_path):
    image = cv2.imread(image_path)

    # Threshold image
    thresh = threshold_image(image)
    thresh = 255 - thresh

    # Dilate (to get dilated lines and large connected components):
    kernel = np.ones((3, 3), np.uint8)
    dilation_image = cv2.dilate(thresh, kernel, iterations=2)

    # Get connected components for whole binary image
    retval, labels, stats_np, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    stats_np = stats_np[1: retval]
    centroids = centroids[1:retval]

    # Get stats for text elements
    stats = stats_np.tolist()
    stats_copy = copy.deepcopy(stats)
    avg_height = average_height(stats)
    text_el_stats = detect_text_elements(stats_copy, avg_height)

    # For lines and tables:
    _, _, stats_np_lines, centroids_lines = cv2.connectedComponentsWithStats(dilation_image, connectivity=8)
    stats_np_lines = stats_np_lines[1: retval]
    centroids_lines = centroids_lines[1:retval]

    # Get stats for lines and tables
    stats_copy_1 = copy.deepcopy(stats_copy)
    stats_lines, indexes_to_remove_for_lines = detect_lines(stats_copy_1, avg_height)

    # Save lines and tables mask
    full_lines_mask = display_labels(labels, retval, indexes_to_remove_for_lines, thresh, image_name)

    # Isolate horizontal and vertical lines using morphological operations
    # SCALE = 35
    scale = 100

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
    dilation_lines = cv2.dilate(lines_mask, kernel, iterations=1)

    # Get attached text elements from lines and tables:
    rem_elem_mask = full_lines_mask - dilation_lines
    utils.save_image(dilation_lines, "results/{0}/binary/{0}_lines_kernel_dilated.jpg".format(image_name))
    utils.save_image(rem_elem_mask, "results/{0}/binary/{0}_detached_elem.jpg".format(image_name))

    elem_image_path = "results/{0}/binary/{0}_detached_elem.jpg".format(image_name)
    elem_image = cv2.imread(elem_image_path)
    elem_gray_image = gray_image(elem_image)
    _, thresh1 = cv2.threshold(elem_gray_image, 127, 255, cv2.THRESH_BINARY)

    # Connected components for remaining text elements:
    retval_rem, _, stats_np_rem, centroids_rem = cv2.connectedComponentsWithStats(thresh1, connectivity=8)
    stats_np_rem = stats_np_rem[1: retval_rem]
    centroids_rem = centroids_rem[1:retval_rem]
    stats_rem = stats_np_rem.tolist()
    stats_copy_rem = copy.deepcopy(stats_rem)

    # Detect text from these elements (might be lines from substraction)
    remaining_text_el_stats = detect_text_for_rem(stats_copy_rem)

    # Combine all text elements
    all_text_stats = text_el_stats + remaining_text_el_stats

    # Connected components for vertical lines:
    retval_vert, _, stats_np_vert, centroids_vert = cv2.connectedComponentsWithStats(vertical, connectivity=8)
    stats_np_vert = stats_np_vert[1: retval_vert]
    centroids_vert = centroids_vert[1:retval_vert]
    stats_vert = stats_np_vert.tolist()
    stats_copy_vert = copy.deepcopy(stats_vert)
    vert_lines_stats, _ = detect_lines(stats_copy_vert, avg_height)

    # Connected components for horizontal lines:
    retval_hor, _, stats_np_hor, centroids_hor = cv2.connectedComponentsWithStats(horizontal, connectivity=8)
    stats_np_hor = stats_np_hor[1: retval_hor]
    centroids_hor = centroids_hor[1:retval_hor]
    stats_hor = stats_np_hor.tolist()
    stats_copy_hor = copy.deepcopy(stats_hor)
    hor_lines_stats, _ = detect_lines(stats_copy_hor, avg_height)

    save_data(image, thresh, all_text_stats, stats_lines,
              vert_lines_stats, hor_lines_stats, avg_height, image_name)

if __name__ == "__main__":
    _image_name = "image_test"
    _image_path = "{}.jpg".format(_image_name)
    main(_image_name, _image_path)
    print(__name__)
