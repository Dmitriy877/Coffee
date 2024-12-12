import json
import requests
import os
import folium
from geopy import distance
from dotenv import load_dotenv


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_near_place(place):
    return place["distance"]


def main():

    load_dotenv()

    apikey = os.getenv("YANDEX_API_KEY")

    address_a = input("Где вы находитесь:")

    cords_a = fetch_coordinates(apikey, address_a)


    longitude_a, latitude_a = cords_a
    longitude_a_float = float(longitude_a)
    latitude_a_float = float(latitude_a)
    cords_revert_a = (latitude_a_float, longitude_a_float)


    with open("coffee.json", "r", encoding = "CP1251") as my_file:
        file_contents = my_file.read()
    file_contents_convert = json.loads(file_contents)


    new_coffee_list = []

    for place in file_contents_convert:
        dictionary = {}

        latitude_b_float = float(place["Latitude_WGS84"])
        longitude_b_float = float(place["Longitude_WGS84"])
        cords_b = (latitude_b_float, longitude_b_float)


        dictionary["title"] = place["Name"]
        dictionary["distance"] = distance.distance(cords_revert_a, cords_b).km
        dictionary["latitude"] = float(place["Latitude_WGS84"])
        dictionary["longitude"] = float(place["Longitude_WGS84"])
        new_coffee_list.append(dictionary)


    coffee_list_near = sorted(new_coffee_list, key=get_near_place)
    coffee_list_near_first = coffee_list_near[:5]


    m = folium.Map(cords_revert_a, zoom_start=12)
    

    for place in coffee_list_near_first:
        folium.Marker(
            location = [place["latitude"], place["longitude"]],
            tooltip = place["title"],
            popup = place["title"],
            icon = folium.Icon(color="red"),
        ).add_to(m)

    m.save("index.html")
  

if __name__ == '__main__':
    main()