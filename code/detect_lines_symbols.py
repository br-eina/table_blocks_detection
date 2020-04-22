import numpy as np
import cv2
import json
import copy
import pickle
import os
import argparse

def show_image(image):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", image)
    cv2.waitKey(0)

def save_image(image, filename):
    cv2.imwrite(filename, image)

def write_to_json(stats, filename):
    data = []
    for ind, stat in enumerate(stats):
        data.append({
            'x': stat[0],
            'y': stat[1],
            'w': stat[2],
            'h': stat[3],
            'A': stat[4]
        })
    with open(filename, 'wb') as outfile:
    # store the data as binary data stream
        pickle.dump(data, outfile)

def gray_image(image):
    NUM_CHANNELS = 3
    if len(image.shape) == NUM_CHANNELS:
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
    show_image(image_to_show)

def display_labels(labels, retval, indexes_to_remove):
    label_mas = []
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
    save_image(full_mask, "results/{0}/binary/{0}_lines_full.jpg".format(image_name))
    return full_mask

def display_bbox(image, stats):
    image_to_show = image.copy()
    for stat in stats:
        p_1 = (stat[0], stat[1])
        p_2 = (stat[0] + stat[2], stat[1] + stat[3])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255))
    show_image(image_to_show)

def remove_small_objects(text_stats):
    indexes_to_remove = []
    for ind, stat in enumerate(text_stats[:]):
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

def detect_text_for_rem(stats, avg_height):
    remaining_text = copy.deepcopy(stats)
    for stat in remaining_text[:]:
        if (
            (stat[2] <= 6 and stat[3] >= 4 * stat[2]) or
            (stat[3] <= 6 and stat[2] >= 4 * stat[3]) or
            stat[4] <= 15
        ):
            remaining_text.remove(stat)
    return remaining_text

def display_lines():
    display_labels(labels, retval, indexes_to_remove_for_lines)

def make_data_lines():
    write_to_json(stats_lines, "data/data_lines_{0}.data".format(image_name))

def make_data_text():
    write_to_json(all_text_stats, "data/data_text_{0}.data".format(image_name))

def make_data_vert_lines():
    write_to_json(vert_lines_stats, "data/data_vert_lines_{0}.data".format(image_name))

def make_data_hor_lines():
    write_to_json(hor_lines_stats, "data/data_hor_lines_{0}.data".format(image_name))

def save_vert_lines(image, lines_elem):
    image_to_show = image.copy()
    for element in lines_elem:
        p_1 = (element[0], element[1])
        p_2 = (element[0] + element[2], element[1] + element[3])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 3)
    save_image(image_to_show, "results/{0}/{0}_lines_vert.jpg".format(image_name))

def save_all_lines(image, lines_elem):
    image_to_show = image.copy()
    for element in lines_elem:
        p_1 = (element[0], element[1])
        p_2 = (element[0] + element[2], element[1] + element[3])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 3)
    save_image(image_to_show, "results/{0}/{0}_lines.jpg".format(image_name))

def save_hor_lines(image, lines_elem):
    image_to_show = image.copy()
    for element in lines_elem:
        p_1 = (element[0], element[1])
        p_2 = (element[0] + element[2], element[1] + element[3])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 3)
    save_image(image_to_show, "results/{0}/{0}_lines_hor.jpg".format(image_name))

def save_data():
    save_image(thresh, "results/{0}/binary/{0}_binary.jpg".format(image_name))
    make_data_text()
    make_data_lines()
    make_data_vert_lines()
    make_data_hor_lines()
    save_vert_lines(image, vert_lines_stats)
    save_hor_lines(image, hor_lines_stats)
    save_all_lines(image, stats_lines)
    # Write avg_height to file
    with open("data/data_avg_h_{0}.data".format(image_name), 'wb') as outfile:
        # store the data as binary data stream
        pickle.dump(avg_height, outfile)

# Get image_name from cmd
parser = argparse.ArgumentParser()
parser.add_argument("--img", help="help_image_name")
args = parser.parse_args()
image_name = str(args.img)

# Create folder for image with add files
if not os.path.exists('results/{0}'.format(image_name)):
    os.makedirs('results/{0}'.format(image_name))

if not os.path.exists('results/{0}/binary'.format(image_name)):
    os.makedirs('results/{0}/binary'.format(image_name))

# Initialize image
# image_path = "docs/{0}.jpg".format(image_name)
# image_path = "categories/___/{0}.jpg".format(image_name)
image_path = r'e:/__PR/docs/pdf2jpg/1C img/{0}.jpg'.format(image_name)
image = cv2.imread(image_path)

