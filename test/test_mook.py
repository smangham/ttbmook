import os
import unittest

from ttbmook.mook import Mook


class MookTest(unittest.TestCase):
    def test_json_load_mooks(self):
        mooks = Mook.mooks_from_json(os.path.join("data", "mooks.json"))
        mook = mooks[0]

        self.assertEqual("Hanged Man", mook.name)
        self.assertEqual(10, mook.willpower)
        self.assertEqual(5, mook.defence)
        self.assertEqual(7, mook.hp)

    def test_json_load_attacks(self):
        mooks = Mook.mooks_from_json(os.path.join("data", "mooks.json"))
        mook = mooks[0]

        self.assertEqual(1, len(mook.attacks))
        self.assertEqual("Fists", mook.attacks[0].name)
        self.assertEqual(2, mook.attacks[0].range)
        self.assertEqual(1, mook.attacks[0].ap)
        self.assertEqual("melee", mook.attacks[0].skill)


if __name__ == '__main__':
    unittest.main()
