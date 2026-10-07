from wifi import WifiManager
from hotspot import HotspotManager
from networkManager import NetworkManager

import os

print("UID:", os.getuid())
print("EUID:", os.geteuid())
print("USER:", os.environ.get("USER"))

'''
wifi = WifiManager()
print(wifi.get_status())
result = wifi.connect("TheHub5", "Zadega201316!")
print(result)
print(wifi.get_status())
result = wifi.disconnect()
print(result)
print(wifi.get_status())
'''

'''
hotspot = HotspotManager()
print(hotspot.status())
print(hotspot.stop())
print(hotspot.status())
'''

# nm = NetworkManager()
# print(nm.status())
# print(nm.start())
# print(nm.wifi.disconnect())
# print(nm.start())
# print(nm.status())
# print(nm.connect("TheHub5", "Zadega201316!"))
# print(nm.status())

