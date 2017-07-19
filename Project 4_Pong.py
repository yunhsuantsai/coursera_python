# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0,0]
paddle1_pos = 150
paddle2_pos = 150
paddle1_vel = 0.0
paddle2_vel = 0.0
player1_score = 0
player2_score = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = - random.randrange(1, 2)
    if direction == LEFT:
        ball_vel[0] = - random.randrange(2, 4)
        ball_vel[1] = - random.randrange(1, 2)  
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global player1_score, player2_score  # these are ints
    paddle1_pos = 150
    paddle2_pos = 150
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    player1_score = 0
    player2_score = 0
    
    spawn_ball(RIGHT)  
    
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global player1_score, player2_score
    
    # draw scores
    canvas.draw_text(str(player1_score), (125,350), 100, "Gray")
    canvas.draw_text(str(player2_score), (425,350), 100, "Gray")          
    canvas.draw_text("Pong", (195,100), 100, "Gray")
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]      
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'Red', 'White')  

    # update paddle's vertical position, keep paddle on the screen    
    if paddle1_pos > 0:
        paddle1_pos += paddle1_vel
    else:
        paddle1_pos = 0.1
    if paddle1_pos < 400 - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    else: 
        paddle1_pos = 400 - PAD_HEIGHT - 0.1
    if paddle2_pos >= 0:
        paddle2_pos += paddle2_vel
    else:
        paddle2_pos = 0.1
    if paddle2_pos < 400 - PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    else:
        paddle2_pos = 400 - PAD_HEIGHT - 0.1
    
    # draw paddles
    canvas.draw_line([6, paddle1_pos], [6, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, "Aqua")
    canvas.draw_line([594, paddle2_pos], [594, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, "Lime")

    # determine whether paddle and ball collide    
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
            ball_vel[0] = - (ball_vel[0] * 1.1)
        else:        
            player2_score += 1
            spawn_ball(RIGHT)
    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
            ball_vel[0] = - (ball_vel[0] * 1.1)
        else:
            player1_score += 1
            spawn_ball(LEFT)

    # set upper and bottom wall
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -5
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 5
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
Restart_button = frame.add_button("Restart", new_game, 200)
label1 = frame.add_label("")
label2 = frame.add_label("How to Control:")
label3 = frame.add_label("Player 1: 'w' & 's'")
label4 = frame.add_label("Player 2: Arrow 'up' & 'down'")
label5 = frame.add_label("")
label6 = frame.add_label("Hope you like it. :)")

# start frame
new_game()
frame.start()
