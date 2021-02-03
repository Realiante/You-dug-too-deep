"""
@author: daniel.fedotov
"""

from os.path import abspath
from itertools import repeat

mazes_dir = f"resources/levels/"


def load_pattern(prebuilt_name: str):
    file_path = abspath(f"{__mazes_dir}{prebuilt_name}.txt")
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
