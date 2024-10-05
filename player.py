import game_logic

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = None

    def receive_hand(self, hand):
        self.hand = hand

    def decide_action(self, game_state):
        # Handle human player input
        return "bet" if game_state.betting_info["current_bet"] < 10 else "check"
