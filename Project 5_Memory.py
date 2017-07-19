# implementation of card game - Memory

import simplegui
import random

deck1 = range(0, 8)
deck2 = range(0, 8)
deck = deck1 + deck2
exposed = []
for i in range(0,16):
    i = exposed.append(False)

# helper function to initialize globals
def new_game():
    global state, turns
    random.shuffle(deck)
    for a in range(0,16):
        exposed[a] = False
    state = 0
    turns = 0
    label.set_text("Turns = 0")
    
# define event handlers
def mouseclick(pos):
    global deck, state, turns, card1, card2
    if exposed[pos[0] // 50] == True:
        pass
    else:
        exposed[pos[0] // 50] = True
        if state == 0:
            card1 = pos[0]// 50
            state = 1
        elif state == 1:
            card2 = pos[0]// 50
            turns += 1
            label.set_text("Turns = " + str(turns))
            state = 2
        else:
            if deck[card1] != deck[card2]:
                exposed[card1] = False
                exposed[card2] = False
            card1 = pos[0]// 50
            state = 1
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global exposed
    h_pos = 0
# position of the numbers
    for i in deck:
        canvas.draw_text(str(i), (12 + h_pos *50 , 70), 50, 'White')
        h_pos += 1
# to determined whether the card is face up or face down
    for e in range(16):
        if exposed[e] == True:
            canvas.draw_polygon([(e * 50 , 0),(e * 50 + 50, 0),
                                 (e * 50 + 50, 100), (e * 50, 100)], 2, 'Black')
        else:
            canvas.draw_polygon([(e * 50 , 0),(e * 50 + 50, 0),
                                 (e * 50 + 50, 100), (e * 50, 100)], 2, 'Black','Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric