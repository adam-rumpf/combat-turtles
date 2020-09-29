"""Main Turtle Combat script.

Running this script automatically loads all necessary modules to play a game
of Turtle Combat, and then starts the game.
"""

import inspect

import tc

#=============================================================================

def turtle_combat():
    """turtle_combat() -> None
    Turtle Combat game driver."""

    # In order to allow the user to place additional AI modules inside the ai/
    # directory, we generate a list of strings which include the full
    # addresses of the AI objects (for example, tc.ai.keyboard.CombatTurtle).
    # These can then be used with the exec() function to instantiate the
    # necessary turtle objects.
    # All Combat Turtle AIs are required to use the class name "CombatTurtle",
    # so this only requires us to find the name of the module.

    # Build list of class names for each module that includes CombatTurtle
    print("Loading Combat Turtle AI modules...", end="")
    turtle_classes = []
    for f in tc.ai.__all__:
        # Use static method to test whether the module includes the class
        try:
            eval("tc.ai." + f + ".CombatTurtle.class_name()")
            turtle_classes.append("tc.ai." + f + ".CombatTurtle")
        # If not, skip
        except AttributeError:
            pass

    # Quit if no valid modules were found
    if len(turtle_classes) == 0:
        print("\nNo valid modules were found in the ai/ directory.")
        print("Please review the documentation to see the required format.")
        print("https://github.com/adam-rumpf/turtle-combat")
        return None

    # Display results
    print(" Done!")
    print(str(len(turtle_classes)) + " module(s) found.")

    # Display AI choices
    print()
    _ai_table(turtle_classes)
    print()

    # Ask the user to choose the turtle AIs
    if len(turtle_classes) == 1:
        # If only one choice, immediately initialize both
        print("Using only AI to initialize both players.")
        ###
    else:
        # Otherwise ask the user to enter the IDs of the two players
        indices = {str(i) for i in range(len(turtle_classes))} # valid indices
        choice = -1

        # Ask for Player 1 choice until getting a valid response
        while choice not in indices:
            choice = input("Input an Index [0-" + str(len(turtle_classes)-1) +
                           "] to choose the AI for Player 1, and then press" +
                           " [Enter]: ")

        # Initialize Player 1
        ###
        ###
        ###

    # Create game object
    print("Opening Turtle Combat.")
    game = tc.tcgame.TurtleCombatGame()

    # Delete game object when done
    print("Closing Turtle Combat.")
    del game

#-----------------------------------------------------------------------------

def _ai_table(classes):
    """_ai_table(classes) -> None
    Prints a table of listed Combat Turtle classes.

    Requires the following positional arguments:
        classes (list (str)) -- list of full class name strings
    """

    # Print header
    print("Index\tName\t\tDescription")
    print("-"*60)

    # Print names and descriptions
    for i in range(len(classes)):
        name = eval(classes[i] + ".class_name()")
        desc = eval(classes[i] + ".class_desc()")
        print(str(i) + "\t" + name + "\t" + desc)

#=============================================================================

# Execute function
turtle_combat()
