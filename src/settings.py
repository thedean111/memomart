# Written by Dean Badr - 2025
# No need to touch this, but this value will be the default on boot
DELAY_TIME = 0

# -------------------------------------------------------------------
# PICTURE POSITIONING
# -------------------------------------------------------------------
# Pixel offset of where the top left corner of the picture should be
# in the memomart frame
PICTURE_OFFSET_X = 45
PICTURE_OFFSET_Y = 234

# How large to resize the taken photo to fit the frame
PICTURE_SIZE_X = 486
PICTURE_SIZE_Y = 648

# How to rotate the image to fit upright in the frame
# -- this depends on the camera orientation
ROTATION = 90

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
# the comm
PRINTER_VID = 0x04b8
PRINTER_PID = 0x0e28

# The amount of time that needs to pass after a signal before the next
# can be reacted to
IR_REBOUNCE_DELAY = 1

# -------------------------------------------------------------------
# ENHANCE MODE
# -------------------------------------------------------------------
BRIGHTNESS_FACTOR = 1

# -------------------------------------------------------------------
# INTERACTIVE SETTINGS
# -------------------------------------------------------------------
# How long after a button press can it be pressed again
BUTTON_COOLDOWN = 2

# This delay will be used in non-prompt mode on IR button "1"
# time between button press and picture taken
PHOTO_DELAY = 1.5

# -------------------------------------------------------------------
# SAVING SETTINGS
# -------------------------------------------------------------------
# Default name of the photo, the extension is added in the code
# -- this can be configured to something like "pic_beltline_06162025"
FILENAME = "photo"

# Name of the frame to paste the taken pictures in, these should exist in the
# /frames directory
FRAME = "RECEIPT_BELTLINE_06_20_2025.png"

# Should the photo be saved for later viewing, otherwise the same file will just
# keep getting overwritten.
# -- This will increment the photos, so refering to the above example the filenames
# -- will appear as "pic_beltline_06162025_1", "pic_beltline_06162025_2", etc
# ---- It refers to the value stored in "index.txt", so change that number to 0
# ---- if you want the file names to start at 0
DEEPSAVE_PHOTO = False
DEEPSAVE_DIR = "beltline_06_20_2025"

# Should a video be recorded?
RECORD_VIDEO = False
VIDEO_NAME = "video"
AUDIO_NAME = "audio"


