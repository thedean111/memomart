'''
File:
logic.py

Purpose:
The main logic for the machine's operations.

Author:
Dean Badr - 06/2025
'''
import cv2
from picamera2 import Picamera2

from gpiozero import Button, PWMLED
# from evdev import InputDevice, ecodes
# import evdev
from PIL import Image

import time

import settings
# import customIR as IR
import customLED as LED
import customCamera as CAM
import customPrinter as printer

# ir = None
button = None
hasCamera = False

# -------------------------------------------------------------------
# Setup: Connects to the different interfaces the user is
# exposed to
# -------------------------------------------------------------------
def Setup():
    # global ir, lastIR
    global button, hasCamera

    # devices = [InputDevice(path) for path in evdev.list_devices()]
    # ir_path = ""
    # for device in devices:
    #     if "gpio_ir_recv" in device.name.lower():
    #         ir_path = device.path

    # ir = InputDevice(ir_path)
    button = Button(17, pull_up=True, bounce_time=0.2)
    LED.Init()
    # lastIR = time.time()
    hasCamera = CAM.SetupCamera()
    printer.SetupPrinter()

# -------------------------------------------------------------------
# ServiceLoop: Enter a loop that will run as long as the service runs
# -------------------------------------------------------------------
def ServiceLoop():
    print("Starting service loop.")
    global hasCamera
    # Initialize state data
    button_ready = True
    last_press = 0
    # lastIR = 0

    # Show user that the device can now be used
    printer.PrintActivationMessage()

    # Loop, polling for different events
    while True:
        # When reading an event from the infrared receiver
        # event = ir.read_one()
        # if ((time.time() - lastIR) >= settings.IR_REBOUNCE_DELAY) and event and event.type == ecodes.EV_MSC and event.code == ecodes.MSC_SCAN:
        #     lastIR = time.time()
        #     val = IR.handleIR(event.value)
        #     if val is not None:
        #         print(val)
        #         printer.PrintSettingsChange()
        #         LED.Blink(val)
            
        #     # Flush all events that may be pending
        #     while ir.read_one():
        #         pass  # Discard the event

        # When the button is pressed
        if button.is_pressed and button_ready:
            # Don't allow second presses
            button_ready = False
            LED.Off()
            
            if not hasCamera:
                printer.Debug(text="There is no camera connected!", beginning_line=5, end_line=5)

            else:   
                # If a preceeding prompt should be printed before the photo is taken
                if settings.PRINT_PROMPT:
                    # Print the prompt
                    printer.PrintPrompt()

                    # Pulse the LED for some feedback
                    LED.Pulse(None)

                # Wait a delay and ensure the led is turned off
                time.sleep(settings.DELAY_TIME)
                LED.Off()

                # Capture the photo from the web cam
                savepath = CAM.Capture()

                # Paste the photo on the frame
                picture = CAM.ConfigureMemomartFormat(savepath)
                
                img = Image.open(savepath).rotate(settings.ROTATION, expand=True).resize((settings.PICTURE_SIZE_X, settings.PICTURE_SIZE_Y))
                
                # Print the result
                printer.PrintPhoto(picture)

                # No longer in progress
                last_press = time.time()

        # Button cooldown time
        if not button_ready:
            if (time.time() - last_press) >= settings.BUTTON_COOLDOWN:
                LED.On()
                button_ready = True

        time.sleep(0.05)
    
      
