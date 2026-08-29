'''
File:
networkManager.py

Purpose:
Determine and execute the proper network state of the system. This device should toggle between
a Wi-Fi consuming state, and a state where it broadcasts a hotspot connection. The hotspot connection
is used for adjusting settings on the fly, whereas the Wi-Fi state is used for development.

Author:
Dean Badr - 08/2026
'''

import subprocess
import time
from gpiozero import Button, PWMLED

WIFI_INTERFACE = "wlan0"
HOTSPOT_CONNECTION = "memomart-hotspot"
WIFI_TIMEOUT = 15
network_led = None
network_button = None

# -------------------------------------------------------------------
# run_nmcli: Safeuly run and report command line function
# -------------------------------------------------------------------
def run_nmcli(args, timeout=10):
    try:
        result = subprocess.run(
            ["nmcli"] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )

        return result

    except subprocess.TimeoutExpired:
        print(f"NetworkManager command timed out: nmcli {' '.join(args)}")
        return None

    except subprocess.CalledProcessError as e:
        print(f"NetworkManager command failed: nmcli {' '.join(args)}")

        if e.stderr:
            print(e.stderr.strip())

        return None

    except OSError as e:
        print(f"Could not execute nmcli: {e}")
        return None

# -------------------------------------------------------------------
# get_wifi_state: Determine the current state of the wifi connection
# -------------------------------------------------------------------
def get_wifi_state():
    """
    Possible results include:
        connected
        disconnected
        connecting
        unavailable
        unknown
    """

    result = run_nmcli(
        [
            "-t",
            "-f",
            "GENERAL.STATE",
            "device",
            "show",
            WIFI_INTERFACE
        ]
    )

    if result is None:
        return "unknown"


    state = result.stdout.strip().lower()

    if "connected" in state and "connecting" not in state:
        return "connected"

    if "connecting" in state:
        return "connecting"

    if "disconnected" in state:
        return "disconnected"

    if "unavailable" in state:
        return "unavailable"

    return "unknown"

# -------------------------------------------------------------------
# start_hotspot: Start the Mem-O-Mart hotspot.
# -------------------------------------------------------------------
def start_hotspot():
    print("Starting Mem-O-Mart hotspot...")

    result = run_nmcli(
        ["connection", "up", HOTSPOT_CONNECTION]
    )

    if result is None:
        print("Failed to start Mem-O-Mart hotspot.")
        return False

    print("Mem-O-Mart hotspot is active.")
    network_led.on()
    return True

