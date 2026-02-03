import requests

def get_lat_lon_by_cep(cep):
    url = f'https://nominatim.openstreetmap.org/search?postalcode={cep}&format=json&countrycodes=BR'
    response = requests.get(url)
    data = response.json()

    if data:
        latitude = data[0]['lat']
        longitude = data[0]['lon']
        return latitude, longitude
    else:
        return None, None

if __name__ == "__main__":
    cep = input("Digite o CEP: ")
    lat, lon = get_lat_lon_by_cep(cep)
    if lat and lon:
        print(f"Latitude: {lat}, Longitude: {lon}")
    else:
        print("Coordenadas não encontradas para o CEP fornecido.")