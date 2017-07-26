import os
import unittest

from ttbmook.mook import Mook
from ttbmook.deck import Card


class DummyDeck:
    def __init__(self):
        self.cards = [
            Card(0, ""),
            Card(1, "T"),
            Card(8, "T"),
            Card(13, "T"),
            Card(14, "CMRT")
        ]

    def flip(self, *args, **kwargs):
        return self.cards.pop(0)


class MookTest(unittest.TestCase):
    def setUp(self):
        mooks = Mook.mooks_from_json(os.path.join("data", "mooks.json"))
        self.mook = mooks[0]

    def test_json_load_mooks(self):
        self.assertEqual("Dummy Mook", self.mook.name)
        self.assertEqual(10, self.mook.willpower)
        self.assertEqual(5, self.mook.defence)
        self.assertEqual(7, self.mook.hp)

    def test_json_load_attacks(self):
        self.assertEqual(1, len(self.mook.attacks))
        self.assertEqual("Fists", self.mook.attacks[0].name)
        self.assertEqual(2, self.mook.attacks[0].range)
        self.assertEqual(1, self.mook.attacks[0].ap)
        self.assertEqual("melee", self.mook.attacks[0].skill)

    def test_mook_attack(self):
        deck = DummyDeck()
        self.assertEqual(7, self.mook.hp)

        # Will flip Black Joker
        self.mook.attack(self.mook, deck=deck)
        self.assertEqual(7, self.mook.hp)

        # Flip 1 of Crows
        self.mook.attack(self.mook, deck=deck)
        self.assertEqual(6, self.mook.hp)

        # Flip 8 of Crows
        self.mook.attack(self.mook, deck=deck)
        self.assertEqual(4, self.mook.hp)

        # Flip 13 of Crows
        self.mook.attack(self.mook, deck=deck)
        self.assertEqual(1, self.mook.hp)

        # Flip Red Joker
        self.mook.attack(self.mook, deck=deck)
        self.assertEqual(-3, self.mook.hp)
        self.assertTrue(self.mook.dead)


if __name__ == '__main__':
    unittest.main()
