import os
import json


# Get List of Files
def get_dir_files(dir_path):
    files_list = []
    for file_name in os.listdir(dir_path):
        files_list.append(os.path.join(dir_path, file_name))
    return files_list

# get all keys from JSON object
def get_all_keys(obj, parent_key):
    keys = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            keys.append(new_key)
            keys.extend(get_all_keys(value, new_key))
    elif isinstance(obj, (list, tuple)):
        for index, item in enumerate(obj):
            new_key = f"{parent_key}[{index}]"
            keys.extend(get_all_keys(item, new_key))
    return keys


# Compare Keys from two files
def validateKeys(opdir, basefile, obj_name):
    l1 = []
    filename = []
# Loop through all files in the Output directory and read their keys
    for i in get_dir_files(opdir):
        with open(i) as file:
            data = json.load(file)
             # Append the filename and its respective keys to the lists
            filename.append(os.path.basename(i))
            l1.append(get_all_keys(data[obj_name], ''))

# Read keys from the basefile
    with open(basefile) as file:
        base_data = json.load(file)
        l2 = get_all_keys(base_data[obj_name], '')


# Compare keys from each file with the keys in the basefile
    for i in range(len(l1)):
        if l1[i] == l2:
            print(f'SUCCESS!!, {obj_name} Keys Matched for Output File {filename[i]}') 
        else:
            print(f"ERROR!!, {obj_name} Keys not matching for File {filename[i]}")
            print(f'\n   Additional {obj_name} Keys in Output File: ')
            for key in list(set(l1[i]) - set(l2)):
                print('       ', key)

            print(f'\n   Additional {obj_name} Keys in Base File: ')
            for key in list(set(l2) - set(l1[i])):
                print('       ', key)
        print('-------------------------------------------------------------------------')

opDir  = "D:/MachinesenseProjects/opjson1"
baseFile = "D:/MachinesenseProjects/opjson2/1690800067_machine-4d1586f0-0f54-11ee-9f89-0f5105fc0649_output.json"
validateKeys(opDir, baseFile, 'header')
