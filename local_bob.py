import xbee

addr_modul_b = b'\x00\x13\xA2\x00\x41\xAE\x9D\x54'
print("local_bob is running\n")
message_payload = "Hallo von MicroPython an API!"
for i in range(3):
    try:
        xbee.transmit(addr_modul_b, message_payload)
        print("Nachricht gesendet.")
    except Exception as e:
        print("Fehler beim Senden:", e)
