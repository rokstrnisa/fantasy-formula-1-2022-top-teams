# Fantasy Formula 1 2022 Top Teams, v5

A simple Python tool that helps you choose your
[Fantasy Formula 1](https://fantasy.formula1.com/) 2022 team based on the
current betting odds.

**The main change from v4 is that v5 now tracks all teams' scores within the
Monte Carlo simulations, not just the winners. Streaks are also taken into
account. Finally, the model now also chooses the mega driver.**

You also tell the program your current team, and it will take into account
the potential penalties due to substitutions beyond the first 3, as per the
[Subs Bank rules](https://fantasy.formula1.com/game-rules).

All the data needs to be entered manually into the code.

## Assumptions & Simplifications

1. All drivers have the same ability to overtake/defend their position.
2. No driver is disqualified, since we have no odds for this.

## Results

After 10k runs and with the wildcard enabled, an excerpt of the output
can be seen in [`results.txt`](results.txt). This assumes a budget of
$101.1M.
