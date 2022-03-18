import itertools
import os.path

import numpy as np
import pandas as pd
from sortedcontainers import SortedList

driver_to_constructor_2021 = {
    'Finland Kimi Räikkönen': 'Alfa Romeo Racing-Ferrari',
    'Poland Robert Kubica': 'Alfa Romeo Racing-Ferrari',
    'Italy Antonio Giovinazzi': 'Alfa Romeo Racing-Ferrari',
    'France Pierre Gasly': 'AlphaTauri-Honda',
    'Japan Yuki Tsunoda': 'AlphaTauri-Honda',
    'Spain Fernando Alonso': 'Alpine-Renault',
    'France Esteban Ocon': 'Alpine-Renault',
    'Germany Sebastian Vettel': 'Aston Martin-Mercedes',
    'Canada Lance Stroll': 'Aston Martin-Mercedes',
    'Monaco Charles Leclerc': 'Ferrari',
    'Spain Carlos Sainz Jr.': 'Ferrari',
    'Russian Automobile Federation Nikita Mazepin': 'Haas-Ferrari',
    'Germany Mick Schumacher': 'Haas-Ferrari',
    'Australia Daniel Ricciardo': 'McLaren-Mercedes',
    'United Kingdom Lando Norris': 'McLaren-Mercedes',
    'United Kingdom Lewis Hamilton': 'Mercedes',
    'Finland Valtteri Bottas': 'Mercedes',
    'Mexico Sergio Pérez': 'Red Bull Racing-Honda',
    'Netherlands Max Verstappen': 'Red Bull Racing-Honda',
    'Canada Nicholas Latifi': 'Williams-Mercedes',
    'United Kingdom George Russell': 'Williams-Mercedes'
}

constructors = set(driver_to_constructor_2021.values())

location_to_driver_to_score = {}
location_to_driver_only_to_score = {}


def add_to_driver(location, driver, points):
    location_to_driver_to_score.setdefault(location, {})
    driver_to_score = location_to_driver_to_score.get(location)
    driver_to_score[driver] = driver_to_score.get(driver, 0) + points


def add_to_driver_only(location, driver, points):
    location_to_driver_only_to_score.setdefault(location, {})
    driver_only_to_score = location_to_driver_only_to_score.get(location)
    driver_only_to_score[driver] = driver_only_to_score.get(driver, 0) + points


def print_constructor_score(constructor_to_score):
    print('=== CONSTRUCTORS ===')
    for constructor in sorted(constructor_to_score, key=constructor_to_score.get, reverse=True):
        print(constructor, constructor_to_score[constructor])
    print()


def print_driver_score(combined_location_to_driver_to_score):
    print('=== DRIVERS ===')
    for location, driver_to_score in combined_location_to_driver_to_score.items():
        print(location)
        for driver in sorted(driver_to_score, key=driver_to_score.get, reverse=True):
            print(f'- {driver}: {driver_to_score[driver]}')
    print()


def get_first_driver(data, constructor):
    constructor_entries = data.loc[data['Constructor'] == constructor].sort_values('Position')
    first = constructor_entries.iloc[0]
    return first


def get_drivers(data, constructor):
    constructor_entries = data.loc[data['Constructor'] == constructor].sort_values('Position')
    return constructor_entries['Driver'].tolist()


def get_driver_positions(data, constructor):
    constructor_entries = data.loc[data['Constructor'] == constructor].sort_values('Position')
    return constructor_entries['Position'].tolist()


def got_qualifying_time(cell):
    return not pd.isna(cell) and cell != 'No time'


def finished_qualifications(row) -> bool:
    final_grid = row['Final grid']
    return type(final_grid) == int or type(final_grid) == np.int64 or final_grid.isnumeric()


driver_qualification_streaks = {}
constructor_qualification_streaks = {}


