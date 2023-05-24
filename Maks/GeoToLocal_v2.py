
'''
geo_to_local() - Przyjmuje cztery argumenty: szerokość i długość pierwszej współrzędnej oraz szerokość i długość drugiej współrzędnej.
                 Funkcja zwraca wartości X,Y nieznanego punktu w lokalnym układzie współrzędnych (jeżeli pierwsza = [0,0]).
                 Czyli zwraca taki niby-wektor.

Aby podać poprawnie niby-wektor należy:
                 1) - otrzymać/wyliczyć promień Ziemi
                 2) - obliczyć dystans z odpowiednich wzorów
                 3) - przeskalować i podać wynik
'''

import math

def geo_to_local(lat1,lon1,lat2,lon2):

    '''
    Pierwsze co należy zrobić to wyliczyć "lokalny" promień ziemi potrzebny do dalszych obliczeń
    '''

    latitude = (lat1+lat2)/2                # Średnia szerokość geograficzna

    Re = 6378137.0                          # Promień Ziemi na równiku
    Rp = 6356752.314245                     # Promień Ziemi na biegunie

    lat_rad = math.radians(latitude)

    licznik = (Re**2 * math.cos(lat_rad))**2 + (Rp**2 * math.sin(lat_rad))**2
    mianownik = (Re * math.cos(lat_rad))**2 + (Rp * math.sin(lat_rad))**2

    radius = math.sqrt(licznik/mianownik)   # Wyznaczenie "lokalnego" promienia Ziemi - potrzebny do dalszych wyliczeń

    '''
    Mając "lokalny promień" możemy przystąić do liczenia z pomocą "Haversine Formula"
    '''

    lat1_rad = math.radians(lat1)           # Konwersja dlugosci i szerokosci geograficznej na radiany
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lat_rad = lat2_rad - lat1_rad     # Obliczanie roznicy odleglosci
    delta_lon_rad = lon2_rad - lon1_rad

    # Tutaj wykorzystuje cos takiego jak "Haversine Formula" - jest na Wikipedia i StackOverflow

    a = math.sin(delta_lat_rad / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon_rad / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    distance = radius * c                   # Zwracamy dystans między punktami

    '''
    Skoro już mamy odległość - należy ją przeskalować i wrzucić odpowiedź
    '''

    # Przeskalowanie

    skala = distance / math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)

    vector_lat = skala * (lat2 - lat1)      # Wektory (czyli nasze szukane X oraz Y)
    vector_lon = skala * (lon2 - lon1)

    '''
    Poniższe "printy" są tylko poglądowe: dla programisty, do analizy
    '''

    print(f"Współrzędne geograficzne:[{lat1},{lon1}],[{lat2},{lon2}]")
    print(f"Wektor geograficzny: [{lat2 - lat1},{lon2 - lon1}]\n")

    print(f"Współrzędne lokalne w metrach:[0,0],[{vector_lat:.4f},{vector_lon:.4f}]")
    print(f"Wektor w metrach: [{vector_lat:.4f},{vector_lon:.4f}]\n")

    print(f"Dystans w metrach: {distance}")

    return vector_lat,vector_lon

# Ta linijka pobiera dwie pary współrzędnych: Szerokość i długość pierwszego punktu, oraz Szerokość i długość drugiego punktu
# IN - Input    | lat/lon - szerokość,długość geograficzna  | 1/2 - nr podanego punktu

IN_lat_1,IN_lon_1,IN_lat_2,IN_lon_2 = list(map(float, input("Podaj [lat1,lon1,lat2,lon2]:\n").split()))

# Funkcja zwracająca "wektor"
print(geo_to_local(IN_lat_1,IN_lon_1,IN_lat_2,IN_lon_2))
