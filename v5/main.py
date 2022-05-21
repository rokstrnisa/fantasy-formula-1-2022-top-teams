import random

import itertools

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

constructor_to_shorthand = {
    'Mercedes': 'MER',
    'Red Bull Racing-RBPT': 'RBR',
    'Ferrari': 'FER',
    'McLaren-Mercedes': 'MCL',
    'Alpine-Renault': 'ARE',
    'Aston Martin Aramco-Mercedes': 'AMA',
    'AlphaTauri-RBPT': 'ATA',
    'Alfa Romeo-Ferrari': 'ARO',
    'Williams-Mercedes': 'WIL',
    'Haas-Ferrari': 'HAA',
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
    'Mercedes': 33.8,
    'Red Bull Racing-RBPT': 32.7,
    'Ferrari': 25.7,
    'McLaren-Mercedes': 17.6,
    'Alpine-Renault': 13.9,
    'Aston Martin Aramco-Mercedes': 10.9,
    'AlphaTauri-RBPT': 10.1,
    'Alfa Romeo-Ferrari': 8.4,
    'Haas-Ferrari': 6.5,
    'Williams-Mercedes': 6.5,
}

driver_prices = {
    'United Kingdom Lewis Hamilton': 30.3,
    'Netherlands Max Verstappen': 30.1,
    'United Kingdom George Russell': 23.9,
    'Monaco Charles Leclerc': 19.0,
    'Mexico Sergio Pérez': 18.5,
    'Spain Carlos Sainz Jr.': 17.2,
    'United Kingdom Lando Norris': 16.0,
    'Australia Daniel Ricciardo': 13.8,
    'France Pierre Gasly': 13.0,
    'France Esteban Ocon': 12.4,
    'Spain Fernando Alonso': 12.4,
    'Germany Sebastian Vettel': 11.4,
    'Finland Valtteri Bottas': 9.4,
    'Canada Lance Stroll': 8.9,
    'China Guanyu Zhou': 8.3,
    'Japan Yuki Tsunoda': 8.3,
    'Thailand Alexander Albon': 7.9,
    'Canada Nicholas Latifi': 6.6,
    'Germany Mick Schumacher': 6.2,
    'Denmark Kevin Magnussen': 6.1,
}

drivers = driver_prices.keys()

driver_to_shorthand = {
    'United Kingdom Lewis Hamilton': 'HAM',
    'Netherlands Max Verstappen': 'VER',
    'United Kingdom George Russell': 'RUS',
    'Monaco Charles Leclerc': 'LEC',
    'Mexico Sergio Pérez': 'PER',
    'Spain Carlos Sainz Jr.': 'SAI',
    'United Kingdom Lando Norris': 'NOR',
    'Australia Daniel Ricciardo': 'RIC',
    'France Pierre Gasly': 'GAS',
    'France Esteban Ocon': 'OCO',
    'Spain Fernando Alonso': 'ALO',
    'Germany Sebastian Vettel': 'VET',
    'Finland Valtteri Bottas': 'BOT',
    'Canada Lance Stroll': 'STR',
    'China Guanyu Zhou': 'ZHO',
    'Japan Yuki Tsunoda': 'TSU',
    'Thailand Alexander Albon': 'ALB',
    'Canada Nicholas Latifi': 'LAT',
    'Germany Mick Schumacher': 'MSC',
    'Denmark Kevin Magnussen': 'MAG',
}

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

upcoming_driver_qualifying_streak = {}

upcoming_constructor_qualifying_streak = {
    'Ferrari',
    'Red Bull Racing-RBPT',
}

upcoming_driver_race_streak = {
    'Mexico Sergio Pérez',
}

upcoming_constructor_race_streak = {
    'Red Bull Racing-RBPT',
}

current_constructor = 'Ferrari'
current_team_drivers = {
    'Netherlands Max Verstappen',
    'Monaco Charles Leclerc',
    'Denmark Kevin Magnussen',
    'Thailand Alexander Albon',
    'Germany Mick Schumacher',
}

