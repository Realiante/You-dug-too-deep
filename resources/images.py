"""
@author: daniel.fedotov
"""

import os
import random
import resources.files

import pygame

img_dir = f"resources/images/"
img_formats = ('.png', '.jpg', '.bmp', '.gif')
__img_dict = {}


# ensures that only one instance of the same image is kept in memory
def load_img(image_path: str):
    if image_path not in __img_dict.keys():
        image = pygame.image.load(os.path.abspath(f"{img_dir}{image_path}"))
        __img_dict[image_path] = image
    return __img_dict[image_path]


def load_directory(directory: str):
    dir_path = f"{img_dir}{directory}"
    file_names = resources.files.list_files(dir_path, __img_formats)
    images = []
    for file_name in file_names:
        file_path = f"{directory}/{file_name}"
        images.append(load_img(file_path))
    return (*images,)  # unwraps the list into a tuple


def __parse_weight_list(weight_path: str):
    weights = {}
    with open(weight_path) as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip(' \n')
        w_text = line.split('=')
        weights[w_text[0]] = int(w_text[1])
    return weights


def load_weighted_images(directory: str):
    weight_path = f"{img_dir}{directory}/weight.txt"
    weights = __parse_weight_list(weight_path)
    weighted_images = {}
    for img_name in weights.keys():
        image = load_img(f"{directory}/{img_name}")
        weighted_images[image] = weights[img_name]
    return weighted_images


def choose_by_weight(weights: dict):
    return random.choices((*weights.keys(),), (*weights.values(),), k=1)[0]
