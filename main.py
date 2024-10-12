from poker_game import PokerGame

def main():
    player_names = input("Enter player names separated by commas: ").split(',')
    player_names = [name.strip() for name in player_names]
    starting_chips = int(input("Enter starting chips for each player: "))
    num_rounds = int(input("Enter number of rounds to play: "))

    game = PokerGame(player_names, starting_chips)
    game.play_game(num_rounds)

if __name__ == "__main__":
    main()