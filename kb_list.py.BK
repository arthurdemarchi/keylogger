# libraries needed
import pyxhook
from datetime import datetime
import time
import requests
import traceback 
import json

# global settings
RESET_READING_TIMEOUT = 1
NEXT_CARD_KEY = 13
CARD_DATA_LENGTH = 16
CARD_LENGTH = 8
GET_URL = "http://localhost:5000/api/v1/resources/search?badge="
POST_URL = "https://webhook.site/374dcafe-4c83-47db-8a3e-a6d81b8f0125"

# global Vars
timer = datetime.now()
card_data = ''
keyboard_stream = ''
running = True
end_reading = False

# callback function when key is stroked
def kbevent(event):
    """function that concatanates last stroked
        key into global variable keyboard_stream.
        
        Checks if keyboard_stream already has enougth
        length to be considered a card_data, in wich case
        it replaces the global variable card_data and 
        raises the end_reading flag.
    """

    try:
        #inserting global variables in this scope
        global CARD_DATA_LENGTH
        global running
        global end_reading
        global timer
        global card_data
        global keyboard_stream

        #insert key into card id
        keyboard_stream = keyboard_stream + chr(event.Ascii)

        #if card maximum length s reached terminates current reading
        if len(keyboard_stream) >= CARD_DATA_LENGTH:
            end_reading = True
            card_data = keyboard_stream
            keyboard_stream = ''

        #resets timer
        timer = datetime.now()

    #in case of exception do nothing  
    except Exception as e:
        print('INFO: Keystroke Event Failed')
        print('EXCEPTION: ', traceback.print_exc(type(e), e, e._traceback_))

# network access function
def allow_entrance(card):
    """ function that gets the employee data from 
        the url of the api, using a get, discriminate
        pid data, and post pid data to another api
        that allows the employee to enter the facilities
    """
    try:
        #get global settings
        global GET_URL
        global POST_URL

        #network communication
        r = requests.get(GET_URL + str(card))
        r = r.json()
        r = requests.post(POST_URL, json={'pid' : r['pid']})

    #in case of exception do nothing
    except Exception as e:
        print('INFO: Request Failed')
        print('EXCEPTION: ', traceback.print_exc())

#filters card_id from card_data
def filter(card_data):
    """ checks if card_data has right length
    takes the n last numbers from card_data,
    checks if all digits are numbers,
    both cases check cases return negative numbers,
    this is importarnt because all valid card_id
    are positive numbers, and returned as int.
    use this inormation to check if card was valid
    """
    try:
        #check for length
        if len(card_data) != CARD_DATA_LENGTH:
            print("Dumping Reading: Read Data has Wrong Length")
            return -1

        #takes last n digits
        card_id = card_data[CARD_DATA_LENGTH-CARD_LENGTH: CARD_DATA_LENGTH: 1]

        #check for nan characters
        if not str.isdecimal(card_id):
            print("Dumping Reading: Read Data has Letters or Special Characters")
            return -2
        
        #return card_id
        return int(card_id)


    #in case of exception do nothing
    except Exception as e:
        print('INFO: Could not Filter card from card_data')
        print('EXCEPTION: ', traceback.print_exc())
        return -3

#main function
def main():
    """ This api keeps listening to key strokes
    and tries to identfie card_id comming from them
    if a card id is identified, it posts the empolyee
    pid somerwhere else
    """

    ### INIT
    #inserting global variabes
    global running
    global end_reading
    global timer
    global card_data
    global keyboard_stream

    # Create hookmanager
    hookman = pyxhook.HookManager()

    # Define our callback to fire when a key is pressed down
    hookman.KeyDown = kbevent

    # Hook the keyboard
    hookman.HookKeyboard()

    # Start our listener
    hookman.start()

    ### BODY
    # Create a loop to keep the application running
    while running:
        try:
            #sleeps to wait for new keystroke events
            time.sleep(0.1)

            #if timer reaches timeout terminates reading
            #rhis is used as a filter for human typing
            if (datetime.now()- timer).seconds > RESET_READING_TIMEOUT:
                #if timeout is reached during a read, saves read data
                if keyboard_stream != '':
                    card_data = keyboard_stream
                    end_reading = True
                    keyboard_stream = ''

                #always resets timer
                timer = datetime.now()

            #if the end_reading flag was raised, call filter and allow entrance
            if end_reading:
                #changes flag status
                end_reading = False
                #filter card_data
                card_id = filter(card_data)
                #if filter returned a valid id, calls allow_entrance
                if card_id >= 0:
                    allow_entrance(card_id)
    
        #in case of exception do nothing
        except Exception as e:
            print('INFO: API Iteration lost')
            print('EXCEPTION: ', traceback.print_exc())

    ### CLOSING
    # Close the listener when loop is donne
    hookman.cancel()

#call main
main()