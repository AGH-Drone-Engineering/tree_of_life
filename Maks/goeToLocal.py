
'''

Robimy dwie funkcje:
 - pierwsza (distance_haversine) oblicza dystans z współrzędnych geograficznych na dystans w metrach z "Haversine Formula"
 - druga (geo_to_vector) tworzy wektor w metrach
Jeżeli pierwsza współrzędna w lokalnym układzie ma być (0,0) to druga jest wynikiem dodania wektora

Trzecią funkcję (geo_to_local) napisałem, by wygodniej było operować w kodzie

'''

import math

##################################################

def distance_haversine(lat1,lon1,lat2,lon2):

    # Promien ziemi w metrach

    Rz = 6371000

    # Konwersja dlugosci i szerokosci geograficznej na radiany

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Obliczanie roznicy odleglosci

    delta_lat_rad = lat2_rad - lat1_rad
    delta_lon_rad = lon2_rad - lon1_rad

    # Tutaj wykorzystuje cos takiego jak "Haversine Formula" - jest na Wikipedia i StackOverflow

    a = math.sin(delta_lat_rad/2)**2 + math.cos(lat1_rad)*math.cos(lat2_rad)*math.sin(delta_lon_rad)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Zwracamy dystans między punktami

    distance = Rz*c

    return distance

def geo_to_vector(lat1,lon1,lat2,lon2):

    # Potrzebujemy dystans

    distance = distance_haversine(lat1,lon1,lat2,lon2)

    # Przeskalowanie

    skala = distance/math.sqrt( (lat2-lat1)**2 + (lon2-lon1)**2 )

    # Wektory

    vector_lat = skala*(lat2-lat1)
    vector_lon = skala*(lon2-lon1)

    return vector_lat,vector_lon

def geo_to_local(lat1,lon1,lat2,lon2):

    # Przerabiamy na metry

    X, Y = geo_to_vector(lat1, lon1, lat2, lon2)

    # Wyniki

    print(f"Wektor geograficzny: [{lat2 - lat1},{lon2 - lon1}]")
    print(f"Wektor w metrach: [{X:.4f},{Y:.4f}]")
    print("")
    print(f"Dystans w metrach: {distance_haversine(lat1, lon1, lat2, lon2)}")
    print("")
    print(f"Współrzędne geograficzne:[{lat1},{lon1}],[{lat2},{lon2}]")
    print(f"Współrzędne lokalne:[0,0],[{X:.4f},{Y:.4f}]")

    return 1

##################################################

# Nasze współrzędne

lat1, lon1 = 49.9285, 19.84829
lat2, lon2 = 49.92806, 19.8558

geo_to_local(lat1,lon1,lat2,lon2)
