import network
import time
import urequests

timeout = 0


wifi = network.WLAN(network.STA_IF)
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
  req=urequests.get('https://www.example.com')
  print(req.status_code)
  print(req.text)
  
else:
    print('Timeout')
    print('Not connected')


