import itertools

from sortedcontainers import SortedList


constructor_to_drivers = {
    'Mercedes': ['United Kingdom Lewis Hamilton', 'United Kingdom George Russell'],
    'Red Bull Racing-RBPT': ['Netherlands Max Verstappen', 'Mexico Sergio Pérez'],
    'Ferrari': ['Monaco Charles Leclerc', 'Spain Carlos Sainz Jr.'],
    'McLaren-Mercedes': ['Australia Daniel Ricciardo', 'United Kingdom Lando Norris'],
    'Alpine-Renault': ['Spain Fernando Alonso', 'France Esteban Ocon'],
    'Aston Martin Aramco-Mercedes': ['Germany Nico Hulkenberg', 'Canada Lance Stroll'],
    'AlphaTauri-RBPT': ['France Pierre Gasly', 'Japan Yuki Tsunoda'],
    'Alfa Romeo-Ferrari': ['Finland Valtteri Bottas', 'China Guanyu Zhou'],
    'Williams-Mercedes': ['Canada Nicholas Latifi', 'Thailand Alexander Albon'],
    'Haas-Ferrari': ['Denmark Kevin Magnussen', 'Germany Mick Schumacher'],
}

constructors = constructor_to_drivers.keys()


def get_driver_to_constructor():
    result = {}
    for constructor, constructor_drivers in constructor_to_drivers.items():
        for driver in constructor_drivers:
            result[driver] = constructor
    return result


driver_to_constructor = get_driver_to_constructor()

constructor_prices = {
    'Mercedes': 34.2,
    'Red Bull Racing-RBPT': 32.3,
    'Ferrari': 25.7,
    'McLaren-Mercedes': 17.8,
    'Alpine-Renault': 13.9,
    'Aston Martin Aramco-Mercedes': 11.2,
    'AlphaTauri-RBPT': 10.4,
    'Alfa Romeo-Ferrari': 8.5,
    'Williams-Mercedes': 6.8,
    'Haas-Ferrari': 6.2,
}

driver_prices = {
    'United Kingdom Lewis Hamilton': 30.8,
    'Netherlands Max Verstappen': 30.5,
    'United Kingdom George Russell': 23.8,
    'Monaco Charles Leclerc': 18.6,
    'Mexico Sergio Pérez': 17.6,
    'Spain Carlos Sainz Jr.': 17.2,
    'United Kingdom Lando Norris': 15.5,
    'Australia Daniel Ricciardo': 13.9,
    'France Pierre Gasly': 13.4,
    'Spain Fernando Alonso': 12.3,
    'France Esteban Ocon': 12.3,
    'Germany Nico Hulkenberg': 11.5,
    'Finland Valtteri Bottas': 9.5,
    'Canada Lance Stroll': 9.2,
    'Japan Yuki Tsunoda': 8.5,
    'China Guanyu Zhou': 8.2,
    'Thailand Alexander Albon': 7.3,
    'Canada Nicholas Latifi': 6.9,
    'Germany Mick Schumacher': 6.4,
    'Denmark Kevin Magnussen': 5.9,
}

drivers = driver_prices.keys()

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

current_team_budget = 100.0
current_constructor = 'Red Bull Racing-RBPT'
current_team_drivers = {
    'Netherlands Max Verstappen',
    'Mexico Sergio Pérez',
    'Thailand Alexander Albon',
    'Germany Mick Schumacher',
    'Denmark Kevin Magnussen',
}

predicted_qualification_order = [
    'Netherlands Max Verstappen',
    'Monaco Charles Leclerc',
    'Spain Carlos Sainz Jr.',
    'Mexico Sergio Pérez',
    'United Kingdom Lewis Hamilton',
    'United Kingdom George Russell',
    'Finland Valtteri Bottas',
    'France Pierre Gasly',
    'Spain Fernando Alonso',
    'Japan Yuki Tsunoda',
    'Denmark Kevin Magnussen',
    'United Kingdom Lando Norris',
    'France Esteban Ocon',
    'China Guanyu Zhou',
    'Germany Mick Schumacher',
    'Australia Daniel Ricciardo',
    'Canada Nicholas Latifi',
    'Thailand Alexander Albon',
    'Canada Lance Stroll',
    'Germany Nico Hulkenberg',
]

