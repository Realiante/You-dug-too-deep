"""
@author: daniel.fedotov
"""
import os


def list_files(directory: str, extensions=()):
    file_names = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    file_names.sort()
    if len(extensions) == 0:
        return __with_directory(directory, file_names)
    new_list = []
    for file_name in file_names:
        if file_name.lower().endswith(extensions):
            new_list.append(file_name)
    return __with_directory(directory, new_list)


def __with_directory(directory: str, name_list: list):
    names_with_dir = []
    for name in name_list:
        names_with_dir.append(f"{directory}/{name}")
    return names_with_dir