def parse_and_score_qualifications(location, path):
    data = pd.read_csv(path)
    for index, row in data.iterrows():
        driver = row['Driver']
        # +1 for Q1 finish
        if got_qualifying_time(row['Q1']):
            add_to_driver(location, driver, 1)
        # +2 for Q2 finish
        if got_qualifying_time(row['Q2']):
            add_to_driver(location, driver, 2)
        # +3 for Q3 finish
        if got_qualifying_time(row['Q3']):
            add_to_driver(location, driver, 3)
        # -5 for not qualifying
        if not finished_qualifications(row):
            add_to_driver(location, driver, -5)
        # -10 for disqualification from qualifying
        position = row['Position']
        if position == 'DSQ':
            add_to_driver(location, driver, -10)
        # +1-10 for top 10 positions
        if is_position_valid(position) and int(position) <= 10:
            add_to_driver(location, driver, 11 - int(position))
            # +5 for top 10 for 5 qualifications in a row
            driver_qualification_streaks[driver] = driver_qualification_streaks.get(driver, 0) + 1
            if driver_qualification_streaks[driver] == 5:
                add_to_driver(location, driver, 5)
                driver_qualification_streaks[driver] = 0
        else:
            driver_qualification_streaks[driver] = 0
    for constructor in constructors:
        # +2 for driver qualifying ahead of their teammate (driver only)
        first = get_first_driver(data, constructor)
        if finished_qualifications(first):
            add_to_driver_only(location, first['Driver'], 2)
        # +5 for top 10 of both drivers for 3 qualifications in a row
        if all(is_position_valid(p) and int(p) <= 10 for p in get_driver_positions(data, constructor)):
            constructor_qualification_streaks[constructor] = constructor_qualification_streaks.get(constructor, 0) + 1
            if constructor_qualification_streaks[constructor] == 3:
                for driver in get_drivers(data, constructor):
                    add_to_driver(location, driver, 5)
                constructor_qualification_streaks[constructor] = 0
        else:
            constructor_qualification_streaks[constructor] = 0


def finished_race(row) -> bool:
    return row['Position'] == '1' or str(row['Time/Retired']).startswith('+')


def parse_and_score_sprint(location, sprint_path):
    data = pd.read_csv(sprint_path)
    for index, row in data.iterrows():
        driver = row['Driver']
        # +1 for finish
        if finished_race(row):
            add_to_driver(location, driver, 1)
        # +1/-1 per position gained/lost; max +5/-5
        previous_position = row['Grid']
        position = row['Position']
        if is_position_valid(position):
            position_diff_points = max(min(previous_position - int(position), 5), -5)
            add_to_driver(location, driver, position_diff_points)
        # -5 for not classifying
        if not finished_race(row):
            add_to_driver(location, driver, -5)
        # -10 for getting disqualified
        if position == 'DSQ':
            add_to_driver(location, driver, -10)
        # +1-10 for position
        if is_position_valid(position) and int(position) <= 10:
            add_to_driver(location, driver, 11 - int(position))
    # +2 for finishing ahead of teammate (driver only)
    for constructor in constructors:
        first = get_first_driver(data, constructor)
        if finished_race(first):
            add_to_driver_only(location, first['Driver'], 2)


race_position_to_points = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
    6: 8,
    7: 6,
    8: 4,
    9: 2,
    10: 1
}


def is_position_valid(position):
    return type(position) == int or position.isnumeric()


driver_race_streaks = {}
constructor_race_streaks = {}


