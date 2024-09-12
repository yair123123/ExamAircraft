import json
import os
from array import array

from toolz import pipe,pluck
from toolz.curried import partial

from models.aircraft import aircraft
from models.pilot import pilot
from typing import List

from models.target import target


# func for json aircraft


class aircraftEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, aircraft):
            return obj.__dict__
        return super().default(obj)

def write_aircrafts_to_json(aircrafts: List[aircraft], filename: str):
    with open(filename, 'w') as jsonfile:
        json.dump(aircrafts, jsonfile, cls=aircraftEncoder, indent=4)

def read_aircrafts_from_json(filename: str) -> List[aircraft]:
    with open(filename, 'r') as jsonfile:
        data1 = json.load(jsonfile)
    return [aircraft(data['type'],data['speed'], data['fuel_capacity']) for data in data1]

def write_aircraft_to_json(person: aircraft, filename: str):
    with open(filename, 'w') as jsonfile:
        json.dump(person.__dict__, jsonfile, indent=4)

def read_aircraft_from_json(filename: str) -> aircraft:
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
    return aircraft(data['name'], data['age'])

# func for json pilot

class pilotEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pilot):
            return obj.__dict__
        return super().default(obj)
def write_pilots_to_json(people: List[pilot], filename: str):
    with open(filename, 'w') as jsonfile:
        json.dump(people, jsonfile, cls=pilotEncoder, indent=4)

def read_pilots_from_json(filename: str) -> List[pilot]:
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
    return [pilot(person['name'], person['skill']) for person in data]

def write_pilot_to_json(person: pilot, filename: str):
    with open(filename, 'w') as jsonfile:
        json.dump(person.__dict__, jsonfile, indent=4)

def read_pilot_from_json(filename: str) -> pilot:
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
    return pilot(data['name'], data['age'])
class targetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, target):
            return obj.__dict__
        return super().default(obj)

def read_target_from_json(filename: str) -> list[target]:
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
        return pipe(
            data,
            lambda x: x['targets'],
            partial(map,lambda y:target(y['city'],y['priority'])),
            list,
        )

def write_dict_to_json(dict, filename: str):
    with open(filename, 'w') as jsonfile:
        json.dump(dict, jsonfile,indent=4)
def read_dict_from_json(filename: str) -> dict:
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
    return data
# jsons

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
