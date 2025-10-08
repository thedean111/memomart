#!/usr/bin/env python3

'''
File:
memomart.py

Purpose:
Entry point for service activation. Starts the logic operations loop.

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
import time
import logic

# -------------------------------------------------------------------
# Main: This is the starting point of the memomart code logic
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Setup interfaces
    logic.Setup()

    # Startup delay to allow devices to "wake up"
    time.sleep(1)

    # Print the successful start message
    logic.ServiceLoop()