qualifying_winner_driver_to_odds = {
    'Monaco Charles Leclerc': 4/5,
    'Netherlands Max Verstappen': 6/4,
    'Spain Carlos Sainz Jr.': 6/1,
    'United Kingdom Lewis Hamilton': 25/1,
    'Mexico Sergio Pérez': 25/1,
    'United Kingdom George Russell': 25/1,
    'United Kingdom Lando Norris': 125/1,
    'Finland Valtteri Bottas': 150/1,
    'Spain Fernando Alonso': 225/1,
    'Canada Nicholas Latifi': 500/1,
    'Germany Sebastian Vettel': 500/1,
    'France Esteban Ocon': 500/1,
    'Germany Mick Schumacher': 500/1,
    'Australia Daniel Ricciardo': 500/1,
    'France Pierre Gasly': 500/1,
    'Japan Yuki Tsunoda': 500/1,
    'Denmark Kevin Magnussen': 500/1,
    'China Guanyu Zhou': 500/1,
    'Canada Lance Stroll': 500/1,
    'Thailand Alexander Albon': 500/1,
}

fastest_lap_driver_to_odds = {
    'Monaco Charles Leclerc': 6/5,
    'Netherlands Max Verstappen': 6/5,
    'Spain Carlos Sainz Jr.': 13/2,
    'Mexico Sergio Pérez': 10/1,
    'United Kingdom Lewis Hamilton': 30/1,
    'United Kingdom George Russell': 30/1,
    'Finland Valtteri Bottas': 70/1,
    'Spain Fernando Alonso': 70/1,
    'Australia Daniel Ricciardo': 100/1,
    'United Kingdom Lando Norris': 100/1,
    'France Esteban Ocon': 100/1,
    'Denmark Kevin Magnussen': 100/1,
    'France Pierre Gasly': 100/1,
    'Germany Sebastian Vettel': 275/1,
    'Germany Mick Schumacher': 275/1,
    'Canada Nicholas Latifi': 275/1,
    'Canada Lance Stroll': 275/1,
    'Thailand Alexander Albon': 275/1,
    'Japan Yuki Tsunoda': 275/1,
    'China Guanyu Zhou': 275/1,
}

not_classifying_driver_to_odds = {
    'Canada Nicholas Latifi': 9/4,
    'Canada Lance Stroll': 5/2,
    'Japan Yuki Tsunoda': 5/2,
    'China Guanyu Zhou': 13/5,
    'Germany Sebastian Vettel': 3/1,
    'Denmark Kevin Magnussen': 3/1,
    'France Esteban Ocon': 3/1,
    'Germany Mick Schumacher': 16/5,
    'Australia Daniel Ricciardo': 16/5,
    'Spain Fernando Alonso': 16/5,
    'United Kingdom Lando Norris': 7/2,
    'Finland Valtteri Bottas': 7/2,
    'France Pierre Gasly': 7/2,
    'Thailand Alexander Albon': 7/2,
    'Netherlands Max Verstappen': 4/1,
    'United Kingdom George Russell': 4/1,
    'Spain Carlos Sainz Jr.': 4/1,
    'United Kingdom Lewis Hamilton': 4/1,
    'Monaco Charles Leclerc': 9/2,
    'Mexico Sergio Pérez': 9/2,
}


def odds_to_probability(odds):
    return 1.0 / (odds + 1.0)


def get_winner(driver_to_odds):
    probability_sum = 0.0
    driver_to_probability_sum = {}
    for driver, odds in driver_to_odds.items():
        probability = odds_to_probability(odds)
        probability_sum += probability
        driver_to_probability_sum[driver] = probability_sum
    random_point = random.random() * probability_sum
    for driver, probability_sum in driver_to_probability_sum.items():
        if probability_sum > random_point:
            return driver
    print(random_point)
    raise 'Unexpected case.'


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
constructor_only_score = {}


def add_to_driver(driver, points):
    driver_to_score[driver] = driver_to_score.get(driver, 0) + points


def add_to_driver_only(driver, points):
    driver_only_to_score[driver] = driver_only_to_score.get(driver, 0) + points