def parse_and_score_race(location, race_path):
    data = pd.read_csv(race_path)
    for index, row in data.iterrows():
        driver = row['Driver']
        # +1 for finish
        if finished_race(row):
            add_to_driver(location, driver, 1)
        # +2/-2 per position gained/lost; max +10/-10
        previous_position = row['Grid']
        if previous_position == 'PL':
            previous_position = 20
        position = row['Position']
        if is_position_valid(position):
            position_diff_points = max(min(2 * (int(previous_position) - int(position)), 10), -10)
            add_to_driver(location, driver, position_diff_points)
        # -10 for not classifying
        if not finished_race(row):
            add_to_driver(location, driver, -10)
        # -20 for getting disqualified
        if position == 'DSQ':
            add_to_driver(location, driver, -20)
        # +1-25 for position
        if is_position_valid(position):
            position_points = race_position_to_points.get(int(position))
            if position_points:
                add_to_driver(location, driver, position_points)
                # +10 for top 10 for 5 races in a row
                driver_race_streaks[driver] = driver_race_streaks.get(driver, 0) + 1
                if driver_race_streaks[driver] == 5:
                    add_to_driver(location, driver, 10)
                    driver_race_streaks[driver] = 0
            else:
                driver_race_streaks[driver] = 0
    for constructor in constructors:
        # +3 for finishing ahead of teammate (driver only)
        first = get_first_driver(data, constructor)
        if finished_race(first):
            add_to_driver_only(location, first['Driver'], 3)
        # +10 for top 10 of both drivers for 3 races in a row
        if all(is_position_valid(p) and int(p) <= 10 for p in get_driver_positions(data, constructor)):
            constructor_race_streaks[constructor] = constructor_race_streaks.get(constructor, 0) + 1
            if constructor_race_streaks[constructor] == 3:
                for driver in get_drivers(data, constructor):
                    add_to_driver(location, driver, 10)
                constructor_race_streaks[constructor] = 0
        else:
            constructor_race_streaks[constructor] = 0


def parse_and_score_fastest_lap(location, fastest_lap_path, points):
    row = pd.read_csv(fastest_lap_path).iloc[0]
    driver = row['Driver']
    add_to_driver(location, driver, points)


def parse_and_score_sprint_fastest_lap(location, fastest_lap_path):
    # +3 for fastest lap
    parse_and_score_fastest_lap(location, fastest_lap_path, 3)


def parse_and_score_race_fastest_lap(location, fastest_lap_path):
    # +5 for fastest lap
    parse_and_score_fastest_lap(location, fastest_lap_path, 5)


location_mapping_2021_2022 = {
    'bahrain': 'bahrain',
    'emilia_romagna': 'emilia_romagna',
    'portuguese': 'australian',
    'spanish': 'spanish',
    'monaco': 'monaco',
    'azerbaijan': 'azerbaijan',
    'french': 'french',
    'styrian': 'japanese',
    'austrian': 'austrian',
    'british': 'british',
    'hungarian': 'hungarian',
    'belgian': 'belgian',
    'dutch': 'dutch',
    'italian': 'italian',
    'russian': 'singapore',
    'turkish': 'miami',
    'us': 'us',
    'mexico': 'mexico',
    'sao_paulo': 'sao_paulo',
    'qatar': 'canadian',
    'saudi_arabian': 'saudi_arabian',
    'abu_dhabi': 'abu_dhabi',
}

locations_2021 = list(location_mapping_2021_2022.keys())

constructor_to_drivers_2022 = {
    'Mercedes': ['United Kingdom Lewis Hamilton', 'United Kingdom George Russell'],
    'Red Bull Racing-Honda': ['Netherlands Max Verstappen', 'Mexico Sergio Pérez'],
    'Ferrari': ['Monaco Charles Leclerc', 'Spain Carlos Sainz Jr.'],
    'McLaren-Mercedes': ['Australia Daniel Ricciardo', 'United Kingdom Lando Norris'],
    'Alpine-Renault': ['Spain Fernando Alonso', 'France Esteban Ocon'],
    'Aston Martin-Mercedes': ['Germany Nico Hulkenberg', 'Canada Lance Stroll'],
    'AlphaTauri-Honda': ['France Pierre Gasly', 'Japan Yuki Tsunoda'],
    'Alfa Romeo Racing-Ferrari': ['Finland Valtteri Bottas', 'China Guanyu Zhou'],
    'Williams-Mercedes': ['Canada Nicholas Latifi', 'Thailand Alexander Albon'],
    'Haas-Ferrari': ['Denmark Kevin Magnussen', 'Germany Mick Schumacher'],
}

