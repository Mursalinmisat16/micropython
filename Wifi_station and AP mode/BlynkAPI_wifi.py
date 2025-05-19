import network
import urequests
import time
from machine import Pin

but_status =0
but_flag = 0
Status = 0

but = Pin(0,Pin.IN)

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect('ssid','password')
    if not wifi.isconnected():
        print('connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout <5):
            print( 5- timeout)
            timeout = timeout + 1
            time.sleep(1)
    if (wifi.isconnected()):
        print('connected!')
    else:
        print('not connected!')

def buttons_irq(pin):
    global but_status
    global but_flag
    but_status = not but_status
    but_flag = 1
but.irq(trigger = Pin.IRQ_FALLING, handler = buttons_irq)
connect_wifi()

while True:
    if (but_status ==True and but_flag ==1):
        req = urequests.get('https://blynk.cloud/dashboard/528066/global/devices/1')
        but_flag =0
        Status = req.status_code
        if(Status ==200):
            print("request successful")
            print("Light ON")
            req.close()
        elif(but_status == False and but_flag ==1):
         req = urequests.get('https://blynk.cloud/dashboard/528066/global/devices/0')
         but_flag = 0
         Status = req.status_code
         if(Status ==200):
            print("request successful")
            print("Light OFF")
            req.close()
        
        