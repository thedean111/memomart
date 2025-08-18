'''
File:
printFromDir.py

Purpose:
Prints all photos in a directory.

Author:
Dean Badr - 06/2025
'''
from escpos.printer import Usb
from PIL import Image
import time
import os
import settings

# Setup relevant paths
dir_path = "saved_photos/beltline_06_18_2025"
frame_path = "frames/RECEIPT_BELTLINE_06182025.png"

# Setup printer
try:
    printer = Usb(settings.PRINTER_VID, settings.PRINTER_PID, 0)
    printer.profile.media['width']['pixels'] = 576
    print("Successfully connect to thermal printer.")

except Exception as e:
    print(f"Printer setup error: {e}")
    exit()

memomartFrame = Image.open(frame_path)

for photo in os.listdir(dir_path):
    time.sleep(0.5)
    file_path = os.path.join(dir_path, photo)
    if os.path.isfile(file_path):
        img = Image.open(file_path).rotate(settings.ROTATION, expand=True).resize((settings.PICTURE_SIZE_X, settings.PICTURE_SIZE_Y))
        memomartFrame.paste(img, (settings.PICTURE_OFFSET_X, settings.PICTURE_OFFSET_Y))
        try:
            printer.image(memomartFrame, center=True)
            printer.cut()
        except Exception as e:
            print(f"Printer error: {e}")
