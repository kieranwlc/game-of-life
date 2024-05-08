# Game of Life
This is an interactive sandbox which contains an implementation of Conway's Game of Life
and several other Cellular Automata. 

Note: This application was developed for the COMP5400 module at the University of Leeds. A supporting
written report has been provided alongside this repository, which presents the work completed
and discusses the use of Cellular Automata as a biological model. This can also be found
in the [docs](/docs) folder.

## Dependencies
* Python 3

## Running
1. Install Python project dependencies:
```
cd src
pip3 install -r requirements.txt
```
2. Run game_of_life.py
```
python3 game_of_life.py
```

# User Guide
## User Interface
#### Grid
The grid is where the automaton output will be displayed. Click on cells within the grid
to interact with them.

#### Play/Pause
Press this button to start or pause the automaton on the current generation.

#### Options
Displays a list of automata to choose from.

#### Clear
Resets all cells in the grid to the default state.

#### Save
Saves the current grid state to a file which can be reloaded later.

#### Load
Load a previously saved file to the grid.

#### Speed Slider
Move the slider to the right to speed up the rate of automata generations.

#### Next
Advance the automata by one generation.

## Automata Options
Several automata are included in the 'options menu,' which have different rules.
#### Vanilla Game
This is the standard ruleset for Conway's Game of Life.
#### Rock Paper Scissors
Click a cell multiple times to change it's type. Each type is able to 'dominate' one type, but
loses to another type.
#### Immigration Game
Cells can be set to specific colors which interact with one another to form new varieties.
#### Shell Pattern
Cells propagate by following rules similar to those which determine crustacean shell patterns
#### Brian's Brain
Brian's Brain, another popular type of cellular automata which produces a lot of gliders.
