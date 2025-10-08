# Import the button
from gpiozero import Button, PWMLED
import time
from PIL import Image
import customPrinter as Printer
import customCamera as Cam
import customLED as LED

# Setup camera and printer
Cam.SetupCamera()
Printer.SetupPrinter()

# Grab the button from the GPIO pin on the pi, gpio 17 -> pin 11
gpioPin = 17
button = Button(17, pull_up=True, bounce_time=0.2)

# Setup the LED
led = PWMLED(18, initial_value=True)

# Setup a simple state timer
cooldownTime = 1
buttonReady = True

# Infinte loop, waiting for the button to be pressed
timestamp = time.time()
while (True):
    if not buttonReady and (time.time() - timestamp >= cooldownTime):
        buttonReady = True
        led.on()

    if (button.is_pressed) and buttonReady:
        timestamp = time.time()
        buttonReady = False
        print("Button pressed!")
        savepath = Cam.Capture()
        img = Cam.ConfigureMemomartFormat(savepath)
        Printer.PrintPhoto(img)
        led.off()

    time.sleep(0.05)