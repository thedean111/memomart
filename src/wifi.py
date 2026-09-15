import subprocess
import time

class WifiManager:
    def __init__( self, interface="wlan0", connect_timeout=15, poll_interval=0.5, hotspotConnection="FM-Hotspot", connectionName="FM-Wifi" ): 
        self.interface = interface 
        self.connect_timeout = connect_timeout 
        self.poll_interval = poll_interval
        self.hotspot = hotspotConnection
        self.connectionName = connectionName

    # -------------------------------------------------------------------
    # exists: Does the wifi connection profile exist
    # -------------------------------------------------------------------
    def exists(self):
        result = subprocess.run(
            ["nmcli", "connection", "show", self.connectionName],
            capture_output=True,
            text=True,
        )

        return result.returncode == 0

    # -------------------------------------------------------------------
    # status: Retrieves the status of the Wi-Fi interface
    # -------------------------------------------------------------------
    def status(self):
        result = subprocess.run(
            [
                "nmcli",
                "-t",
                "-f",
                "GENERAL.CONNECTION",
                "device",
                "show",
                self.interface,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr.strip(),
            }

        connection = None
        for line in result.stdout.splitlines():
            if line.startswith("GENERAL.CONNECTION:"):
                connection = line.split(":", 1)[1]
                break

        connected = connection == self.connectionName   
        if not connected:
            return {
                "success": True,
                "connected": False,
                "interface": self.interface,
            }

        # Get IP
        result = subprocess.run(
            [
                "nmcli",
                "-t",
                "-f",
                "IP4.ADDRESS",
                "device",
                "show",
                self.interface,
            ],
            capture_output=True,
            text=True,
        )

        ip = None

        for line in result.stdout.splitlines():
            if line.startswith("IP4.ADDRESS:"):
                ip = line.split(":", 1)[1].split("/", 1)[0]
                break

        # Get SSID
        result = subprocess.run(
            [
                "nmcli",
                "-t",
                "-f",
                "802-11-wireless.ssid",
                "connection",
                "show",
                self.connectionName,
            ],
            capture_output=True,
            text=True,
        )

        ssid = None

        for line in result.stdout.splitlines():
            if line.startswith("802-11-wireless.ssid:"):
                ssid = line.split(":", 1)[1]
                break

        return {
            "success": True,
            "connected": True,
            "interface": self.interface,
            "ssid": ssid,
            "ip": ip,
        }

    # -------------------------------------------------------------------
    # connect_saved: Try and connect to the saved wifi profile
    # -------------------------------------------------------------------
    def connect_saved(self):
        if not self.exists():
            return {
                "success": False,
                "configured": False,
                "error": "MemoMart Wi-Fi profile does not exist",
            }

        result = subprocess.run(
            [
                "nmcli",
                "connection",
                "up",
                self.connectionName,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "configured": True,
                "error": result.stderr.strip(),
            }

        return {
            "success": True,
            "configured": True,
            "connected": True,
        }
    
    # -------------------------------------------------------------------
    # connect: Connects to a Wi-Fi network
    # -------------------------------------------------------------------
    def connect(self, ssid, password):
        # Check whether our profile already exists
        result = subprocess.run(
            [
                "nmcli",
                "connection",
                "show",
                self.connectionName,
            ],
            capture_output=True,
            text=True,
        )

        # Profile doesn't exist so create it
        if result.returncode != 0:
            # Profile doesn't exist, so create it
            result = subprocess.run(
                [
                    "nmcli",
                    "connection",
                    "add",
                    "type",
                    "wifi",
                    "ifname",
                    self.interface,
                    "con-name",
                    self.connectionName,
                    "ssid",
                    ssid,
                    "connection.autoconnect",
                    "no",
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                return {
                    "success": False,
                    "error": result.stderr.strip()
            }

        # Update the profile with the requested Wi-Fi
        result = subprocess.run(
            [
                "nmcli",
                "connection",
                "modify",
                self.connectionName,
                "802-11-wireless.ssid",
                ssid,
                "wifi-sec.key-mgmt",
                "wpa-psk",
                "wifi-sec.psk",
                password,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr.strip()
            }

        # Activate the profile
        result = subprocess.run(
            [
                "nmcli",
                "connection",
                "up",
                self.connectionName,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr.strip()
            }

        return {
            "success": True,
            "connected": True,
            "ssid": ssid,
            "interface": self.interface,
        }
    
    # -------------------------------------------------------------------
    # disconnect: Disconnects from the current Wi-Fi network
    # -------------------------------------------------------------------
    def disconnect(self):
        result = subprocess.run(
            [
                "nmcli",
                "device",
                "disconnect",
                self.interface,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr.strip()
            }
            
        return {
            "success": True,
            "connected": False,
            "interface": self.interface,
        }
