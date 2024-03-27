import board
import busio
from digitalio import DigitalInOut
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_airlift.esp32 import ESP32

class BleSensor:
    def __init__(self):
        """
        Initializes a BLE Echo object.
        """
        self.esp32 = ESP32()
        self.adapter = self.esp32.start_bluetooth()
        self.ble = BLERadio(self.adapter)
        self.uart = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart)

        self.ble.start_advertising(self.advertisement)
        print("Waiting to connect...")
        while not self.ble.connected:
            pass
        print("Connected!")

    def read_ble_if_able(self):
        line = b""
        one_byte = self.uart.read(1)
        line += one_byte
        if one_byte:
            while True:
                one_byte = self.uart.read(1)
                if one_byte:
                    # 如果读取到换行符，则停止
                    if one_byte == b'\n':
                        break
                    line += one_byte
        return line.decode('utf-8')
    
    def write_ble_if_able(self, word):
        if self.ble.connected:
            self.uart.write(word)