driver_mapping_2022_2021 = {
    'Finland Valtteri Bottas': ['Finland Kimi Räikkönen', 'Poland Robert Kubica'],
    'China Guanyu Zhou': ['Italy Antonio Giovinazzi'],
    'France Pierre Gasly': ['France Pierre Gasly'],
    'Japan Yuki Tsunoda': ['Japan Yuki Tsunoda'],
    'Spain Fernando Alonso': ['Spain Fernando Alonso'],
    'France Esteban Ocon': ['France Esteban Ocon'],
    'Germany Nico Hulkenberg': ['Germany Sebastian Vettel'],
    'Canada Lance Stroll': ['Canada Lance Stroll'],
    'Monaco Charles Leclerc': ['Monaco Charles Leclerc'],
    'Spain Carlos Sainz Jr.': ['Spain Carlos Sainz Jr.'],
    'Denmark Kevin Magnussen': ['Russian Automobile Federation Nikita Mazepin'],
    'Germany Mick Schumacher': ['Germany Mick Schumacher'],
    'Australia Daniel Ricciardo': ['Australia Daniel Ricciardo'],
    'United Kingdom Lando Norris': ['United Kingdom Lando Norris'],
    'United Kingdom Lewis Hamilton': ['United Kingdom Lewis Hamilton'],
    'United Kingdom George Russell': ['Finland Valtteri Bottas'],
    'Mexico Sergio Pérez': ['Mexico Sergio Pérez'],
    'Netherlands Max Verstappen': ['Netherlands Max Verstappen'],
    'Canada Nicholas Latifi': ['Canada Nicholas Latifi'],
    'Thailand Alexander Albon': ['United Kingdom George Russell']
}

constructor_prices_2022 = {
    'Mercedes': 34.5,
    'Red Bull Racing-Honda': 32.5,
    'Ferrari': 25.0,
    'McLaren-Mercedes': 18.5,
    'Alpine-Renault': 14.0,
    'Aston Martin-Mercedes': 11.5,
    'AlphaTauri-Honda': 10.5,
    'Alfa Romeo Racing-Ferrari': 8.0,
    'Williams-Mercedes': 7.0,
    'Haas-Ferrari': 6.0,
}

driver_prices_2022 = {
    'United Kingdom Lewis Hamilton': 31.0,
    'Netherlands Max Verstappen': 30.5,
    'United Kingdom George Russell': 24.0,
    'Monaco Charles Leclerc': 18.0,
    'Mexico Sergio Pérez': 17.5,
    'Spain Carlos Sainz Jr.': 17.0,
    'United Kingdom Lando Norris': 16.0,
    'Australia Daniel Ricciardo': 14.5,
    'France Pierre Gasly': 13.5,
    'Spain Fernando Alonso': 12.5,
    'France Esteban Ocon': 12.0,
    'Germany Nico Hulkenberg': 11.5,
    'Canada Lance Stroll': 9.5,
    'Finland Valtteri Bottas': 9.0,
    'Japan Yuki Tsunoda': 8.5,
    'China Guanyu Zhou': 8.0,
    'Thailand Alexander Albon': 7.5,
    'Canada Nicholas Latifi': 7.0,
    'Germany Mick Schumacher': 6.5,
    'Denmark Kevin Magnussen': 5.5,
}


def get_constructor_to_score():
    constructor_to_score = {}
    for location, driver_to_score in location_to_driver_to_score.items():
        for driver, score in driver_to_score.items():
            constructor = driver_to_constructor_2021[driver]
            constructor_to_score[constructor] = constructor_to_score.get(constructor, 0) + score
    return constructor_to_score


def get_combined_location_to_driver_to_score():
    combined_location_to_driver_to_score = {}
    for location, driver_to_score in location_to_driver_to_score.items():
        combined_location_to_driver_to_score.setdefault(location, {})
        combined_driver_to_score = combined_location_to_driver_to_score[location]
        driver_only_to_score = location_to_driver_only_to_score.get(location, {})
        for driver in driver_to_score:
            combined_driver_to_score[driver] = driver_to_score[driver] + driver_only_to_score.get(driver, 0)
    return combined_location_to_driver_to_score


