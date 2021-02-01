import os
import pygame
import pygame.constants as constants
import xml.dom.minidom as parser
import itertools

rb = "resources"


def load_img(image_path: str):
    return pygame.image.load(os.path.join(f"{rb}/img/{image_path}"))


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
            line.extend(list(itertools.repeat("w", correction)))

    return pattern
