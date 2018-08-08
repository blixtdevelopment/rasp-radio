#!/usr/bin/python
import subprocess
import time
import httplib
import os
import sys
import socket
import RPi.GPIO as GPIO
from collections import OrderedDict, defaultdict

# Setup GPIO and global variables
GPIO.setmode(GPIO.BCM)
BOUNCE_TIME = 900
CHNL_CURRENT = None
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
radio_process = None

# Initialise channels GPIO input
# Could be made into an enum
CHNL_INPUT_DICT = {"CHNL_ANR": 5,
                   "CHNL_RADIO_SOFT": 6,
                   "CHNL_P3": 13,
                   "CHNL_NORDJYSKE": 19,
                   "CHNL_NOVA": 26,
                   "CHNL_ABC": 16}
GPIO.setup(CHNL_INPUT_DICT.values(), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Create the ordered dictionary, such that the radio number will be consistent
RADIO_DICT = OrderedDict()
RADIO_DICT["ANR"] = 'http://stream.anr.dk/anr'
RADIO_DICT["RADIO_SOFT"] = 'http://onair.100fmlive.dk/soft_live.mp3'  # 'http://edge-bauerdk-03-gos2.sharp-stream.com/radiosoft_dk_mp3'
RADIO_DICT["P3"] = 'http://live-icy.gss.dr.dk/A/A05H.mp3'
RADIO_DICT["NORDJYSKE"] = 'http://stream.anr.dk/nordjyske'
RADIO_DICT["NOVA"] = 'http://stream.novafm.dk/nova128'  # 'http://edge-bauerdk-02-gos1.sharp-stream.com/nova_dk_mp3'
RADIO_DICT["ABC"] = 'http://89.249.7.68/abc'


def is_connected():
    hostname = 'www.google.com'
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


# Deprecated because of instability --> use id_connected()
def internet_on():
    conn = httplib.HTTPConnection("www.google.com")
    try:
        conn.request("HEAD", "/")
        return True
    except httplib.HTTPException:
        return False
    

# Add all of the channels listed in RADIO_DICT
def add_player():
    global radio_process
    print("Initialising radio channels")

    if radio_process != None:
        print("radio_process already exist; terminating the process and restarting...")
        radio_process.terminate()

    subprocess.Popen(["/usr/bin/mpc", "clear"])
    time.sleep(0.05)
    _error_adding_channels = False
    for radio, url in RADIO_DICT.iteritems():
        try:
            print("Adding channel: " + radio + " --- at url: " + url)
            subprocess.Popen(["/usr/bin/mpc", "add", url])
            time.sleep(0.1)
        except Exception as er:
            print("Unable to add channel " + radio + " --- at url: " + url)
            print("Error: " + str(er))
            _error_adding_channels = True
    if not _error_adding_channels:
        print("\nAll channels added to mpc!")
        print("The playlist is:")
        subprocess.Popen(["/usr/bin/mpc", "playlist"])
    else:
        print("Not all channels was added successfully...")
        print("Retrying!")
        time.sleep(2)
        add_player()

# Find out which pin input is active on boot
def init_current_channel():
    for channel in CHNL_INPUT_DICT.values():
        if GPIO.input(channel):
            channel_selection(channel)
            return
    # If no channel is active
    anr()


# The following functions is each radio station, were the following happens:
#       Stop the current played channel
#       Play the new channel
#       Update the global variable, keeping track of which channel is currently active.
# TODO: Could potentially be made into its own class for "better programming ethics"
def anr():
    global radio_process, CHNL_CURRENT
    print("\nPlaying ANR!")
    try:
        radio_process = subprocess.Popen(["/usr/bin/mpc", "stop"])
        #subprocess.call(["/usr/bin/aplay", CURRENT_DIR + "/channel_name/anr.wav"])
        time.sleep(0.1)
        radio_process = subprocess.Popen(["/usr/bin/mpc", "play", str(RADIO_DICT.keys().index("ANR") + 1)])
        CHNL_CURRENT = CHNL_INPUT_DICT["CHNL_ANR"]
    except Exception as er:
        print("Error in playing ANR; error: " + str(er))
        time.sleep(2)
        anr()


def radio_soft():
    global radio_process, CHNL_CURRENT
    try:
        print("\nPlaying Radio Soft!")
        radio_process = subprocess.Popen(["/usr/bin/mpc", "stop"])
        #subprocess.call(["/usr/bin/aplay", CURRENT_DIR + "/channel_name/radio_soft.wav"])
        time.sleep(0.1)
        radio_process = subprocess.Popen(["/usr/bin/mpc", "play", str(RADIO_DICT.keys().index("RADIO_SOFT") + 1)])
        CHNL_CURRENT = CHNL_INPUT_DICT["CHNL_RADIO_SOFT"]
    except Exception as er:
        print("Error in playing Radio Soft; error: " + str(er))
        time.sleep(2)
        radio_soft()


def p3():
    global radio_process, CHNL_CURRENT
    try:
        print("\nPlaying P3!")
        radio_process = subprocess.Popen(["/usr/bin/mpc", "stop"])
        #subprocess.call(["/usr/bin/aplay", CURRENT_DIR + "/channel_name/p3.wav"])
        time.sleep(0.1)
        radio_process = subprocess.Popen(["/usr/bin/mpc", "play", str(RADIO_DICT.keys().index("P3") + 1)])
        CHNL_CURRENT = CHNL_INPUT_DICT["CHNL_P3"]
    except Exception as er:
        print("Error in playing P3; error: " + str(er))
        time.sleep(2)
        p3()


def nordjyske():
    global radio_process, CHNL_CURRENT
    try:
        print("\nPlaying Nordjyske!")
        radio_process = subprocess.Popen(["/usr/bin/mpc", "stop"])
        #subprocess.call(["/usr/bin/aplay", CURRENT_DIR + "/channel_name/nordjyske.wav"])
        time.sleep(0.1)
        radio_process = subprocess.Popen(["/usr/bin/mpc", "play", str(RADIO_DICT.keys().index("NORDJYSKE") + 1)])
        CHNL_CURRENT = CHNL_INPUT_DICT["CHNL_NORDJYSKE"]
    except Exception as er:
        print("Error in playing Nordjyske; error: " + str(er))
        time.sleep(2)
        nordjyske()


def nova():
    global radio_process, CHNL_CURRENT
    try:
        print("\nPlaying NOVA!")
        radio_process = subprocess.Popen(["/usr/bin/mpc", "stop"])
        #subprocess.call(["/usr/bin/aplay", CURRENT_DIR + "/channel_name/nova.wav"])
        time.sleep(0.1)
        radio_process = subprocess.Popen(["/usr/bin/mpc", "play", str(RADIO_DICT.keys().index("NOVA") + 1)])
        CHNL_CURRENT = CHNL_INPUT_DICT["CHNL_NOVA"]
    except Exception as er:
        print("Error in playing Nova; error: " + str(er))
        time.sleep(2)
        nova()


def abc():
    global radio_process, CHNL_CURRENT
    try:
        print("\nPlaying ABC!")
        radio_process = subprocess.Popen(["/usr/bin/mpc", "stop"])
        #subprocess.call(["/usr/bin/aplay", CURRENT_DIR + "/channel_name/abc.wav"])
        time.sleep(0.1)
        radio_process = subprocess.Popen(["/usr/bin/mpc", "play", str(RADIO_DICT.keys().index("ABC") + 1)])
        CHNL_CURRENT = CHNL_INPUT_DICT["CHNL_ABC"]
    except Exception as er:
        print("Error in playing ABC; error: " + str(er))
        time.sleep(2)
        abc()


# Select the channel bassed on channel number (i.e. GPIO Pin number)
def channel_selection(_chnl_number):
    try:
        _chnl = CHNL_INPUT_DICT.keys()[CHNL_INPUT_DICT.values().index(_chnl_number)]
        if _chnl == "CHNL_ANR":
            anr()
        elif _chnl == "CHNL_RADIO_SOFT":
            radio_soft()
        elif _chnl == "CHNL_P3":
            p3()
        elif _chnl == "CHNL_NORDJYSKE":
            nordjyske()
        elif _chnl == "CHNL_NOVA":
            nova()
        elif _chnl == "CHNL_ABC":
            abc()
        else:  # Default if other fails
            print("Unknown channel number in channel selection, selecting default (anr)!")
            anr()
    except ValueError as ve:
        print("Error in channel selection (using ANR), error: " + str(ve))
        anr()


# Handle the interrupt by the pin number (channel)
def callback(channel):
    if GPIO.input(channel):     # if the pin is active (The probably the channel is correct)
        channel_read = 0
        for i in range(5):      # If the pin is active  > 3  then it must be correct
            if GPIO.input(channel):
                channel_read += 1
            time.sleep(0.01)
        if channel_read < 3:
            return
        if CHNL_CURRENT != channel:     # Check if the channel is already active
            print("Channel is: " + str(channel))
            channel_selection(channel)
    else:
        _channel_list = []
        _value_list = []
        for i in range(5):      # The pin is not active, however it might still be the right channel.
            for _channel in CHNL_INPUT_DICT.values():   # Therefore check all pin inputs
                _channel_list.append(_channel)
                _value_list.append(GPIO.input(_channel))
            time.sleep(0.01)

        _channel_value = zip(_channel_list, _value_list)
        dd = defaultdict(int)

        for _channel, _state in _channel_value:
            if _state == 1:                     # Only store pins that were active
                dd[_channel] += 1

        max_occurrence = max(dd.iteritems(), key=lambda x: x[1])
        if max_occurrence[1] < 3:               # If one pin were active more > 3 then select that pin
            return
        if CHNL_CURRENT != max_occurrence[0]:   # Check if the channel is already active
            print("Channel is: " + str(max_occurrence[0]))
            channel_selection(max_occurrence[0])


# Initialise the interrupts
GPIO.add_event_detect(5, GPIO.RISING, callback=callback, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(6, GPIO.RISING, callback=callback, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(13, GPIO.RISING, callback=callback, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(19, GPIO.RISING, callback=callback, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(26, GPIO.RISING, callback=callback, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(16, GPIO.RISING, callback=callback, bouncetime=BOUNCE_TIME)

if __name__ == "__main__":
    if is_connected():  # Check for internet first
        add_player()
        time.sleep(0.1)
        init_current_channel()
    else:
        print("No connection - trying reconnecting...")
        time.sleep(2)
        python = sys.executable
        os.execl(python, python, *sys.argv)
    try:
        while True:
                time.sleep(0.1)
    except Exception as e:
        # Keyboard interrupt or other stuff that causes termination -
        # clean up any running child process.
        if radio_process != None:
                radio_process.terminate()
                GPIO.cleanup()
