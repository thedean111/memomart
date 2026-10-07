'''
File:
settings.py

Purpose:
Contains many parameters that are used throughout the machine's operations. The main
interface for configuring the machine.

Author:
Dean Badr - 06/2025
'''
# No need to touch this, but this value will be the default on boot
DELAY_TIME = 0

# -------------------------------------------------------------------
# PICTURE POSITIONING
# -------------------------------------------------------------------
# Pixel offset of where the top left corner of the picture should be
# in the memomart frame
PICTURE_OFFSET_X = 45
PICTURE_OFFSET_Y = 156

# How large to resize the taken photo to fit the frame
PICTURE_SIZE_X = 486
PICTURE_SIZE_Y = 648

# How to rotate the image to fit upright in the frame
# -- this depends on the camera orientation
ROTATION = 90

FONT_SIZE = 28
EVENT_DESCRIPTION = "1x VALLEY ROAD"
EVENT_LOCATION = "MONTCLAIR, NJ"
EVENT_DATE = "9/2/2026"
# -------------------------------------------------------------------
# PROMPT CONFIGURATION
# -------------------------------------------------------------------
# Should the prompt print at all prior to taking a photo
PRINT_PROMPT = False

# Should the prompt write the time on it
TIMED_PROMPT = False

# How long to wait between printing the prompt and taking the photo
PROMPT_DELAY = 10

# -------------------------------------------------------------------
# DEVICE SETTINGS
# -------------------------------------------------------------------
# Is a webcam or picam plugged in, webcam here refers to a camera
# setup via usb
# -- These should never both be true
USE_WEBCAM = True
USE_PICAM = False

# The IDs of the printer so the code can find the usb connection
# PRINTER_VID = 0x04b8
# PRINTER_PID = 0x0e28

PRINTER_VID = 0x0485
PRINTER_PID = 0x5741
PRINTER_OUT = 0x02
PRINTER_IN = 0x82

# The amount of time that needs to pass after a signal before the next
# can be reacted to
IR_REBOUNCE_DELAY = 0.2

# -------------------------------------------------------------------
# CAMERA MODES
# -------------------------------------------------------------------
MIN_EXPOSURE = 20 #100
MIN_BRIGHTNESS = 10 #128
MIN_GAIN = 10 #150

MAX_EXPOSURE = 1000
MAX_BRIGHTNESS = 200
MAX_GAIN = 300

BRIGHTNESS = 100
GAIN = 100
EXPOSURE = 100

CAM_MODE_INCREMENTS = 20

# -------------------------------------------------------------------
# INTERACTIVE SETTINGS
# -------------------------------------------------------------------
# How long after a button press can it be pressed again
BUTTON_COOLDOWN = 3

# This delay will be used in non-prompt mode on IR button "1"
# time between button press and picture taken
PHOTO_DELAY = 1.0

# Will holding the button execute the hold action
ENABLE_HOLD = True

# How long the button needs to be held for special behavior
BUTTON_HOLD_THRESHOLD = 3

# File path to the business card
BUSINESS_CARD_PATH = "media/business_cards/BIZ CARD 2.png"

# -------------------------------------------------------------------
# SAVING SETTINGS
# -------------------------------------------------------------------
# Default name of the photo, the extension is added in the code
# -- this can be configured to something like "pic_beltline_06162025"
FILENAME = "photo"

# Name of the frame to paste the taken pictures in, these should exist in the
# /frames directory
FRAME = "bantam 1.png"

# Should the photo be saved for later viewing, otherwise the same file will just
# keep getting overwritten.
# -- This will increment the photos, so refering to the above example the filenames
# -- will appear as "pic_beltline_06162025_1", "pic_beltline_06162025_2", etc
# ---- It refers to the value stored in "index.txt", so change that number to 0
# ---- if you want the file names to start at 0
DEEPSAVE_PHOTO = False
DEEPSAVE_DIR = "test_save"

# Should a video be recorded?
RECORD_VIDEO = False
VIDEO_NAME = "video"
AUDIO_NAME = "audio"