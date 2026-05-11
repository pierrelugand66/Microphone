import struct


def calculer_checksum(trame_sans_chk):
    """Calcule un checksum XOR sur la trame"""
    resultat = 0
    for char in trame_sans_chk:
        resultat ^= ord(char)
    return format(resultat, '02X')

def verifier_checksum(trame):
    """Vérifie l'intégrité de la trame"""
    try:
        parties = trame.rsplit(";CHK:", 1)
        if len(parties) != 2:
            return False
        chk_recu = parties[1]
        chk_calcule = calculer_checksum(parties[0])
        return chk_recu == chk_calcule
    except:
        return False

def parser_trame(trame):
    """
    Parse une trame texte et retourne un dictionnaire
    Exemple : ID:01;TYPE:ADC;VAL:3.27;UNIT:V;TS:1714823456;CHK:A3
    Retourne : {'ID':'01', 'TYPE':'ADC', 'VAL':'3.27', 'UNIT':'V', 'TS':'1714823456', 'CHK':'A3'}
    """
    try:
        # Vérification checksum
        if not verifier_checksum(trame):
            print(f"Checksum invalide : {trame}")
            return None

        # Parse les champs
        champs = {}
        for partie in trame.split(";"):
            if ":" in partie:
                cle, valeur = partie.split(":", 1)
                champs[cle.strip()] = valeur.strip()

        # Vérification champs obligatoires
        champs_obligatoires = ["ID", "TYPE", "TS", "CHK"]
        for champ in champs_obligatoires:
            if champ not in champs:
                print(f"Champ manquant : {champ}")
                return None

        # Conversion des types
        champs["TS"] = int(champs["TS"])

        # Trame simple (VAL)
        if "VAL" in champs:
            champs["VAL"] = float(champs["VAL"])

        # Trame bloc (DATA)
        if "DATA" in champs:
            champs["DATA"] = [float(x) for x in champs["DATA"].split(",")]
            if "BINS" in champs:
                champs["BINS"] = int(champs["BINS"])
            if "FMAX" in champs:
                champs["FMAX"] = float(champs["FMAX"])
            if "SR" in champs:
                champs["SR"] = float(champs["SR"])
            if "SAMPLES" in champs:
                champs["SAMPLES"] = int(champs["SAMPLES"])

        return champs

    except Exception as e:
        print(f"Erreur parsing : {e} — trame : {trame}")
        return None

def parser_ack(ack):
    """
    Parse un ACK reçu de la carte
    Exemple : ACK:WAKE;ID:02;SEQ:001;STATUS:OK;CHK:YY
    """
    try:
        champs = {}
        for partie in ack.split(";"):
            if ":" in partie:
                cle, valeur = partie.split(":", 1)
                champs[cle.strip()] = valeur.strip()
        return champs
    except Exception as e:
        print(f"Erreur parsing ACK : {e}")
        return None
    

def parser_trame_binaire(data):
    """Parse un paquet binaire MIC"""
    try:
        if len(data) < 10:
            return None

        magic    = data[0]
        id_carte = data[1]
        bins     = struct.unpack_from('<H', data, 2)[0]
        ts       = struct.unpack_from('<H', data, 4)[0]
        rssi     = struct.unpack_from('b',  data, 6)[0]
        crc_recu = struct.unpack_from('<H', data, 8)[0]

        nb_samples = (len(data) - 10) // 2
        samples = struct.unpack_from(f'<{nb_samples}h', data, 10)

        # Vérifier CRC
        crc_calcule = 0
        for s in samples:
            crc_calcule ^= (s & 0xFFFF)

        if crc_recu != crc_calcule:
            print(f"CRC invalide : recu={crc_recu} calcule={crc_calcule}")
            return None

        return {
            "ID":   f"{id_carte:02d}",
            "TYPE": "MIC",
            "BINS": bins,
            "TS":   ts,
            "RSSI": rssi,
            "DATA": list(samples)
        }
    except Exception as e:
        print(f"Erreur parsing binaire : {e}")
        return None
