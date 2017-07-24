import unittest
import os

from ttbmook.mook import Mook


class MookTest(unittest.TestCase):
    def test_json_load_mooks(self):
        mooks = Mook.mooks_from_json(os.path.join("data", "mooks.json"))
        mook = mooks[0]
        self.assertEqual("Hanged Man", mook.name)


if __name__ == '__main__':
    unittest.main()
