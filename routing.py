from openrouteservice import client
import folium
import webbrowser

api_key = '5b3ce3597851110001cf6248ceb027611ac04ba796da742ff02ea8d1'  # https://openrouteservice.org/sign-up
ors = client.Client(key=api_key)

map_kempten = folium.Map(location=([47.72167778891493, 10.313657870248395]), zoom_start=15)  # Create map

folium.Marker([47.716080, 10.313525], popup='Hochschule Kreisel').add_to(map_kempten)
folium.Marker([47.728723272725006, 10.312297325822115], popup='Residenz').add_to(map_kempten)

# Request route
coordinates = [[10.313525, 47.716080], [10.312297325822115, 47.728723272725006]]
direction_params = {'coordinates': coordinates,
                    'profile': 'driving-car',  # 'driving-car', 'cycling-regular', 'foot-walking'
                    'format_out': 'geojson',
                    'preference': 'shortest',  # 'fastest', 'shortest'
                    'geometry': 'true'}

regular_route = ors.directions(**direction_params)

distance, duration = regular_route['features'][0]['properties']['summary'].values()

popup_route = "<h4>{0} route</h4><hr>" \
              "<strong>Duration: </strong>{1:.1f} mins<br>" \
              "<strong>Distance: </strong>{2:.3f} km"

popup = folium.map.Popup(popup_route.format('Regular',
                                            duration / 60,
                                            distance / 1000))

def style_function(color):  # To style data
    return lambda feature: dict(color=color,
                                opacity=0.5,
                                weight=4, )

gj = folium.GeoJson(regular_route,
                    name='Regular Route',
                    style_function=style_function('blue')) \
    .add_child(popup) \
    .add_to(map_kempten)

map_kempten.save("index.html")
webbrowser.open("index.html")
