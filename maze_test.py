import unittest
import maze
import resources


class MyTestCase(unittest.TestCase):
    def test_maze_class_init(self):
        loaded = maze.Maze(resources.load_prebuilt_pattern("test/micro"))
        self.assertEqual(True, loaded.dirty)
        self.assertEqual((0, 0), loaded.key_pos)
        self.assertEqual((1, 0), loaded.player_pos)
        self.assertEqual((1, 1), loaded.end_pos)


if __name__ == '__main__':
    unittest.main()