import game_state

def main():
    game = game_state.GameState()
    game.start_game(2)
    while True:
        game.play_round()

if __name__ == "__main__":
    main()