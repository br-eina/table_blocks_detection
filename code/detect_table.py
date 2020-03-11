import numpy as np
import cv2 
import json
import copy
import random
from collections import Counter
import pickle
import csv
import os
import argparse

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

def show_lines(image, lines_elem):
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

parser = argparse.ArgumentParser()
parser.add_argument("--img", help="help_image_name")
args = parser.parse_args()

image_name = str(args.img)

# image_name = 'schet_opl-23'

# image_path = "docs/{0}.jpg".format(image_name)
image_path = "categories/___/{0}.jpg".format(image_name)

image = cv2.imread(image_path)

# Load text_blocks elem
with open('data/data_text_blocks_{0}.data'.format(image_name), 'rb') as filehandle:
    # read the data as binary data stream
    text_blocks_rows = pickle.load(filehandle)

# Load lines elem
with open('data/data_lines_{0}.data'.format(image_name), 'rb') as filehandle:
    # read the data as binary data stream
    line_elements = pickle.load(filehandle)

# Load average height
with open('data/data_avg_h_{0}.data'.format(image_name), 'rb') as filehandle:
    # read the data as binary data stream
    avg_height = pickle.load(filehandle)

# Load vertical lines elem
with open('data/data_vert_lines_{0}.data'.format(image_name), 'rb') as filehandle:
    # read the data as binary data stream
    vert_lines = pickle.load(filehandle)

# Load horizontal lines elem
with open('data/data_hor_lines_{0}.data'.format(image_name), 'rb') as filehandle:
    # read the data as binary data stream
    hor_lines = pickle.load(filehandle)

# Load text elem
with open('data/data_text_{0}.data'.format(image_name), 'rb') as filehandle:
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


# Add parameter to text block
# in_table: False
for ind_row, row in enumerate(text_blocks_rows):
    for ind_block, block in enumerate(row):
        text_blocks_rows[ind_row][ind_block]['in_table'] = False

# Add parameter to symbol
# in_table: False
for ind in range(len(text_elements)):
    text_elements[ind]['in_table'] = False



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
                # else:
                #     if not text_blocks_rows[ind_row][ind_block]['in_table']:
                #         text_blocks_rows[ind_row][ind_block]['in_table'] = False
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
        # (num_vert == 1 and num_hor >= 3) or
        # (num_hor == 1 and num_vert >= 3)
    ):
        return 1
    else:
        return 0
    # if (
    #     num_hor >= 1 and num_vert >= 1
    # ):
    #     return 1
    # else:
    #     return 0

table_elements_with_lines = []

def find_tables_without_lines():
    for table in line_elements_copy:
    # for table in table_elements:
        if check_number_lines_in_table(table, hor_lines, vert_lines) == 1:
            table_elements_with_lines.append(table)
            # if check_number_blocks_in_table(table, text_blocks_rows) == 0:
            #     table_elements_with_lines.remove(table)

def save_tables_lines(image, lines_elem):
    image_to_show = image.copy()
    for element in lines_elem:
        p_1 = (element['x'], element['y'])
        p_2 = (element['x'] + element['w'], element['y'] + element['h'])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 3)
    # save_image(image_to_show, "results/{}_tables.jpg".format(image_name))
    save_image(image_to_show, "categories/___/debug/{}_tables.jpg".format(image_name))

def save_image_symbols_not_in_table(image, symbols_not_in_table):
    image_to_show = image.copy()
    for element in symbols_not_in_table:
        p_1 = (element['x'], element['y'])
        p_2 = (element['x'] + element['w'], element['y'] + element['h'])
        cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 2)
    save_image(image_to_show, "categories/___/debug/{}_symbols_not_in_table.jpg".format(image_name))

def save_text_blocks():
    with open("data/data_text_blocks_tables_{0}.data".format(image_name), 'wb') as outfile:
        pickle.dump(text_blocks_rows, outfile)

# Сохранение символов, не лежащих в таблице:
def save_symbols_not_in_table(text_elements, tables):
    symbols_not_in_table = []
    for table in tables:
        for ind, symbol in enumerate(text_elements):
            if check_if_symbol_in_table(symbol, table) == 1:
                text_elements[ind]['in_table'] = True
    for symbol in text_elements:
        if symbol['in_table'] == False:
            symbols_not_in_table.append(symbol)
    save_image_symbols_not_in_table(image, symbols_not_in_table)
    with open("categories/___/data/symbols_not_in_table_{0}.data".format(image_name), 'wb') as outfile:
        pickle.dump(symbols_not_in_table, outfile)