# -------------------------------------------------------------------
# stop_hotspot: top the Mem-O-Mart hotspot.
# -------------------------------------------------------------------
def stop_hotspot():
    print("Stopping Mem-O-Mart hotspot...")

    result = subprocess.run(
        [
            "nmcli",
            "connection",
            "down",
            HOTSPOT_CONNECTION
        ],
        capture_output=True,
        text=True,
        timeout=10
    )

    # Force the physical interface to fully release AP mode
    subprocess.run(
        [
            "nmcli",
            "device",
            "disconnect",
            WIFI_INTERFACE
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        # It's okay if the hotspot was already inactive.
        print("Hotspot was already inactive or could not be stopped.")
        return False

    print("Mem-O-Mart hotspot stopped.")
    return True

# -------------------------------------------------------------------
# get_current_mode: Extract the active connection. Returns false
# if unsuccessful
# -------------------------------------------------------------------
def get_current_mode():
    # If wlan0 is connected to a normal Wi-Fi connection,
    # consider that development mode.
    if get_wifi_state() == "connected":
        return "development"

    # Check whether hotspot is active.
    result = run_nmcli(
        [
            "-t",
            "-f",
            "NAME",
            "connection",
            "show",
            "--active"
        ]
    )

    if result is None:
        return "unknown"

    active_connections = result.stdout.splitlines()

    if HOTSPOT_CONNECTION in active_connections:
        return "business"

    return "unknown"

# -------------------------------------------------------------------
# enter_development_mode: Turn off the hotspot and turn on the wifi
# connection
# -------------------------------------------------------------------
def enter_development_mode():
    print("Entering DEVELOPMENT mode")

    # Allow wlan0 to autoconnect again.
    subprocess.run(
        [
            "nmcli",
            "device",
            "set",
            WIFI_INTERFACE,
            "autoconnect",
            "yes"
        ],
        capture_output=True,
        text=True
    )

    stop_hotspot()

    time.sleep(1)

    if activate_wifi():
        network_led.off()
        return True

    print("No Wi-Fi available. Falling back to hotspot.")
    return start_hotspot()
    # # Make sure the hotspot isn't running.
    # stop_hotspot()

    # # Give NetworkManager a moment to release the interface.
    # time.sleep(1)

    # # Try normal Wi-Fi.
    # if activate_wifi():
    #     network_led.off()
    #     print("Development mode active.")
    #     return True

    # # No usable Wi-Fi was found.
    # print("No usable Wi-Fi connection found.")
    # print("Falling back to Mem-O-Mart hotspot.")

    # if start_hotspot():
    #     print("Development mode active using fallback hotspot.")
    #     return True

    # print("ERROR: Could not establish any network connection.")
    # return False

# -------------------------------------------------------------------
# enter_business_mode: Turn off the wifi connection and turn on the
# hotspot
# -------------------------------------------------------------------
def enter_business_mode():
    print("Entering BUSINESS mode")

    # Prevent normal Wi-Fi profiles from automatically reconnecting.
    result = subprocess.run(
        [
            "nmcli",
            "device",
            "set",
            WIFI_INTERFACE,
            "autoconnect",
            "no"
        ],
        capture_output=True,
        text=True
    )

    print(f"Disable Wi-Fi autoconnect: {result.returncode}")
    print(result.stdout)
    print(result.stderr)

    # Disconnect current Wi-Fi connection.
    result = subprocess.run(
        [
            "nmcli",
            "device",
            "disconnect",
            WIFI_INTERFACE
        ],
        capture_output=True,
        text=True
    )

    print(f"Disconnect Wi-Fi: {result.returncode}")
    print(result.stdout)
    print(result.stderr)

    time.sleep(1)

    # Start hotspot.
    return start_hotspot()
    # # Stop normal Wi-Fi.
    # print("Disconnecting normal Wi-Fi...")

    # result = subprocess.run(
    #     [
    #         "nmcli",
    #         "device",
    #         "disconnect",
    #         WIFI_INTERFACE
    #     ],
    #     capture_output=True,
    #     text=True,
    #     timeout=10
    # )

    # if result.returncode != 0:
    #     print("Warning: Wi-Fi may already be disconnected.")

    # time.sleep(1)

    # # Start the hotspot.
    # if start_hotspot():
    #     network_led.on()
    #     print("Business mode active.")
    #     return True

    # print("ERROR: Could not start Mem-O-Mart hotspot.")
    # return False

# -------------------------------------------------------------------
# toggle_network_mode: Toggle the state of the network when the
# button is pressed
# -------------------------------------------------------------------
def toggle_network_mode():
    print()
    print("Network mode button pressed.")

    current_mode = get_current_mode()

    print(f"Current network mode: {current_mode}")

    if current_mode == "development":
        enter_business_mode()

    elif current_mode == "business":
        enter_development_mode()

    else:
        print("Network mode is unknown.")
        print("Attempting to enter development mode.")

        enter_development_mode()

# -------------------------------------------------------------------
# activate_wifi: Attempt to connect to a known wifi network.
# -------------------------------------------------------------------
def activate_wifi():
    print("Attempting to connect to available Wi-Fi...")

    result = run_nmcli(
        ["device", "connect", WIFI_INTERFACE],
        timeout=10
    )

    if result is None:
        print("NetworkManager could not initiate Wi-Fi connection.")
        return False

    # NetworkManager may return before the connection is completely
    # established, so wait for the interface to actually become connected.
    start_time = time.monotonic()

    while time.monotonic() - start_time < WIFI_TIMEOUT:

        state = get_wifi_state()

        if state == "connected":
            print("Wi-Fi connected successfully.")
            return True

        time.sleep(0.5)

    print(
        f"Wi-Fi connection timed out after {WIFI_TIMEOUT} seconds."
    )

    return False

# -------------------------------------------------------------------
# Setup: Configure the button and LED
# -------------------------------------------------------------------
def Setup():
    global network_button, network_led

    network_led = PWMLED(24, initial_value=False)
    network_button = Button(23, pull_up=True, bounce_time=0.1)
    network_button.when_pressed = toggle_network_mode
    
    # Tell the pi to connect to a known host, if possible
    enter_development_mode()