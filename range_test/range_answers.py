import xbee
import time

LOCAL_ADDRESS = b'\x00\x13\xA2\x00\x41\x98\x18\x31'
print("--- Remote Slave (Single) gestartet ---")
print("Warte auf PING-Nachrichten...")

# Endlosschleife zum Empfangen und Antworten
while True:
    try:
        # Warte blockierend auf ein eingehendes Paket
        while True:
            packet = xbee.receive()
            if packet:
                break
        print("got something")
        # Absenderadresse und RSSI des eingehenden Pakets auslesen
        #sender_addr = packet.get('sender_eui64')
        rssi = packet.get('rssi', 0)  # Lese RSSI, Standardwert 0 falls nicht vorhanden
        if rssi == 0:
            rssi = xbee.atcmd('DB')
        print("read rssi: ", rssi)
        #payload = packet.get('payload')

        # Nur auf "PING" Nachrichten reagieren
        #if payload == b'PING':
        #print(f"PING von {sender_addr.hex()} empfangen mit RSSI: {rssi} dBm")

        # Sende den gemessenen RSSI-Wert als String zurück an den Absender
        response_payload = str(rssi)
        xbee.transmit(LOCAL_ADDRESS, response_payload)
        #print(f"  Antwort mit RSSI-Wert '{response_payload}' gesendet.")
        print("sent answer")

    except Exception as e:
        print("Fehler")
        #print(f"Ein Fehler ist aufgetreten: {e}")
        # Kurze Pause vor dem nächsten Versuch, um Fehler-Loops zu vermeiden
        time.sleep(1)

