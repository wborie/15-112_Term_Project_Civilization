# 15-112_Term_Project_Civilization
Final Project for 15-112 CMU course. A basic remake of a video game called Civilization 5, which is a turn-based strategy game played on a grid of hexagonal tiles.

Usage: 
1. Download Term_Project.py and Main_Menu.pgm
2. Go to download directory
3. python Term_Project.py

Functionality:
1. Clicking on an empty tile causes nothing to happen.

2. Clicking on a tile with a unit on it highlights that tile and allows
you to move that unit. If (after clicking on the unit) you want to move
it, press 'm' and a display of possible moves will be brought up. You can
move to any of the tiles that are newly highlighted (currently in blue) by
clicking on the desired tile. Illegal moves (such as moving outside the
board, onto another unit, or through another unit) will not be executed.

3. Clicking on units will bring up a little box on the bottom-left corner
of the window, the first line of information in that box displays the type
of that unit, the second line displays the health of that unit.

4. If you are currently selecting a "settler" unit (a settler unit is
highlighted), pressing 'p' will place a city on the current tile of that
settler unit, destroying that unit in the process. A city is for now just
a specially colored tile (a lot more to be done here).

5. Clicking on a tile with a city will bring up a little box on the
bottom-right corner of the window, which displays the name of that city and
it's production. You can choose production by highlighting a city and
using the '1' '2' '3' and '4' keys.

6. Pressing 'r' will end the current turn and start a new turn. New turns
reset the movement ability of each unit and spawn (and move) enemy units.

7. Pressing 'a' while one of your units is highlighted will display the
tiles that can be attacked that turn. Clicking on a tile after pressing
'a' while a unit is selected will
cause the selected unit to attack the unit on the clicked tile.
