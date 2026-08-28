'''
File:
logic.py

Purpose:
The main logic for the machine's operations.

Author:
Dean Badr - 06/2025
'''

from gpiozero import Button, PWMLED
from PIL import Image

import cv2
import time
import os

import settings
import customLED as LED
import customCamera as CAM
import customPrinter as printer

# ir = None
button = None
hasCamera = False
press_time = 0
release_time = 0
button_ready = True
button_held = False
hold_action_executed = False


# -------------------------------------------------------------------
# QuickPress: Behavior to execute when the button is tapped
# -------------------------------------------------------------------
def QuickPress():
    if not hasCamera:
        printer.Debug(text="There is no camera connected!", beginning_line=5, end_line=5)
        return
        
    # If a preceeding prompt should be printed before the photo is taken
    if settings.PRINT_PROMPT:
        # Print the prompt
        printer.PrintPrompt()

        # Pulse the LED for some feedback
        LED.Pulse(None)

    # Wait a delay and ensure the led is turned off
    time.sleep(settings.DELAY_TIME)
    

    # Capture the photo from the web cam
    savepath = CAM.Capture()

    # Paste the photo on the frame
    picture = CAM.ConfigureMemomartFormat(savepath)
    
    img = Image.open(savepath).rotate(settings.ROTATION, expand=True).resize((settings.PICTURE_SIZE_X, settings.PICTURE_SIZE_Y))
    
    # Print the result
    printer.PrintPhoto(picture)


# -------------------------------------------------------------------
# HoldPress: Behavior to execute when the button is held
# -------------------------------------------------------------------
def HoldPress():
    global hold_action_executed
    hold_action_executed = True
    printer.PrintBusinessCard()

def OnPress():
    global press_time, button_ready, button_held, hold_action_executed
    if button_ready:
        LED.Off()
        press_time = time.time()
        button_held = True
        hold_action_executed = False

def OnRelease():
    global press_time, button_ready, release_time, button_held, hold_action_executed
    if not button_ready:
        return

    button_ready = False
    button_held = False

    # Calculate how long the button was just pressed for
    # Only take the picture if the hold action wasn't executed
    if not hold_action_executed:
        print("Tapped the button")
        time.sleep(settings.PHOTO_DELAY)
        QuickPress()
        
# -------------------------------------------------------------------
# Setup: Connects to the different interfaces the user is
# exposed to
# -------------------------------------------------------------------
def Setup():
    global button, hasCamera


    button = Button(17, pull_up=True, bounce_time=0.01)
    button.when_pressed = OnPress
    button.when_released = OnRelease

    LED.Init()
    hasCamera = CAM.SetupCamera()
    printer.SetupPrinter()

# -------------------------------------------------------------------
# ServiceLoop: Enter a loop that will run as long as the service runs
# -------------------------------------------------------------------
def ServiceLoop():
    print("Starting service loop.")
    global hasCamera


    abspath = os.path.abspath(".")
    path = os.path.join(abspath, settings.BUSINESS_CARD_PATH)
    print(path)

    # Obtain state data
    global button_ready, release_time, press_time, button_held, hold_action_executed

    # Show user that the device can now be used
    printer.PrintActivationMessage()

    # Loop, polling for different events
    while True:   
        if button_held and settings.ENABLE_HOLD and not hold_action_executed and ((time.time() - press_time) >= settings.BUTTON_HOLD_THRESHOLD):
            HoldPress()

        # When the button is not ready, update the cooldown
        if not button_ready:
            if (time.time() - release_time) >= settings.BUTTON_COOLDOWN:
                LED.On()
                button_ready = True

        time.sleep(0.05)
    
      
