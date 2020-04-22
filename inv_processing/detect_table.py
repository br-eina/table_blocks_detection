import cv2
import copy
import pickle

def show_image(image):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", image)
    cv2.waitKey(0)

def save_image(image, filename):
    cv2.imwrite(filename, image)

def sort_rows(rows):
    sorted_rows = []
    for row in rows:
        row = sorted(row, key = lambda el: (el['x'], el['y']))
        sorted_rows.append(row)
    return sorted_rows

def show_lines(image, lines_elem, image_name):
    image_to_show = image.copy()
    for element in lines_elem:
        p_1 = (element['x'], element['y'])
        p_2 = (element['x'] + element['w'], element['y'] + element['h'])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 3)
    save_image(image_to_show, "images/lines/{}_lines.jpg".format(image_name))

def show_bbox(image, element):
    image_to_show = image.copy()
    p_1 = (element['x'], element['y'])
    p_2 = (element['x'] + element['w'], element['y'] + element['h'])
    cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 5)
    show_image(image_to_show)

def show_text_blocks_in_row(image, rows):
    image_to_show = image.copy()
    for row in rows:
        for element in row:
            p_1 = (element['x'], element['y'])
            p_2 = (element['x'] + element['w'], element['y'] + element['h'])
            cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 4)
        show_image(image_to_show)

def vertical_condition(block_1, block_2):
    t = 3
    x_l1 = block_1['x']
    x_r1 = x_l1 + block_1['w']
    x_c1 = (x_l1 + x_r1) // 2

    x_l2 = block_2['x']
    x_r2 = x_l2 + block_2['w']
    x_c2 = (x_l2 + x_r2) // 2

    if abs(x_l1 - x_l2) <= t or abs(x_c1 - x_c2) <= t or abs(x_r1 - x_r2) <= t:
    # if abs(x_c1 - x_c2) <= t:
        return 1
    else:
        return 0

def check_rows_for_two_el(rows):
    key = 0
    for ind_row, row in enumerate(rows):
        if ind_row != len(rows) - 1:
            if len(row) != 0 and len(rows[ind_row + 1]) != 0:
                key += 1
                ind_row_1 = ind_row
                break
    if key > 0:
        return 1, ind_row_1
    else:
        return 0, 0

def check_number_blocks_in_table(tables, text_blocks_rows):
    # Add parameter to text block
    # If in table: True
    num_blocks_in_table = 0

    for ind_row, row in enumerate(text_blocks_rows):
        for ind_block, block in enumerate(row):
            for table in tables:
                if (
                    (block['x'] >= table['x']) and (block['x'] + block['w'] <= table['x'] + table['w']) and
                    (block['y'] >= table['y']) and (block['y'] + block['h'] <= table['y'] + table['h'])
                ):
                    text_blocks_rows[ind_row][ind_block]['in_table'] = True
                    num_blocks_in_table += 1
    if num_blocks_in_table >= 4:
        return 1
    else:
        return 0

def check_if_line_in_table(line, table):
    t = 10
    if (
        (table['x'] <= line['x'] + t) and (table['x'] + table['w'] >= line['x'] + line['w'] - t) and
        (table['y'] <= line['y'] + t) and (table['y'] + table['h'] >= line['y'] + line['h'] - t)
    ):
        return 1
    else:
        return 0

def check_if_symbol_in_table(symbol, table):
    t = 4
    if (
        (table['x'] <= symbol['x'] + t) and (table['x'] + table['w'] >= symbol['x'] + symbol['w'] - t) and
        (table['y'] <= symbol['y'] + t) and (table['y'] + table['h'] >= symbol['y'] + symbol['h'] - t)
    ):
        return 1
    else:
        return 0


def check_number_lines_in_table(table, hor_lines, vert_lines):
    # Count number of horiz lines within the table:
    num_hor = 0
    for line in hor_lines:
        if check_if_line_in_table(line, table) == 1:
            num_hor += 1

    num_vert = 0
    for line in vert_lines:
        if check_if_line_in_table(line, table) == 1:
            num_vert += 1

    if (
        (num_hor == 2 and num_vert > 2) or
        (num_vert == 2 and num_hor > 2) or
        (num_hor > 2 and num_vert > 2) or
        (num_hor >= 3) or
        (num_vert >= 3)
    ):
        return 1
    else:
        return 0

def find_tables_without_lines(line_elements_copy, hor_lines, vert_lines,
                              table_elements_with_lines):
    for table in line_elements_copy:
        if check_number_lines_in_table(table, hor_lines, vert_lines) == 1:
            table_elements_with_lines.append(table)

def save_tables_lines(image, lines_elem, image_name):
    image_to_show = image.copy()
    for element in lines_elem:
        p_1 = (element['x'], element['y'])
        p_2 = (element['x'] + element['w'], element['y'] + element['h'])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 3)
    save_image(image_to_show, "results/{}_tables.jpg".format(image_name))

def save_image_symbols_not_in_table(image, symbols_not_in_table, image_name):
    image_to_show = image.copy()
    for element in symbols_not_in_table:
        p_1 = (element['x'], element['y'])
        p_2 = (element['x'] + element['w'], element['y'] + element['h'])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 2)
    save_image(image_to_show, "results/{0}/{0}_symbols_not_in_table.jpg".format(image_name))

