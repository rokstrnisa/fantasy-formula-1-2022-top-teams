# Fantasy Formula 1 2022 Top Teams, v2

A simple Python tool that helps you choose your
[Fantasy Formula 1](https://fantasy.formula1.com/) 2022 team based on the
current betting odds.

You also tell the program your current team, and it will take into account
the potential penalties due to substitutions beyond the first 3, as per the
[Subs Bank rules](https://fantasy.formula1.com/game-rules).

All the data needs to be entered manually into the code.

## Assumptions & Simplifications

1. The betting odds for the qualifications/race winner imply the
   qualifications/race final order.
2. All drivers qualify and finish the race.
3. Data from the previous races in this season is not taken into account. This
   is fine for the second race location, since no streaks can happen yet.
4. The tool chooses the turbo driver, but does not choose the mega driver. This
   is probably fine for the second race location, since mega drivers often
   benefit the most from streaks.

## Results

The program is currently configured to output the top 100 teams, and assumes
that the wildcard is used. You can see the output in [`results.txt`](results.txt).
