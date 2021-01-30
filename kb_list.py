# libraries needed
import pyxhook
from datetime import datetime
import time
import requests
import traceback 

# global settings
RESET_READING_TIMEOUT = 1
NEXT_CARD_KEY = 13
CARD_DATA_LENGTH = 16
CARD_LENGTH = 8
STOP_KEY = 32

# global Vars
timer = datetime.now()
last_card = ''
card_id = ''
running = True
end_reading = False

# callback function when key is stroked
def kbevent(event):
    #inserting global variables in this scope
    global NEXT_CARD_KEY
    global CARD_DATA_LENGTH
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
    if len(card_id) >= CARD_DATA_LENGTH:
        end_reading = True
        last_card = card_id
        card_id = ''

    #resets timer
    timer = datetime.now()

#    except Exception as e:
#        print('INFO: Could not interpret last key ASCII code')
#        print('EXCEPTION: ', e)
#        card_id = ''
#        end_reading = True
#        timer = datetime.now()
#        return


def allow_entrance(card):
    try:
        r = requests.get('http://localhost:5000/api/v1/resources/search?badge=' + str(card))
        r_json = r.json()
        pid = r_json[0]['pid']
        print("Seu pid é: ", pid)

    except Exception as e:
        print('INFO: Request Failed')
        print('EXCEPTION: ', traceback.print_exc())
        return

    return

def filter(card_data):
    try:
        if len(card_data) != CARD_DATA_LENGTH:
            print("Dumping Reading: Read Data has Wrong Length")
            return -1
        
        card = card_data[CARD_DATA_LENGTH-CARD_LENGTH: CARD_DATA_LENGTH: 1]

        if not str.isdecimal(card):
            print("Dumping Reading: Read Data has Letters or Special Characters")
            return -2

        return int(card)

    except Exception as e:
        print('INFO: Could not Filter card from card_data')
        print('EXCEPTION: ', e)

def main():
    #inserting global 
    #' RESET_READING_TIMEOUT
    global running
    global end_reading
    global timer
    global last_card
    global card_id

    # Create hookmanager
    hookman = pyxhook.HookManager()

    # Define our callback to fire when a key is pressed down
    hookman.KeyDown = kbevent

    # Hook the keyboard
    hookman.HookKeyboard()

    # Start our listener
    hookman.start()

    # Create a loop to keep the application running
    while running:
        try:
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
            #if terminates reading flag is up, do what its suppose to do
            if end_reading:
                end_reading = False
                card = filter(last_card)
                if card >= 0:
                    allow_entrance(card)
        
        except Exception as e:
            print('INFO: API Iteration lost')
            print('EXCPETION: ', e)

    # Close the listener when we are done
    hookman.cancel()

main()