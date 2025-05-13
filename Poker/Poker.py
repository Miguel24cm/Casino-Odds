import random
from collections import Counter

suits = ["♠", "♥", "♦", "♣"]
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_values = {r: i for i, r in enumerate(ranks, start=2)}

# Card and Deck Utilities
def create_deck():
    return [f"{rank} {suit}" for suit in suits for rank in ranks]

def deal(deck, num):
    return [deck.pop() for _ in range(num)]

def card_rank(card):
    return card.split()[0]

def card_suit(card):
    return card.split()[-1]

# Poker Hand Evaluator
def evaluate_hand(hand):
    ranks = sorted([rank_values[card_rank(c)] for c in hand], reverse=True)
    suits = [card_suit(c) for c in hand]
    rank_counts = Counter(ranks)
    most_common = rank_counts.most_common()

    is_flush = len(set(suits)) == 1
    is_straight = ranks == list(range(ranks[0], ranks[0] - 5, -1))

    if ranks == [14, 5, 4, 3, 2]:  # Special case: A-2-3-4-5
        is_straight = True
        ranks = [5, 4, 3, 2, 1]

    if is_flush and is_straight:
        return (9, ranks)  # Straight flush
    if most_common[0][1] == 4:
        return (8, [most_common[0][0], most_common[1][0]])  # Four of a kind
    if most_common[0][1] == 3 and most_common[1][1] == 2:
        return (7, [most_common[0][0], most_common[1][0]])  # Full house
    if is_flush:
        return (6, ranks)
    if is_straight:
        return (5, ranks)
    if most_common[0][1] == 3:
        return (4, [most_common[0][0]] + sorted([r for r in ranks if r != most_common[0][0]], reverse=True))
    if most_common[0][1] == 2 and most_common[1][1] == 2:
        high_pair = max(most_common[0][0], most_common[1][0])
        low_pair = min(most_common[0][0], most_common[1][0])
        kicker = [r for r in ranks if r != high_pair and r != low_pair][0]
        return (3, [high_pair, low_pair, kicker])  # Two pair
    if most_common[0][1] == 2:
        return (2, [most_common[0][0]] + [r for r in ranks if r != most_common[0][0]])  # One pair
    return (1, ranks)  # High card

# Game Logic
def play_poker(num_players=2):
    if not 2 <= num_players <= 6:
        raise ValueError("Poker game supports 2 to 6 players.")

    # Setup
    deck = create_deck()
    random.shuffle(deck)
    players = [deal(deck, 2) for _ in range(num_players)]
    community = deal(deck, 5)

    print("\n=== Texas Hold'em Poker ===")
    print("Community Cards:", ", ".join(community))
    print()

    scores = []
    for i, hand in enumerate(players):
        full_hand = hand + community
        best = best_five_card_hand(full_hand)
        score = evaluate_hand(best)
        scores.append((score, i))
        print(f"Player {i+1}: {', '.join(hand)}")
        print(f"  Best Hand: {', '.join(best)}")
        print(f"  Rank: {hand_rank_name(score[0])}\n")

    # Determine Winner(s)
    scores.sort(reverse=True)
    top_score = scores[0][0]
    winners = [i for score, i in scores if score == top_score]
    
    if len(winners) == 1:
        print(f"🏆 Winner: Player {winners[0] + 1}")
    else:
        print(f"🤝 It's a tie between: " + ", ".join(f"Player {i+1}" for i in winners))

# Extract best hand out of 7 cards
from itertools import combinations
def best_five_card_hand(cards):
    return max(combinations(cards, 5), key=lambda c: evaluate_hand(list(c)))

# Human-readable hand rank
def hand_rank_name(rank):
    return [
        "High Card", "One Pair", "Two Pair", "Three of a Kind",
        "Straight", "Flush", "Full House", "Four of a Kind",
        "Straight Flush", "Royal Flush"
    ][rank - 1]

# Run the game
if __name__ == "__main__":
    play_poker(num_players=4)
