import random
from collections import Counter

# Define card ranks and suits
RANKS = '23456789TJQKA'
SUITS = 'CDHS'

# Create a deck of cards
deck = [rank + suit for rank in RANKS for suit in SUITS]

def deal_hand(deck, num_cards):
    return [deck.pop(random.randint(0, len(deck) - 1)) for _ in range(num_cards)]

def hand_rank(hand):
    """Return a value indicating the ranking of a hand."""
    ranks = sorted((RANKS.index(r) for r, s in hand), reverse=True)
    if len(set(ranks)) == 5 and (ranks[0] - ranks[4] == 4):
        return (8, ranks)  # Straight
    rank_counts = Counter(ranks)
    if 4 in rank_counts.values():
        return (7, ranks)  # Four of a kind
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        return (6, ranks)  # Full house
    if 3 in rank_counts.values():
        return (3, ranks)  # Three of a kind
    if list(rank_counts.values()).count(2) == 2:
        return (2, ranks)  # Two pair
    if 2 in rank_counts.values():
        return (1, ranks)  # One pair
    return (0, ranks)  # High card

def best_hand(hands):
    """Determine the best hand from a list of hands."""
    return max(hands, key=hand_rank)

def ai_decision(ai_hand, community_cards, ai_chips, current_bet, pot):
    """AI decision-making with a bit more risk."""
    ai_best_hand = best_hand([ai_hand + community_cards])
    rank = hand_rank(ai_best_hand)[0]
    if rank >= 6 or random.random() < 0.2:  # Full house or better, or 20% chance to bluff
        return "raise", min(ai_chips, current_bet + 10)
    elif rank >= 3 or random.random() < 0.3:  # Three of a kind or better, or 30% chance to call
        return "call", current_bet
    else:
        return "fold", 0

def player_action(player_chips, current_bet, position, pot):
    """Get the player's action."""
    print(f"\n{position}'s turn. Pot: {pot} chips.")
    while True:
        action = input("Your action (check/call/raise/fold/all-in): ").strip().lower()
        if action == "raise":
            while True:
                try:
                    amount = int(input("Enter raise amount: "))
                    if amount > player_chips:
                        print("You don't have enough chips.")
                    elif amount <= current_bet:
                        print("Raise must be higher than the current bet.")
                    else:
                        return action, amount
                except ValueError:
                    print("Please enter a valid number.")
        elif action == "all-in":
            return action, player_chips
        elif action in ["check", "call", "fold"]:
            return action, current_bet
        print("Invalid action. Please choose from check, call, raise, fold, or all-in.")

def betting_round(player_chips, ai_chips, player_hand, ai_hand, community_cards, dealer_is_player, pot, current_bet, preflop=False):
    """Handle a betting round with potential re-raises."""
    while True:
        if dealer_is_player:
            # Player acts first
            player_action_choice, player_bet = player_action(player_chips, current_bet, "Player", pot)
            if player_action_choice == "fold":
                print("You fold. AI wins!")
                ai_chips += pot
                return player_chips, ai_chips, True
            elif player_action_choice in ["raise", "all-in"]:
                pot += player_bet
                player_chips -= player_bet
                current_bet = player_bet

            print(f"\nAI's turn. Pot: {pot} chips.")
            ai_action_choice, ai_bet = ai_decision(ai_hand, community_cards, ai_chips, current_bet, pot)
            print(f"AI decides to {ai_action_choice}")
            if ai_action_choice == "fold":
                print("AI folds. You win!")
                player_chips += pot
                return player_chips, ai_chips, True
            elif ai_action_choice in ["raise", "all-in"]:
                pot += ai_bet
                ai_chips -= ai_bet
                current_bet = ai_bet
        else:
            # AI acts first
            print(f"\nAI's turn. Pot: {pot} chips.")
            ai_action_choice, ai_bet = ai_decision(ai_hand, community_cards, ai_chips, current_bet, pot)
            print(f"AI decides to {ai_action_choice}")
            if ai_action_choice == "fold":
                print("AI folds. You win!")
                player_chips += pot
                return player_chips, ai_chips, True
            elif ai_action_choice in ["raise", "all-in"]:
                pot += ai_bet
                ai_chips -= ai_bet
                current_bet = ai_bet

            player_action_choice, player_bet = player_action(player_chips, current_bet, "Player", pot)
            if player_action_choice == "fold":
                print("You fold. AI wins!")
                ai_chips += pot
                return player_chips, ai_chips, True
            elif player_action_choice in ["raise", "all-in"]:
                pot += player_bet
                player_chips -= player_bet
                current_bet = player_bet

        # If both players have called or checked, end the betting round
        if player_action_choice in ["check", "call"] and ai_action_choice in ["check", "call"]:
            break

        # Ensure preflop round doesn't end until the small blind has called or folded
        if preflop and (player_action_choice == "check" or ai_action_choice == "check"):
            continue

    return player_chips, ai_chips, False

