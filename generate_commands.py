from os import listdir
from os.path import isfile, join
mypath = r'e:/__PR/docs/pdf2jpg/1C img/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# print(onlyfiles)

new_list = []

for filename in onlyfiles:
    new = filename[:-4]
    new_list.append(new)

print(new_list)

with open("commands_cmd.txt", "w+") as text_file:
    for ind, image_name in enumerate(new_list):
        string1 = "python code\detect_lines_symbols.py --img {0} & ".format(image_name)
        string2 = "python code\constr_rows.py --img {0} & ".format(image_name)
        string3 = "python code\constr_blocks.py --img {0} & ".format(image_name)
        if ind != len(new_list) - 1:
            string4 = "python code\\detect_table.py --img {0} &".format(image_name)
        else:
            string4 = "python code\\detect_table.py --img {0}".format(image_name)
        string = string1 + string2 + string3 + string4
        print(string, file=text_file)