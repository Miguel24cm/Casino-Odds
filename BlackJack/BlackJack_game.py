import random

# Configuration
NUM_DECKS = 6  # Number of decks used in shoe
INITIAL_BANKROLL = 10000
MIN_CARDS_BEFORE_SHUFFLE = 120  # Threshold to stop dealing new hands


# Build a deck of cards
def build_deck(num_decks=NUM_DECKS):
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    values = {
        "A": 11,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
    }
    deck = []
    for _ in range(num_decks):
        for suit in suits:
            for rank in ranks:
                deck.append((rank + suit, values[rank]))
    random.shuffle(deck)
    return deck


# Draw a card from deck into discard pile
def draw_card(deck, discard):
    if not deck:
        deck.extend(discard)
        discard.clear()
        random.shuffle(deck)
    card = deck.pop()
    discard.append(card)
    return card


# Calculate hand score, adjust aces
def calculate_score(hand):
    total = sum(val for (_, val) in hand)
    aces = sum(1 for (rank, _) in hand if rank[0] == "A")
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total


# Display a hand
def show_hand(hand):
    return [card for (card, _) in hand]


# Bet bot
def bet_bot(deck, discard):
    running_count = 0
    for _, v in discard:
        if v >= 10:
            running_count -= 1
        elif v <= 6:
            running_count += 1
    if (running_count / (len(deck) / 52)) > 6:
        return 200
    elif (running_count / (len(deck) / 52)) > 5:
        return 100
    elif (running_count / (len(deck) / 52)) > 4:
        return 50
    elif (running_count / (len(deck) / 52)) > 3:
        return 25
    elif (running_count / (len(deck) / 52)) > 2:
        return 10
    else:
        return 5


# Bot
def bot(player, d1, m):
    score = calculate_score(player)
    if player[0][1] == player[1][1] and m == 0:
        if player[0][1] == 2 or player[0][1] == 3 or player[0][1] == 7:
            if d1 < 8:
                return "p"
            else:
                return "h"
        elif player[0][1] == 4:
            if d1 == 5 or d1 == 6:
                return "p"
            else:
                return "h"
        elif player[0][1] == 5:
            if d1 < 10:
                return "d"
            else:
                return "h"
        elif player[0][1] == 6:
            if d1 < 7:
                return "p"
            else:
                return "h"
        elif player[0][1] == 8:
            return "p"
        elif player[0][1] == 9:
            if d1 == 7 or d1 == 10 or d1 == 11:
                return "s"
            else:
                return "p"
        elif player[0][1] == 10:
            return "s"
        elif player[0][1] == 11:
            return "p"
    elif player[0][1] == 11 or player[1][1] == 11:
        if score == 13 or score == 14:
            if d1 == 5 or d1 == 6:
                return "d"
            else:
                return "h"
        elif score == 15 or score == 16:
            if d1 == 4 or d1 == 5 or d1 == 6:
                return "d"
            else:
                return "h"
        elif score == 17:
            if d1 == 3 or d1 == 4 or d1 == 5 or d1 == 6:
                return "d"
            else:
                return "h"
        elif score == 18:
            if d1 == 3 or d1 == 4 or d1 == 5 or d1 == 6:
                return "d"
            elif d1 < 9:
                return "s"
            else:
                return "h"
        else:
            return "s"
    else:
        if score < 9:
            return "d"
        elif score == 9:
            if d1 == 3 or d1 == 4 or d1 == 5 or d1 == 6:
                return "d"
            else:
                return "h"
        elif score == 10:
            if d1 < 10:
                return "d"
            else:
                return "h"
        elif score == 11:
            if d1 < 11:
                return "d"
            else:
                return "h"
        elif score == 12:
            if d1 == 4 or d1 == 5 or d1 == 6:
                return "s"
            else:
                return "h"
        elif score < 15:
            if d1 < 7:
                return "s"
            else:
                return "h"
        elif score == 15:
            if d1 < 7:
                return "s"
            elif d1 == 10:
                return "r"
            else:
                return "h"
        elif score == 16:
            if d1 < 7:
                return "s"
            elif d1 > 8:
                return "r"
            else:
                return "h"
        else:
            return "s"


# Player decision for a single hand
def play_hand(deck, discard, hand, bet, bankroll, d1, m=0):
    # Check for initial blackjack
    sp = []
    if calculate_score(hand) == 21 and len(hand) == 2:
        print("Blackjack on initial deal! Payout 3:2")
        return bet * 1.5, bankroll, sp

    # Offer options
    action = ""
    while action not in ("h", "s", "d", "r", "p"):
        action = bot(hand, d1, m)
        # action = input("Choose action: [h]it, [s]tand, [d]ouble, su[r]render, s[p]lit: ")
        # Surrender
        if action == "r":
            print("You surrendered. Lose half your bet.")
            return -bet / 2, bankroll, sp

        # Double down
        if action == "d":
            if bankroll < 2 * bet:
                print("Insufficient funds to double down.")
            else:
                bet *= 2
                hand.append(draw_card(deck, discard))
                print(
                    f"Hand after double: {show_hand(hand)} Score: {calculate_score(hand)}"
                )
                return bet, bankroll, sp

        # Split
        if action == "p" and m == 0 and hand[0][0][0] == hand[1][0][0]:
            m += 1
            print("Splitting hand.")
            hand1 = [hand[0], draw_card(deck, discard)]
            hand2 = [hand[1], draw_card(deck, discard)]
            for h in (hand1, hand2):
                print(f"Playing split hand: {show_hand(h)} Score: {calculate_score(h)}")
                res, bankroll, spsp = play_hand(
                    deck, discard, h, bet, bankroll, d1, True
                )
                sp.append((h, res))
            return bet, bankroll, sp
        # when spliting more than 2 times is multiplying or 3
        # still missing counting system

        # Hit/stand
        while action == "h":
            hand.append(draw_card(deck, discard))
            print(f"Hand: {show_hand(hand)} Score: {calculate_score(hand)}")
            if calculate_score(hand) > 21:
                return bet, bankroll, sp
            # action = input("Hit [h] or stand [s]? ")
            action = bot(hand, d1, m)
            if action == "d" or action == "r":
                action = "h"

            while action not in ("h", "s"):
                action = input("Invalid. Type h or s: ")

    # No immediate resolution; return original bet placeholder
    return bet, bankroll, sp


