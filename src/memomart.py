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

# export FM_SECRET_KEY="$(openssl rand -hex 32)"
# export FM_PASSWORD_HASH="$(python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('Pura_Vida'))")"
# IMPORTS
from devices import FM_LED, FM_Printer, FM_Camera, FM_Button
from api import FM_Server
from PIL import Image, ImageFont, ImageDraw

import time
import os
import settings
import threading

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
        self.mainCamera.SetParameters(
            gain=settings.GAIN, 
            brightness=settings.BRIGHTNESS, 
            exposure=settings.EXPOSURE)
        self.pictureButton = FM_Button(17)
        self.pictureButton.quickAction = self.PrintCapturedPhoto
        self.pictureButton.holdAction = self.HoldAction
        self.pictureButton.onReady = self.buttonLED.Blink(2, 0.3)
        self.UpdateFrame()

    # -------------------------------------------------------------------
    # GetSettings: Return a dictionary of whatever is in config.json
    # -------------------------------------------------------------------
    def GetSettings(self):
        return {
            "min_brightness": settings.MIN_BRIGHTNESS, 
            "max_brightness": settings.MAX_BRIGHTNESS,
            "min_gain": settings.MIN_GAIN, 
            "max_gain": settings.MAX_GAIN,
            "min_exposure": settings.MIN_EXPOSURE, 
            "max_exposure": settings.MAX_EXPOSURE,
            "brightness": settings.BRIGHTNESS,
            "gain": settings.GAIN,
            "exposure": settings.EXPOSURE,
            "eventDescription": settings.EVENT_DESCRIPTION,
            "eventLocation": settings.EVENT_LOCATION,
            "eventDate": settings.EVENT_DATE
        }

    # -------------------------------------------------------------------
    # UpdateSettings: Take whatever is in the data package and store it
    # in config.json
    # -------------------------------------------------------------------
    def UpdateSettings(self, data):
        b = None
        e = None
        g = None
        if "brightness" in data:
            b = data["brightness"]
            settings.BRIGHTNESS = b

        if "gain" in data:
            g = data["gain"]
            settings.GAIN = g

        if "exposure" in data:
            e = data["exposure"]
            settings.EXPOSURE = e

        if "eventDescription" in data:
            settings.EVENT_DESCRIPTION = data["eventDescription"].upper()

        if "eventLocation" in data:
            settings.EVENT_LOCATION = data["eventLocation"].upper()

        if "eventDate" in data:
            settings.EVENT_DATE = data["eventDate"].upper()
        
        self.mainCamera.SetParameters(brightness=b, exposure=e, gain=g)

    # -------------------------------------------------------------------
    # GenerateFramedImage: Put the image at imgPath in a frame and save
    # it to savePath
    # -------------------------------------------------------------------
    def GenerateFramedImage(self, imgPath, framePath, savePath):
        try:
            # Open the image saved by the webcam and do necessary adjustments
            img = Image.open(imgPath).rotate(settings.ROTATION, expand=True).resize((settings.PICTURE_SIZE_X, settings.PICTURE_SIZE_Y))

            # Open the frame
            abspath = os.path.abspath(".")
            dir_path = os.path.join(abspath, framePath)
            memomartFrame = Image.open(dir_path)

            # Combine the two images
            memomartFrame.paste(img, (settings.PICTURE_OFFSET_X, settings.PICTURE_OFFSET_Y))
            memomartFrame.convert('L').save(savePath)
            
            return memomartFrame
        
        except Exception as e:
            print("Photo error:", e)
            return

    # -------------------------------------------------------------------
    # UpdateFrame: Update the frame that camera images should be 
    # placed in
    # -------------------------------------------------------------------
    def UpdateFrame(self):
        # Define spacing for the frame layout
        topTxt = 50
        spacing = 20
        imgOffset = topTxt + spacing + settings.FONT_SIZE
        evtOffset = imgOffset + settings.PICTURE_SIZE_Y + spacing + spacing
        lineHeight = settings.FONT_SIZE + settings.FONT_SIZE + 50
        lineWidth = 2
        receiptLenPixels = evtOffset + settings.FONT_SIZE + settings.FONT_SIZE + 5 + 120
        photoX = (self.printer.pixelWidth - settings.PICTURE_SIZE_X) // 2

        # Create the new frame image
        font = ImageFont.truetype("fonts/Lekton/Lekton-Regular.ttf", size=settings.FONT_SIZE)
        im = Image.new("RGB", (self.printer.pixelWidth, receiptLenPixels), "white")

        # Header Text
        d = ImageDraw.Draw(im)
        d.text((self.printer.pixelWidth // 2, topTxt), "FREE MEMORIES", fill="black", anchor='ma', font=font)

        # Draw a black square where the image is supposed to be
        d.rectangle([(photoX, imgOffset), (photoX + settings.PICTURE_SIZE_X, imgOffset + settings.PICTURE_SIZE_Y)], fill="black")

        # Event details
        d.rectangle([(photoX, evtOffset), (photoX + lineWidth, evtOffset + lineHeight)], fill="black")
        mid = evtOffset + (lineHeight // 2)
        d.text((photoX + lineWidth + 20, mid - 3), settings.EVENT_DESCRIPTION, fill="black", anchor='ld', font=font)
        d.text((photoX + lineWidth + 20, mid + 3), f"{settings.EVENT_LOCATION} - {settings.EVENT_DATE}", fill="black", anchor='la', font=font)

        settings.PICTURE_OFFSET_X = photoX
        settings.PICTURE_OFFSET_Y = imgOffset
        im.convert('L').save("media/frames/memomart_frame.png")
        return im
    
    # -------------------------------------------------------------------
    # PrintCapturedPhoto: Print the frame from the camera in the
    # appropriate outline
    # -------------------------------------------------------------------
    def PrintCapturedPhoto(self):
        abspath = os.path.abspath(".")
        # filepath = f"media/{settings.FILENAME}.png"
        filepath = os.path.join(abspath, f"media/{settings.FILENAME}.png")

        if settings.DEEPSAVE_PHOTO:
            filename = ""
            with open ("media/saved_photos/index.txt", "r+") as f:
                count = int(f.read().strip())
                filename = f"{settings.FILENAME}_{count}.png"
                f.seek(0)
                f.write(str(count + 1))
                f.truncate()

            
            dirpath = os.path.join(abspath, f"media/saved_photos/{settings.DEEPSAVE_DIR}")
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)
            filepath = os.path.join(dirpath, filename)

        self.mainCamera.Capture(filepath)
        self.buttonLED.Off()
        # self.printer.PrintPhoto(self.GenerateFramedImage(filepath, "media/memomart_photo.png"))
        self.printer.PrintPhoto(self.GenerateFramedImage(filepath, "media/frames/memomart_frame.png", "media/memomart_photo.png"))

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
            file_path = os.path.join(dirPath, photo)
            if os.path.isfile(file_path):
                img = Image.open(file_path).rotate(settings.ROTATION, expand=True).resize((settings.PICTURE_SIZE_X, settings.PICTURE_SIZE_Y))
                frame.paste(img, (settings.PICTURE_OFFSET_X, settings.PICTURE_OFFSET_Y))
                try:
                    self.printer.PrintPhoto(frame)
                except Exception as e:
                    print(f"Printer error: {e}")

    # -------------------------------------------------------------------
    # GetCameraFrame: Pull frame from camera
    # -------------------------------------------------------------------
    def GetCameraFrame(self):
        return self.mainCamera.GetFrame()

    # -------------------------------------------------------------------
    # Start: Initiates the operational loop
    # -------------------------------------------------------------------
    def Start(self):
        print("Starting Memomart!")

        self.printer.PrintStartMessage()

        while True:
            self.pictureButton.UpdateState()
            time.sleep(0.05)

# -------------------------------------------------------------------
# Main: This is the starting point of the memomart code logic
# -------------------------------------------------------------------
if __name__ == "__main__":
    app = MemomartApp()
    server = FM_Server(app)

    server_thread = threading.Thread(
        target=server.Run,
        daemon=True
    )

    server_thread.start()

    app.Start()
