import pygame
import pygame.constants as constants
import xml.dom.minidom as parser
import random
from itertools import repeat
from os import listdir
from os.path import isfile, abspath, join

__img_dir = f"resources/img/"
__scheme_dir = f"resources/scheme/"
__prebuilt_dir = f"resources/prebuilt/"

__img_formats = ('.png', '.jpg', '.bmp', '.gif')
__img_dict = {}


# ensures that only one instance of the same image is kept in memory
def load_img(image_path: str):
    if image_path not in __img_dict.keys():
        image = pygame.image.load(abspath(f"{__img_dir}{image_path}"))
        __img_dict[image_path] = image
    return __img_dict[image_path]


def load_img_dir(dir: str):
    dir_path = f"{__img_dir}{dir}"
    file_names = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
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


def load_scheme(scheme_name: str):
    xml_doc = parser.parse(abspath(f"{__scheme_dir}{scheme_name}.xml"))
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
    file_path = abspath(f"{__prebuilt_dir}{prebuilt_name}.txt")
    pattern = []

    with open(file_path) as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip(' ,\n')
        line_layers = line.split(',')
        p_layers = []
        for layers in line_layers:
            layers = layers.split(':')
            p_layers.append(layers)
        pattern.append(p_layers)

    # correcting the short pattern lines by making them equal to the longest line/column in length
    max_len = len(max(pattern, key=len))
    for line in pattern:
        correction = max_len - len(line)
        if correction > 0:
            line.extend([*repeat(["w"], correction)])

    # correcting the missing pattern rows by copying the last line to form a square grid
    while max_len > len(pattern):
        pattern.append([*repeat(["w"], max_len)])

    return pattern
