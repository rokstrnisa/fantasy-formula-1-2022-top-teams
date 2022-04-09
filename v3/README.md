# Fantasy Formula 1 2022 Top Teams, v3

A simple Python tool that helps you choose your
[Fantasy Formula 1](https://fantasy.formula1.com/) 2022 team based on the
current betting odds.

**The main addition to v2 is that it doesn't use the odds to directly imply
the order/ranking, but instead performs a Monte Carlo simulation.**

You also tell the program your current team, and it will take into account
the potential penalties due to substitutions beyond the first 3, as per the
[Subs Bank rules](https://fantasy.formula1.com/game-rules).

All the data needs to be entered manually into the code.

## Assumptions & Simplifications

1. All drivers qualify and finish the race, i.e. only the odds for the
   qualifications' winner, the fastest lap, and race winner are used.
2. Data from the previous races in this season is not taken into account. This
   means that constructor streaks are ignored. However, this turns out to be fine,
   since Ferrari is the constructor of choice anyway.
3. The tool chooses the turbo driver, but does not choose the mega driver. This
   is probably fine for the third race weekend, since mega drivers often
   benefit the most from driver streaks.

## Results

The program currently runs the simulation 1000 times, records the top team for
each run, then counts the number of wins for each team, and finally prints out
the teams by most wins. You can see the output in [`results.txt`](results.txt).
