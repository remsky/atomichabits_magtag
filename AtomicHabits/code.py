# SPDX-FileCopyrightText: 2020 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MagTag Shower Thoughts
# Be sure to put WiFi access point info in secrets.py file to connect

import time
import random
import json
from adafruit_magtag.magtag import MagTag
from adafruit_fakerequests import Fake_Requests


#showerthoughts = random.randint(0,10)
#showerthoughts = True if showerthoughts < 2 else False

showerthoughts = False


# in seconds, we can refresh about 100 times on a battery
TIME_BETWEEN_REFRESHES = 1 * 60 * 60  # one hour delay


def blink_lights(magtag,start=True):
    buttons = magtag.peripherals.buttons
    if start:
        button_colors = ((255, 0, 0), (255, 150, 0), (0, 255, 255), (180, 0, 255))
    else:
        button_colors = ((180, 0, 255), (180, 0, 255), (0, 255, 255), (180, 0, 255))
    #button_tones = [60,80,40,80,80]
    #timestamp = time.monotonic()
    #for tone in button_tones:
    #magtag.peripherals.play_tone(200, 0.1)
    for t in range(5):
        time.sleep(0.1)
        for i,b in enumerate(range(len(buttons))):
            time.sleep(0.1)
            magtag.peripherals.neopixel_disable = False
            magtag.peripherals.neopixels.fill(button_colors[i])

    magtag.peripherals.neopixel_disable = True





if showerthoughts:
# Set up where we'll be fetching data from
    DATA_SOURCE = "https://www.reddit.com/r/showerthoughts/hot.json?limit=10"
    quote_num = random.randint(0, 9)  # we get 10 possibilities, pick one of them
    QUOTE_LOCATION = ["data", "children", quote_num, "data", "title"]
    AUTHOR_LOCATION = ["data", "children", quote_num, "data", "author"]


    magtag = MagTag(
        url=DATA_SOURCE,
        json_path=(QUOTE_LOCATION, AUTHOR_LOCATION),
    )

    magtag.graphics.set_background("/bmps/magtag_geo1_bg.bmp")
    blink_lights(magtag)
# quote in bold text, with text wrapping
    magtag.add_text(
        text_font="/fonts/Arial-Bold-12.pcf",
        text_wrap=28,
        text_maxlen=120,
        text_position=(
            (magtag.graphics.display.width // 2),
            (magtag.graphics.display.height // 2) - 10,
        ),
        line_spacing=0.75,
        text_anchor_point=(0.5, 0.5),  # center the text on x & y
    )


    try:
        magtag.network.connect()
        value = magtag.fetch()
        print("Response is", value)
    except (ValueError, RuntimeError, ConnectionError, OSError) as e:
        magtag.set_text(e)
        print("Some error occured, retrying! -", e)

else:
# Set up where we'll be fetching data from
    f = open(r"atomic.json")
    atoms = json.load(f)
    quote_num = random.randint(0, len(atoms))  # we get 10 possibilities, pick one of them
    quote = atoms[str(quote_num)]
    magtag = MagTag()

    magtag.graphics.set_background("/bmps/magtag_geo1_bg.bmp")
    blink_lights(magtag)
# quote in bold text, with text wrapping
    magtag.add_text(
        text_font="/fonts/Arial-Bold-12.pcf",
        text_wrap=28,
        text_maxlen=120,
        text_position=(
            (magtag.graphics.display.width // 2),
            (magtag.graphics.display.height // 2) - 10,
        ),
        line_spacing=0.75,
        text_anchor_point=(0.5, 0.5),  # center the text on x & y
    )
    batt_volt = magtag.peripherals.battery
    if batt_volt < 3.3:
        quote = quote + "LowBattery"

    magtag.set_text(quote)
    blink_lights(magtag,start=False)



#    try:
#        magtag.network.connect()
#        value = magtag.fetch()
#        print("Response is", value)
#    except (ValueError, RuntimeError, ConnectionError, OSError) as e:
#        magtag.set_text(e)
#        print("Some error occured, retrying! -", e)

# wait 2 seconds for display to complete
time.sleep(2)
magtag.exit_and_deep_sleep(TIME_BETWEEN_REFRESHES)
