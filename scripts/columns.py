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
image_path = "docs/{0}.jpg".format(image_name)
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


table_elements = []
# Diff tables apart from lines:
for line in line_elements[:]:
    if line['w'] < 50 * line['h']:
        table_elements.append(line)
        line_elements.remove(line)

    
# Определяем позиции рядов текстовых блоков:
row_positions = []
for ind_row, row in enumerate(text_blocks_rows):
    mass_y_top = []
    mass_y_bot = []
    for elem in row:
        mass_y_top.append(elem['y'])
        mass_y_bot.append(elem['y'] + elem['h'])
    y_top = min(mass_y_top)
    y_bot = max(mass_y_bot)

    row_positions.append({
        'ind': ind_row,
        'y_top': y_top,
        'y_bot': y_bot
    })


# Определяем, есть ли ряд блоков между линией и таблицей:
if len(table_elements) != 0:
    for table in table_elements:
        for line in line_elements[:]:
            # Если линия выше таблицы:
            if line['y'] < table['y']:
                # Определяем координаты площади м-ду ними:
                area_between = {}
                area_between['y_top'] = line['y'] + line['h']
                area_between['y_bot'] = table['y']
                # Определяем к-во рядов, входящих в площадь:
                num_rows = 0
                for row_pos in row_positions:
                    if (
                        row_pos['y_top'] >= area_between['y_top'] and
                        row_pos['y_bot'] <= area_between['y_bot']
                    ):
                        num_rows += 1
                # Если таких рядов нет, то удаляем линию:
                if num_rows == 0:
                    line_elements.remove(line)

def remove_empty_rows(rows):
    for row in rows[:]:
        if len(row) == 0:
            rows.remove(row)
    return rows

def get_blocks_inside_table(text_blocks_rows, table_element):
    # first_table = table_elements[0]
    text_blocks_roi = []
    for ind_row, blocks_row in enumerate(text_blocks_rows):
        text_blocks_roi.append([])
        for text_block in blocks_row:
            if (
                text_block['x'] >= table_element['x'] and
                text_block['y'] >= table_element['y'] and
                (text_block['x'] + text_block['w']) <= (table_element['x'] + table_element['w']) and
                (text_block['y'] + text_block['h']) <= (table_element['y'] + table_element['h'])
            ):
                text_blocks_roi[ind_row].append(text_block)
    text_blocks_roi = remove_empty_rows(text_blocks_roi)

    # Создаем единичный список из вложенных:
    flat_text_blocks = [item for sublist in text_blocks_roi for item in sublist]
    return flat_text_blocks

# Construct columns
def construct_columns(flat_text_blocks, columns):
    for base_text_block in flat_text_blocks[:]:
        consid_text_blocks = copy.deepcopy(flat_text_blocks)
        if base_text_block in consid_text_blocks:
            consid_text_blocks.remove(base_text_block)
        search_for_vert_in_consid_for_base_block(base_text_block, flat_text_blocks, consid_text_blocks)
    return columns

def search_for_vert_in_consid_for_base_block(base_text_block, flat_text_blocks, consid_text_blocks):
    column = []
    numb_vert_blocks = 0
    for text_block in consid_text_blocks[:]:
        if vertical_condition(base_text_block, text_block):
            numb_vert_blocks += 1
            # Добавляем элементы в столбец
            if base_text_block not in column:
                column.append(base_text_block)
            column.append(text_block)
            # Удаляем элементы из рассм и исходного списка:
            if base_text_block in flat_text_blocks:
                flat_text_blocks.remove(base_text_block)
            flat_text_blocks.remove(text_block)
            consid_text_blocks.remove(text_block)
    
    # Если ни одного элемента не было добавлено - удаляем базов текст блок
    if numb_vert_blocks == 0:
        if base_text_block in flat_text_blocks:
            flat_text_blocks.remove(base_text_block)
    # Если сформировался столбец, то рассм оставшиеся элементы по всем эл-там столбца
    else:
        search_for_vert_in_consid_for_column(flat_text_blocks, consid_text_blocks, column)
    
def search_for_vert_in_consid_for_column(flat_text_blocks, consid_text_blocks, column):
    numb_vert_blocks = 0
    for col_block in column:
        for text_block in consid_text_blocks[:]:
            if vertical_condition(col_block, text_block):
                numb_vert_blocks += 1
                # Добавляем элемент в столбец
                column.append(text_block)
                
                # Удаляем элемент из рассм и исх списка:
                if text_block in flat_text_blocks:
                    flat_text_blocks.remove(text_block)
                consid_text_blocks.remove(text_block)
    # Если эл-ты были добавлены, то опять проходим по столбцу
    if numb_vert_blocks != 0:
        search_for_vert_in_consid_for_column(flat_text_blocks, consid_text_blocks, column)
    # Если нет - тогда формируем столбец
    else:
        columns.append(column)
        column = []


def show_columns(image, columns, table):
    # image_to_show = image.copy()
    

    t_p_1 = (table['x'], table['y'])
    t_p_2 = (table['x'] + table['w'], table['y'] + table['h'])
    cv2.rectangle(image, t_p_1, t_p_2, (0, 0, 255), 3)

    for column in columns:
        r = random.randint(0, 255)
        b = random.randint(0, 255)
        g = random.randint(0, 255)
        for element in column:
            p_1 = (element['x'], element['y'])
            p_2 = (element['x'] + element['w'], element['y'] + element['h'])
            cv2.rectangle(image, p_1, p_2, (r, b, g), 4)
    save_image(image, "images/columns/columns_{}.jpg".format(image_name))




columns_tables = []
tables = []
# Рассматриваем все большие связные эл-ты и смотрим, не таблица ли
for table_element in table_elements:
    flat_text_blocks = get_blocks_inside_table(text_blocks_rows, table_element)
    numb_all_blocks = len(flat_text_blocks)
    columns = []
    columns = construct_columns(flat_text_blocks, columns)
    
    # Define number of column elements:
    numb_col_blocks = 0
    for column in columns:
        for element in column:
            numb_col_blocks += 1
    
    # Условие, при котором считаем область таблицей:
    if numb_all_blocks != 0:
        if numb_col_blocks / numb_all_blocks >= 0.7:
            columns_tables.append(columns)
            tables.append(table_element)



# Save pictures of tables with labeled columns
image_tables = image.copy()
image_without_tables = image.copy()
for ind, columns_table in enumerate(columns_tables):
    table = tables[ind]
    

    flat_text_blocks = get_blocks_inside_table(text_blocks_rows, table)
    show_columns(image_tables, columns_table, table)
    