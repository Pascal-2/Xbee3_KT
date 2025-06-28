import xbee
from machine import Pin
import time
led = Pin("D4", Pin.OUT)
print("remote_receiving_n is running\n")

while True:
    received_packet = xbee.receive()
    if received_packet:
        n = int.from_bytes(received_packet['payload'], 'big')
        for i in range(n):
            led.value(0)
            time.sleep_ms(100)
            led.value(1)
            time.sleep_ms(100)
