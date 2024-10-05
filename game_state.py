import game_logic
import ai_enemies
import player

class GameState:
    def __init__(self):
        self.deck = game_logic.Deck()
        self.community_cards = []
        self.player_hands = []
        self.ai_hands = []
        self.betting_info = {}
        self.game_logic = game_logic.GameLogic()

    def start_game(self, num_players):
        # Deal cards to players and AI enemies
        self.player_hands = self.game_logic.deal_cards(num_players)
        self.ai_hands = self.game_logic.deal_cards(num_players)

        # Create AI enemies and player
        self.ai_enemies = [ai_enemies.AIEnemy(f"AI {i}") for i in range(num_players)]
        self.player = player.Player("Human")

        # Set up betting information
        self.betting_info = {"current_bet": 0, "pot": 0}

    def play_round(self):
        # Play a round of the game
        for enemy in self.ai_enemies:
            action = enemy.decide_action(self)
            print(f"{enemy.name} decides to {action}")

        action = self.player.decide_action(self)
        print(f"Human decides to {action}")

        # Update betting information
        self.betting_info["current_bet"] += 1
        self.betting_info["pot"] += 1
        print("Current betting information:")
        print(self.betting_info)

        # Check if the game is over
        if self.betting_info["pot"] >= 100:
            print("Game over!")
            return