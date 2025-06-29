# XBee A (Sender)

import xbee
import time
from machine import I2C

MEGA_I2C_ADDR = 0x08

REMOTE_XBEE_ADDR = b'\x00\x13\xa2\x00\x41\xae\x9d\x54'

i2c = I2C(1, freq=100000)

print("--- XBee Sender (I2C Master) Running ---")
print("Reading from Arduino Mega at I2C address: ", MEGA_I2C_ADDR)

while True:
    try:
        distance_data = i2c.readfrom(MEGA_I2C_ADDR, 2)

        print("Read from Mega: {}".format(distance_data))

        xbee.transmit(REMOTE_XBEE_ADDR, distance_data)
        print("Transmitted to remote XBee.")

    except OSError as e:
        print("I2C Error: Could not read from Mega. Check wiring and address.", e)

    time.sleep_ms(200)