if len(table_elements) != 0:
    find_tables_without_lines()
    check_number_blocks_in_table(table_elements_with_lines, text_blocks_rows)
    save_tables_lines(image, table_elements_with_lines)
    print(table_elements_with_lines)
    save_symbols_not_in_table(text_elements, table_elements_with_lines)
    save_text_blocks()
    with open("number_tables.txt", "a") as myfile:
        string = str(len(table_elements_with_lines)) + "\n"
        myfile.write(string)

    # save_symbols_not_in_table(text_elements, table_elements_with_lines)






# # Определяем позиции рядов текстовых блоков:
# row_positions = []
# for ind_row, row in enumerate(text_blocks_rows):
#     mass_y_top = []
#     mass_y_bot = []
#     for elem in row:
#         mass_y_top.append(elem['y'])
#         mass_y_bot.append(elem['y'] + elem['h'])
#     y_top = min(mass_y_top)
#     y_bot = max(mass_y_bot)

#     row_positions.append({
#         'ind': ind_row,
#         'y_top': y_top,
#         'y_bot': y_bot
#     })

# # Определяем, есть ли ряд блоков между линией и таблицей:
# if len(table_elements) != 0:
#     for table in table_elements:
#         for line in line_elements[:]:
#             # Если линия выше таблицы:
#             if line['y'] < table['y']:
#                 # Определяем координаты площади м-ду ними:
#                 area_between = {}
#                 area_between['y_top'] = line['y'] + line['h']
#                 area_between['y_bot'] = table['y']
#                 # Определяем к-во рядов, входящих в площадь:
#                 num_rows = 0
#                 for row_pos in row_positions:
#                     if (
#                         row_pos['y_top'] >= area_between['y_top'] and
#                         row_pos['y_bot'] <= area_between['y_bot']
#                     ):
#                         num_rows += 1
#                 # Если таких рядов нет, то удаляем линию:
#                 if num_rows == 0:
#                     line_elements.remove(line)



# # print(table_elements)
# # show_lines(image, table_elements)

# def remove_empty_rows(rows):
#     for row in rows[:]:
#         if len(row) == 0:
#             rows.remove(row)
#     return rows



# def get_blocks_inside_table(text_blocks_rows, table_element):
#     # first_table = table_elements[0]
#     text_blocks_roi = []
#     for ind_row, blocks_row in enumerate(text_blocks_rows):
#         text_blocks_roi.append([])
#         for text_block in blocks_row:
#             if (
#                 text_block['x'] >= table_element['x'] and
#                 text_block['y'] >= table_element['y'] and
#                 (text_block['x'] + text_block['w']) <= (table_element['x'] + table_element['w']) and
#                 (text_block['y'] + text_block['h']) <= (table_element['y'] + table_element['h'])
#             ):
#                 text_blocks_roi[ind_row].append(text_block)
#     text_blocks_roi = remove_empty_rows(text_blocks_roi)

#     # Создаем единичный список из вложенных:
#     flat_text_blocks = [item for sublist in text_blocks_roi for item in sublist]
#     return flat_text_blocks
            

# # Construct columns
# def construct_columns(flat_text_blocks, columns):
#     for base_text_block in flat_text_blocks[:]:
#         consid_text_blocks = copy.deepcopy(flat_text_blocks)
#         if base_text_block in consid_text_blocks:
#             consid_text_blocks.remove(base_text_block)
#         search_for_vert_in_consid_for_base_block(base_text_block, flat_text_blocks, consid_text_blocks)
#     return columns

# def search_for_vert_in_consid_for_base_block(base_text_block, flat_text_blocks, consid_text_blocks):
#     column = []
#     numb_vert_blocks = 0
#     for text_block in consid_text_blocks[:]:
#         if vertical_condition(base_text_block, text_block):
#             numb_vert_blocks += 1
#             # Добавляем элементы в столбец
#             if base_text_block not in column:
#                 column.append(base_text_block)
#             column.append(text_block)
#             # Удаляем элементы из рассм и исходного списка:
#             if base_text_block in flat_text_blocks:
#                 flat_text_blocks.remove(base_text_block)
#             flat_text_blocks.remove(text_block)
#             consid_text_blocks.remove(text_block)
    
