import os
import unittest

from ttbmook.mook import Mook
from ttbmook.deck import Card


class DummyDeck:
    def __init__(self):
        self.cards = [
            Card(1, "T"),
            Card(11, "T"),
            Card(8, "R"),
            Card(11, "T"),
            Card(14, "CMRT"),
            Card(11, "T"),
            Card(1, "R"),
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

    def test_dead_flag(self):
        self.assertFalse(self.mook.dead)
        self.mook.hp = -1
        self.assertTrue(self.mook.dead)

    def test_dead_flag_enforcer(self):
        self.mook.is_enforcer = True
        self.assertFalse(self.mook.dead)
        self.mook.hp = -1
        self.assertFalse(self.mook.dead)

    def test_mook_attack_get_damage(self):
        attack = self.mook.attacks[0]
        self.assertEqual(0, attack.get_damage("None"))
        self.assertEqual(1, attack.get_damage("Mild"))
        self.assertEqual(2, attack.get_damage("Moderate"))
        self.assertEqual(3, attack.get_damage("Severe"))
        self.assertEqual(4, attack.get_damage("Mild+Severe"))

    def test_mook_attack(self):
        # TODO add non-straight damage flips
        deck = DummyDeck()
        self.assertEqual(7, self.mook.hp)

        # Will flip 1 of Tomes and miss
        self.assertFalse(self.mook.attack(self.mook, deck=deck))
        self.assertEqual(7, self.mook.hp)

        # Flip 11 of Tomes - straight damage flip
        # Flip 8 of Rams - moderate damage
        self.assertTrue(self.mook.attack(self.mook, deck=deck))
        self.assertEqual(5, self.mook.hp)

        # Flip 11 of Tomes - straight damage flip
        # Flip Red Joker - strong + weak damage
        self.assertTrue(self.mook.attack(self.mook, deck=deck))
        self.assertEqual(1, self.mook.hp)

        # Flip 11 of Tomes - straight damage flip
        # Flip 1 of Rams - weak damage
        self.assertTrue(self.mook.attack(self.mook, deck=deck))
        self.assertEqual(0, self.mook.hp)

        self.assertTrue(self.mook.dead)


if __name__ == '__main__':
    unittest.main()