def pick_mega_driver_and_location(combined_location_to_driver_to_score, driver_selection_2022, selected_locations):
    mega_driver_score = float('-inf')
    mega_driver_driver = None
    mega_driver_location = None
    for location in selected_locations:
        for driver_2022 in driver_selection_2022:
            drivers_2021 = driver_mapping_2022_2021[driver_2022]
            score = sum([combined_location_to_driver_to_score[location].get(driver_2021, 0)
                         for driver_2021 in drivers_2021])
            if score > mega_driver_score:
                mega_driver_score = score
                mega_driver_driver = driver_2022
                mega_driver_location = location
    return mega_driver_driver, mega_driver_location


def get_score_multiplier(location, driver_2022, turbo_driver,
                         mega_driver_first_half_location, mega_driver_first_half_driver,
                         mega_driver_second_half_location, mega_driver_second_half_driver):
    multiplier = 1
    if driver_2022 == turbo_driver:
        multiplier = 2
    elif location == mega_driver_first_half_location and driver_2022 == mega_driver_first_half_driver:
        multiplier = 3
    elif location == mega_driver_second_half_location and driver_2022 == mega_driver_second_half_driver:
        multiplier = 3
    return multiplier


def get_driver_score(selected_location_to_driver_to_score, driver_2022, location):
    drivers_2021 = driver_mapping_2022_2021[driver_2022]
    return sum([selected_location_to_driver_to_score[location].get(driver_2021, 0)
                for driver_2021 in drivers_2021])


class Team:
    def __init__(self, score, constructor, driver_selection, mega_driver_first_half, mega_driver_first_half_location,
                 mega_driver_second_half, mega_driver_second_half_location, location_to_turbo_driver):
        self.score = score
        self.constructor = constructor
        self.driver_selection = driver_selection
        self.mega_driver_first_half = mega_driver_first_half
        self.mega_driver_first_half_location = mega_driver_first_half_location
        self.mega_driver_second_half = mega_driver_second_half
        self.mega_driver_second_half_location = mega_driver_second_half_location
        self.location_to_turbo_driver = location_to_turbo_driver

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        return f'Constructor: {self.constructor}\n' \
               f'Drivers: {self.driver_selection}\n' \
               f'Mega Drivers: ({self.mega_driver_first_half}, {self.mega_driver_first_half_location}), ' \
               f'({self.mega_driver_second_half}, {self.mega_driver_second_half_location})\n' \
               f'Turbo Drivers: {self.location_to_turbo_driver}'


