#!/usr/bin/env python3

# Written by Dean Badr - 2025
# SERVICE COMMANDS
# sudo systemctl restart memomart.service
# sudo systemctl stop memomart.service
# sudo systemctl start memomart.service
# journalctl -u memomart.service -f
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
