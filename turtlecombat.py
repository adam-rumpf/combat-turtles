"""Main Turtle Combat script.

Running this script automatically loads all necessary modules to play a game
of Turtle Combat, and then starts the game.
"""

from tc.tcgame import TurtleCombatGame

# Create game object
print("Opening Turtle Combat.")

# Get game options from user
###

# Create game object
game = TurtleCombatGame()

# Delete game object when done
print("Closing Turtle Combat.")
del game
