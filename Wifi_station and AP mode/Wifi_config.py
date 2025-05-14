import network
import time

timeout = 0


wifi = network.WLAN(network.STA_IF)
wifi.active(False)
time.sleep(0.5)
wifi.active(True)

wifi.connect('ssid','password')

if not wifi.isconnected():
  print('connecting...')
  while (not wifi.isconnected() and timeout < 5):
      print(5-timeout)
      timeout = timeout + 1
      time.sleep(1)


if wifi.isconnected():
  print('wifi is connected!')
else:
    print('Timeout')

