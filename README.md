# Mem-O-Mart
Codebase for Mem-O-Mart, an Atlanta-based installation meant to deliver spontaneous moments to its users.

## Author(s)
Dean Badr

## Useful Commands
The follow lines are useful terminal commands that help control and inspect the service:

_Restart the currently running service_
`sudo systemctl restart memomart.service`
<br>
_Stop the currently running service_
`sudo systemctl stop memomart.service`
<br>
_Start the service if it is not already running_
`sudo systemctl start memomart.service`
<br>
_View a live feed of logging from the service_
`journalctl -u memomart.service -f`
<br>
_Observe the throttled status of the raspberry pi_
`vcgencmd get_throttled`

## Notes
Refer to `/src/settings.py` for the main configuration parameters of the machine. Most of these settings will give the user the flexibility to operate the machine as desired.