def play_round(player_chips, ai_chips, dealer_is_player):
    random.shuffle(deck)
    player_hand = deal_hand(deck, 2)
    ai_hand = deal_hand(deck, 2)

    print(f"Your hand: {player_hand}")
    print(f"Your chips: {player_chips}, AI chips: {ai_chips}")

    # Determine blinds
    if dealer_is_player:
        small_blind = 1
        big_blind = 2
        print("\nSmall Blind: Player, Big Blind: AI")
    else:
        small_blind = 2
        big_blind = 1
        print("\nSmall Blind: AI, Big Blind: Player")

    pot = 0
    player_chips -= small_blind if dealer_is_player else big_blind
    ai_chips -= big_blind if dealer_is_player else small_blind
    pot += small_blind + big_blind
    current_bet = big_blind

    # Preflop
    player_chips, ai_chips, round_over = betting_round(player_chips, ai_chips, player_hand, ai_hand, [], dealer_is_player, pot, current_bet, preflop=True)
    if round_over:
        return player_chips, ai_chips

    # Flop
    community_cards = deal_hand(deck, 3)
    print(f"\n--- Flop ---")
    print(f"Community cards: {community_cards}")
    print(f"Your chips: {player_chips}, AI chips: {ai_chips}")

    player_chips, ai_chips, round_over = betting_round(player_chips, ai_chips, player_hand, ai_hand, community_cards, dealer_is_player, pot, current_bet)
    if round_over:
        return player_chips, ai_chips

    # Turn
    community_cards += deal_hand(deck, 1)
    print(f"\n--- Turn ---")
    print(f"Community cards: {community_cards}")
    print(f"Your chips: {player_chips}, AI chips: {ai_chips}")

    player_chips, ai_chips, round_over = betting_round(player_chips, ai_chips, player_hand, ai_hand, community_cards, dealer_is_player, pot, current_bet)
    if round_over:
        return player_chips, ai_chips

    # River
    community_cards += deal_hand(deck, 1)
    print(f"\n--- River ---")
    print(f"Community cards: {community_cards}")
    print(f"Your chips: {player_chips}, AI chips: {ai_chips}")

    player_chips, ai_chips, round_over = betting_round(player_chips, ai_chips, player_hand, ai_hand, community_cards, dealer_is_player, pot, current_bet)
    if round_over:
        return player_chips, ai_chips

    # Showdown
    print("\n--- Showdown ---")
    player_best_hand = best_hand([player_hand + community_cards])
    ai_best_hand = best_hand([ai_hand + community_cards])

    print(f"Your best hand: {player_best_hand} ({hand_rank(player_best_hand)})")
    print(f"AI's best hand: {ai_best_hand} ({hand_rank(ai_best_hand)})")

    if hand_rank(player_best_hand) > hand_rank(ai_best_hand):
        print("You win the pot of", pot, "chips!")
        player_chips += pot
    elif hand_rank(player_best_hand) < hand_rank(ai_best_hand):
        print("AI wins the pot of", pot, "chips!")
        ai_chips += pot
    else:
        print("It's a tie! The pot is split.")
        player_chips += pot // 2
        ai_chips += pot // 2

    print(f"Your chips: {player_chips}")
    print(f"AI chips: {ai_chips}")
    return player_chips, ai_chips

def play_game():
    player_chips = 500
    ai_chips = 500
    dealer_is_player = True

    while player_chips > 0 and ai_chips > 0:
        player_chips, ai_chips = play_round(player_chips, ai_chips, dealer_is_player)
        # Swap dealer
        dealer_is_player = not dealer_is_player

    if player_chips <= 0:
        print("You are out of chips. AI wins the game!")
    elif ai_chips <= 0:
        print("AI is out of chips. You win the game!")

if __name__ == "__main__":
    play_game()