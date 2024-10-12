from card_representation import Deck, Card

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []

    def bet(self, amount):
        if amount <= self.chips:
            self.chips -= amount
            return amount
        return 0

    def __str__(self):
        return f"{self.name} (Chips: {self.chips})"

class PokerGame:
    def __init__(self, player_names, starting_chips):
        self.deck = Deck()
        self.players = [Player(name, starting_chips) for name in player_names]
        self.pot = 0
        self.community_cards = []

    def start_round(self):
        self.deck.shuffle()
        self.pot = 0
        self.community_cards = []
        for player in self.players:
            player.hand = self.deck.deal(2)

    def betting_round(self):
        for player in self.players:
            print(f"\n{player.name}'s turn:")
            print(f"Your hand: {', '.join(str(card) for card in player.hand)}")
            bet = int(input(f"Enter your bet (0 to fold, current chips: {player.chips}): "))
            if bet > 0:
                actual_bet = player.bet(bet)
                self.pot += actual_bet
                print(f"{player.name} bets {actual_bet}")
            else:
                print(f"{player.name} folds")
                self.players.remove(player)

    def deal_community_cards(self, num_cards):
        new_cards = self.deck.deal(num_cards)
        if new_cards:
            self.community_cards.extend(new_cards)
            print(f"Community cards: {', '.join(str(card) for card in self.community_cards)}")

    def play_round(self):
        self.start_round()
        print("Initial deal:")
        self.betting_round()

        self.deal_community_cards(3)  # Flop
        self.betting_round()

        self.deal_community_cards(1)  # Turn
        self.betting_round()

        self.deal_community_cards(1)  # River
        self.betting_round()

        self.determine_winner()

    def determine_winner(self):
        # This is a simplified version. In a real poker game, you'd implement proper hand evaluation.
        if len(self.players) == 1:
            winner = self.players[0]
        else:
            winner = max(self.players, key=lambda p: p.hand[0].rank)
        
        winner.chips += self.pot
        print(f"\n{winner.name} wins the pot of {self.pot}!")

    def play_game(self, num_rounds):
        for round in range(num_rounds):
            print(f"\n--- Round {round + 1} ---")
            self.play_round()
            print("\nCurrent standings:")
            for player in self.players:
                print(player)
