import math

def berechne_distanz(lat1, lon1, lat2, lon2):
    R = 6371 # Radius Erde
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Standardwerte: Bochum -> Köln
lat1 = 51.4818
lon1 = 7.2162
lat2 = 50.9375
lon2 = 6.9603

choice = input("Eigene Koordinaten eingeben? (y/n): ")

if choice == "y":
    print("Punkt 1:")
    lat1 = float(input("Breitengrad: "))
    lon1 = float(input("Längengrad: "))
    print("Punkt 2:")
    lat2 = float(input("Breitengrad: "))
    lon2 = float(input("Längengrad: "))
else:
    print("Verwendete Standardwerte: Bochum -> Köln")

distanz = berechne_distanz(lat1, lon1, lat2, lon2)
print("Distanz:", round(distanz, 2), "km")
