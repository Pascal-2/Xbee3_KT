import xbee
import time

# --- Konfiguration ---
# WICHTIG: Trage hier die 64-Bit-Adresse deines entfernten Moduls ein!
REMOTE_ADDRESS = b'\x00\x13\xA2\x00\x41\xAE\x9D\x54'  # Adresse des Remote-Geräts (SH+SL)

NUM_ROUNDS = 20  # Anzahl der Testrunden
RESPONSE_TIMEOUT_MS = 2000  # Wartezeit für die Antwort in Millisekunden

# --- Initialisierung ---
# Datenstruktur zum Speichern der Ergebnisse
results = {
    'success_count': 0,
    'local_rssi': [],
    'remote_rssi': [],
}

print("--- Single-Device Range Test Start ---")
print("Zielgerät: ", REMOTE_ADDRESS)
#print(f"Test wird mit {NUM_ROUNDS} Runden durchgeführt.")
#print(f"Timeout pro Runde: {RESPONSE_TIMEOUT_MS} ms")
#print("-" * 35)

# --- Haupt-Testschleife ---
for i in range(NUM_ROUNDS):
    #print(f"Runde {i + 1}/{NUM_ROUNDS}...")
    print("Runde: ", i + 1)

    # 1. Leere den Empfangspuffer, um alte Pakete zu verwerfen
    while xbee.receive() is not None:
        pass

    # 2. Sende PING-Nachricht an das entfernte Gerät
    try:
        xbee.transmit(REMOTE_ADDRESS, "PING")
    except Exception as e:
        print("  Fehler beim Senden: ", e)
        time.sleep(1)  # Kurze Pause vor der nächsten Runde
        continue

    # 3. Warte auf eine Antwort mit Timeout
    while True:
        packet = xbee.receive()  # Warte maximal die Timeout-Zeit !!!gestrichen!!!
        if packet:
            break

    if packet:
        #sender_addr = packet.get('sender_eui64')

        # Sicherstellen, dass die Antwort vom richtigen Gerät kommt
        if True:#if sender_addr == REMOTE_ADDRESS:
            try:
                # Lokalen RSSI des Antwortpakets auslesen
                local_rssi = packet.get('rssi', 0)
                if local_rssi == 0:
                    local_rssi = xbee.atcmd('DB')
                # Entfernten RSSI aus der Nutzlast des Antwortpakets auslesen
                remote_rssi_from_payload = int(packet.get('payload', b'0').decode()) # = int.from_bytes(received_packet['payload'], 'big')

                # Ergebnisse speichern
                results['success_count'] += 1
                results['local_rssi'].append(local_rssi)
                results['remote_rssi'].append(remote_rssi_from_payload)

                #print(
                #    f"  Antwort erhalten! Lokaler RSSI: {local_rssi} dBm | Entfernter RSSI: {remote_rssi_from_payload} dBm")
                print("Antwort erhalten: Local RSSI, Remote RSSI: ", local_rssi, remote_rssi_from_payload)

            except (ValueError, TypeError) as e:
                print("  Fehlerhafte Antwort empfangen: ", e)
        else:
            print("  Antwort von unerwartetem Gerät empfangen. ")
    else:
        # Timeout ist aufgetreten
        print("  Timeout: Keine Antwort erhalten.")

    time.sleep(1)  # Pause zwischen den Runden

# --- Auswertung und Ergebnispräsentation ---
print("\n--- Testergebnisse ---")


def calculate_mean(data_list):
    if not data_list:
        return 0
    return sum(data_list) / len(data_list)


success_percentage = (results['success_count'] / NUM_ROUNDS) * 100
print("Erfolgsrate: ", results['success_count'], NUM_ROUNDS, success_percentage)

if results['success_count'] > 0:
    # Statistik für Lokalen RSSI (Rückweg)
    min_local = min(results['local_rssi'])
    max_local = max(results['local_rssi'])
    mean_local = calculate_mean(results['local_rssi'])
    print("Lokaler RSSI (Rückweg): Min, Max, Mean: ", min_local, max_local, mean_local)

    # Statistik für Entfernten RSSI (Hinweg)
    min_remote = min(results['remote_rssi'])
    max_remote = max(results['remote_rssi'])
    mean_remote = calculate_mean(results['remote_rssi'])
    print("Entfernter RSSI (Hinweg): Min, Max, Mean: ", min_remote, max_remote, mean_remote)
else:
    print("Keine erfolgreichen Uebertragungen, keine RSSI-Daten.")

print("\n--- Test beendet ---")
