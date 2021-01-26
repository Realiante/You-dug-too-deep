import unittest
import resources
import pygame


class MyTestCase(unittest.TestCase):

    def test_load_img_gob_preview(self):
        test_img = resources.load_img("character/goblin/_preview.png")
        self.assertEqual((16, 16), test_img.get_size())

    def test_load_img_dir_floor(self):
        floor_images = resources.load_img_dir("tex/floor")
        print(floor_images)

    def test_load_scheme_wasd(self):
        test_scheme_wasd = resources.load_scheme("wasd")
        self.assertEqual(119, test_scheme_wasd[0])
        self.assertEqual(115, test_scheme_wasd[1])
        self.assertEqual(97, test_scheme_wasd[2])
        self.assertEqual(100, test_scheme_wasd[3])
        self.assertEqual(32, test_scheme_wasd[4])
        self.assertEqual(113, test_scheme_wasd[5])

    def test_load_prebuilt_test(self):
        test_pattern = resources.load_prebuilt_pattern("maze_test")
        self.assertEqual("end", test_pattern[0][0])
        self.assertEqual("f", test_pattern[1][0])
        self.assertEqual("key", test_pattern[2][6])
        self.assertEqual("start", test_pattern[6][1])


if __name__ == '__main__':
    unittest.main()
