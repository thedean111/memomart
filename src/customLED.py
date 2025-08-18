'''
File:
customLED.py

Purpose:
Dedicated file for all LED-related operations that memomart should use. Provides
helper functions to control the lighting of the LED.

Author:
Dean Badr - 06/2025
'''
# IMPORTS
from gpiozero import PWMLED
import time

led = None

# -------------------------------------------------------------------
# Init: Setup the led
# -------------------------------------------------------------------
def Init():
    global led
    led = PWMLED(18, initial_value=True)

# -------------------------------------------------------------------
# Off: Turn off the led
# -------------------------------------------------------------------
def Off():
    led.off()

# -------------------------------------------------------------------
# On: Turn on the led
# -------------------------------------------------------------------
def On():
    led.on()

# -------------------------------------------------------------------
# Blink: Turn off and on a designated amoutn of times
# -------------------------------------------------------------------
def Blink(n):
    led.off()
    time.sleep(0.2)

    for _ in range(n):
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)
    led.on()

# -------------------------------------------------------------------
# Pulse: Turns on and off by fading
# -------------------------------------------------------------------
def Pulse(n):
    # Delay a little for people to get in position
    led.pulse(0.5, 0.5, n)
