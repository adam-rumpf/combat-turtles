"""Main Turtle Combat module.

The Turtle Combat module uses the turtle module to implement a game where two
turtles fight in an arena by shooting rockets at each other. This can be
played between a human player (using keyboard input) and an AI opponent, but
its main purpose is for having AI turtles play against each other.

The local player/ directory contains all of the AI submodules, each of which
should consist entirely of a subclass definition of the CombatTurtle class.
This module loads all submodules in the folder and allows the user to choose
pairs of submodules to play against each other.
"""

import modules.master as tc

def play_game():
    """Main driver for the Turtle Combat game."""

    p1 = tc.CombatTurtle("Turt", (2,1), None)
    print(p1.x)
