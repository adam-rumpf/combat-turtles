"""Main Turtle Combat script.

Running this script automatically loads all necessary modules to play a game
of Turtle Combat, and then starts the game.
"""

import tc

# Create game object
print("Opening Turtle Combat.")

# Get game options from user
###

# Create game object
game = tc.tcgame.TurtleCombatGame()

# Delete game object when done
print("Closing Turtle Combat.")
del game
