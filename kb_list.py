# libraries needed
import pyxhook
from datetime import datetime
import time

# global settings
RESET_READING_TIMEOUT = 1
NEXT_CARD_KEY = 13
NEXT_CARD_LENGTH = 16
STOP_KEY = 32
running = True
end_reading = False

# initiates timer
timer = datetime.now()
last_card = ''
card_id = ''

# callback function when key is stroked
def kbevent(event):
    #inserting global variables in this scope
    global NEXT_CARD_KEY
    global NEXT_CARD_LENGTH
    global STOP_KEY
    global running
    global end_reading
    global timer
    global last_card
    global card_id

    #insert key into card id
    card_id = card_id + chr(event.Ascii)

    #if stop key is pressed stop process
    if event.Ascii == STOP_KEY:
        running = False

    #if end of reading key is stroked terminates current reading
    if event.Ascii == NEXT_CARD_KEY:
        end_reading = True
        last_card = card_id
        card_id = ''

    #if card maximum length s reached terminates current reading
    if len(card_id) >= NEXT_CARD_LENGTH:
        end_reading = True
        last_card = card_id
        card_id = ''
    
    #resets timer
    timer = datetime.now()

def listener_init():
    # Create hookmanager
    hookman = pyxhook.HookManager()

    # Define our callback to fire when a key is pressed down
    hookman.KeyDown = kbevent

    # Hook the keyboard
    hookman.HookKeyboard()

    # Start our listener
    hookman.start()

def main():
    #inserting global variables in this scope
    global RESET_READING_TIMEOUT
    global running
    global end_reading
    global timer
    global last_card
    global card_id

    #initializes keylogger
    listener_init()

    # Create a loop to keep the application running
    while running:
        #sleeps
        time.sleep(0.1)

        #if timer reaches timeout terminates reading
        if (datetime.now()- timer).seconds > RESET_READING_TIMEOUT:
            #if timeout is reached during a read, saves read data
            if card_id != '':
                last_card = card_id
                end_reading = True
                card_id = ''

            #resets timer
            timer = datetime.now()
        
        #if terminates reading flag is up, do what its suppose todo
        if end_reading:
            print('Fazer alguma coisa com:', last_card)
            end_reading = False

    # Close the listener when we are done
    hookman.cancel()

main()