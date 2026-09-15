import subprocess

class HotspotManager:
	def __init__(self, interface="wlan0", hotspotConnection="FM-Hotspot"):
		self.interface = interface
		self.connection_name = hotspotConnection
		self.ssid = "FM Hotspot"
		self.password = "Pura_Vida"
		
	def status(self):
		result = subprocess.run(
			[
				"nmcli",
				"connection",
				"show",
				"--active",
			],
			capture_output=True,
			text=True,
		)
		
		if result.returncode != 0:
			return {
				"success": False,
				"error": result.stderr.strip(),
			}
			
		connected = False
		for line in result.stdout.splitlines():
			if self.connection_name in line:
				connected = True
				break
				
		return {
			"success": True,
			"active": connected,
			"interface": self.interface,
			"ssid": self.ssid,
		}
		
	def start(self):
		result = subprocess.run(
			[
				"nmcli",
				"device",
				"wifi",
				"hotspot",
				"ifname",
				self.interface,
				"con-name",
				self.connection_name,
				"ssid",
				self.ssid,
				"password",
				self.password,
			],
			capture_output=True,
			text=True,
		)
		
		
		if result.returncode != 0:
			return {"success": False, "error": result.stderr.strip(),}
			
		return {
			"success": True,
			"active": True,
			"interface": self.interface,
			"ssid": self.ssid,
		}
		
	def stop(self):
		result = subprocess.run(
			[
				"nmcli",
				"connection",
				"down",
				self.connection_name,
			],
			capture_output=True,
			text=True,
		)
		
		if result.returncode != 0:
			return {"success": False, "error": result.stderr.strip(),}
			
		return {
			"success": True,
			"active": False,
			"interface": self.interface,
			"ssid": self.ssid,
		}
