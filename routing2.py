from openrouteservice import client
import folium
import webbrowser

def make_map():
    map_kempten = folium.Map(location=([47.72167778891493, 10.313657870248395]), zoom_start=15)  # Create map

    folium.Marker([47.716080, 10.313525], popup='Hochschule Kreisel').add_to(map_kempten)
    folium.Marker([47.728723272725006, 10.312297325822115], popup='Residenz').add_to(map_kempten)

    return map_kempten


def style_function(color):  # To style data
    return lambda feature: dict(color=color,
                                opacity=0.5,
                                weight=4, )

def add_route(map):
    api_key = '5b3ce3597851110001cf6248ceb027611ac04ba796da742ff02ea8d1'  # https://openrouteservice.org/sign-up
    ors = client.Client(key=api_key)

    # Request route
    coordinates = [[10.313525, 47.716080], [10.312297325822115, 47.728723272725006]]
    direction_params = {'coordinates': coordinates,
                    'profile': 'driving-car',  # 'driving-car', 'cycling-regular', 'foot-walking'
                    'format_out': 'geojson',
                    'preference': 'shortest',  # 'fastest', 'shortest'
                    'geometry': 'true'}

    regular_route = ors.directions(**direction_params)

    gj = folium.GeoJson(regular_route,
                    name='Regular Route',
                    style_function=style_function('blue')) \
    .add_to(map)
    return

def main():

    m = make_map()
    add_route(m)

    m.save("index.html")
    webbrowser.open("index.html")

    return


if __name__ == "__main__":
    print('Ich werde ausgeführt!')
    main()