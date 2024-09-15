import math
from os.path import exists
from toolz import pipe, curry
from api.weather_api import *
from models.mission import mission
from repository.csv_repository import write_missions_to_csv
from repository.json_repository import *
from service.score_calculation import calculate_score_all_missions
from itertools import groupby
from functools import partial


def start(api_url, cities):
    if not exists('./cities_location.json'):
        write_all_to_json(api_url, cities)


def find_all_locations(cities: list[str], url_api):
    return pipe(
        cities,
        lambda xs: map(lambda x: {**find_city_location(x, url_api)}, xs),
        lambda xs: map(lambda x: {**x, 'distance': distances(location_israel = find_city_location('jerusalem',url_api),location_other= x)}, xs),
        list
    )


def distances(location_israel, location_other):
    distance = haversine_distance(location_israel['lat'], location_israel['lon'], location_other['lat'],
                                  location_other['lon'])
    return distance


def write_all_to_json(api_url, cities):
    cities_location = find_all_locations(cities, api_url)
    write_pilots_to_json(pilots, 'pilots.json')
    write_aircrafts_to_json(aircrafts, 'aircrafts.json')
    write_dict_to_json(cities_location, 'cities_location.json')


def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371.0  # Radius of the Earth in kilometers
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    # Calculate differences between the coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    # Apply Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Calculate the distance
    distance = r * c
    return distance


def find_city_distance_from_json(city_name, path_json):
    data = read_dict_from_json(path_json)
    try:
        return pipe(
            data,
            lambda data: next(filter(lambda x: get_in(['name'], x) == city_name, data))
        )
    except StopIteration:
        raise ValueError(f"City {city_name} not found in {path_json}")


def get_all_mission(path_target, path_pilot, path_aircraft, api_url):
    aircrafts = read_aircrafts_from_json(path_aircraft)
    pilots = read_pilots_from_json(path_pilot)
    targets = read_target_from_json(path_target)
    missions = []
    cities_weather = pipe(
        targets,
        partial(map, lambda x: x.city),
        lambda x: map(lambda y: find_weather_by_city(y, url_api=api_url), x),
        list
    )
    location_israel = find_city_location('jerusalem', api_url)
    for aircraft in aircrafts:
        for pilot in pilots:
            for target in targets:
                print(aircraft.type, pilot.name, target.city)
                distance = distances(location_israel, find_city_distance_from_json(target.city, 'cities_location.json'))
                try:
                    weather = pipe(
                        cities_weather,
                        partial(filter, lambda x: get_in(['city'], x) == target.city),
                        next
                    )
                except StopIteration:
                    raise ValueError(f"City {target.city} not found")
                new_mission = mission(
                    target_city=target.city,
                    priority=target.priority,
                    assigned_pilot=pilot.name,
                    assigned_aircraft=aircraft.type,
                    distance=distance,
                    weather_conditions=weather['weather'],
                    pilot_skill=pilot.skill,
                    aircraft_speed=aircraft.speed,
                    fuel_capacity=aircraft.fuel_capacity,
                    mission_fit_score=0
                )
                missions.append(new_mission)
    return missions


def sort_missions(missions: list[mission]):
    missions = calculate_score_all_missions(missions)
    sorted_missions = sorted(missions, key=lambda x: x.mission_fit_score, reverse=True)
    return sorted_missions


def filter_missions(missions):
    def find_best_mission(group, missions):
        # Find the mission with the highest fit score
        best_mission = max(group, key=lambda x: x.mission_fit_score)
        assigned_aircrafts = set(m.assigned_aircraft for m in missions)
        assigned_pilots = set(m.assigned_pilot for m in missions)

        if best_mission.assigned_aircraft in assigned_aircrafts or best_mission.assigned_pilot in assigned_pilots:
            group = [m for m in group if m != best_mission]
            if group:
                best_mission = find_best_mission(group, missions)
        return best_mission

    grouped = groupby(sorted(missions, key=lambda x: x.target_city), key=lambda x: x.target_city)
    max_score_entries = []
    for key, group in grouped:
        group = list(group)
        best_entry = find_best_mission(group, max_score_entries)
        max_score_entries.append(best_entry)
    return max_score_entries
