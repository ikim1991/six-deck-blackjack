import random
import math

class Deck():

    #52 Cards in a deck
    def __init__(self, deck=[2,3,4,5,6,7,8,9,10,'J','Q','K','A']*4):
        self.deck = deck

    #Algorithm for randomly shuffling a deck
    def shuffle_deck(self):
        for i, n in enumerate(self.deck):
            x = math.floor(random.uniform(0,1)*len(self.deck))
            tmp = self.deck[i]
            self.deck[i] = self.deck[x]
            self.deck[x] = tmp

class Dealer():
    def __init__(self, hand=[0],count=0):
        self.hand = hand
        self.count = count

class Player():

    bank = 1000000

    def __init__(self, hand=[0,0], count=0):
        self.hand = hand
        self.count = count

def start_game():

    while True:
        game_start = input('Welcome to Six Deck Black Jack: Would you like to Start? (Start(Y) / Exit(N))\t')
        print('\n')
        if game_start == 'y' or game_start == 'Y':

            # Shuffle Deck
            shuffle_check()
            # Create player
            global player
            player = Player()
            # Create Dealer
            global dealer
            dealer = Dealer()
            break
        elif game_start == 'n' or game_start == 'N':
            break
        else:
            print('Come again?')
            game_start = input('Welcome to Six Deck Black Jack: Would you like to Start? (Type Y to Start)\t')
            print('\n')
            continue

def shuffle_check():
    # Creates 6 Decks
    d1 = Deck()
    d2 = Deck()
    d3 = Deck()
    d4 = Deck()
    d5 = Deck()
    d6 = Deck()
    # Shuffles 6 Decks
    d1.shuffle_deck()
    d2.shuffle_deck()
    d3.shuffle_deck()
    d4.shuffle_deck()
    d5.shuffle_deck()
    d6.shuffle_deck()
    global master_deck
    # Create 1 Master Deck from the randomized 6 Decks
    master_deck = d1.deck + d2.deck + d3.deck + d4.deck + d5.deck + d6.deck

def place_bet():
    while True:
        print(f'You have {player.bank} to Bet')
        try:
            global ante
            ante = int(input('Place Your Bet\t'))
            print('\n')
            if int(ante) > player.bank:
                print('Insufficient Funds\n')
            elif int(ante) >= 0:
                player.bank -= ante
                print(f'Amount Placed: {ante}\nAmount in Bank: {player.bank}\n')
                break
            else:
                print('Input Amount\n')
        except:
            print('Input Integer Value\n')

def deal_hand():
    # Player is dealt 2 cards from the Master Deck
    for i,n in enumerate(player.hand):
        player.hand[i] = master_deck.pop()
    # Dealer is dealt one card showing from the Master Deck
    dealer.hand[0] = master_deck.pop()
    # Checks for a Face Card and assigns it the appropriate card value
    if 'J' not in player.hand and 'Q' not in player.hand and 'K' not in player.hand and 'A' not in player.hand:
        player.count = sum(player.hand)
    else:
        # Loops through the hand and assigns the appropriate hand count
        for card in player.hand:
            if type(card) == int:
                player.count += card
            elif card == 'A' and player.count == 11:
                player.count += 1
            elif card == 'A':
                player.count += 11
            else:
                player.count += 10

# Algorithm for assigning the optimal value of an Ace, as it can either be a 1 or an 11
def high_or_low(check):
    tmp = 0
    aces = 0
    for card in check.hand:
        if card == 'A':
            tmp += 11
            aces += 1
        elif type(card) == str:
            tmp += 10
        else:
            tmp += card
        check.count = tmp
        while tmp > 21 and aces != 0:
            tmp -= 10
            aces -= 1
            if tmp > 21 and aces != 0:
                continue
            else:
                check.count = tmp
                break

# Checks hand based on the card dealt and reassigns a hand value accordingly
def check_hand(take_card):
    if type(take_card) == int:
        player.count += take_card
        if 'A' in player.hand:
            high_or_low(player)
    else:
        if take_card == 'A':
            high_or_low(player)
        else:
            player.count +=10
            if 'A' in player.hand:
                high_or_low(player)

def player_action():
    while True:
        print(f'You have: {player.hand} {player.count}\nThe Dealer is Showing for: {dealer.hand}\n')
        decision = input('What Would You Like to Do? Hit(H) or Stay(S)?\t')
        print('\n')

        #Player Hits a new card and the hand value is reevaluated
        if decision == 'h' or decision == 'H':
            new_card = master_deck.pop()
            player.hand.append(new_card)
            check_hand(new_card)
            # If a player hits 21 but not a blackjack, it automatically Stays and becomes the dealer's turn
            if player.count == 21:
                print(f'You have: {player.hand} {player.count}\nThe Dealer is Showing for: {dealer.hand}\n')
                break
            # If the hand count is less than 21, the player has the option to hit or stay again
            elif player.count < 21:
                continue
            else:
                break
        # Once the player decides to stay, it will be the dealer's turn
        elif decision == 's' or decision == 'S':
                break

