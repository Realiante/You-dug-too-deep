"""
@author: daniel.fedotov
"""

import os
import random

import pygame

__img_dir = f"resources/images/"
__img_formats = ('.png', '.jpg', '.bmp', '.gif')
__img_dict = {}


# ensures that only one instance of the same image is kept in memory
def load_img(image_path: str):
    if image_path not in __img_dict.keys():
        image = pygame.image.load(os.path.abspath(f"{__img_dir}{image_path}"))
        __img_dict[image_path] = image
    return __img_dict[image_path]


def load_directory(dir: str):
    dir_path = f"{__img_dir}{dir}"
    file_names = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    file_names.sort()
    images = []
    for file_name in file_names:
        if file_name.lower().endswith(__img_formats):
            file_path = f"{dir}/{file_name}"
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


def load_weighted_images(dir: str):
    weight_path = f"{__img_dir}{dir}/weight.txt"
    weights = __parse_weight_list(weight_path)
    weighted_images = {}
    for img_name in weights.keys():
        image = load_img(f"{dir}/{img_name}")
        weighted_images[image] = weights[img_name]
    return weighted_images


def choose_by_weight(weights: dict):
    return random.choices((*weights.keys(),), (*weights.values(),), k=1)[0]
