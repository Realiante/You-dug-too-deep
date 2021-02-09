"""
@author: daniel.fedotov
"""
import pygame
import thorpy
import tilescript
import resources.images as images
import resources.files as files
import xml.dom.minidom as xml
import os.path
import copy
import character
import maze

config_path = "config.xml"
__config_doc = xml.parse(os.path.abspath(config_path)).firstChild
__properties_doc = __config_doc.getElementsByTagName("properties")[0]
__p1_doc = __config_doc.getElementsByTagName("player_one")[0].getElementsByTagName("player")[0]
__p2_doc = __config_doc.getElementsByTagName("player_two")[0].getElementsByTagName("player")[0]
__player1_data = character.CharacterData(doc=__p1_doc)
__player2_data = character.CharacterData(doc=__p2_doc)


# todo: modify player data from settings.
# todo: figure how to properly start the game screen

class GamePainter(thorpy.painters.painter.Painter):

    def __init__(self, lvl: maze.MazeData, player: character.Character):
        super(GamePainter, self).__init__((len(lvl.grid) * 16, len(lvl.grid[0]) * 16), clip=None)
        # references to the GameElement's lvl and player parameters
        self.lvl = lvl
        self.player = player

    def get_surface(self):
        width, height = self.size
        surface = pygame.Surface(self.size).convert()
        for height_index in range(0, height // 16):
            cur_height = height_index * 16
            for width_index in range(0, width // 16):
                cur_width = width_index * 16
                for layer in self.lvl.grid[height_index][width_index]:
                    tex_dist = tilescript.dictionary[layer][0]
                    if tex_dist is not None:
                        surface.blit(images.choose_by_weight(tex_dist), (cur_width, cur_height))
        return surface


class GameElement(thorpy.Element):

    def __init__(self, lvl: maze.MazeData, player: character.Character):
        super(GameElement, self).__init__(finish=False)
        self.lvl = copy.copy(lvl)
        self.player = player
        self.set_painter(GamePainter(self.lvl, self.player))
        self.finish()


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
    values_element = __config_doc.getElementsByTagName("properties")[0]
    prop_element = values_element.getElementsByTagName(prop)[0]
    attribute_value = prop_element.getAttribute("value")
    value = int(attribute_value)
    return thorpy.SliderX(length=100, limvals=(ll, ul), text=f"{prop}:", type_=int, initial_value=value)


def __save_properties_to_xml(*props: tuple):
    for prop in props:
        attr, value = prop
        prop_element = __properties_doc.getElementsByTagName(attr)[0]
        prop_element.setAttribute(attname="value", value=str(value))


def __write_to_config():
    with open(config_path, mode='w', encoding="UTF-8") as file:
        file.write(__config_doc.toxml())


def __get_properties():
    audio = __properties_doc.getElementsByTagName("audio")[0]
    speed = __properties_doc.getElementsByTagName("speed")[0]
    shield = __properties_doc.getElementsByTagName("shield")[0]
    return audio, speed, shield


# menu initialization script
# function environment to not bog up the global environment, returns the main menu
def __create_menus():
    ft_color = (0, 0, 0, 125)

    # main menu box
    start = __create_img_button(files.list_files(f"{images.img_dir}ui/start", images.img_formats))
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

    # game box
    empty_game_text = thorpy.make_text("No game loaded!")
    game_box = thorpy.Box.make(elements=[empty_game_text])

    def start_game():
        properties = __get_properties()
        game_box.remove_all_elements()
        lvl_gen = maze.MazeBuilder(25, 25)  # todo: should probably keep an instance of the maze builder
        lvl = maze.MazeData(lvl_gen.maze)
        player = __player1_data.create_character(properties[1], properties[2])  # todo: load both players.
        game_box.add_element(GameElement(lvl, player))

    start.user_func = start_game
    thorpy.set_launcher(start, BackgroundElement(elements=[game_box]))

    return main_menu


def __exit():
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def init():
    thorpy.set_theme('human')
    __create_menus().play()