def main():
    # Calculate last year's scores per location.
    for location_2021 in locations_2021:
        parse_and_score_qualifications(location_2021, f'data/2021_{location_2021}_qualifications.csv')
        sprint_path = f'data/2021_{location_2021}_sprint.csv'
        if os.path.isfile(sprint_path):
            parse_and_score_sprint(location_2021, sprint_path)
            sprint_fastest_lap_path = f'data/2021_{location_2021}_sprint_fastest_lap.csv'
            if os.path.isfile(sprint_fastest_lap_path):
                parse_and_score_sprint_fastest_lap(location_2021, sprint_fastest_lap_path)
        parse_and_score_race(location_2021, f'data/2021_{location_2021}_race.csv')
        race_fastest_lap_path = f'data/2021_{location_2021}_race_fastest_lap.csv'
        if os.path.isfile(race_fastest_lap_path):
            parse_and_score_race_fastest_lap(location_2021, race_fastest_lap_path)

    # Combine normal and driver-only scores, per location.
    combined_location_to_driver_to_score = get_combined_location_to_driver_to_score()

    # Split locations into two parts for mega driver selection.
    locations_first_half = locations_2021[:int(len(locations_2021) / 2)]
    locations_second_half = locations_2021[int(len(locations_2021) / 2):]

    # Keep track of the top teams.
    team_count = 0
    top_teams = SortedList()

    drivers_2022 = driver_prices_2022.keys()

    # Go through all driver combinations of size 5.
    for team_drivers_2022 in itertools.combinations(drivers_2022, 5):
        team_drivers_2022_price = sum(map(lambda d: driver_prices_2022[d], team_drivers_2022))

        # Go through all constructors.
        for constructor in constructors:

            # Ignore selection if the price is too high.
            price = team_drivers_2022_price + constructor_prices_2022[constructor]
            if price > 100:
                continue

            team_count += 1

            # Pick the mega drivers based on the top scores in each half from the selected drivers (after mapping).
            mega_driver_first_half, mega_driver_first_half_location = pick_mega_driver_and_location(
                combined_location_to_driver_to_score, team_drivers_2022, locations_first_half)
            mega_driver_second_half, mega_driver_second_half_location = pick_mega_driver_and_location(
                combined_location_to_driver_to_score, team_drivers_2022, locations_second_half)

            # Pick the turbo driver per location based on the top score in each location from the selected drivers
            # (after mapping), excluding mega drivers and drivers more expensive than $20M.
            location_2021_to_turbo_driver = {}
            for location_2021 in locations_2021:
                top_location_score = float('-inf')
                for driver_2022 in team_drivers_2022:
                    is_first_mega_driver =\
                        location_2021 == mega_driver_first_half_location and driver_2022 == mega_driver_first_half
                    is_second_mega_driver =\
                        location_2021 == mega_driver_second_half_location and driver_2022 == mega_driver_second_half
                    if driver_prices_2022[driver_2022] >= 20 or is_first_mega_driver or is_second_mega_driver:
                        continue
                    drivers_2021 = driver_mapping_2022_2021[driver_2022]
                    team_score = sum([combined_location_to_driver_to_score[location_2021].get(driver_2021, 0)
                                      for driver_2021 in drivers_2021])
                    if team_score > top_location_score:
                        top_location_score = team_score
                        location_2021_to_turbo_driver[location_2021] = driver_2022

            team_score = 0

            # Add driver scores to the team score.
            for location_2021 in locations_2021:
                turbo_driver = location_2021_to_turbo_driver[location_2021]
                for driver_2022 in team_drivers_2022:
                    multiplier = get_score_multiplier(location_2021, driver_2022, turbo_driver,
                                                      mega_driver_first_half_location, mega_driver_first_half,
                                                      mega_driver_second_half_location, mega_driver_second_half)
                    driver_score = get_driver_score(combined_location_to_driver_to_score, driver_2022, location_2021)
                    team_score += driver_score * multiplier

            # Add scores (excluding driver-only) from the two drivers in the chosen constructor to the team score.
            for location_2021 in locations_2021:
                turbo_driver = location_2021_to_turbo_driver[location_2021]
                for driver_2022 in constructor_to_drivers_2022[constructor]:
                    multiplier = get_score_multiplier(location_2021, driver_2022, turbo_driver,
                                                      mega_driver_first_half_location, mega_driver_first_half,
                                                      mega_driver_second_half_location, mega_driver_second_half)
                    driver_score = get_driver_score(location_to_driver_to_score, driver_2022, location_2021)
                    team_score += driver_score * multiplier

            # If the best score so far, store it.
            location_2022_to_turbo_driver = {location_mapping_2021_2022[location_2021]: turbo_driver
                                             for location_2021, turbo_driver in location_2021_to_turbo_driver.items()}
            team = Team(team_score, constructor, team_drivers_2022,
                        mega_driver_first_half, location_mapping_2021_2022[mega_driver_first_half_location],
                        mega_driver_second_half, location_mapping_2021_2022[mega_driver_second_half_location],
                        location_2022_to_turbo_driver)
            top_teams.add(team)
            if len(top_teams) > 100:
                top_teams.pop(0)

    print(f'Explored all of the valid {team_count} teams.\n')
    for index, team in enumerate(reversed(top_teams)):
        print(f'=== TEAM AT POSITION {index + 1} WITH SCORE {team.score} ===')
        print(team)
        print()


if __name__ == "__main__":
    main()