#     # Если ни одного элемента не было добавлено - удаляем базов текст блок
#     if numb_vert_blocks == 0:
#         if base_text_block in flat_text_blocks:
#             flat_text_blocks.remove(base_text_block)
#     # Если сформировался столбец, то рассм оставшиеся элементы по всем эл-там столбца
#     else:
#         search_for_vert_in_consid_for_column(flat_text_blocks, consid_text_blocks, column)
    
# def search_for_vert_in_consid_for_column(flat_text_blocks, consid_text_blocks, column):
#     numb_vert_blocks = 0
#     for col_block in column:
#         for text_block in consid_text_blocks[:]:
#             if vertical_condition(col_block, text_block):
#                 numb_vert_blocks += 1
#                 # Добавляем элемент в столбец
#                 column.append(text_block)
                
#                 # Удаляем элемент из рассм и исх списка:
#                 if text_block in flat_text_blocks:
#                     flat_text_blocks.remove(text_block)
#                 consid_text_blocks.remove(text_block)
#     # Если эл-ты были добавлены, то опять проходим по столбцу
#     if numb_vert_blocks != 0:
#         search_for_vert_in_consid_for_column(flat_text_blocks, consid_text_blocks, column)
#     # Если нет - тогда формируем столбец
#     else:
#         columns.append(column)
#         column = []


# def show_columns(image, columns, table):
#     # image_to_show = image.copy()
    

#     t_p_1 = (table['x'], table['y'])
#     t_p_2 = (table['x'] + table['w'], table['y'] + table['h'])
#     cv2.rectangle(image, t_p_1, t_p_2, (0, 0, 255), 3)

#     for column in columns:
#         r = random.randint(0, 255)
#         b = random.randint(0, 255)
#         g = random.randint(0, 255)
#         for element in column:
#             p_1 = (element['x'], element['y'])
#             p_2 = (element['x'] + element['w'], element['y'] + element['h'])
#             cv2.rectangle(image, p_1, p_2, (r, b, g), 4)
#     save_image(image, "images/columns/columns_{}.jpg".format(image_name))

# columns_tables = []
# tables = []
# # Рассматриваем все большие связные эл-ты и смотрим, не таблица ли
# for table_element in table_elements:
#     flat_text_blocks = get_blocks_inside_table(text_blocks_rows, table_element)
#     numb_all_blocks = len(flat_text_blocks)
#     columns = []
#     columns = construct_columns(flat_text_blocks, columns)
    
#     # Define number of column elements:
#     numb_col_blocks = 0
#     for column in columns:
#         for element in column:
#             numb_col_blocks += 1
    
#     # Условие, при котором считаем область таблицей:
#     if numb_all_blocks != 0:
#         if numb_col_blocks / numb_all_blocks >= 0.7:
#             columns_tables.append(columns)
#             tables.append(table_element)


# print(len(columns_tables))        



# def save_blocks_table(image_without_tables, table, table_ind, flat_text_blocks, columns):
#     # image_to_show = image.copy()
#     # Save image without table
#     image_without_tables_path = "images/images_without_tables/{0}_mod.jpg".format(image_name)
#     original_image_path = "images/images_without_tables/{0}.jpg".format(image_name)
#     y_table = table['y'] - 3
#     h_table = table['h'] + 6
#     x_table = table['x'] - 3
#     w_table = table['w'] + 6
#     # image_without_tables = image.copy()
#     image_without_tables[y_table: y_table + h_table, x_table: x_table + w_table] = (255, 255, 255)
#     save_image(image_without_tables, image_without_tables_path)
#     save_image(image, original_image_path)


#     if not os.path.exists('images/images_without_tables/cropped_{0}'.format(image_name)):
#         os.makedirs('images/images_without_tables/cropped_{0}'.format(image_name))
    
#     if not os.path.exists('images/images_without_tables/cropped_{0}/table_{1}'.format(image_name, table_ind)):
#         os.makedirs('images/images_without_tables/cropped_{0}/table_{1}'.format(image_name, table_ind))
    
#     table_image_path = "images/images_without_tables/cropped_{0}/table_{1}.jpg".format(image_name, table_ind)
#     table_image = image[y_table: y_table + h_table, x_table: x_table + w_table].copy()
#     save_image(table_image, table_image_path)

