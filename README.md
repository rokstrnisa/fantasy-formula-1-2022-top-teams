# Fantasy Formula 1 2022 Predictor

## Table of Contents
[Description](#description)
[Version History](#version-history)
[Languages, Libraries, and Modules](#languages-libraries-and-modules)
[Installation Instructions](#installation-instructions)
[Copyright and License](#copyright-and-license)

## Description
This tool is used to make predictions on Formula 1 race winners for the new 2022 season, to be utilized for [Fantasy Formula 1](https://fantasy.formula1.com/) team formation on.

Each version of the Fantasy Formula 1 2022 Predictor tool uses different estimation criteria to form predictions of the best fantasy team selection. It is recommended that multiple versions be run to achieve an ideal team selection. Further details on each version’s functionality can be found in the README of its according subdirectory.

## Version History
* [v1](v1): Predicts top N teams based on last year's data.
* [v2](v2): Uses external predictions to find the best team.
* [v3](v3): Uses external predictions with Monte Carlo to find the best team.
* [v4](v4): Like v3, but uses not-classifying odds rather than race odds.
* [v5](v5): Like v4, but tracks all teams' scores and considers streaks.

## Languages, Libraries, and Modules
This tool is written in python and utilizes the following modules and libraries:
* Itertools (Versions 1, 2, 3, 4, & 5) - https://docs.python.org/3/library/itertools.html
* Os.path (Version 1) - https://docs.python.org/3/library/os.path.html
* Numpy (Version 1) - https://numpy.org/
* Pandas (Version 1) - https://pandas.pydata.org/
* SortedContainers (Versions 1, 2) - https://pypi.org/project/sortedcontainers/0.8.4/
* Typing (Versions 3 & 4) - https://docs.python.org/3/library/typing.html
* Random (Versions 3, 4, & 5) - https://docs.python.org/3/library/random.html

## Installation Instructions
The code for this repository can be obtained via one of the following methods:
1) Clone this repository - Further details on this method can be found [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
2) Download the .zip file. Navigate to the main page of this directory, select the green "Code" button, and select "Download ZIP".

You must have python or python3 installed on your system to run this tool. You will also need the according modules and libraries installed for the version you are attempting to run, as listed in the "Languages, Libraries, and Modules" section. These libraries and modules may be installed individually at the command line using pip or pip3.

Version 1 of this tool relies on data from previous races, so the `'/data'` folder contained in the v1 directory must be present in the same directory as `'main.py'`.

## Copyright and License
This project is released under the MIT License. More information on the copyright of this code and its license limitations, [click here](https://github.com/rokstrnisa/fantasy-formula-1-2022-top-teams/blob/main/LICENSE).
