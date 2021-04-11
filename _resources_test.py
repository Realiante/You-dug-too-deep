"""
@author: daniel.fedotov
"""

import unittest
import resources.images as images
import resources.levels as levels
import resources.schemes as schemes
import os


class SingleResourceCase(unittest.TestCase):

    def test_load_img_gob_preview(self):
        test_img = images.load_img("character/goblin/_preview.png")
        self.assertEqual((16, 16), test_img.get_size())

    def test_load_img_dir_floor(self):
        equal = images.load_directory_equal("tex/floor")
        weighted = images.load_weighted_images("tex/floor")
        self.assertEqual(len(equal), len(weighted))
        self.assertEqual(equal.keys(), weighted.keys())


def test_load_scheme_wasd(self):
    test_scheme_wasd = schemes.load_scheme("wasd")
    self.assertEqual(119, test_scheme_wasd.up)
    self.assertEqual(115, test_scheme_wasd.down)
    self.assertEqual(97, test_scheme_wasd.left)
    self.assertEqual(100, test_scheme_wasd.right)
    self.assertEqual(32, test_scheme_wasd.action)
    self.assertEqual(113, test_scheme_wasd.switch)


def test_load_prebuilt(self):
    test_pattern = levels.load_pattern("maze_test")
    self.assertEqual(["f", "end"], test_pattern[0][0])
    self.assertEqual(["f"], test_pattern[1][0])
    self.assertEqual(["f", "key"], test_pattern[2][6])
    self.assertEqual(["f", "start"], test_pattern[6][1])
    self.assertEqual(["f"], test_pattern[9][9])


def test_load_broken_prebuilt(self):
    test_pattern = levels.load_pattern("test/broken")
    print(test_pattern)
    self.assertEqual(["f", "f"], test_pattern[0][0])
    self.assertEqual(["f", "f", "w"], test_pattern[0][7])
    self.assertEqual(["f", "key"], test_pattern[1][1])
    self.assertEqual(["w"], test_pattern[7][0])
    self.assertEqual(["w"], test_pattern[7][7])


if __name__ == '__main__':
    unittest.main()
