from os import listdir
from os.path import isfile, join
import numpy as np

mypath = "categories/___/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# print(onlyfiles)

no_extension_filenames = []

for filename in onlyfiles:
    no_extension_filename = filename[:-4]
    no_extension_filenames.append(no_extension_filename)

# print(no_extension_filenames)

# with open ("commands_categories.txt", "w+") as text_file:
with open ("commands_categories_detect_block + table.txt", "w+") as text_file:
    for ind, image_name in enumerate(no_extension_filenames):
        string1 = "python code\detect_lines_symbols.py --img {0} & ".format(image_name)
        string2 = "python code\constr_rows.py --img {0} & ".format(image_name)
        string3 = "python code\constr_blocks.py --img {0} & ".format(image_name)
        if ind != len(no_extension_filenames) - 1:
            string4 = "python code\\detect_table.py --img {0} &".format(image_name)
        else:
            string4 = "python code\\detect_table.py --img {0}".format(image_name)
        # string = string1 + string2 + string3 + string4
        string = string3 + string4
        print(string, file=text_file)


# 11










# dict_matching = {
#     'inv-0074': 'akt-01',
#     'inv-0087': 'akt-02',
#     'inv-0054': 'akt-03',
#     'inv-0051': 'akt-04',
#     'inv-0003': 'akt-05',

# }