def add_to_constructor_only(constructor, points):
    constructor_only_score[constructor] = constructor_only_score.get(constructor, 0) + points


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
    for index, driver in enumerate(qualifying_order):
        # +1 for Q1 finish
        add_to_driver(driver, 1)
        # +2 for Q2 finish
        add_to_driver(driver, 2)
        # +3 for Q3 finish
        add_to_driver(driver, 3)
        # +1-10 for top 10 positions
        position = index + 1
        if position <= 10:
            add_to_driver(driver, 11 - position)
            # +5 for top 10 for 5 qualifications in a row
            if driver in upcoming_driver_qualifying_streak:
                add_to_driver(driver, 5)
    for driver in drivers:
        # -5 for not qualifying
        if driver not in qualifying_order:
            add_to_driver(driver, -5)
        # Ignored since no data: -10 points for being disqualified
    for constructor in constructors:
        # +2 for driver qualifying ahead of their teammate (driver only)
        first = get_first_driver(qualifying_order, constructor)
        if first:
            add_to_driver_only(first, 2)
        # +5 for constructor when both drivers within first 10 for 3 qualifications in a row
        if constructor in upcoming_constructor_qualifying_streak \
                and all(p <= 10 for p in get_driver_positions(qualifying_order, constructor)):
            add_to_constructor_only(constructor, 5)


def score_race_fastest_lap(fastest_lap):
    # +5 for fastest lap
    add_to_driver(fastest_lap, 5)


def score_race_order(qualifying_order, race_order):
    for index, driver in enumerate(race_order):
        # +1 for finish
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
            # +10 for top 10 for 5 qualifications in a row
            if driver in upcoming_driver_race_streak:
                add_to_driver(driver, 10)
    for driver in drivers:
        # -10 for not classifying
        if driver not in race_order:
            add_to_driver(driver, -10)
        # Ignored since no data: -10 points for being disqualified
    for constructor in constructors:
        # +3 for finishing ahead of teammate (driver only)
        first = get_first_driver(race_order, constructor)
        if first:
            add_to_driver_only(first, 3)
        # +10 for constructor when both drivers within first 10 for 3 qualifications in a row
        if constructor in upcoming_constructor_race_streak \
                and all(p <= 10 for p in get_driver_positions(race_order, constructor)):
            add_to_constructor_only(constructor, 10)


def get_combined_driver_to_score():
    combined_driver_to_score = {}
    for driver in driver_to_score.keys():
        combined_driver_to_score[driver] = driver_to_score[driver] + driver_only_to_score.get(driver, 0)
    return combined_driver_to_score


class Team:
    def __init__(self, constructor, driver_selection, substitutions_needed, turbo_driver, mega_driver=None):
        self.constructor = constructor
        self.driver_selection = driver_selection
        self.substitutions_needed = substitutions_needed
        self.turbo_driver = turbo_driver
        self.mega_driver = mega_driver

    def __eq__(self, other):
        return self.constructor == other.constructor and self.driver_selection == other.driver_selection \
               and self.mega_driver == other.mega_driver and self.turbo_driver == other.turbo_driver

    def __hash__(self):
        return hash((self.constructor, self.driver_selection, self.mega_driver, self.turbo_driver))

    def __str__(self):
        drivers_string = ', '.join([self.__driver_to_string(d) for d in self.driver_selection])
        return f'({drivers_string}, {constructor_to_shorthand[self.constructor]}) [{self.substitutions_needed}]'

    def __driver_to_string(self, driver):
        suffix = ''
        if driver == self.mega_driver:
            suffix = ' M'
        elif driver == self.turbo_driver:
            suffix = ' T'
        return f'{driver_to_shorthand[driver]}{suffix}'


budget = 101.8
use_wildcard = True
team_to_score_sum = {}
use_mega_driver = False


