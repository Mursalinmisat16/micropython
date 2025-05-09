from machine import Pin
from machine import Timer
from time import sleep_ms
import ubluetooth

message = ""

class ESP32_BLE():
    def __init__(self, name):
        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.conn_handle = None  # Store connection handle
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self, conn_handle):
        self.conn_handle = conn_handle
        self.led.value(1)
        self.timer1.deinit()

    def disconnected(self):
        self.conn_handle = None
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    def ble_irq(self, event, data):
        global message
        if event == 1:  # _IRQ_CENTRAL_CONNECT
            conn_handle, _, _ = data
            self.connected(conn_handle)

        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT
            self.advertiser()
            self.disconnected()
        
        elif event == 3:  # _IRQ_GATTS_WRITE
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            print(message)

    def register(self):        
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART,)
        ((self.tx, self.rx,),) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        if self.conn_handle is not None:
            self.ble.gatts_notify(self.conn_handle, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = b'\x02\x01\x02' + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print(adv_data)


led = Pin(2, Pin.OUT)
but = Pin(0, Pin.IN)
ble = ESP32_BLE("ESP32")

def buttons_irq(pin):
    led.value(not led.value())
    ble.send('LED state will be toggled.')
    print('LED state will be toggled.')   

but.irq(trigger=Pin.IRQ_FALLING, handler=buttons_irq)

while True:
    if message == "STATUS":
        message = ""
        ble.send('LED is ON.' if led.value() else 'LED is OFF')
    sleep_ms(100)
