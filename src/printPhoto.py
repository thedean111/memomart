'''
File:
printPhoto.py

Purpose:
Prints a single photo.

Author:
Dean Badr - 06/2025
'''
import customPrinter as Printer
import customCamera as Cam
import logic
import time
from PIL import Image

DIRECTORY = "beltline_06_19_2025"
PHOTO_NAME = "photo_501.png"

#filepath = f"saved_photos/{DIRECTORY}/{PHOTO_NAME}"
filepath = f"WHATIS.png"

#logic.Setup()
#Cam.SetupCamera()
Printer.SetupPrinter()

time.sleep(1)

# Capture the photo from the web cam
savepath = Cam.Capture()

time.sleep(1)
savepath = Cam.Capture()
img = Cam.ConfigureMemomartFormat(filepath)
# img = Image.open(settings.BUSINESS_CARD_PATH)
Printer.PrintPhoto(img)