# Threshold image
thresh = threshold_image(image)
thresh = 255 - thresh

# Dilate (to get dilated lines and large connected components):
kernel = np.ones((3,3), np.uint8)
dilation_image = cv2.dilate(thresh, kernel, iterations=2)

# Get connected components for whole binary image
retval, labels, stats_np, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
stats_np = stats_np[1: retval]
nb_components = retval - 1
centroids = centroids[1:retval]

# Get stats for text elements
stats = stats_np.tolist()
stats_copy = copy.deepcopy(stats)
avg_height = average_height(stats)
text_el_stats = detect_text_elements(stats_copy, avg_height)
print("All el: ", len(stats))
print("Avg height: ", avg_height)


# For lines and tables:
retval_lines, labels_lines, stats_np_lines, centroids_lines = cv2.connectedComponentsWithStats(dilation_image, connectivity=8)
stats_np_lines = stats_np_lines[1: retval]
nb_components_lines = retval_lines - 1
centroids_lines = centroids_lines[1:retval]

stats_lines_1 = stats_np_lines.tolist()
stats_copy_lines = copy.deepcopy(stats_lines_1)

# Get stats for lines and tables
stats_copy_1 = copy.deepcopy(stats_copy)
stats_lines, indexes_to_remove_for_lines = detect_lines(stats_copy_1, avg_height)

# Save lines and tables mask
full_lines_mask = display_labels(labels, retval, indexes_to_remove_for_lines)

# Isolate horizontal and vertical lines using morphological operations
# SCALE = 35
SCALE = 100

horizontal = full_lines_mask.copy()
vertical = full_lines_mask.copy()

horizontal_size = int(horizontal.shape[1] / SCALE)
horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT,
    (horizontal_size, 1))
isolate_lines(horizontal, horizontal_structure)

vertical_size = int(vertical.shape[0] / SCALE)
vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT,
    (1, vertical_size))
isolate_lines(vertical, vertical_structure)

# Get lines from morphological operations
lines_mask = horizontal + vertical
dilation_lines = cv2.dilate(lines_mask, kernel, iterations=1)

# Get attached text elements from lines and tables:
rem_elem_mask = full_lines_mask - dilation_lines
save_image(dilation_lines, "results/{0}/binary/{0}_lines_kernel_dilated.jpg".format(image_name))
save_image(rem_elem_mask, "results/{0}/binary/{0}_detached_elem.jpg".format(image_name))

elem_image_path = "results/{0}/binary/{0}_detached_elem.jpg".format(image_name)
elem_image = cv2.imread(elem_image_path)
elem_gray_image = gray_image(elem_image)
ret,thresh1 = cv2.threshold(elem_gray_image,127,255,cv2.THRESH_BINARY)

# Connected components for remaining text elements:
retval_rem, labels_rem, stats_np_rem, centroids_rem = cv2.connectedComponentsWithStats(thresh1, connectivity=8)
stats_np_rem = stats_np_rem[1: retval_rem]
nb_components_rem = retval_rem - 1
centroids_rem = centroids_rem[1:retval_rem]
stats_rem = stats_np_rem.tolist()
stats_copy_rem = copy.deepcopy(stats_rem)

# Detect text from these elements (might be lines from substraction)
remaining_text_el_stats = detect_text_for_rem(stats_copy_rem, avg_height)

# Combine all text elements
all_text_stats = text_el_stats + remaining_text_el_stats

# Connected components for vertical lines:
retval_vert, labels_vert, stats_np_vert, centroids_vert = cv2.connectedComponentsWithStats(vertical, connectivity=8)
stats_np_vert = stats_np_vert[1: retval_vert]
nb_components_vert = retval_vert - 1
centroids_vert = centroids_vert[1:retval_vert]
stats_vert = stats_np_vert.tolist()
stats_copy_vert = copy.deepcopy(stats_vert)
vert_lines_stats, indexes_to_remove_for_vert_lines = detect_lines(stats_copy_vert, avg_height)

# Connected components for horizontal lines:
retval_hor, labels_hor, stats_np_hor, centroids_hor = cv2.connectedComponentsWithStats(horizontal, connectivity=8)
stats_np_hor = stats_np_hor[1: retval_hor]
nb_components_hor = retval_hor - 1
centroids_hor = centroids_hor[1:retval_hor]
stats_hor = stats_np_hor.tolist()
stats_copy_hor = copy.deepcopy(stats_hor)
hor_lines_stats, indexes_to_remove_for_hor_lines = detect_lines(stats_copy_hor, avg_height)

save_data()