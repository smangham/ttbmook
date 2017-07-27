import json


class Mook:
    """
    A Malifaux TTB NPC.
    """
    def __init__(self, name, willpower, defence, hp,
                 is_enforcer=False, attacks=None):
        self.name = name
        self.willpower = willpower
        self.defence = defence
        self.hp = hp
        self.dead = False
        self.is_enforcer = is_enforcer

        self.attacks = attacks

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, x):
        """
        Setter for hp.  Sets dead flag if hp is below zero and not enforcer level.

        :param int x: New hp
        """
        self.__hp = x
        if self.__hp < 0 and not self.is_enforcer:
            self.dead = True

    def attack(self, target, attack_id=0, deck=None):
        """
        Perform an attack against target.

        :param Mook target: Target Mook
        :param int attack_id: Attack id if Mook has multiple attacks
        :param deck: Deck from which to draw Cards
        """
        self.attacks[attack_id].attack(target, deck)

    @classmethod
    def mooks_from_json(cls, filename):
        """
        Get list of Mooks from JSON file.

        :param str filename: JSON file to process
        :return: List of Mooks
        """
        with open(filename) as f:
            json_all = json.load(f, object_hook=AttrDict)

        mooks = []  # TODO should this be a dictionary of {name: Mook}
        for json_mook in json_all.mooks:
            mooks.append(cls.from_json(json_mook))

        return mooks

    @classmethod
    def from_json(cls, json_block):
        """
        Construct a single Mook from a JSON block/AttrDict.

        :param AttrDict json_block: JSON block in AttrDict format
        :return Mook: New Mook
        """
        attacks = []
        for json_attack in json_block.attacks:
            attacks.append(Attack.from_json(json_attack))

        mook = cls(name=json_block.name, willpower=json_block.willpower,
                   defence=json_block.defence, hp=json_block.HP, attacks=attacks)
        return mook


class Attack:
    def __init__(self, name, range, ap, skill):
        self.name = name
        self.range = range
        self.ap = ap
        self.skill = skill

    def attack(self, target, deck=None):
        """
        Perform this attack against a target.

        :param Mook target: Target Mook of this attack
        :param deck: Deck from which to draw Cards
        """
        if deck is None:
            pass  # Get default deck
        raise NotImplementedError

    @classmethod
    def from_json(cls, json_block):
        """
        Construct a single Attack from a JSON block/AttrDict.

        :param AttrDict json_block: JSON block in AttrDict format
        :return: New Attack
        """
        return cls(name=json_block.name, range=json_block.range,
                   ap=json_block.AP, skill=json_block.skill)


class SkillCheck:
    """A general skill check."""
    def __init__(self, target_number, modifier=0, target_suit=None):
        self.target_number = target_number
        self.modifier = modifier
        self.target_suit = target_suit


class AttackCheck(SkillCheck):
    """An attack skill check.  Provides description and handles damage."""
    def __init__(self, target_number, modifier=0, target_suit=None):
        super().__init__(target_number, modifier, target_suit)

    @classmethod
    def from_json(cls, json_block):
        raise NotImplementedError


class AttrDict(dict):
    """Allow dictionary entries to be accessed as attributes as well as keys."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
