# About Mem-O-Mart
Codebase for Mem-O-Mart, an Atlanta-based installation meant to deliver spontaneous moments to its users.

# Author(s)
Dean Badr

# Setting up a new PI
## PI Imager
Install the raspberry pi imager from: <br>
https://www.raspberrypi.com/software/
<br><br>
Plug in a microSD card of _at least 16 GB_ to your device, then follow the prompts in the imager. 
<br><br>
__Notes:__
- Set the hostname of the pi to a unique string that doens't match the other established pi devices. This helps prevent cache conflicts when using the same device to connect to multiple devices.
- Ensure __ssh__ is enabled. It is recommended to use the ssh keys for connecting to the pi, but not required.

### Generating Keys
On your device, open the terminal/powershell and run the following command to generate the private and public keys.
<br>
`ssh-keygen -t ed25519 -y`
<br><br>
Next, copy the public key into the corresponding field in the raspberry pi imager GUI. To view and copy the key via terminal/powershell, run: <br><br>
__[Mac]__<br>
`pbcopy < ~/.ssh/id_ed25519.pub`
<br><br>
__[Linux] (requires xclip)__<br>
`xclip -sel clip < ~/.ssh/id_ed25519.pub`
<br><br>
__[Windows]__<br>
`Get-Content $HOME/.ssh/id_ed25519.pub | Set-Clipboard`

### Connecting to the PI
This step slightly varies depending on if the pi's ssh was configured to use keys or the device password. For __both__ setups, ensure the external device is on the same network as the one defined in the pi imager.
<br><br>
Begin by attempting to connect to the pi with its user and host name. This can be done either through a terminal or IDE ssh extension: <br>
`<username>@<hostname>.local`
<br><br>

If ssh keys are being used and were setup correctly, then the devices should seamlessly connect. If password setup was configured in the imager than you must enter the defined password every time.

__Notes:__<br>
- The user and host name is defined in the imaging step.
- If your external device has previously connected to a _different_ pi that shares the same hostname, you may need to remove knowledge of the previous host with: `ssh-keygen -R <hostname>`

### Repository Setup
1. Ensure git is installed on the raspberry pi:<br>
`sudo apt update`<br>
`sudo apt install git`

2. Change directories into the desired project director and clone this repo: <br>
`cd <path>/<to>/<projects>` <br>
`git clone https://github.com/thedean111/memomart`

3. Run the system setup script: <br>
`chmod +x setup_pi.sh && ./setup_pi.sh`

4. Create a virtual environment that has visibility of the system packages: <br>
`python3 -m venv --system-site-packages .venv`

5. Activate the virtual environment and install the python dependencies for the project: <br>
`source .venv/bin/activate` <br>
`pip install -r requirements.txt`

# Configuring the Service
To run the software on boot, a systemd service should be setup on the new pi.

The service file may be created with nana or another text editor, but essential we want `<filename>.service` file placed at `/etc/systemd/system/`, so the final path would be: <br>
`/etc/systemd/system/<filename>.service`

Within this service file the following outline should be followed: <br>
```
[Unit]
Description=Mem-O-Mart Photobooth
After=network.target

[Service]
Type=simple
User=<username>
WorkingDirectory=<path>/<to>/<memomart>/<repository>
ExecStart=<path>/<to>/<memomart>/<repository>/.venv/bin/python <path>/<to>/<memomart>/<repository>/src/memomart.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Next, run the following lines to enable and start the service:
```
sudo systemctl daemon-reload
sudo systemctl enable memomart.service
sudo systemctl start memomart.service
```
# Useful Commands
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

## Customization
Refer to `/src/settings.py` for the main configuration parameters of the machine. Most of these settings will give the user the flexibility to operate the machine as desired.

### Configuring a new printer
These steps will be useful when trying to connect a new printer to the current architecture. The values we are looking to define correctly are:<br>
`PRINTER_VID = 0x0485` -> vendor ID<br>
`PRINTER_PID = 0x5741` -> product ID<br>
`PRINTER_OUT = 0x02`-> output endpoint<br>
`PRINTER_IN = 0x82` -> input endpoint

__VID and PID__<br>
The VID and PID can easily be identified using the `lsusb` command on the pi. If there is not an obvious device named "thermal printer" or something similar, it is easiest to:
1. Execute the `lsusb`
2. Unplug the printer from usb port
3. Execute the `lsusb` again
4. Identify the device that is missing the second time.

The device will be listed in the format of: <br>
`Bus <num> Device <num>: ID <VID>:<PID> <some port name>`
__Endpoints__ <br>
The input and output endpoints can be seen by printing the details of the device, once the VID and PID are obtained: <br>
`sudo lsusb -v -d <VID>:<PID>`

Scan the printed information for `bEndpointAddress`. This will provide the hexidecimal endpoint address to use for the printer, along with if its the output or input endpoint: <br>
`bEndpointAddress <hex>  EP 2 <in/out>`

__Permissions__<br>
When using a new printer, there is a good chance the python code will not have permission to send data directly to the printer across the USB connection. To resolve the a _udev_ rule should be setup to reconfigure the permissions.

From a terminal on the pi, run:<br>
`sudo nano /etc/udev/rules.d/99-memomart-printer.rules`

This will open the file `99-memomart-printer.rules`. It is prefixed by "99" so that these rules load towards the end and overwrite rules defined before it. In this file, copy and paste the following line (_0666 gives read + write permission to everyone on the device_): <br>
`SUBSYSTEM=="usb", ATTR{idVendor}=="0485", ATTR{idProduct}=="5741", MODE="0666"`

When copied, you can save and exit with the following key-strokes: <br>
- Ctrl+O
- Enter
- Ctrl+X

Now, reload the rules
```
sudo udevadm control --reload-rules
sudo udevadm trigger
```
