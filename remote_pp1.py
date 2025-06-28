import xbee
print("remote is running\n")

while True:
    received_packet = xbee.receive()
    if received_packet:
        print("Nachricht empfangen!")
        print("Von:", received_packet['sender_eui64']) # EUI64 ist die 64-Bit Adresse
        print("Daten:", received_packet['payload'].decode())
