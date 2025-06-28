import xbee
import time
from machine import I2C
import struct

MEGA_I2C_ADDR = 0x08

REMOTE_XBEE_ADDR = b'\x00\x13\xA2\x00\x41\xAE\x9D\x54'

i2c = I2C(1, freq=100000)

while True:
    try:
        distance_data = i2c.readfrom(MEGA_I2C_ADDR, 4)
        distance_float = struct.unpack("f", distance_data)[0]

        print("Read from Mega: ", distance_float)

        #xbee.transmit(REMOTE_XBEE_ADDR, distance_data)
        #print("Transmitted to remote XBee.")

    except OSError as e:
        print("I2C Error: Could not read from Mega. Check wiring and address.", e)

    time.sleep_ms(500)