# Mem-O-Mart
Codebase for Mem-O-Mart, an Atlanta-based installation meant to deliver spontaneous moments to its users.

## Author(s)
Dean Badr

## Connecting to the PI
If the raspberry pi for the device was configured consistently with the other existing devices, a connection with it can be established at:
_memomart@memomart.local_

If you are on a device that has previously connected to a device with the same name, you may need to remove knowledge of the previous host with:
_ssh _

## Useful Commands
The follow lines are useful terminal commands that help control and inspect the service:

_Restart the currently running service_\
`sudo systemctl restart memomart.service`
<br><br>
_Stop the currently running service_\
`sudo systemctl stop memomart.service`
<br><br>
_Start the service if it is not already running_\
`sudo systemctl start memomart.service`
<br><br>
_View a live feed of logging from the service_\
`journalctl -u memomart.service -f`
<br><br>
_Observe the throttled status of the raspberry pi_\
`vcgencmd get_throttled`

## Notes
Refer to `/src/settings.py` for the main configuration parameters of the machine. Most of these settings will give the user the flexibility to operate the machine as desired.
