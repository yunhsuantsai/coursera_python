""" 
Please feel free to leave your comment or suggestion
It will help me a lot on improving my coding skill.
Thank you very much!
"""

# Stopwatch: The Game

import simplegui
# define global variables
time = 0
x = 0
y = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    stopwatch = ""
    milliseconds = t % 10
    seconds = (t / 10) % 60
    # to make sure A:BC.D format if seconds less than 10
    if seconds < 10:
        seconds = "0" + str(seconds)
    minutes = (t / 600) % 60
    # to make sure A will not over 10:00.0
    if minutes == 10:
        timer.stop()
    return str(minutes) + ":" + str(seconds) + "." + str(milliseconds)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def button_start():
    timer.start()
    
def button_stop():
    global x, y
    if timer.is_running():
        y += 1
        if time % 10 == 0:
            x += 1
    timer.stop()

def button_reset():
    global time, x, y
    timer.stop()
    time = 0
    x = 0
    y = 0
    
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(time) , (50,130), 80, "White")
    canvas.draw_text(str(x) + " / " + str(y), (200, 40), 40, "Orange")
    
# create frame
frame = simplegui.create_frame("Stopwatch Game", 300, 200)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
button_start = frame.add_button("Start", button_start, 200)
button_stop = frame.add_button("Stop", button_stop, 200)
button_reset = frame.add_button("Reset", button_reset, 200)

# start frame
frame.start()

# Please remember to review the grading rubric
