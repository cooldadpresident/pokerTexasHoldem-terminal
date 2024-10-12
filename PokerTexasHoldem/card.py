# card.py
import random
RANKS = '23456789TJQKA'
SUITS = 'CDHS' # C = Clubs, D = Diamonds, H = Hearts, S = Spades

# create 52 deck of cards
def create_deck():
    """Create and shuffle a deck of cards."""
    deck = [rank + suit for rank in RANKS for suit in SUITS]
    random.shuffle(deck)
    return deck

def deal_hand(deck, num_cards):
    """Deal a hand of cards from the deck."""
    return [deck.pop() for _ in range(num_cards)]

# Create and shuffle the deck
deck = create_deck()

# Deal two cards
hand = deal_hand(deck, 2)

# Print the dealt hand
print("Dealt hand:", hand)

