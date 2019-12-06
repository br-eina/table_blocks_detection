import json

# with open('gt_tables.txt') as json_file:
#     data = json.load(json_file)
#     # for p in data['people']:
#     #     print('Name: ' + p['name'])
#     #     print('Website: ' + p['website'])
#     #     print('From: ' + p['from'])
#     #     print('')

# print(data)

# from os import listdir
# from os.path import isfile, join
# mypath = "docs/"
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# print(onlyfiles)

# new_list = []

# for filename in onlyfiles:
#     new = filename[:-4]
#     new_list.append(new)

# print(new_list)

# with open("gt_tables.txt", "w+") as text_file:
#     for ind, image_name in enumerate(new_list):
#         string = '{} : '.format(image_name)
#         # string1 = "python code\detect_lines_symbols.py --img {0} & ".format(image_name)
#         # string2 = "python code\constr_rows.py --img {0} & ".format(image_name)
#         # string3 = "python code\constr_blocks.py --img {0} & ".format(image_name)
#         # if ind != len(new_list) - 1:
#         #     string4 = "python code\\detect_table.py --img {0} &".format(image_name)
#         # else:
#         #     string4 = "python code\\detect_table.py --img {0}".format(image_name)
#         # string = string1 + string2 + string3 + string4
#         print(string, file=text_file)










# define an empty list
gt_number_tables = []

# open file and read the content in a list
with open('gt_number_tables.txt', 'r') as filehandle:
    for line in filehandle:
        # remove linebreak which is the last character of the string
        currentPlace = line[0]

        # add item to the list
        gt_number_tables.append(currentPlace)


print(gt_number_tables)