# Dealer plays
def dealer_play(deck, discard, hand):
    while calculate_score(hand) < 17:
        hand.append(draw_card(deck, discard))
    return calculate_score(hand)


# Who won
def winner(bankroll, dealer, hand, bet, dealer_score):
    player_score = calculate_score(hand)
    if player_score > 21:
        bankroll -= bet
        print(f"Busted!, You lose ${bet}.")
        return bankroll
    elif (
        calculate_score(hand) == 21
        and len(hand) == 2
        and dealer_score == 21
        and len(dealer) == 2
    ):
        print("Push BlackJack.")
        return bankroll
    elif (
        calculate_score(hand) == 21
        and dealer_score == 21
        and len(hand) == 2
        and len(dealer) > 2
    ):
        bankroll += bet
        print(f"You win ${bet}!")
        return bankroll
    elif (
        calculate_score(hand) == 21
        and dealer_score == 21
        and len(dealer) == 2
        and len(hand) > 2
    ):
        bankroll -= bet
        print(f"You lose ${bet}.")
        return bankroll
    elif dealer_score > 21 or player_score > dealer_score:
        bankroll += bet
        print(f"You win ${bet}!")
        return bankroll
    elif player_score < dealer_score:
        bankroll -= bet
        print(f"You lose ${bet}.")
        return bankroll
    else:
        print("Push.")
        return bankroll


# Main game flow
def blackjack():
    deck = build_deck()
    discard = []
    bankroll = INITIAL_BANKROLL
    while bankroll > 100:
        if len(deck) < MIN_CARDS_BEFORE_SHUFFLE:
            print("Not enough cards left in shoe to continue. Ending game.")
            break

        print(f"\nCurrent bankroll: ${bankroll}")

        try:
            bet = bet_bot(deck, discard)
            # bet = input("Place your bet: $")
            if bet == "n" or bet == "o":
                break
            bet = int(bet)
        except ValueError:
            print("Invalid bet.")
            continue

        if bet < 5 or bet > bankroll:
            print("Bet must be 5 or more and <= current bankroll.")
            continue

        player = [draw_card(deck, discard), draw_card(deck, discard)]
        dealer = [draw_card(deck, discard), draw_card(deck, discard)]
        print(f"Dealer shows: {dealer[0][0]}")
        print(f"Your hand: {show_hand(player)} Score: {calculate_score(player)}")

        # Offer insurance
        insurance = 0
        if dealer[0][0][0] == "A":
            if (
                False
            ):  # input("Dealer has Ace up. Take insurance? (y/n): ").lower() == 'y':
                max_ins = min(bankroll, bet // 2)
                while True:
                    try:
                        insurance = int(input(f"Insurance bet up to ${max_ins}: $"))
                        if 0 < insurance <= max_ins:
                            break
                    except ValueError:
                        pass

        # Handle dealer blackjack
        DBJ = False
        if calculate_score(dealer) == 21 and len(dealer) == 2:
            DBJ = True
            sp = []
            if insurance:
                win_ins = insurance * 2
                bankroll += win_ins
                print(f"Insurance pays ${win_ins}.")
            print("Dealer has Blackjack!")
        elif insurance:
            print(f"Insurance lost ${insurance}.")

        # Player turn(s)
        if DBJ == False:
            bet, bankroll, sp = play_hand(
                deck, discard, player, bet, bankroll, dealer[0][1], 0
            )

        # Reveal dealer
        print(f"Dealer reveals: {show_hand(dealer)} Score: {calculate_score(dealer)}")

        # Dealer draws and compare
        dealer_score = dealer_play(deck, discard, dealer)
        print(f"Dealer final: {show_hand(dealer)} Score: {dealer_score}")

        if sp == []:
            bankroll = winner(bankroll, dealer, player, bet, dealer_score)
        else:
            bankroll = winner(bankroll, dealer, sp[0][0], sp[0][1], dealer_score)
            bankroll = winner(bankroll, dealer, sp[1][0], sp[1][1], dealer_score)
            # print(sp)

    print(f"Final bankroll: ${bankroll}")
    return bankroll
    # print(deck)
    counts = {}
    for _, v in deck:
        counts[v] = counts.get(v, 0) + 1
    print("\nRemaining cards by value:")
    for val in sorted(counts):
        print(f"Value {val}: {counts[val]}")

    countsdis = {}
    for _, v in discard:
        countsdis[v] = countsdis.get(v, 0) + 1
    print("\nDiscarted cards by value:")
    for val in sorted(countsdis):
        print(f"Value {val}: {countsdis[val]}")

    running_count = 0
    for _, v in discard:
        if v >= 10:
            running_count -= 1
        elif v <= 6:
            running_count += 1
    print(f"\nCount value:{running_count}")


bank = []
games = 100
for i in range(games):
    bankr = blackjack() - INITIAL_BANKROLL
    bank.append(bankr)
# print(bank)
print(sum(bank))
