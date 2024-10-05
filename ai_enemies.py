import game_logic

class AIEnemy:
    def __init__(self, name):
        self.name = name
        self.hand = None
        self.game_logic = game_logic.GameLogic()

    def receive_hand(self, hand):
        self.hand = hand

    def decide_action(self, game_state):
        # Simple decision-making algorithm based on hand strength
        hand_strength = self.game_logic.evaluate_hand(self.hand)  # Call evaluate_hand on the GameLogic instance
        if hand_strength > 0.5:
            return "bet"
        else:
            return "check"