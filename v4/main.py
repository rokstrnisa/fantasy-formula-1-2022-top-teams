import random

import itertools
from typing import Optional

constructor_to_drivers = {
    'Mercedes': ['United Kingdom Lewis Hamilton', 'United Kingdom George Russell'],
    'Red Bull Racing-RBPT': ['Netherlands Max Verstappen', 'Mexico Sergio Pérez'],
    'Ferrari': ['Monaco Charles Leclerc', 'Spain Carlos Sainz Jr.'],
    'McLaren-Mercedes': ['Australia Daniel Ricciardo', 'United Kingdom Lando Norris'],
    'Alpine-Renault': ['Spain Fernando Alonso', 'France Esteban Ocon'],
    'Aston Martin Aramco-Mercedes': ['Germany Sebastian Vettel', 'Canada Lance Stroll'],
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
    'Mercedes': 33.9,
    'Red Bull Racing-RBPT': 32.1,
    'Ferrari': 25.8,
    'McLaren-Mercedes': 17.5,
    'Alpine-Renault': 14.1,
    'Aston Martin Aramco-Mercedes': 11.0,
    'AlphaTauri-RBPT': 10.2,
    'Alfa Romeo-Ferrari': 8.4,
    'Haas-Ferrari': 6.7,
    'Williams-Mercedes': 6.6,
}

