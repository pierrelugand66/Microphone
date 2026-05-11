import socket
import time

def calculer_checksum(trame_sans_chk):
    resultat = 0
    for char in trame_sans_chk:
        resultat ^= ord(char)
    return format(resultat, '02X')

def construire_trame(trame_sans_chk):
    chk = calculer_checksum(trame_sans_chk)
    return f"{trame_sans_chk};CHK:{chk}"

IP_DEST = "127.0.0.1"
PORT_DEST = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Trame ADC
trame_adc = construire_trame("ID:01;TYPE:ADC;VAL:3.27;UNIT:V;TS:1714823456")

# Trame FFT avec données
data_fft = ",".join([str(round(abs(16 - i) * 10.0, 2)) for i in range(32)])
trame_fft = construire_trame(f"ID:01;TYPE:FFT;FMAX:5000;BINS:32;DATA:{data_fft};TS:1714823456")

# ACK WAKE
trame_ack = construire_trame("ACK:WAKE;ID:02;SEQ:001;STATUS:OK")

trames = [trame_ack, trame_adc, trame_fft]

for trame in trames:
    sock.sendto(trame.encode("utf-8"), (IP_DEST, PORT_DEST))
    print(f"Envoyé : {trame[:60]}...")
    time.sleep(1)

sock.close()