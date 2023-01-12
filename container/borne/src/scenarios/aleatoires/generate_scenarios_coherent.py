from datetime import datetime
import string
import random
import json

def generate_coordinates():
    res = { "lat": round(random.uniform(44.5, 45), 6), "lon": round(random.uniform(4.8, 5), 6)}

    return res

def generate_coordinates_close_to(lat, lon):
    # Ecart d'a peu pres 400 m maximum si les deux sont a +0.003
    ecart_lat = 0.0030
    ecart_lon = 0.0030

    lat_start = round(lat,6)
    lat_end = round(lat+ecart_lat,6)

    lon_start = round(lon,6)
    lon_end = round(lon+ecart_lon,6)

    res = { "lat": round(random.uniform(lat_start, lat_end), 6), "lon": round(random.uniform(lon_start, lon_end), 6)}

    return res

def generate_immatriculation():
    a = random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
    b = random.choice(string.digits) + random.choice(string.digits) + random.choice(string.digits)
    c = random.choice(string.ascii_letters) + random.choice(string.ascii_letters)

    return "-".join([a.upper(),b,c.upper()])

def generate_packet_perio(isembouteillage=False):
    if isembouteillage:
        # Generating first point
        a = { "type": "periodique"}

        a["vitesse"] = round(random.uniform(0, 80), 1)

        a["timestamp"] = round(datetime.timestamp(datetime.now()))
        a["immatriculation"] = generate_immatriculation()
    
        a["geo"] = generate_coordinates()

        # Generating second point close to first one
        b = { "type": "periodique"}

        b["vitesse"] = round(random.uniform(0, 80), 1)

        b["timestamp"] = round(datetime.timestamp(datetime.now()))
        b["immatriculation"] = generate_immatriculation()
    
        b["geo"] = generate_coordinates_close_to(a["geo"]["lat"], a["geo"]["lon"])

        # Generating third point close to second one
        c = { "type": "periodique"}

        c["vitesse"] = round(random.uniform(0, 80), 1)

        c["timestamp"] = round(datetime.timestamp(datetime.now()))
        c["immatriculation"] = generate_immatriculation()
    
        c["geo"] = generate_coordinates_close_to(b["geo"]["lat"], b["geo"]["lon"])

        return [a, b, c]
    
    else:
        data = { "type": "periodique"}

        data["vitesse"] = round(random.uniform(90, 100), 1)

        data["timestamp"] = round(datetime.timestamp(datetime.now()))
        data["immatriculation"] = generate_immatriculation()

        data["geo"] = generate_coordinates()

        return [data]


def generate_packet_ponct(close=False):
    if close:
        # Generating first point
        a = { "type": "ponctuelle", "accident": True }

        a["timestamp"] = round(datetime.timestamp(datetime.now()))
        a["immatriculation"] = generate_immatriculation()
    
        a["geo"] = generate_coordinates()

        # Generating second point close to first one
        b = { "type": "ponctuelle", "accident": True }

        b["timestamp"] = round(datetime.timestamp(datetime.now()))
        b["immatriculation"] = generate_immatriculation()
    
        b["geo"] = generate_coordinates_close_to(a["geo"]["lat"], a["geo"]["lon"])

        return [a, b]
    else:
        data = { "type": "ponctuelle", "accident": True }

        data["timestamp"] = round(datetime.timestamp(datetime.now()))
        data["immatriculation"] = generate_immatriculation()

        data["geo"] = generate_coordinates()

        return [data]
    
    

def generate_file(n_perio=30, n_ponct=9, n_pont_close=3, n_embouteillage=5):
    """Generate file with desired proportion of datas

    Args:
        n_perio (int, optional): nombre de valeurs de type periodique. Defaults to 30.
        n_ponct (int, optional): nombre de valeurs de type ponctuelle (accident). Defaults to 9.
        n_pont_close (int, optional): nombre de valeurs de type ponctuelle (accident) proche l'une de l'autre par couple de 2. Si a 3 Donc genere 6 valeurs ponct proche Defaults to 3.
        n_embouteillage (int, optional): nombre de valeurs periodique qui doivent provoquer des alertes embouteillages. Defaults to 5.
    """

    packets = []

    for i in range(n_perio-n_embouteillage):
        packets = packets + generate_packet_perio()

    for i in range(n_ponct-(n_pont_close*2)):
        packets = packets + generate_packet_ponct()
    
    for i in range(n_pont_close):
        packets = packets + generate_packet_ponct(close=True)
    
    for i in range(n_embouteillage):
        packets = packets + generate_packet_perio(isembouteillage=True)
    
    res = { 'packets': packets }

    # json to file
    json_object = json.dumps(res, indent=4)
    with open(f"DATAS_ALEA_MIX_{n_perio}_{n_ponct}_{n_embouteillage}.json", "w") as outfile:
        outfile.write(json_object)