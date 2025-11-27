from openrouteservice import client
import folium
import webbrowser
import yaml
import argparse

def make_map(config):

    center = config.get('map_center', [47.32167778891493, 10.313657870248395])
    zoom_start = config.get('zoom_start', 15)
    map_kempten = folium.Map(location=center, zoom_start=zoom_start)  # Create map

    for marker in config.get('markers', []):
        lat = marker.get('lat')
        lon = marker.get('lon')
        popup = marker.get('popup', '') 
        folium.Marker([lat, lon], popup=popup).add_to(map_kempten)

    return map_kempten


def style_function(color):  # To style data
    return lambda feature: dict(color=color,
                                opacity=0.5,
                                weight=4, )

def add_route(map, config):


    api_key = config.get('api_key', '')  # https://openrouteservice.org/sign-up
    
    ors = client.Client(key=api_key)

    route_config = config.get('route', {})

    coordinates = route_config.get('coordinates', [])

    # Request route
    coordinates = [coordinates[0], coordinates[1]]

    preference = route_config.get('preference', 'shortest')
    format_out = route_config.get('format_out', 'geojson')
    profile = route_config.get('profile', 'driving-car')
    geometry = route_config.get('geometry', 'true')

    direction_params = {'coordinates': coordinates,
                    'profile': profile,  # 'driving-car', 'cycling-regular', 'foot-walking'
                    'format_out': format_out,
                    'preference': preference,  # 'fastest', 'shortest'
                    'geometry': geometry}

    regular_route = ors.directions(**direction_params)

    gj = folium.GeoJson(regular_route,
                    name='Regular Route',
                    style_function=style_function('blue')) \
    .add_to(map)
    return

def main(config):

    m = make_map(config)
    add_route(m, config)

    m.save("index.html")
    webbrowser.open("index.html")

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Routing Application')
    parser.add_argument('--config', type=str, default='config.yaml',
                        help='Path to the configuration YAML file')
    args = parser.parse_args()

    cfg = yaml.safe_load(open(args.config))

    print(cfg)

    main(cfg)