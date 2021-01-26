import pygame
import pygame.constants as constants
import xml.dom.minidom as parser
from itertools import repeat
from os import walk

rb = "resources"
img_dir = f"{rb}/img/"


def load_img(image_path: str):
    return pygame.image.load(f"{img_dir}{image_path}")


def load_img_dir(dir: str):
    dir_path = f"{img_dir}{dir}"
    non, non, file_names = next(walk(dir_path))
    file_names.sort()
    images = []
    for file in file_names:
        file_path = f"{dir_path}/{file}"
        images.append(pygame.image.load(file_path))
    return (*images,)  # unwraps the list into a tuple


def load_scheme(scheme_name: str):
    xml_doc = parser.parse(f"{rb}/scheme/{scheme_name}.xml")
    control_scheme = xml_doc.getElementsByTagName("control_scheme")[0]

    k = "K_"
    up = getattr(constants, k + control_scheme.getAttribute("up"))
    down = getattr(constants, k + control_scheme.getAttribute("down"))
    left = getattr(constants, k + control_scheme.getAttribute("left"))
    right = getattr(constants, k + control_scheme.getAttribute("right"))
    action = getattr(constants, k + control_scheme.getAttribute("action"))
    switch = getattr(constants, k + control_scheme.getAttribute("switch"))

    return up, down, left, right, action, switch


def load_prebuilt_pattern(prebuilt_name: str):
    file_path = f"{rb}/prebuilt/{prebuilt_name}.txt"
    # loading the pattern from file path
    pattern = []
    with open(file_path) as file:
        lines = file.readlines()
        for line in lines:
            line.strip(" ,")
            pattern.append(line.split(','))

    # correcting the short pattern lines by making them equal to the longest in length
    max_len = len(max(pattern))
    for line in pattern:
        correction = max_len - len(line)
        if correction > 0:
            line.extend(list(repeat("w", correction)))

    return tuple(map(tuple, pattern))  # wrapping every sublist into a tuple, then wrapping the list
