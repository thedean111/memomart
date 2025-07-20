# Written by Dean Badr - 2025
from escpos.printer import Usb
from PIL import Image
import settings
import os

# -------------------------------------------------------------------
# SetupPrinter: Connect to the thermal printer given the PID and VID
# in the user-defined settings
# -------------------------------------------------------------------
def SetupPrinter():
    global printer

    try:
        printer = Usb(settings.PRINTER_VID, settings.PRINTER_PID, 0)
        printer.profile.media['width']['pixels'] = 576
        print("Successfully connect to thermal printer.")

    except Exception as e:
        print(f"Printer setup error: {e}")
        exit()


# -------------------------------------------------------------------
# PrintActivationMessage: Prints a short bit of text to confirm
# successful configuration of memomart
# -------------------------------------------------------------------
def PrintActivationMessage():  
    if printer == None:
        print("Cannot access printer.")
        return
    
    print("Printing activation message.")
    printer.ln(5)
    printer.set(align='center', font='b', custom_size=True, width=2, height=2)
    printer.text("WELCOME TO MEM-O-MART!\n")
    printer.ln(2)
    printer.set(align='center', font='a', custom_size=True, width=1, height=1)
    printer.text("Please press the button to receive a \ncopy of your memory! ")
    printer.ln(5)
    printer.cut()  

# -------------------------------------------------------------------
# PrintPhoto: Prints the passed in photo
# -------------------------------------------------------------------
def PrintPhoto(photo):
    if printer == None:
        print("Cannot access printer.")
        return
    
    printer.image(photo, center=True)
    printer.cut()

# -------------------------------------------------------------------
# PrintPrompt: Prints one of the prompts, defined by the user
# -------------------------------------------------------------------
def PrintPrompt():
    abspath = os.path.abspath(".")
    path = ""
    # Open the prompt and print it
    if settings.TIMED_PROMPT:
        path = os.path.join(abspath, "PROMPT_MEMOMART_A.png")
    else:
        path = os.path.join(abspath, "PROMPT_MEMOMART_B.png")

    prompt = Image.open(path)
    PrintPhoto(prompt)

# -------------------------------------------------------------------
# PrintSettingsChange: Print a little slip that describes the new
# mode the machine is on
# -------------------------------------------------------------------
def PrintSettingsChange():
    printer.ln(2)
    printer.set(align='center', font='b', custom_size=True, width=2, height=2)
    printer.text("SETTINGS CHANGED\n")
    printer.ln(1)
    printer.set(align='left', font='a', custom_size=True, width=1, height=1)
    printer.text(f"Print prompt?        -> {settings.PRINT_PROMPT}\n")
    printer.text(f"  Prompt with time?  -> {settings.TIMED_PROMPT}\n")
    printer.text(f"Image delay (s)      -> {settings.DELAY_TIME}\n")
    printer.text(f"Save to directory    -> {settings.DEEPSAVE_PHOTO}\n")
    printer.text(f"Currently recording? -> {settings.RECORD_VIDEO}\n")
    printer.ln(2)
    printer.cut()
