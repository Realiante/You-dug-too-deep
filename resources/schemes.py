"""
@author: daniel.fedotov
"""

import xml.dom.minidom as minidom
import os.path
import pygame.constants as constants

scheme_dir = f"resources/scheme/"


def load_scheme(scheme_name: str):
    xml_doc = minidom.parse(f"{scheme_dir}{scheme_name}.xml")
    control_scheme = xml_doc.getElementsByTagName("control_scheme")[0]

    k = "K_"
    up = getattr(constants, k + control_scheme.getAttribute("up"))
    down = getattr(constants, k + control_scheme.getAttribute("down"))
    left = getattr(constants, k + control_scheme.getAttribute("left"))
    right = getattr(constants, k + control_scheme.getAttribute("right"))
    action = getattr(constants, k + control_scheme.getAttribute("action"))
    switch = getattr(constants, k + control_scheme.getAttribute("switch"))

    return Scheme((up, down, left, right, action, switch))


class Scheme:

    def __init__(self, controls):
        self.up = controls[0]
        self.down = controls[1]
        self.left = controls[2]
        self.right = controls[3]
        self.action = controls[4]
        self.switch = controls[5]
