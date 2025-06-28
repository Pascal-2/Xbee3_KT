import xbee
import time
from machine import Pin

addr_modul_b = b'\x00\x13\xA2\x00\x41\xAE\x9D\x54'
print("bob_sends_n is running\n")
for i in range(20):
    try:
        xbee.transmit(addr_modul_b, i.to_bytes(1, 'big'))
        print("Nachricht gesendet.")
        time.sleep(4)
    except Exception as e:
        print("Fehler beim Senden:", e)