def dealer_draw():
    # The dealer will loop and hit until it achieves a hand greater than or equal to 17
    while True:
        # The first hit
        if len(dealer.hand) == 1:
            new_card = master_deck.pop()
            print(f'Dealer Hits! {new_card}')
            dealer.hand.append(new_card)
            for card in dealer.hand:
                if type(card) == int:
                    dealer.count += card
                elif card == 'A' and dealer.count == 11:
                    dealer.count += 1
                elif card == 'A':
                    dealer.count += 11
                else:
                    dealer.count += 10
            if dealer.count == 21:
                check_win()
                break
        # If the dealer does not have a hand greater than or equal to 17 after the first hit, the dealer will hit again
        if dealer.count < 17:
            new_card = master_deck.pop()
            dealer.hand.append(new_card)
            print(f'Dealer Hits! {new_card}')

            if type(new_card) == int:
                dealer.count += new_card
                if 'A' in dealer.hand:
                    high_or_low(dealer)
            else:
                if new_card == 'A':
                    high_or_low(dealer)
                else:
                    dealer.count += 10
                    if 'A' in dealer.hand:
                        high_or_low(dealer)
        # If the dealer realizes a hand between 17 and 21, the loop will break and the winner or loser will be decided
        if dealer.count >= 17 and dealer.count <= 21:
            check_win()
            break
        elif dealer.count < 17:
            continue
        # If the dealer has a hand over 21, the loop will break and the dealer will bust
        else:
            check_win()
            break

# All possible scenario of win/lose conditions are defined below
def check_win():
    global player_wins
    # Dealer hits a Blackjack
    if dealer.count == 21 and len(dealer.hand) == 2:
        player_wins = False
        print(f'You have: {player.hand} {player.count}\nThe Dealer is Showing for: {dealer.hand} {dealer.count}')
        print('Dealer has Blackjack!\nThe House Always Wins!\n')
    # Player hits a Blackjack
    elif player.count == 21 and len(player.hand) == 2:
        player_wins = 'blackjack'
        print(f'You have: {player.hand} {player.count}\nThe Dealer is Showing for: {dealer.hand}')
        print('Blackjack! Player Wins Hand!\n')
    # Player Bust
    elif player.count > 21:
        player_wins = False
        print(f'You have: {player.hand} {player.count}\nThe Dealer is Showing for: {dealer.hand}')
        print('Player Bust!\nThe House Always Wins!\n')
    # Dealer Bust
    elif dealer.count > 21:
        player_wins = True
        print(f'You have: {player.hand} {player.count}\nThe Dealer is Showing for: {dealer.hand} {dealer.count}')
        print('Dealer Bust!\nWinner, Winner Chicken Dinner!\n')
    else:
        # Dealer's hand beats the Player's hand
        if dealer.count > player.count:
            player_wins = False
            print(f'You have: {player.hand} {player.count}\nThe Dealer is Showing for: {dealer.hand} {dealer.count}')
            print('The House Always Wins!\n')
        # Player's hand beats the Dealer's hand
        elif player.count > dealer.count:
            player_wins = True
            print(f'You have: {player.hand} {player.count}\nThe Dealer is Showing for: {dealer.hand} {dealer.count}')
            print('Winner, Winner Chicken Dinner!\n')
        # Push, Player and Dealer hands tie
        elif player.count == dealer.count:
            player_wins = None
            print(f'You have: {player.hand} {player.count}\nThe Dealer is Showing for: {dealer.hand} {dealer.count}')
            print('Push!\n')
    results(player_wins)
    reset_hand()

def results(result):
    # Player Wins and paid out
    if result == True:
        player.bank = player.bank + (ante * 2)
    # Player hits Blackjack, 3/2 odds
    elif result == 'blackjack':
        player.bank = player.bank + int(ante * 1.5) + ante
    # Player loses, loses bet placed
    elif result == False:
        pass
    # Push balance stays the same
    else:
        player.bank = player.bank + ante

def reset_hand():
    player.count = 0
    dealer.count = 0
    player.hand = [0,0]
    dealer.hand = [0]
    player_wins = None

# Flow and Gameplay
def start_up():
    # Prompts user to start game
    start_game()
    while True:
        #Prompts user to place bet
        place_bet()
        # Deals first hand
        deal_hand()
        # Checks for Blackjack
        if len(player.hand) == 2 and player.count == 21:
            check_win()
        # Else prompts for player action (Hit or Stay)
        else:
            player_action()
            if player.count > 21:
                check_win()
            else:
                dealer_draw()

        while True:
            # Shuffle Check. The Master Deck is reshuffled after half of the cards have been dealt
            if len(master_deck) <= 156:
                shuffle_check()
                print('Shuffle Check')
            # Prompts user to play or exit the game
            play_again = input('Would You Like to Play Another Hand? Continue(Y) / Exit(N)')
            if play_again == 'y' or play_again == 'Y':
                if player.bank == 0:
                    print('You Do Not Have Enough Minerals! Exiting')
                    break
                break
            elif play_again == 'n' or play_again == 'N':
                break
            else:
                print('Input Response')
        # If player does not have enough funds, the game will exit
        if player.bank == 0:
            break
        if play_again == 'y' or play_again == 'Y':
            continue
        if play_again == 'n' or play_again == 'N':
            break
                   
# The program will automatically start when run on the terminal
if __name__ == '__main__':
	start_up()