def save_image_blocks_not_in_table(image, blocks_not_in_table, image_name):
    image_to_show = image.copy()
    for element in blocks_not_in_table:
        p_1 = (element['x'], element['y'])
        p_2 = (element['x'] + element['w'], element['y'] + element['h'])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 2)
    save_image(image_to_show, "results/{0}/{0}_blocks_not_in_table.jpg".format(image_name))

def save_text_blocks(text_blocks_rows, image_name):
    with open("inv_processing/data/data_text_blocks_tables_{0}.data".format(image_name), 'wb') as outfile:
        pickle.dump(text_blocks_rows, outfile)


# Сохранение символов, не лежащих в таблице:
def save_symbols_not_in_table(text_elements, tables, image, image_name):
    symbols_not_in_table = []
    for table in tables:
        for ind, symbol in enumerate(text_elements):
            if check_if_symbol_in_table(symbol, table) == 1:
                text_elements[ind]['in_table'] = True
    for symbol in text_elements:
        if symbol['in_table'] == False:
            symbols_not_in_table.append(symbol)
    save_image_symbols_not_in_table(image, symbols_not_in_table, image_name)
    with open("data_not_in_table/symbols_not_in_table_{0}.data".format(image_name), 'wb') as outfile:
        pickle.dump(symbols_not_in_table, outfile)

# Сохранение блоков, не лежащих в таблице:
def save_blocks_not_in_table(text_blocks, image, image_name):
    blocks_not_in_table = []
    for row in text_blocks:
        for block in row:
            if block['in_table'] == False:
                blocks_not_in_table.append(block)
    save_image_blocks_not_in_table(image, blocks_not_in_table, image_name)
    with open("data_not_in_table/blocks_not_in_table_{0}.data".format(image_name), 'wb') as f:
        pickle.dump(blocks_not_in_table, f)

def main(image_name, image_path):

    image = cv2.imread(image_path)

    # Load text_blocks elem
    with open('inv_processing/data/data_text_blocks_{0}.data'.format(image_name), 'rb') as filehandle:
        # read the data as binary data stream
        text_blocks_rows = pickle.load(filehandle)

    # Load lines elem
    with open('inv_processing/data/data_lines_{0}.data'.format(image_name), 'rb') as filehandle:
        # read the data as binary data stream
        line_elements = pickle.load(filehandle)

    # Load vertical lines elem
    with open('inv_processing/data/data_vert_lines_{0}.data'.format(image_name), 'rb') as filehandle:
        # read the data as binary data stream
        vert_lines = pickle.load(filehandle)

    # Load horizontal lines elem
    with open('inv_processing/data/data_hor_lines_{0}.data'.format(image_name), 'rb') as filehandle:
        # read the data as binary data stream
        hor_lines = pickle.load(filehandle)

    # Load text elem
    with open('inv_processing/data/data_text_{0}.data'.format(image_name), 'rb') as filehandle:
        # read the data as binary data stream
        text_elements = pickle.load(filehandle)

    line_elements_copy = copy.deepcopy(line_elements)

    table_elements = []
    # Diff tables apart from lines:
    for line in line_elements[:]:
        if line['w'] < 50 * line['h']:
            table_elements.append(line)
            line_elements.remove(line)

    # Clear horizontal and vertical lines from wide ones:
    for line in vert_lines[:]:
        if line['w'] >= line['h'] // 25:
            vert_lines.remove(line)
    for line in hor_lines[:]:
        if line['h'] >= line['w'] // 25:
            hor_lines.remove(line)

    # Разрешение изображения:
    height, width = image.shape[:2]

    # Add parameter to text block
    # in_table: False
    for ind_row, row in enumerate(text_blocks_rows):
        for ind_block in range(len(row)):
            text_blocks_rows[ind_row][ind_block]['in_table'] = False
            text_blocks_rows[ind_row][ind_block]['img_h'] = height
            text_blocks_rows[ind_row][ind_block]['img_w'] = width

    # Add parameter to symbol
    # in_table: False
    for ind in range(len(text_elements)):
        text_elements[ind]['in_table'] = False
        text_elements[ind]['img_h'] = height
        text_elements[ind]['img_w'] = width

    table_elements_with_lines = []

    if len(table_elements) != 0:
        find_tables_without_lines(line_elements_copy, hor_lines, vert_lines,
                                  table_elements_with_lines)
        check_number_blocks_in_table(table_elements_with_lines, text_blocks_rows)
        save_tables_lines(image, table_elements_with_lines, image_name)
        save_symbols_not_in_table(text_elements, table_elements_with_lines, image, image_name)
        save_text_blocks(text_blocks_rows, image_name)
        save_blocks_not_in_table(text_blocks_rows, image, image_name)
        # with open("number_tables.txt", "a") as myfile:
        #     string = str(len(table_elements_with_lines)) + "\n"
        #     myfile.write(string)

if __name__ == "__main__":
    _image_name = "image_test"
    _image_path = "{}.jpg".format(_image_name)
    main(_image_name, _image_path)
