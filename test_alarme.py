import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5001

def checksum(trame):
    resultat = 0
    for char in trame:
        resultat ^= ord(char)
    return format(resultat, '02X')

trame_sans_chk = "ID:TEST01;TYPE:ADC;VAL:5.0;UNIT:V;TS:1714823456"
chk = checksum(trame_sans_chk)
trame = f"{trame_sans_chk};CHK:{chk}"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(trame.encode("utf-8"), (UDP_IP, UDP_PORT))
print(f"Trame envoyée : {trame}")
sock.close()