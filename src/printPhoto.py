# Written by Dean Badr - 2025
import customPrinter as Printer
import customCamera as Cam
import logic

DIRECTORY = "beltline_06_19_2025"
PHOTO_NAME = "photo_501.png"

filepath = f"saved_photos/{DIRECTORY}/{PHOTO_NAME}"

logic.Setup()
img = Cam.ConfigureMemomartFormat(filepath)

Printer.PrintPhoto(img)
