import xbee

print("remote_receiving_n is running\n")
addr_modul_a = b'\x00\x13\xA2\x00\x41\x98\x18\x31'

while True:
    received_packet = xbee.receive()
    if received_packet:
        rssi = received_packet.get('rssi', 0)
        xbee.transmit(addr_modul_a, rssi)
        print("Nachricht gesendet.")
