from toolz import pipe
from models.mission import mission

def get_score_priority(priority, max_priority):
    return (priority / max_priority) * 0.1

def get_score_distance(distance, min_distance):
    return (distance / min_distance) * 0.2

def get_score_type_aircraft(speed, max_speed):
    return (speed / max_speed) * 0.25

def get_score_skill_pilot(skill_point, max_skill_point):
    return (skill_point / max_skill_point) * 0.25

def get_score_weather(weather):
    weather_score = calculate_weather(weather)
    return weather_score

def calculate_weather(weather):
    weather_dict = {"Clear": 1.0, "clouds": 0.7, "Rain": 0.4, "Stormy": 0.2}
    return weather_dict.get(weather, 0)

def calculate_score_all_missions(missions: list[mission]) -> list[mission]:
    all_max = {
        "max_priority": max(mission.priority for mission in missions),
        "distance": max(mission.distance for mission in missions),
        "weather_conditions": max(calculate_weather(mission.weather_conditions) for mission in missions),
        "pilot_skill": max(mission.pilot_skill for mission in missions),
        "aircraft_speed": max(mission.aircraft_speed for mission in missions),
    }

    for m in missions:
        calculation_score(m, all_max)

    return missions

def calculation_score(mission: mission, all_max: dict) -> mission:
    mission.mission_fit_score = pipe(
        0,  # Initial score
        lambda x: x + get_score_priority(mission.priority, all_max['max_priority']),
        lambda x: x + get_score_distance(mission.distance, all_max['distance']),
        lambda x: x + get_score_type_aircraft(mission.aircraft_speed, all_max['aircraft_speed']),
        lambda x: x + get_score_skill_pilot(mission.pilot_skill, all_max['pilot_skill']),
        lambda x: x + get_score_weather(mission.weather_conditions),
        lambda x: x * 100
    )
    return mission