#     for ind, text_block in enumerate(flat_text_blocks):
#         y = text_block['y'] - 3
#         h = text_block['h'] + 6
#         x = text_block['x'] - 3
#         w = text_block['w'] + 6
#         cropped_image = image[y:y+h, x:x+w].copy()
#         filename = "images/images_without_tables/cropped_{0}/table_{1}/{2}-{3}.jpg".format(image_name, table_ind, image_name, ind)
#             # file_for_tesser.write("{0}-{1}-{2}.jpg\n".format(image_name, ind_row, ind_block))
#         save_image(cropped_image, filename)
    
#     for ind_col, column in enumerate(columns):
#         if not os.path.exists('images/images_without_tables/cropped_{0}/table_{1}/column_{2}'.format(image_name, table_ind, ind_col)):
#             os.makedirs('images/images_without_tables/cropped_{0}/table_{1}/column_{2}'.format(image_name, table_ind, ind_col))
#         r = random.randint(0, 255)
#         b = random.randint(0, 255)
#         g = random.randint(0, 255)
#         for ind_block, element in enumerate(column):
#             y = element['y'] - 3
#             h = element['h'] + 6
#             x = element['x'] - 3
#             w = element['w'] + 6
#             cropped_image = image[y:y+h, x:x+w].copy()
#             filename = "images/images_without_tables/cropped_{0}/table_{1}/column_{2}/{3}.jpg".format(image_name, table_ind, ind_col, ind_block)
#                 # file_for_tesser.write("{0}-{1}-{2}.jpg\n".format(image_name, ind_row, ind_block))
#             save_image(cropped_image, filename)

  

# # Save pictures of tables with labeled columns
# image_tables = image.copy()
# image_without_tables = image.copy()
# for ind, columns_table in enumerate(columns_tables):
#     table = tables[ind]
    

#     flat_text_blocks = get_blocks_inside_table(text_blocks_rows, table)
#     show_columns(image_tables, columns_table, table)
    
#     save_blocks_table(image_without_tables, table, ind, flat_text_blocks, columns_table)
    
               
# # filename_for_tesser = "images/cropped_blocks/input.txt"
# # file_for_tesser = open(filename_for_tesser, 'w')

# # binary_image_path = "images/thresh_{0}.jpg".format(image_name)

# # binary_image = cv2.imread(binary_image_path)
# # binary_image = 255 - binary_image

# # show_image(binary_image)

# # image_without_tables_path = "images/images_without_tables/{0}.jpg".format(image_name)


# def save_cropped_blocks(binary_image, text_blocks_rows):
#     for ind_row, blocks_row in enumerate(text_blocks_rows):
#         for ind_block, text_block in enumerate(blocks_row):
#             y = text_block['y'] - 3
#             h = text_block['h'] + 6
#             x = text_block['x'] - 3
#             w = text_block['w'] + 6
#             cropped_image = image[y:y+h, x:x+w].copy()
#             # recognized_string = pytesseract.image_to_string(cropped_image, lang='rus')
#             filename = "images/cropped_blocks/{0}-{1}-{2}.jpg".format(image_name, ind_row, ind_block)
#             file_for_tesser.write("{0}-{1}-{2}.jpg\n".format(image_name, ind_row, ind_block))
#             save_image(cropped_image, filename)
            

























# def search_for_vert_for_column(column, flat_text_blocks):
#     numb_add = 0
#     for column_elem in column:
#         for text_block in flat_text_blocks[:]:
#             if vertical_condition(column_elem, text_block):
#                 numb_add += 1
#                 column.append(text_block)
#                 flat_text_blocks.remove(text_block)
                
#     if numb_add != 0:
#         search_for_vert_for_column(column, flat_text_blocks)
#     else:
#         columns.append(column)



# for base_text_block in flat_text_blocks[:]:
#     column = []
#     column.append(base_text_block)
#     columns.append(column)
#     # if base_text_block in flat_text_blocks:
#     #     flat_text_blocks.remove(base_text_block)
#     # search_for_vert_for_column(column, flat_text_blocks)



# remaining_text_blocks = copy.deepcopy(text_blocks_rows)
# columns = []
# column = []
# elem = remaining_text_blocks[0][0]
# elem_row_ind = 0
# elem_ind_in_row = 0
# row_ind = 1

# construct_columns(remaining_text_blocks, columns, column, elem, elem_row_ind, elem_ind_in_row, row_ind)