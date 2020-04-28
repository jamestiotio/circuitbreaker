# Circuit Breaker
SUTD 2020 10.009 The Digital World Final Exam Programming Assignment

A cheeky game made using Python by James Raphael Tiovalen. Formatted with `autopep8`.

[Video Tutorial Link](https://youtu.be/JITYpzk-0Uo)

## Usage

Before playing this game, ensure that you have Python 3.7 or above (it should work for Python 3.6 as well). This game does NOT utilize Anaconda (i.e. there might be issues if you are using Anaconda to run this game). Clone this [repo](https://github.com/jamestiotio/circuitbreaker.git) and install the dependencies in `requirements.txt` by running the command `pip3 install -r requirements.txt`. Change directory to the `src` folder by running `cd src\` and run the `game.py` file by executing `python3 game.py`.

The `libdw` library is used for its state machine (`sm.SM`) capabilities, required for the bonus point for this assignment.

IMPORTANT NOTE: This game uses the `curses` library. While it is part of Python's standard library (and thus fulfilling the course assignment requirements), it is not bundled together for the Windows version of Python. If you are on Windows, you can install `curses` by running `pip3 install windows-curses`. It is included in the `requirements.txt` file. Running the `game.py` file will also automate this installation.

## Documentation

`curses` will act as the GUI handler library, while `libdw.sm.SM` will handle the state-based and data-based backend of the game's machinery.

The `stages.py` file currently contains our initial prototype of the turn-based RPG variant. Each instance of a variant is instantiated in the `game.py` file, which is then added into the `variants` list. The list's order is then shuffled to provide a more diverse variety of gameplay. `data.json` contains the full data of the different possible enemies to improve replayability.

For the `Pokemon` variant class, it contains the `BattleEngine` class which inherits the `sm.SM` class.

## Current Issues

- Each audio only plays once. Further work needs to be conducted to allow the audio to loop without using a blocking `while True` loop.
- Stopping audio only works on Windows for now.

## Future Implementations

- Add MORE COLORS
- Add MORE SPRITES
- Revamp the plot to actually focus on the grading of the SUTD Digital World Final Programming Game Assignment by an associate professor, with multiple game variants to be graded.
- Add a map system and an item system for the RPG game variant, as well as more characters.
- Add another game variant where it allows the player to code their own game in Python, thus being super meta (?).
- More game variants, maybe? (Ideas include: Snake, Tetris, Metroidvania-Style Platformer, Text-Based D&D-Style Adventure, Text-Based Multiplayer Shooter, Point-and-Click Detective Investigation, etc).
- Add an ongoing continuous plot that integrates all variants such as ending with a final boss battle which transitions/glitches between variants (more inspiration from Undertale Ink Sans Fight).
- Add some doggos.