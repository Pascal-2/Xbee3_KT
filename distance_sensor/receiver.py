import xbee
import time
from machine import I2C

NANO_I2C_ADDR = 0x09

i2c = I2C(1, freq=100000)

print("--- XBee Receiver (I2C Master) Running ---")
print("Writing to Arduino Nano at I2C address: ", NANO_I2C_ADDR)

while True:
    packet = xbee.receive()

    if packet:
        payload = packet['payload']
        print("Received wireless packet: ", payload)
        
        try:
            i2c.writeto(NANO_I2C_ADDR, payload)
            print("Wrote data to Nano via I2C.")
        
        except OSError as e:
            print("I2C Error: Could not write to Nano. Check wiring and address.", e)
            
    time.sleep_ms(10)