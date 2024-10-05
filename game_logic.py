import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

        for suit in self.suits:
            for value in self.values:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]

class GameLogic:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

    def deal_cards(self, num_players):
        return [self.deck.deal(2) for _ in range(num_players)]

    def flop(self):
        return self.deck.deal(3)

    def turn(self):
        return self.deck.deal(1)

    def river(self):
        return self.deck.deal(1)

    def evaluate_hand(self, hand):
        # Simple hand evaluation logic
        return len(set([card.value for card in hand]))