driver_prices = {
    'United Kingdom Lewis Hamilton': 30.4,
    'Netherlands Max Verstappen': 30.3,
    'United Kingdom George Russell': 23.9,
    'Monaco Charles Leclerc': 18.8,
    'Mexico Sergio Pérez': 18.0,
    'Spain Carlos Sainz Jr.': 17.3,
    'United Kingdom Lando Norris': 15.9,
    'Australia Daniel Ricciardo': 14.0,
    'France Pierre Gasly': 13.1,
    'France Esteban Ocon': 12.6,
    'Spain Fernando Alonso': 12.5,
    'Germany Sebastian Vettel': 11.4,
    'Finland Valtteri Bottas': 9.4,
    'Canada Lance Stroll': 9.0,
    'China Guanyu Zhou': 8.5,
    'Japan Yuki Tsunoda': 8.4,
    'Thailand Alexander Albon': 7.1,
    'Canada Nicholas Latifi': 6.7,
    'Germany Mick Schumacher': 6.2,
    'Denmark Kevin Magnussen': 6.0,
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

current_constructor = 'Ferrari'
current_team_drivers = {
    'Netherlands Max Verstappen',
    'Monaco Charles Leclerc',
    'Spain Fernando Alonso',
    'Thailand Alexander Albon',
    'Denmark Kevin Magnussen',
}

qualifying_winner_driver_to_odds = {
    'Monaco Charles Leclerc': 1/1,
    'Netherlands Max Verstappen': 8/5,
    'Spain Carlos Sainz Jr.': 11/2,
    'Mexico Sergio Pérez': 12/1,
    'United Kingdom Lewis Hamilton': 14/1,
    'United Kingdom George Russell': 30/1,
    'United Kingdom Lando Norris': 125/1,
    'Australia Daniel Ricciardo': 150/1,
    'Spain Fernando Alonso': 175/1,
    'France Esteban Ocon': 200/1,
    'France Pierre Gasly': 325/1,
    'Finland Valtteri Bottas': 425/1,
    'Canada Lance Stroll': 500/1,
    'Canada Nicholas Latifi': 500/1,
    'China Guanyu Zhou': 500/1,
    'Denmark Kevin Magnussen': 500/1,
    'Germany Mick Schumacher': 500/1,
    'Germany Sebastian Vettel': 500/1,
    'Japan Yuki Tsunoda': 500/1,
    'Thailand Alexander Albon': 500/1,
}

fastest_lap_driver_to_odds = {
    'Netherlands Max Verstappen': 8/5,
    'Monaco Charles Leclerc': 8/5,
    'Spain Carlos Sainz Jr.': 9/2,
    'Mexico Sergio Pérez': 13/2,
    'United Kingdom Lewis Hamilton': 12/1,
    'United Kingdom George Russell': 20/1,
    'United Kingdom Lando Norris': 70/1,
    'Spain Fernando Alonso': 75/1,
    'Australia Daniel Ricciardo': 125/1,
    'France Esteban Ocon': 150/1,
    'France Pierre Gasly': 175/1,
    'Finland Valtteri Bottas': 225/1,
    'Denmark Kevin Magnussen': 275/1,
    'Germany Mick Schumacher': 275/1,
    'Japan Yuki Tsunoda': 275/1,
    'China Guanyu Zhou': 325/1,
    'Canada Lance Stroll': 500/1,
    'Canada Nicholas Latifi': 500/1,
    'Germany Sebastian Vettel': 500/1,
    'Thailand Alexander Albon': 500/1,
}

not_classifying_driver_to_odds = {
    'China Guanyu Zhou': 3/1,
    'Canada Nicholas Latifi': 16/5,
    'Canada Lance Stroll': 16/5,
    'Japan Yuki Tsunoda': 16/5,
    'Germany Sebastian Vettel': 16/5,
    'Germany Mick Schumacher': 4/1,
    'Spain Carlos Sainz Jr.': 4/1,
    'Netherlands Max Verstappen': 4/1,
    'France Esteban Ocon': 4/1,
    'Thailand Alexander Albon': 4/1,
    'Spain Fernando Alonso': 4/1,
    'France Pierre Gasly': 4/1,
    'Mexico Sergio Pérez': 4/1,
    'Denmark Kevin Magnussen': 9/2,
    'Australia Daniel Ricciardo': 9/2,
    'United Kingdom Lando Norris': 5/1,
    'United Kingdom George Russell': 5/1,
    'Monaco Charles Leclerc': 11/2,
    'Finland Valtteri Bottas': 11/2,
    'United Kingdom Lewis Hamilton': 11 / 2,
}


def odds_to_probability(odds):
    return 1.0 / (odds + 1.0)


def get_winner(driver_to_odds):
    probability_sum = 0.0
    for driver, odds in driver_to_odds.items():
        probability = odds_to_probability(odds)
        probability_sum += probability
    normalized_probability_sum = 0
    driver_to_normalized_probability_sum = {}
    for driver, odds in driver_to_odds.items():
        probability = odds_to_probability(odds)
        normalized_probability = probability / probability_sum
        normalized_probability_sum += normalized_probability
        driver_to_normalized_probability_sum[driver] = normalized_probability_sum
    # print(driver_to_normalized_probability_sum)
    random_point = random.random()
    for driver, normalized_probability_sum in driver_to_normalized_probability_sum.items():
        if normalized_probability_sum > random_point:
            return driver
    print(random_point)
    raise 'hmm'


def get_order(driver_to_odds):
    order = []
    driver_to_odds = dict(driver_to_odds)
    while len(driver_to_odds) != 0:
        winner = get_winner(driver_to_odds)
        order.append(winner)
        del driver_to_odds[winner]
    return order


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
    constructor_drivers = get_drivers(order, constructor)
    return constructor_drivers[0] if len(constructor_drivers) > 0 else None


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


def score_qualifying_order(qualifying_order):
    # Assumed to have qualified. Not looking at streaks yet.
    for index, driver in enumerate(qualifying_order):
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
        first = get_first_driver(qualifying_order, constructor)
        add_to_driver_only(first, 2)


def score_race_fastest_lap(fastest_lap):
    # +5 for fastest lap (assumed to be the driver that won)
    add_to_driver(fastest_lap, 5)


def score_race_order(qualifying_order, race_order):
    # Assumed to have finished the race. Not looking at streaks yet.
    for index, driver in enumerate(race_order):
        # +1 for finish (assumed to have finished)
        add_to_driver(driver, 1)
        # +2/-2 per position gained/lost; max +10/-10
        previous_position = get_driver_position(qualifying_order, driver)
        position = index + 1
        position_diff_points = max(min(2 * (previous_position - position), 10), -10)
        add_to_driver(driver, position_diff_points)
        # +1-25 for position
        position_points = race_position_to_points.get(position)
        if position_points:
            add_to_driver(driver, position_points)
    for constructor in constructors:
        # +3 for finishing ahead of teammate (driver only)
        first = get_first_driver(race_order, constructor)
        if first:
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

    def __eq__(self, other):
        return self.constructor == other.constructor and self.driver_selection == other.driver_selection \
               and self.turbo_driver == other.turbo_driver

    def __hash__(self):
        return hash((self.constructor, self.driver_selection, self.turbo_driver))

    def __str__(self):
        return f'Constructor: {self.constructor}\n' \
               f'Drivers: {self.driver_selection}\n' \
               f'Turbo Driver: {self.turbo_driver}\n' \
               f'Substitutions Needed: {self.substitutions_needed}'


total_value = 100.9
use_wildcard = True


def get_winning_team(qualifying_order, fastest_lap, race_order):
    global driver_to_score
    global driver_only_to_score

    driver_to_score = {}
    driver_only_to_score = {}

    score_qualifying_order(qualifying_order)
    score_race_fastest_lap(fastest_lap)
    score_race_order(qualifying_order, race_order)

    combined_driver_to_score = get_combined_driver_to_score()

    team_count = 0
    top_team: Optional[Team] = None

    # Go through all driver combinations of size 5.
    for team_drivers in itertools.combinations(drivers, 5):
        team_drivers_price = sum(map(lambda d: driver_prices[d], team_drivers))

        # Go through all constructors.
        for constructor in constructors:

            # Ignore selection if the price is too high.
            price = team_drivers_price + constructor_prices[constructor]
            if price > total_value:
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
            if not top_team or team.score > top_team.score:
                top_team = team

    return top_team


def remove_drivers_not_classifying(qualifying_order):
    for driver, not_classifying_odds in not_classifying_driver_to_odds.items():
        not_classifying_probability = odds_to_probability(not_classifying_odds)
        if random.random() < not_classifying_probability:
            qualifying_order.remove(driver)


def main():
    team_to_win_count = {}
    team_to_score_sum = {}
    for run in range(100000):
        qualifying_order = get_order(qualifying_winner_driver_to_odds)
        fastest_lap = get_order(fastest_lap_driver_to_odds)[0]
        race_order = qualifying_order.copy()
        remove_drivers_not_classifying(race_order)
        winning_team = get_winning_team(qualifying_order, fastest_lap, race_order)
        team_to_win_count.setdefault(winning_team, 0)
        team_to_score_sum.setdefault(winning_team, 0)
        team_to_win_count[winning_team] += 1
        team_to_score_sum[winning_team] += winning_team.score
        if run != 0 and run % 100 == 0:
            print('======================================')
            print(f'========== AFTER {run:5} RUNS ==========')
            print('======================================')
            for position, team in enumerate(sorted(team_to_win_count, key=team_to_win_count.get, reverse=True)):
                if position < 5:
                    print(f'===== {team_to_win_count[team]} WINS =====')
                    print(team)
                    print(f'Total score across wins: {team_to_score_sum[team]}')
                    print(f'Average score per win: {team_to_score_sum[team]/team_to_win_count[team]:.2f}')


if __name__ == "__main__":
    main()
