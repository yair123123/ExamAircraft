from toolz import pipe
from toolz.curried import partial

from api.weather_api import find_weather_by_city, find_city_location
from models.target import target
from repository.csv_repository import write_missions_to_csv
from repository.json_repository import read_target_from_json
from service.mission_service import start, get_all_mission, sort_missions, filter_missions

if __name__ == "__main__":
    targets: list[target] = read_target_from_json('./ass/targets.json')
    cities = map(lambda x: x.city, targets)
    API_URL = 'https://api.openweathermap.org/'
    start(API_URL, cities)
    pilots = [
        {"name": "John Doe", "skill": 8},
        {"name": "Jane Smith", "skill": 6},
        {"name": "Michael Clark", "skill": 9},
        {"name": "Alice Johnson", "skill": 7},
        {"name": "Robert White", "skill": 10},
        {"name": "Tom Cruise", "skill": 9},
        {"name": "Chris Pratt", "skill": 6},
        {"name": "David Miller", "skill": 5},
        {"name": "Sarah Connor", "skill": 8}
    ]
    aircrafts = [
        {"type": "Fighter Jet", "speed": 1500, "fuel_capacity": 3000},
        {"type": "Bomber", "speed": 900, "fuel_capacity": 5000},
        {"type": "Drone", "speed": 500, "fuel_capacity": 1000},
        {"type": "Helicopter", "speed": 400, "fuel_capacity": 800},
        {"type": "Stealth Fighter", "speed": 1800, "fuel_capacity": 3500},
        {"type": "Recon Drone", "speed": 600, "fuel_capacity": 1200},
        {"type": "Heavy Bomber", "speed": 850, "fuel_capacity": 6000}
    ]
    URL_API = 'https://api.openweathermap.org/'

    start(API_URL, cities)
    missions = get_all_mission('./ass/targets.json', './pilots.json', './aircrafts.json', API_URL)

    sorted_mission = filter_missions(sort_missions(missions))
    write_missions_to_csv(sorted_mission, 'sort_missions.csv')
