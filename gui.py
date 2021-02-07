"""
@author: daniel.fedotov
"""
import pygame
import thorpy

import resources.images as images
import resources.files as files
import xml.dom.minidom as xml
import os.path
import character

config_path = "config.xml"
config_doc = xml.parse(os.path.abspath(config_path)).firstChild
# todo: load player data for further use

player1_data = character.CharacterData(
    doc=config_doc.getElementsByTagName("player_one")[0].getElementsByTagName("player")[0])
player2_data = character.CharacterData(
    doc=config_doc.getElementsByTagName("player_two")[0].getElementsByTagName("player")[0])


class BackgroundPainter(thorpy.painters.painter.Painter):

    def __init__(self, size, clip=None):
        super(BackgroundPainter, self).__init__(size, clip)

    def get_surface(self):
        bg_tex = images.load_weighted_images("tex/wall")
        bgt_w, bgt_h = (*bg_tex.keys(),)[0].get_size()
        surface = pygame.Surface(self.size).convert()
        screen_width, screen_height = self.size
        for height_index in range(0, screen_height, bgt_h):
            for width_index in range(0, screen_width, bgt_w):
                surface.blit(images.choose_by_weight(bg_tex), (width_index, height_index))
                width_index += bgt_w
            height_index += bgt_h
        return surface


class BackgroundElement(thorpy.Element):

    def __init__(self, elements):
        super(BackgroundElement, self).__init__(elements=elements, finish=False)
        display_info = pygame.display.Info()
        self.set_painter(BackgroundPainter((display_info.current_w, display_info.current_h)))
        self.finish()


def __create_img_button(image_paths: tuple):
    btn = thorpy.make_image_button(img_normal=image_paths[0], img_pressed=image_paths[1], img_hover=image_paths[2],
                                   alpha=255, colorkey=(0, 0, 0), force_convert_alpha=True)
    return btn


def __set_slider_from_property(prop: str, ll: int, ul: int):
    values_element = config_doc.getElementsByTagName("properties")[0]
    prop_element = values_element.getElementsByTagName(prop)[0]
    attribute_value = prop_element.getAttribute("value")
    value = int(attribute_value)
    return thorpy.SliderX(length=100, limvals=(ll, ul), text=f"{prop}:", type_=int, initial_value=value)


def __save_properties_to_xml(*props: tuple):
    values_element = config_doc.getElementsByTagName("properties")[0]
    for prop in props:
        prop_element = values_element.getElementsByTagName(prop[0])[0]
        prop_element.setAttribute(attname="value", value=str(prop[1]))


def __write_to_config():
    with open(config_path, mode='w', encoding="UTF-8") as file:
        file.write(config_doc.toxml())


# menu initialization script
# function environment to not bog up the global environment, returns the main menu
def __create_menus():
    ft_color = (200, 200, 200, 30)

    # main menu box
    start = __create_img_button(files.list_files(f"{images.img_dir}ui/start", images.img_formats))
    start.user_func = __start_game
    config = __create_img_button(files.list_files(f"{images.img_dir}ui/config", images.img_formats))
    escape = __create_img_button(files.list_files(f"{images.img_dir}ui/exit", images.img_formats))
    escape.user_func = __exit
    mm_box = thorpy.Box.make([start, config, escape])
    mm_box.set_main_color(ft_color)
    mm_box.center()
    mm_bg = BackgroundElement(elements=[mm_box])

    # config menu box
    conf_text = thorpy.make_text("Configuration", font_size=24)
    s_audio = __set_slider_from_property("audio", 0, 100)
    s_speed = __set_slider_from_property("speed", 1, 3)
    s_shield = __set_slider_from_property("shield", 0, 2)

    def save_to_xml():
        __save_properties_to_xml(
            ("audio", s_audio.get_value()), ("speed", s_speed.get_value()), ("shield", s_shield.get_value()))
        config_launcher.unlaunch()
        __write_to_config()

    cm_confirm = thorpy.make_button("Confirm", func=save_to_xml)
    cm_box = thorpy.Box.make([conf_text, s_audio, s_speed, s_shield, cm_confirm])
    cm_box.set_main_color(ft_color)
    cm_box.center()
    config_launcher = thorpy.set_launcher(config, BackgroundElement(elements=[cm_box]))
    main_menu = thorpy.Menu(mm_bg)
    return main_menu


def __start_game():
    pass  # todo: when the game is in


def __exit():
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def init():
    thorpy.set_theme('human')
    __create_menus().play()
