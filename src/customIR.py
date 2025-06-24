# IMPORTS
import settings
import customCamera as CAM

# -------------------------------------------------------------------
# IR REMOTE CODES
# -------------------------------------------------------------------
NUM_0 = 0x16 # (22) #
NUM_1 = 0x0c # (12) #
NUM_2 = 0x18 # (24) # 
NUM_3 = 0x5e # (94) #
NUM_4 = 0x08 # (08)
NUM_5 = 0x1c # (28)
NUM_6 = 0x5a # (90)
NUM_7 = 0x42 # (66)
NUM_8 = 0x52 # (82) #
NUM_9 = 0x4a # (74) #
DOWN_ARROW = 0x07 # no save mode #
UP_ARROW = 0x09 # save mode #


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
    elif value == NUM_4:
        settings.BRIGHTNESS_FACTOR = 1
        return 5
    
    # Night mode
    elif value == NUM_5:
        settings.BRIGHTNESS_FACTOR = 1.75
        return 6
    
    return None