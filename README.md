# RASP-RADIO
A Python program meant to control net-radio on the Raspberry Pi, located in an vintage radio (or any radio).
Furthermore, it also have build in Google Assistant SDK if that is wanted.

## Getting Started
In order to get this working on your own system, follow the steps.

### Prerequisites
Both hardware and software is needed for this so the prerequisites for both is listed.
#### Hardware
* Raspberry Pi, with latest Raspbian OS 
* A old radio (or alike) with speakers and rotary switch knob (or other buttons)
* Audio Amplifier
* USB Microphone
* Power cables, sound cables, jumper wires

##### Pin Connections
The rotary switch knob is connected to Pin 1 (3v3)
The different channels is connected to the following pins:
* Pin 29 (GPIO 5)
* Pin 31 (GPIO 6)
* Pin 33 (GPIO 13)
* Pin 35 (GPIO 19)
* Pin 37 (GPIO 26)
* Pin 36 (GPIO 16)

#### Software
The following software Prerequisites apply:
* Python 3.5
* MPD/MPC for controlling the channels ([see here](https://github.com/sindresorhus/awesome/blob/master/awesome.md)) 
* The latest version of RPi.GPIO
* Google Assistant SDK (with Developer Project and Actions on Google).
    * Follow the official guide from ([Google](https://developers.google.com/assistant/sdk/guides/library/python/embed/setup)), until `Next Steps`

### Installing
The program mostly work as-is, however, two steps needs to be taken: launch on boot and assistant files.

#### Launch on boot
The program uses the built in systemd to start on boot. Run the command `sudo systemctl enable rasp-radio.service`
and the program should run on boot. 

#### Google Assistant Files
When setting up the Google Assistant SDK, a client_secret.json file is downloaded, this should be in the same installation directory (preferably /home/pi/).

Secondly, when creating Actions on Google, a Model ID is created. This can be found on [https://console.actions.google.com/](https://console.actions.google.com/)
under Device Registration. This Model ID should be added to a file named config.ini (use config.ini.example to get started)

## Deployment
Out of the box it comes with 6 net-radio stations (ANR, Soft Radio, P3, Nordjyske, Nova, ABC) which are all danish
radios. Therefore if one need to change them, the following steps is needed  (all in `google_assistant_radio.py`):

### Find Stream
First the stream for the net radio should be found. This is different for site to site.
However, it can normally be found in the net-radios sites HTML or associated JavaScript. An example of this:
 ```
$(document).ready(function () {
    $("#jquery_jplayer_1").jPlayer({
        ready: function (event) {
            $(this).jPlayer("setMedia", {
                mp3: "http://stream.anr.dk:80/anr"
            }).jPlayer("play");
        },
        swfPath: "/scripts/jplayer/jplayer",
        supplied: "mp3",
        wmode: "window",
        useStateClassSkin: true
    });
});
        
```
 Where `http://stream.anr.dk:80/anr` is the official stream.
 
### Add to Rasp-Radio
In `radio.py` add the name of the channel, stream url and pin number to switch to it. 
Example could be Name: __Radio 123__, Url: __http://stream.radio123.com__, Pin: __GPIO 21__

Add it to `CHNL_INPUT_DICT` as `CHNL_RADIO_123 = 21`

Add stream to `RADIO_DICT["RADIO_123"] = 'http://stream.radio123.com'`

Create a radio function as follows:
```
def radio_123():
    global radio_process, CHNL_CURRENT
    try:
        print("\nPlaying Radio 123!")
        radio_process = subprocess.Popen(["/usr/bin/mpc", "stop"])
        time.sleep(0.1)
        radio_process = subprocess.Popen(["/usr/bin/mpc", "play", str(RADIO_DICT.keys().index("RADIO_123") + 1)])
        CHNL_CURRENT = CHNL_INPUT_DICT["CHNL_RADIO_123"]
    except Exception as er:
        print("Error in playing Nordjyske; error: " + str(er))
        time.sleep(2)
        radio_123()
```
To `channel_selection` add:
```
        elif _chnl == "CHNL_RADIO_123":
            radio_123()
```

And at last an interrupt to the selected pin:
```
GPIO.add_event_detect(21, GPIO.RISING, callback=callback, bouncetime=BOUNCE_TIME)
```
## Author
* Emil Blixt Hansen - [Blixt Development](http://blixtdevelopment.com/) :zap:

## License 
This project is licensed under the MIT License!

## Acknowledgments
Doing development of this project, it was not planned to be shared.
Therefore, aspects like channel adding is kinda hard-coded... It was only meant to serve as a radio at my own house.
* Any contributions/questions/etc. are welcome.
* The code does not come with any warranty, it is provided as-is. 