def score_all_possible_teams(qualifying_order, fastest_lap, race_order):
    global driver_to_score
    global driver_only_to_score
    global constructor_only_score
    global team_to_score_sum

    driver_to_score = {}
    driver_only_to_score = {}
    constructor_only_score = {}

    score_qualifying_order(qualifying_order)
    score_race_fastest_lap(fastest_lap)
    score_race_order(qualifying_order, race_order)

    combined_driver_to_score = get_combined_driver_to_score()

    # Go through all driver combinations of size 5.
    for team_drivers in itertools.combinations(drivers, 5):
        team_drivers_price = sum(map(lambda d: driver_prices[d], team_drivers))

        # Go through all constructors.
        for constructor in constructors:

            constructor_drivers = constructor_to_drivers[constructor]

            # Ignore selection if the price is too high.
            price = team_drivers_price + constructor_prices[constructor]
            if price > budget:
                continue

            # Pick both the turbo driver and the mega driver based on the score they will contribute, where the two
            # cannot be the same driver, and where the turbo driver cannot be more expensive than $20M.
            team_driver_to_score = {d: combined_driver_to_score[d] for d in team_drivers}
            # Only need to consider the top 3 scoring members of the team, since (according to the current prices) all
            # possible teams can contain at most 2 members with price above $20M. The cheapest team containing all 3
            # drivers with price above $20M would require a budget of $103.3M.
            top_driver_score_pairs = sorted(team_driver_to_score.items(), key=lambda kv: kv[1], reverse=True)[:3]
            top_turbo_driver = None
            top_mega_driver = None
            if use_mega_driver:
                top_turbo_mega_score = float('-inf')
                for turbo_driver, turbo_driver_score in top_driver_score_pairs:
                    if driver_prices[turbo_driver] >= 20:
                        continue
                    for mega_driver, mega_driver_score in top_driver_score_pairs:
                        if mega_driver == turbo_driver:
                            continue
                        mega_turbo_score = 2*turbo_driver_score + 3*mega_driver_score
                        if mega_turbo_score > top_turbo_mega_score:
                            top_turbo_mega_score = mega_turbo_score
                            top_turbo_driver = turbo_driver
                            top_mega_driver = mega_driver
            else:
                top_turbo_score = float('-inf')
                for turbo_driver in team_driver_to_score:
                    if driver_prices[turbo_driver] < 20 and team_driver_to_score[turbo_driver] > top_turbo_score:
                        top_turbo_driver = turbo_driver
                        top_turbo_score = team_driver_to_score[turbo_driver]

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
                multiplier = 1
                if driver == top_turbo_driver:
                    multiplier = 2
                elif driver == top_mega_driver:
                    multiplier = 3
                team_score += combined_driver_to_score[driver] * multiplier

            # Add scores (excluding driver-only) from the two drivers in the chosen constructor to the team score.
            # As per the rules, these are added without the multiplier.
            for driver in constructor_drivers:
                team_score += driver_to_score[driver]

            # Add constructor-only score (e.g. constructor streaks).
            team_score += constructor_only_score.get(constructor, 0)

            # Count the team's score towards its sum.
            team = Team(constructor, team_drivers, substitutions_needed, top_turbo_driver, top_mega_driver)
            team_to_score_sum.setdefault(team, 0)
            team_to_score_sum[team] += team_score


def get_drivers_not_classifying():
    result = set()
    for driver, not_classifying_odds in not_classifying_driver_to_odds.items():
        not_classifying_probability = odds_to_probability(not_classifying_odds)
        if random.random() < not_classifying_probability:
            result.add(driver)
    return result


def main():
    runs = 10000
    for run in range(runs):
        drivers_not_classifying = get_drivers_not_classifying()
        qualifying_order = get_order(qualifying_winner_driver_to_odds)
        qualifying_order = [d for d in qualifying_order if d not in drivers_not_classifying]
        fastest_lap_order = get_order(fastest_lap_driver_to_odds)
        fastest_lap_order = [d for d in fastest_lap_order if d not in drivers_not_classifying]
        fastest_lap = fastest_lap_order[0]
        race_order = qualifying_order.copy()
        score_all_possible_teams(qualifying_order, fastest_lap, race_order)
        if run > 0 and run % 10 == 0 or run == runs - 1:
            print(f'================ AFTER {run:5} RUNS ================')
            for position, team in enumerate(sorted(team_to_score_sum, key=team_to_score_sum.get, reverse=True)):
                if position < 30:
                    print(f'{position+1:2}. {team}: {team_to_score_sum[team]/(run+1):.2f} ')


if __name__ == "__main__":
    main()