predicted_race_fastest_lap = 'Netherlands Max Verstappen'

predicted_race_order = [
    'Netherlands Max Verstappen',
    'Monaco Charles Leclerc',
    'Spain Carlos Sainz Jr.',
    'United Kingdom Lewis Hamilton',
    'Mexico Sergio Pérez',
    'United Kingdom George Russell',
    'France Pierre Gasly',
    'Spain Fernando Alonso',
    'Finland Valtteri Bottas',
    'France Esteban Ocon',
    'Japan Yuki Tsunoda',
    'Denmark Kevin Magnussen',
    'Australia Daniel Ricciardo',
    'Germany Mick Schumacher',
    'United Kingdom Lando Norris',
    'China Guanyu Zhou',
    'Thailand Alexander Albon',
    'Canada Lance Stroll',
    'Canada Nicholas Latifi',
    'Germany Nico Hulkenberg',
]

driver_to_score = {}
driver_only_to_score = {}


def add_to_driver(driver, points):
    driver_to_score[driver] = driver_to_score.get(driver, 0) + points


def add_to_driver_only(driver, points):
    driver_only_to_score[driver] = driver_only_to_score.get(driver, 0) + points


def print_constructor_score(constructor_to_score):
    print('=== CONSTRUCTORS ===')
    for constructor in sorted(constructor_to_score, key=constructor_to_score.get, reverse=True):
        print(constructor, constructor_to_score[constructor])
    print()


def print_driver_score(combined_driver_to_score):
    print('=== DRIVERS ===')
    for driver in sorted(combined_driver_to_score, key=combined_driver_to_score.get, reverse=True):
        print(f'- {driver}: {combined_driver_to_score[driver]}')
    print()


def get_drivers(order, constructor):
    result = []
    for driver in order:
        if driver_to_constructor[driver] == constructor:
            result.append(driver)
    return result


def get_first_driver(order, constructor):
    return get_drivers(order, constructor)[0]


def get_driver_positions(order, constructor):
    result = []
    for index, driver in enumerate(order):
        if driver_to_constructor[driver] == constructor:
            result.append(index + 1)
    return result


def get_driver_position(order, specific_driver):
    for index, driver in enumerate(order):
        if driver == specific_driver:
            return index + 1


def score_predicted_qualification_order():
    # Assumed to have qualified. Not looking at streaks yet.
    for index, driver in enumerate(predicted_qualification_order):
        # +1 for Q1 finish (assumed to have finished)
        add_to_driver(driver, 1)
        # +2 for Q2 finish (assumed to have finished)
        add_to_driver(driver, 2)
        # +3 for Q3 finish (assumed to have finished)
        add_to_driver(driver, 3)
        # +1-10 for top 10 positions
        position = index + 1
        if position <= 10:
            add_to_driver(driver, 11 - position)
    for constructor in constructors:
        # +2 for driver qualifying ahead of their teammate (driver only)
        first = get_first_driver(predicted_qualification_order, constructor)
        add_to_driver_only(first, 2)


def score_predicted_race_fastest_lap():
    # +5 for fastest lap (assumed to be the driver that won)
    add_to_driver(predicted_race_fastest_lap, 5)


def score_predicted_race_order():
    # Assumed to have finished the race. Not looking at streaks yet.
    for index, driver in enumerate(predicted_race_order):
        # +1 for finish (assumed to have finished)
        add_to_driver(driver, 1)
        # +2/-2 per position gained/lost; max +10/-10
        previous_position = get_driver_position(predicted_qualification_order, driver)
        position = index + 1
        position_diff_points = max(min(2 * (previous_position - position), 10), -10)
        add_to_driver(driver, position_diff_points)
        # +1-25 for position
        position_points = race_position_to_points.get(position)
        if position_points:
            add_to_driver(driver, position_points)
    for constructor in constructors:
        # +3 for finishing ahead of teammate (driver only)
        first = get_first_driver(predicted_race_order, constructor)
        add_to_driver_only(first, 3)


