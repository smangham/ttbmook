import random
import copy
import json

class Card:
    def __init__(self, value, suit):
        self._value = value
        self._suit = suit
    def __repr__(self):
        return "Card()"
    def __str__(self):
        return "{}{}".format(self._value, self._suit)
    def value(self):
        return self._value
    def is_suit(self, suit):
        return suit in self._suit
    def damage(self):
        if value is 0:
            return "None"
        elif value <= 5:
            return "Mild"
        elif value <= 10:
            return "Moderate"
        elif value <= 13:
            return "Severe"
        else:
            return "Mild+Severe"
    def print(self):
        return "{}{}".format(self._value,self._suit)

class Deck:
    def __init__(self):
        self._cards = []
        for value in range(1,14):
            for suit in ['C', 'M', 'R', 'T']:
                self._cards.append(Card(value, suit))
        self._cards.append(Card(0,''))
        self._cards.append(Card(14,'CMRT'))
        self._cards_current = copy.copy(self._cards)

    def _deal(self):
        index = random.randint(0,len(self._cards_current)-1)
        card = self._cards_current[index]
        self._cards_current.remove(card)
    
        # If we ran through the deck, refill it and issue a notification!
        if len(self._cards_current) is 0:
            self._cards_current = copy.copy(self._cards)
            # TRIGGER MESSAGE OF SOME KIND
            print("DECK CYCLED")

        return card

    def flip(self, modifier=0, preferred_suit=None):
        if bonus is 0:
            # Do a straight flip
            return self._deal()
        else:
            # Deal the correct number of cards
            cards = []
            for i in range(0, 1+abs(modifier)):
                cards.append(self._deal())
            card_min = cards[0]
            card_max = cards[0]

            # Check for black joker, and find lowest card in preferred suit
            for card in cards:
                if card.value() is 0:
                    return card
                elif card.value() <= card_min.value() and preferred_suit is not None and card.is_suit(preferred_suit):
                    card_min = card
                elif card.value() < card_min.value():
                    card_min = card

            # Check for red joker, and find highest card in preferred suit
            for card in cards:
                if card.value() is 14:
                    return card
                elif card.value() >= card_max.value() and preferred_suit is not None and card.is_suit(preferred_suit):
                    card_min = card
                elif card.value() > card_max.value():
                    card_max = card

            # Return the appropriate card
            if modifier < 0:
                return card_min
            else:
                return card_max




deck = Deck()
for i in range(0,10):
    print(deck.flip(bonus=0))
print("+")
for i in range(0,10):
    print(deck.flip(bonus=1))
print("++")
for i in range(0,10):
    print(deck.flip(bonus=2))
print("-")
for i in range(0,10):
    print(deck.flip(bonus=-1))
print("--")
for i in range(0,10):
    print(deck.flip(bonus=-2))
