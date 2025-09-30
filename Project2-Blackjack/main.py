import random
suits = ('Hearts', 'Clubs', 'Spades', 'Diamonds')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
playing  = True

class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    
    def __init__(self):
        self.deck = [] 
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        return "\n".join(str(card) for card in self.deck)
        
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        card = self.deck.pop()
        return card
    
class Hand:
    def __init__(self):
        self.cards = []  
        self.value = 0 
        self.aces = 0   
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        if card.rank == 'Ace':
            self.aces+=1
        self.adjust_for_ace()
    
    def adjust_for_ace(self):
        while self.aces and self.value>21:
            self.value -= 10
            self.aces -= 1
            
class Chips:
    
    def __init__(self):
        self.total = 100  
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -=self.bet
        
def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Enter valid amount')
        else:
            if chips.bet > chips.total:
                print("Bet Exceeded",chips.total)
            else:
                break

def hit(deck,hand):
    card = deck.deal()
    hand.add_card(card)
    hand.adjust_for_ace()
    
def hit_or_stand(deck,hand):
    global playing 
    
    while True:
        i = input("Do you want to Hit or Stand? say 'h' (hit) or 's'(stand)")
        if i[0].lower()=='h':
            hit(deck, hand)
        elif i[0].lower()=='s':
            print("Dealer is playing. Player Stands")
            playing =False
        else:
            print("Sorry please enter valid input")
            continue
        break
            
def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <hidden card>")          
    print("", dealer.cards[1])         

    print("\nPlayer's Hand:")
    for card in player.cards:
        print("", card)
    print("Value =", player.value)


def show_all(player, dealer):
    print("\nDealer's Hand:")
    for card in dealer.cards:
        print("", card)
    print("Dealer's Hand =", dealer.value)

    print("\nPlayer's Hand:")
    for card in player.cards:
        print("", card)
    print("Player's Hand =", player.value)
    
def player_busts(player, dealer, chips):
    print("\n Player busts! Dealer wins.")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("\n Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("\n Dealer busts! Player wins.")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("\n Dealer wins.")
    chips.lose_bet()

def push(player, dealer):
    print("\n Push (tie). No one wins or loses chips.")

while True:
    
    print("Welcome to Blackjack! Get as close to 21 as you can without going over!\n" "Dealer hits until reaching 17. Aces count as 1 or 11.\n")
    
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
        
    
    player_chips = Chips()


    while True:
        try:
            player_chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Sorry, please provide an integer.")
        else:
            if player_chips.bet > player_chips.total:
                print(f"Sorry, your bet can't exceed {player_chips.total}")
            else:
                break
            
    show_some(player_hand, dealer_hand)
    
    while playing:
        
        hit_or_stand(deck, player_hand)
        
        show_some(player_hand, dealer_hand)
        
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            dealer_hand.add_card(deck.deal())
            
        show_all(player_hand, dealer_hand)
    
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

     
    print(f"\nPlayer's total chips are at: {player_chips.total}")
    
    new_game = input("Would you like to play another hand? (y/n): ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing Blackjack!")
        break