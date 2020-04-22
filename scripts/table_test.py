# define an empty list
gt_number_tables = []

# open file and read the content in a list
with open('gt_number_tables.txt', 'r') as filehandle:
    for line in filehandle:
        # remove linebreak which is the last character of the string
        currentPlace = line[0]

        # add item to the list
        gt_number_tables.append(currentPlace)


# print(gt_number_tables)

number_tables = []

# open file and read the content in a list
with open('number_tables.txt', 'r') as filehandle:
    for line in filehandle:
        # remove linebreak which is the last character of the string
        currentPlace = line[0]

        # add item to the list
        number_tables.append(currentPlace)

number_of_all_tables = 0
number_found_tables = 0
number_false_tables = 0
for ind, element in enumerate(gt_number_tables):
    number_of_all_tables += int(element)
    if int(number_tables[ind]) <= int(element):
        number_found_tables += int(number_tables[ind])
    else:
        # num = int(element) - (int(number_tables[ind]) - int(element))
        num = int(element)
        number_found_tables += num
        number_false_tables += int(number_tables[ind]) - int(element)
        

print("found", number_found_tables)
print("all", number_of_all_tables)
print('%', number_found_tables/number_of_all_tables)
print("false", number_false_tables)
print("'%' of false", number_false_tables / number_of_all_tables)


    
