# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
win = 0
lose = 0
giveup = 0
dealer = []
player = []
deck = []
current = ""


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, num_x, suit_y, facedown):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [num_x + CARD_CENTER[0], suit_y + CARD_CENTER[1]], CARD_SIZE)
        if facedown == True:
            card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
            canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [num_x + CARD_BACK_CENTER[0], suit_y + CARD_BACK_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        return ','.join([card.get_suit()+card.get_rank() for card in self.hand])
    
    def add_card(self, card):
        self.hand.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        sum = 0
        get_ace = False
    # if have a ace in hand, change get_ace into "True" as a flag
        for card in self.hand:
            sum += VALUES.get(card.get_rank())
            if card.get_rank() == 'A':
                get_ace = True
        if get_ace and sum <= 11:
            return sum+10
        else:
            return sum
    
    def hit(self, deck):
        self.add_card(deck.deal_card())

    def busted(self):
        global busted
        sum = self.get_value()
        if sum > 21:
            return True
            
    def draw(self, canvas, suit_y, facedown):
        for card in self.hand:
            card.draw(canvas, 50+80*self.hand.index(card), suit_y, False)

# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        return ','.join([card.get_suit() + card.get_rank() for card in self.deck])        

#define event handlers for buttons
def reset():
    global outcome, in_play, win, lose, giveup, deck, dealer, player, giveup, current
    outcome = ""
    win = 0
    lose = 0
    giveup = 0
    
    deck = Deck()
    deck.shuffle()
    
    player = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    dealer = Hand()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    current = "Hit or Stand?"
    in_play = True
        
def deal():
    global outcome, win, lose, giveup, in_play, deck, dealer, player, giveup, current
    outcome = ""
    deck = Deck()
    deck.shuffle()
    
    player = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    dealer = Hand()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    current = "Hit or Stand?"
    
    if in_play:
        outcome = "You Give up."
        lose += 1
        giveup += 1

    in_play = True

def hit():
    global outcome, in_play, win, lose, giveup, current
    # if the hand is in play, hit the player
    if in_play == True:
        outcome = ""
        player.hit(deck)
    else :
        pass
    # if busted, assign a message to outcome, update in_play and score
    if player.busted():
        if in_play == True:
            outcome = 'You have busted'
            lose += 1
            current = 'Next Game?'
            in_play = False
        else:
            pass
    
def stand():
    global outcome, in_play, win, lose, giveup, current
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while dealer.get_value() < 17:
            dealer.hit(deck)
        if dealer.busted():
            outcome = "Dealer busted. You Win!"
            win += 1
            current = "One more Game?"
        if not dealer.busted():
            if dealer.get_value() > player.get_value():
                outcome = "Dealer Wins!"
                current = "Next Game?"
                lose += 1
            elif dealer.get_value() == player.get_value():
                outcome = "Dealer wins ties."
                lose += 1
                current = "Next Game?"
            else:
                outcome = "You Win!"
                win += 1
                current = "One more Game?"
    in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("      Win: "+str(win), (400, 50), 30, "Black")
    canvas.draw_text("     Lose: "+str(lose), (400, 80), 30, "Black")
    canvas.draw_text("( Give up: "+str(giveup) + " )", (430, 110), 20, "Black")
    canvas.draw_text("Blackjack", (30,80), 70, "Black")
    canvas.draw_text("Dealer", (50, 150), 26, "Black")
    canvas.draw_text("Player", (50, 300), 26, "Black")
    canvas.draw_text(outcome, (50, 500), 50, "Black")
    canvas.draw_text(current, (50, 550), 30, "Black")
    dealer.draw(canvas, 170, True)
    player.draw(canvas, 310, False)
    card = Card("S", "A")
    if in_play:
        card.draw(canvas, 50, 170, True)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Silver")

#create buttons and canvas callback
label0 = frame.add_label('')
frame.add_button("Deal / Next Game", deal, 200)
label1 = frame.add_label('')
label2 = frame.add_label('If you clicked "Deal / New Game" during the middle of a round, will count as "Give up" and "lose"')
label3 = frame.add_label('')
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)

label4 = frame.add_label('')
label5 = frame.add_label('')
label6 = frame.add_label('')
label7 = frame.add_label('')
label8 = frame.add_label('')
label9 = frame.add_label('')
label10 = frame.add_label('')

frame.add_button("Reset", reset, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric