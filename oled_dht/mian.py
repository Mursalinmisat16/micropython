from machine import Pin,SoftI2C
import dht
import time
import ssd1306

i2c = SoftI2C(scl=Pin(22),sda=Pin(21))

oled=ssd1306.SSD1306_I2C(128,64,i2c)

sensor = dht.DHT11(Pin(5))  # Use GPIO4 instead of 15

def call_dht():
    try:
        global temp
        global hum
        temp = sensor.temperature()
        hum = sensor.humidity()
        print('Temp:', temp, '°C', 'Humidity:', hum, '%')
    except OSError as e:
        print("Failed to connect", e)

while True:
    call_dht()
    oled.text('Temp:',0,0)
    oled.text(str(temp),110,0)
    oled.text('Humidity:',0,10)
    oled.text(str(hum),110,10)
    oled.show()
    time.sleep(2)
