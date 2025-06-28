import xbee
import time

addr_modul_b = b'\x00\x13\xA2\x00\x41\xAE\x9D\x54'
print("bob_sends_n is running\n")
for i in range(20):
    xbee.transmit(addr_modul_b, i.to_bytes(1, 'big'))
    print("Nachricht gesendet.")
    received_packet = xbee.receive()
    if received_packet:
        rssi = received_packet.get('rssi', 0)
        print(f"My RSSI: {rssi}, Remote RSSI: {received_packet}")
    time.sleep(4)


