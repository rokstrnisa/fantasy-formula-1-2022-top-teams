# Fantasy Formula 1 2022 Top Teams, v4

A simple Python tool that helps you choose your
[Fantasy Formula 1](https://fantasy.formula1.com/) 2022 team based on the
current betting odds.

**The main addition to v3 is that it doesn't use race odds, but instead uses
not-classifying odds.**

You also tell the program your current team, and it will take into account
the potential penalties due to substitutions beyond the first 3, as per the
[Subs Bank rules](https://fantasy.formula1.com/game-rules).

All the data needs to be entered manually into the code.

## Assumptions & Simplifications

1. All drivers have the same ability to overtake/defend their position.
2. Data from the previous races in this season is not taken into account. This
   means that constructor streaks are ignored.
3. The tool chooses the turbo driver, but does not choose the mega driver. This
   is probably fine for the fourth race weekend, since mega drivers often
   benefit the most from driver streaks.

## Results

After 10k runs and with the wildcard enabled, an excerpt of the output
can be seen in [`results.txt`](results.txt).
