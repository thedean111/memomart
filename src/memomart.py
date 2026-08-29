#!/usr/bin/env python3

'''
File:
memomart.py

Purpose:
Entry point for service activation. Starts the logic operations loop.
Interface for the application layer of the architecture

Author:
Dean Badr - 06/2025
'''
# SERVICE COMMANDS
# sudo systemctl restart memomart.service
# sudo systemctl stop memomart.service
# sudo systemctl start memomart.service
# journalctl -u memomart.service -f (this will show the log)
# vcgencmd get_throttled

# IMPORTS
from devices import FM_LED, FM_Printer, FM_Camera, FM_Button
from PIL import Image

import time
import os
import settings

class MemomartApp:
    # -------------------------------------------------------------------
    # __init__: Establish devices
    # -------------------------------------------------------------------
    def __init__(self):
        self.buttonLED = FM_LED(18)

        self.printer = FM_Printer(
                    settings.PRINTER_VID, 
                    settings.PRINTER_PID,
                    settings.PRINTER_OUT,
                    settings.PRINTER_IN)

        self.mainCamera = FM_Camera()

        self.pictureButton = FM_Button(17)
        self.pictureButton.quickAction = self.PrintCapturedPhoto
        self.pictureButton.holdAction = self.HoldAction
        self.pictureButton.onReady = self.buttonLED.Blink(2, 0.3)


    # -------------------------------------------------------------------
    # GenerateFramedImage: Put the image at imgPath in a frame and save
    # it to savePath
    # -------------------------------------------------------------------
    def GenerateFramedImage(self, imgPath, savePath):
        try:
            # Open the image saved by the webcam and do necessary adjustments
            img = Image.open(imgPath).rotate(settings.ROTATION, expand=True).resize((settings.PICTURE_SIZE_X, settings.PICTURE_SIZE_Y))

            # Open the frame
            abspath = os.path.abspath(".")
            dir_path = os.path.join(abspath, f"media/frames/{settings.FRAME}")
            memomartFrame = Image.open(dir_path)

            # Combine the two images
            memomartFrame.paste(img, (settings.PICTURE_OFFSET_X, settings.PICTURE_OFFSET_Y))
            memomartFrame.convert('L').save(savePath)
            
            return memomartFrame
        
        except Exception as e:
            print("Photo error:", e)
            return

    # -------------------------------------------------------------------
    # PrintCapturedPhoto: Print the frame from the camera in the
    # appropriate outline
    # -------------------------------------------------------------------
    def PrintCapturedPhoto(self):
        filepath = f"media/{settings.FILENAME}.png"
        if settings.DEEPSAVE_PHOTO:
            filename = ""
            with open ("media/saved_photos/index.txt", "r+") as f:
                count = int(f.read().strip())
                filename = f"{settings.FILENAME}_{count}.png"
                f.seek(0)
                f.write(str(count + 1))
                f.truncate()

            abspath = os.path.abspath(".")
            dirpath = os.path.join(abspath, f"media/saved_photos/{settings.DEEPSAVE_DIR}")
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            filepath = os.path.join(dirpath, filename)

        self.mainCamera.Capture(filepath)
        self.buttonLED.Off()
        # self.printer.PrintPhoto(self.GenerateFramedImage(filepath, "media/memomart_photo.png"))

    # -------------------------------------------------------------------
    # HoldAction: What to do when the main button is held. Branch can be
    # added here to provide options on what action to take
    # -------------------------------------------------------------------
    def HoldAction(self):
        self.printer.PrintBusinessCard("media/business_cards/bc2.png")

    # -------------------------------------------------------------------
    # PrintDirectory: Print all the photos from a directory after
    # pasting them in a frame
    # -------------------------------------------------------------------
    def PrintDirectory(self, dirPath, framePath):
        frame = Image.open(framePath)
        for photo in os.listdir(dirPath):
            time.sleep(0.5)
            file_path = os.path.join(dir_path, photo)
            if os.path.isfile(file_path):
                img = Image.open(file_path).rotate(settings.ROTATION, expand=True).resize((settings.PICTURE_SIZE_X, settings.PICTURE_SIZE_Y))
                memomartFrame.paste(img, (settings.PICTURE_OFFSET_X, settings.PICTURE_OFFSET_Y))
                try:
                    self.printer.PrintPhoto(memomartFrame)
                except Exception as e:
                    print(f"Printer error: {e}")

    # -------------------------------------------------------------------
    # Start: Initiates the operational loop
    # -------------------------------------------------------------------
    def Start(self):
        print("Starting Memomart!")

        # self.printer.PrintStartMessage()

        while True:
            self.pictureButton.UpdateState()
            time.sleep(0.05)

# -------------------------------------------------------------------
# Main: This is the starting point of the memomart code logic
# -------------------------------------------------------------------
if __name__ == "__main__":
    app = MemomartApp()
    app.Start()