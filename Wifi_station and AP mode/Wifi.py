import network

wifi = network.WLAN(network.AP_IF)
wifi.active(True)

wifi.config(essid ='mursa',password = '12345678', authmode = network.AUTH_WPA_WPA2_PSK)
print(wifi.ifconfig())
