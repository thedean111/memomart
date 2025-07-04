import customPrinter as Printer
import customCamera as Cam
import logic
from PIL import Image

DIRECTORY = "beltline_06_19_2025"
PHOTO_NAME = "photo_501.png"

filepath = f"saved_photos/{DIRECTORY}/{PHOTO_NAME}"

logic.Setup()
img = Cam.ConfigureMemomartFormat(filepath)

img1 = Image.open("extra/receipt_annotations.png")

Printer.PrintPhoto(img1)