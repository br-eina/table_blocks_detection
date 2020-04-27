def create_folders(*folders):
    for folder in folders:
        print(folder)

f_list = ['docs/', '1212/', '1111/']
create_folders(*f_list)

create_folders('test_folder/')

create_folders('11/', '22/')
