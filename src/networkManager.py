from wifi import WifiManager
from hotspot import HotspotManager

class NetworkManager:
    def __init__(self):
        con = "FM-Hotspot"
        self.wifi = WifiManager(hotspotConnection=con)
        self.hotspot = HotspotManager(hotspotConnection = con)

    # -------------------------------------------------------------------
    # status: What is the current state of wireless connection
    # -------------------------------------------------------------------
    def status(self):
        wifiStatus = self.wifi.status()
        hotspotStatus = self.hotspot.status()
        
        if not wifiStatus["success"]:
            return wifiStatus
        elif not hotspotStatus["success"]:
            return hotspotStatus
        
        return {
            "success": True,
            "wifi": wifiStatus,
            "hotspot": hotspotStatus,
        }

    # -------------------------------------------------------------------
    # start: Try and connect to wifi, if not wifi then open a hotspot
    # -------------------------------------------------------------------
    def start(self):
        wifiResult = self.wifi.connect_saved()
        if wifiResult["success"]:
            return {
                "success": True,
                "mode": "wifi",
            }
            
        hotspotStatus = self.hotspot.start()
        if not hotspotStatus["success"]:
            return hotspotStatus
            
        return {
            "success": True,
            "mode": "hotspot",
        }

    # -------------------------------------------------------------------
    # connect: Attempt wifi connection with the provided ssid and
    # password
    # -------------------------------------------------------------------
    def connect(self, ssid, password):
        result = self.wifi.connect(ssid, password)
        if not result["success"]:
            return result
            
        hotspot = self.hotspot.status()
        if hotspot["active"]:
            result = self.hotspot.stop()
            
            if not result["success"]:
                return result
            
        return {
            "success": True,
            "mode": "wifi",
            "ssid": ssid,
        }

    # -------------------------------------------------------------------
    # disconnect: Disconnect from wifi and open a hotspot
    # -------------------------------------------------------------------
    def disconnect(self):
        wifi_status = self.wifi.status()

        if not wifi_status["success"]:
            return wifi_status

        if wifi_status["connected"]:
            result = self.wifi.disconnect()

            if not result["success"]:
                return result

        hotspot_status = self.hotspot.status()

        if not hotspot_status["success"]:
            return hotspot_status

        if not hotspot_status["active"]:
            hotspot_status = self.hotspot.start()

            if not hotspot_status["success"]:
                return hotspot_status

        return {
            "success": True,
            "mode": "hotspot",
        }
