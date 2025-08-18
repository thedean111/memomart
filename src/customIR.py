# Written by Dean Badr - 2025
# IMPORTS
import settings
import customCamera as CAM

# -------------------------------------------------------------------
# IR REMOTE CODES
# -------------------------------------------------------------------
NUM_0 = 0x16 # (22) # Instant
NUM_1 = 0x0c # (12) # No prompt, slight delay
NUM_2 = 0x18 # (24) # Print prompt, no time
NUM_3 = 0x5e # (94) # Print prompt, with time
NUM_4 = 0x08 # (08)
NUM_5 = 0x1c # (28)
NUM_6 = 0x5a # (90)
NUM_7 = 0x42 # (66)
NUM_8 = 0x52 # (82) # Record
NUM_9 = 0x4a # (74) # Stop Recording
DOWN_ARROW = 0x07   # no save mode #
UP_ARROW = 0x09     # save mode #
REWIND = 0x44       # Decrease low-light
FORWARD = 0x43      # Increase low-light


# -------------------------------------------------------------------
# handleIR: Handle events from the IR receiver
# -------------------------------------------------------------------
def handleIR(value):
    # Instant print mode
    if value == NUM_0:
        settings.PRINT_PROMPT = False
        settings.DELAY_TIME = 0
        return 1
    
    # Instant with a small delay
    elif value == NUM_1:
        settings.PRINT_PROMPT = False
        settings.DELAY_TIME = settings.PHOTO_DELAY
        return 2
    
    # Print the prompt, delay, take picture
    elif value == NUM_2:
        settings.TIMED_PROMPT = False
        settings.PRINT_PROMPT = True
        settings.DELAY_TIME = settings.PROMPT_DELAY
        return 3
    
    elif value == NUM_3:
        settings.TIMED_PROMPT = True
        settings.PRINT_PROMPT = True
        settings.DELAY_TIME = settings.PROMPT_DELAY
        return 4
    
    # Turn off saving
    elif value == DOWN_ARROW:
        settings.DEEPSAVE_PHOTO = False
        return -1
    
    # Turn on saving
    elif value == UP_ARROW:
        settings.DEEPSAVE_PHOTO = True
        return -2
    
    # Start recording a video
    elif value == NUM_8:
        CAM.RecordStart()
        return 9
    
    # Stop recording the current video
    elif value == NUM_9:
        CAM.RecordStop()
        return 10
    
    # Day mode
    elif value == REWIND:
        CAM.SetCameraParams(-1)
        return 1
    
    # Night mode
    elif value == FORWARD:
        CAM.SetCameraParams(1)
        return 1
    
    return None