def get_constructor_to_score():
    constructor_to_score = {}
    for driver, score in driver_to_score.items():
        constructor = driver_to_constructor[driver]
        constructor_to_score[constructor] = constructor_to_score.get(constructor, 0) + score
    return constructor_to_score


def get_combined_driver_to_score():
    combined_driver_to_score = {}
    for driver in driver_to_score.keys():
        combined_driver_to_score[driver] = driver_to_score[driver] + driver_only_to_score.get(driver, 0)
    return combined_driver_to_score


class Team:
    def __init__(self, score, constructor, driver_selection, turbo_driver, substitutions_needed):
        self.score = score
        self.constructor = constructor
        self.driver_selection = driver_selection
        self.turbo_driver = turbo_driver
        self.substitutions_needed = substitutions_needed

    def __lt__(self, other):
        return self.score < other.score

    def __str__(self):
        return f'Constructor: {self.constructor}\n' \
               f'Drivers: {self.driver_selection}\n' \
               f'Turbo Driver: {self.turbo_driver}\n' \
               f'Substitutions Needed: {self.substitutions_needed}'


def main():
    score_predicted_qualification_order()
    score_predicted_race_fastest_lap()
    score_predicted_race_order()
    combined_driver_to_score = get_combined_driver_to_score()

    print(f'Current Constructor: {current_constructor}')
    print(f'Current Drivers: {current_team_drivers}')
    print()

    use_wildcard = True

    # Keep track of the top teams.
    team_count = 0
    top_teams = SortedList()

    # Go through all driver combinations of size 5.
    for team_drivers in itertools.combinations(drivers, 5):
        team_drivers_price = sum(map(lambda d: driver_prices[d], team_drivers))

        # Go through all constructors.
        for constructor in constructors:

            # Ignore selection if the price is too high.
            price = team_drivers_price + constructor_prices[constructor]
            if price > current_team_budget:
                continue

            team_count += 1

            # Pick the turbo driver based on the top score in the next location from the selected drivers, excluding
            # drivers more expensive than $20M.
            top_driver_score = float('-inf')
            turbo_driver = None
            for driver in team_drivers:
                if driver_prices[driver] >= 20:
                    continue
                driver_score = driver_to_score[driver]
                if driver_score > top_driver_score:
                    top_driver_score = driver_score
                    turbo_driver = driver

            team_score = 0

            # Count substitutions needed and deduct score appropriately (unless using wildcard).
            substitutions_needed = 0
            for driver in team_drivers:
                if driver not in current_team_drivers:
                    substitutions_needed += 1
            if constructor != current_constructor:
                substitutions_needed += 1
            if not use_wildcard:
                substitutions_incurring_penalty = max(substitutions_needed - 3, 0)
                team_score -= substitutions_incurring_penalty * 10

            # Add driver scores to the team score.
            for driver in team_drivers:
                multiplier = 2 if driver == turbo_driver else 1
                team_score += combined_driver_to_score[driver] * multiplier

            # Add scores (excluding driver-only) from the two drivers in the chosen constructor to the team score.
            for driver in constructor_to_drivers[constructor]:
                multiplier = 2 if driver == turbo_driver else 1
                team_score += driver_to_score[driver] * multiplier

            # If the best score so far, store it.
            team = Team(team_score, constructor, team_drivers, turbo_driver, substitutions_needed)
            top_teams.add(team)
            if len(top_teams) > 100:
                top_teams.pop(0)

    print(f'Explored all of the valid {team_count} teams.\n')

    if use_wildcard:
        print(f'Using wildcard!\n')

    for index, team in enumerate(reversed(top_teams)):
        print(f'=== TEAM AT POSITION {index + 1} WITH SCORE {team.score} ===')
        print(team)
        print()


if __name__ == "__main__":
    main()
