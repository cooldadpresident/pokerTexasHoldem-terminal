class Card: # defines a new class named Card, classes are used to define custom data types
        def __init__(self, suit, rank): # initializes, this method is called when an object is created from the class and it is used to set the initial state of the object
                self.rank = rank # rank is a property of the object
        
        def __str__(self):
            return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]
