# Fantasy Formula 1 2022 Top Teams, v1

A simple Python tool that finds the top N teams for the
[Fantasy Formula 1](https://fantasy.formula1.com/) 2022.

The model also picks the turbo driver for each location, and the mega driver
for two locations.

## Assumptions & Simplifications

1. The predictions are made based only on 2021 data. While this is certainly
   far from ideal, the recent data is probably much more relevant than the
   older data.
2. The two drivers of a particular constructor in 2021 are considered
   equivalent to the two drivers of the same constructor in 2022. The
   exact driver mapping can be seen in `driver_mapping_2022_2021`. Without
   this assumption, the model would be substantially more complex. For
   example, it assumes that George Russell will be roughly as good in
   Mercedes 2022 as Valtteri Bottas was in Mercedes in 2021.
3. The model assumes that the 2021 locations are equivalent to 2022 locations.
   The exact location mapping can be seen in `location_mapping_2021_2022`. The
   sprints locations are also assumed to be equivalent.
4. The model assumes that the prices of the drivers don't change.
5. The model doesn't make use of subs (Subs Bank or Wildcard), i.e. it assumes
   that the team stays constant.

## Results

The program is currently configured to output the top 100 teams. You can see
the output in [`results.txt`](results.txt).
