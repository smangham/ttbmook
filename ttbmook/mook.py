import json


class Mook:
    def __init__(self, name):
        self.name = name

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
            mooks.append(cls.mook_from_json(json_mook))

        return mooks

    @classmethod
    def mook_from_json(cls, json_block):
        mook = cls(json_block.name)
        return mook


class SkillCheck:
    """A general skill check."""
    def __init__(self, target_number, modifier=0, target_suit=None):
        self.target_number = target_number
        self.modifier = modifier
        self.target_suit = target_suit


class Attack(SkillCheck):
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
