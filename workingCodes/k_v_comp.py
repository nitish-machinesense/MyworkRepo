import os
import json


# Get List of Files
def get_dir_files(dir_path):
    files_list = []
    for file_name in os.listdir(dir_path):
        files_list.append(os.path.join(dir_path, file_name))
    return files_list


# get all keys from JSON object along with their values
def get_all_keys_with_values(obj, parent_key):
    keys_values = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, (dict, list, tuple)):
                keys_values.extend(get_all_keys_with_values(value, new_key))
            else:
                keys_values.append((new_key, value))
    elif isinstance(obj, (list, tuple)):
        for index, item in enumerate(obj):
            new_key = f"{parent_key}[{index}]"
            if isinstance(item, (dict, list, tuple)):
                keys_values.extend(get_all_keys_with_values(item, new_key))
            else:
                keys_values.append((new_key, item))
    return keys_values


# Compare Keys and Values from two files
def validate_keys_and_values(opdir, basefile, obj_name):
    l1 = []
    filename = []
    # Loop through all files in the Output directory and read their keys and values
    for i in get_dir_files(opdir):
        with open(i) as file:
            data = json.load(file)
            # Append the filename and its respective keys and values to the lists
            filename.append(os.path.basename(i))
            l1.append(get_all_keys_with_values(data[obj_name], ''))

    # Read keys and values from the basefile
    with open(basefile) as file:
        base_data = json.load(file)
        l2 = get_all_keys_with_values(base_data[obj_name], '')

    # Compare keys and values from each file with the keys and values in the basefile
    for i in range(len(l1)):
        if l1[i] == l2:
            print(f'SUCCESS!!, {obj_name} Keys and Values Matched for Output File {filename[i]}')
        else:
            print(f"ERROR!!, {obj_name} Keys and Values not matching for File {filename[i]}")
            print(f'\n   Additional {obj_name} Keys and Values in Output File: ')
            for key, value in list(set(l1[i]) - set(l2)):
                print('       ', key, value)

            print(f'\n   Additional {obj_name} Keys and Values in Base File: ')
            for key, value in list(set(l2) - set(l1[i])):
                print('       ', key, value)
        print('-------------------------------------------------------------------------')


opDir = "D:/MachinesenseProjects/opjson1"
baseFile = "D:/MachinesenseProjects/opjson2/1690800067_machine-4d1586f0-0f54-11ee-9f89-0f5105fc0649_output.json"
validate_keys_and_values(opDir, baseFile, 'header')
