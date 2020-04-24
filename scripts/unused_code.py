# def detect_text_for_rem(stats):
#     remaining_text = copy(stats)
#     for stat in remaining_text[:]:
#         if (
#             (stat[2] <= 6 and stat[3] >= 4 * stat[2]) or
#             (stat[3] <= 6 and stat[2] >= 4 * stat[3]) or
#             stat[4] <= 15
#         ):
#             remaining_text.remove(stat)
#     return remaining_text











# # Dilate (to get dilated lines and large connected components):
#     kernel = np.ones((3, 3), np.uint8)
#     dilation_image = cv2.dilate(thresh, kernel, iterations=2)

# # For lines and tables:
# retval_dil, _, stats_np_dil, _ = cv2.connectedComponentsWithStats(dilation_image, connectivity=8)
# stats_np_lines = stats_np_dil[1:retval_dil]















    # # Make ROI for 4th line:
    # if len(line_elements) > 0:
    #     line = line_elements[0]
    #     roi = {}
    #     roi['x'] = line['x']
    #     roi['y'] = line['y']
    #     roi['w'] = line['w']
    #     roi['h'] = 15 * 5 * avg_height

    # if len(line_elements) > 0:
    #     # Detect text elem in ROI
    #     text_elem_in_roi = []
    #     for text_elem in text_elements:
    #         if check_if_el_in_roi(text_elem, roi) == 1:
    #             text_elem_in_roi.append(text_elem)

# print(type(None))




















# # Сохранение блоков, не лежащих в таблице:
# def save_blocks_not_in_table(text_blocks, image, image_name):
#     blocks_not_in_table = []
#     for row in text_blocks:
#         for block in row:
#             if block['in_table'] == False:
#                 blocks_not_in_table.append(block)
#     save_image_blocks_not_in_table(image, blocks_not_in_table, image_name)
#     with open("data_not_in_table/blocks_not_in_table_{0}.data".format(image_name), 'wb') as f:
#         pickle.dump(blocks_not_in_table, f)

# # Сохранение символов, не лежащих в таблице:
# def save_symbols_not_in_table(text_elements, tables, image, image_name):
#     symbols_not_in_table = []
#     for table in tables:
#         for ind, symbol in enumerate(text_elements):
#             if elem_in_table(symbol, table):
#                 text_elements[ind]['in_table'] = True
#     for symbol in text_elements:
#         if symbol['in_table'] == False:
#             symbols_not_in_table.append(symbol)
#     save_image_symbols_not_in_table(image, symbols_not_in_table, image_name)
#     with open("data_not_in_table/symbols_not_in_table_{0}.data".format(image_name), 'wb') as outfile:
#         pickle.dump(symbols_not_in_table, outfile)

# def save_text_blocks(text_blocks_rows, image_name):
#     with open("inv_processing/data/data_text_blocks_tables_{0}.data".format(image_name), 'wb') as outfile:
#         pickle.dump(text_blocks_rows, outfile)

# def save_image_blocks_not_in_table(image, blocks_not_in_table, image_name):
#     image_to_show = image.copy()
#     for element in blocks_not_in_table:
#         p_1 = (element['x'], element['y'])
#         p_2 = (element['x'] + element['w'], element['y'] + element['h'])
#         cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 2)
#     utils.save_image(image_to_show, "results/{0}/{0}_blocks_not_in_table.jpg".format(image_name))

# def save_image_symbols_not_in_table(image, symbols_not_in_table, image_name):
#     image_to_show = image.copy()
#     for element in symbols_not_in_table:
#         p_1 = (element['x'], element['y'])
#         p_2 = (element['x'] + element['w'], element['y'] + element['h'])
#         cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 2)
#     utils.save_image(image_to_show, "results/{0}/{0}_symbols_not_in_table.jpg".format(image_name))


# def save_tables_lines(image, lines_elem, image_name):
#     image_to_show = image.copy()
#     for element in lines_elem:
#         p_1 = (element['x'], element['y'])
#         p_2 = (element['x'] + element['w'], element['y'] + element['h'])
#         cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 3)
#     utils.save_image(image_to_show, "results/{}_tables.jpg".format(image_name))
#     utils.save_image(image_to_show, "results/{0}/{0}_tables.jpg".format(image_name))


# def check_number_blocks_in_table(tables, text_blocks_rows):
#     # Add parameter to text block
#     # If in table: True

#     for ind_row, row in enumerate(text_blocks_rows):
#         for ind_block, block in enumerate(row):
#             for table in tables:
#                 if (
#                     (block['x'] >= table['x']) and (block['x'] + block['w'] <= table['x'] + table['w']) and
#                     (block['y'] >= table['y']) and (block['y'] + block['h'] <= table['y'] + table['h'])
#                 ):
#                     text_blocks_rows[ind_row][ind_block]['in_table'] = True

# def find_tables_without_lines(line_elements_copy, hor_lines, vert_lines,
#                               table_elements_with_lines):
#     for table in line_elements_copy:
#         if table_by_lines(table, hor_lines, vert_lines) == 1:
#             table_elements_with_lines.append(table)





















# def check_rows_for_two_el(rows):
#     key = 0
#     for ind_row, row in enumerate(rows):
#         if ind_row != len(rows) - 1:
#             if len(row) != 0 and len(rows[ind_row + 1]) != 0:
#                 key += 1
#                 ind_row_1 = ind_row
#                 break
#     if key > 0:
#         return 1, ind_row_1
#     else:
#         return 0, 0

# def vertical_condition(block_1, block_2):
#     t = 3
#     x_l1 = block_1['x']
#     x_r1 = x_l1 + block_1['w']
#     x_c1 = (x_l1 + x_r1) // 2

#     x_l2 = block_2['x']
#     x_r2 = x_l2 + block_2['w']
#     x_c2 = (x_l2 + x_r2) // 2

#     if abs(x_l1 - x_l2) <= t or abs(x_c1 - x_c2) <= t or abs(x_r1 - x_r2) <= t:
#     # if abs(x_c1 - x_c2) <= t:
#         return 1
#     else:
#         return 0








# def show_lines(image, lines_elem, image_name):
#     image_to_show = image.copy()
#     for element in lines_elem:
#         p_1 = (element['x'], element['y'])
#         p_2 = (element['x'] + element['w'], element['y'] + element['h'])
#         cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 3)
#     utils.save_image(image_to_show, "images/lines/{}_lines.jpg".format(image_name))

# def show_bbox(image, element):
#     image_to_show = image.copy()
#     p_1 = (element['x'], element['y'])
#     p_2 = (element['x'] + element['w'], element['y'] + element['h'])
#     cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 5)
#     utils.show_image(image_to_show)

# def show_text_blocks_in_row(image, rows):
#     image_to_show = image.copy()
#     for row in rows:
#         for element in row:
#             p_1 = (element['x'], element['y'])
#             p_2 = (element['x'] + element['w'], element['y'] + element['h'])
#             cv2.rectangle(image_to_show, p_1, p_2, (0, 0, 255), 4)
#         utils.show_image(image_to_show)






# if num_blocks_in_table >= 4:
#         return 1
#     else:
#         return 0