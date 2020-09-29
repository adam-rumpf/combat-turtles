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
    # These can then be used with the exec() or eval() function to instantiate
    # the necessary turtle objects.
    # All Combat Turtle AIs are required to use the class name "CombatTurtle",
    # so this only requires us to find the name of the module.

    # Build list of class names for each module that includes CombatTurtle
    print("Finding Combat Turtle AI modules...", end="")
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

    # Ask the user to choose the turtle AIs (assuming more than one is loaded)
    choice1 = 0 # index of Player 1 AI
    choice2 = 0 # index of PLayer 2 AI
    if len(turtle_classes) > 1:
        indices = {str(i) for i in range(len(turtle_classes))} # valid indices

        # Ask for Player 1 choice until getting a valid response
        choice = ""
        while choice not in indices:
            choice = input("Input an Index [0-" + str(len(turtle_classes)-1) +
                           "] to choose the AI for Player 1, and then press" +
                           " [Enter]: ")
        choice1 = int(choice)

        # Ask for Player 2 choice until getting a valid response
        choice = ""
        while choice not in indices:
            choice = input("Input an Index [0-" + str(len(turtle_classes)-1) +
                           "] to choose the AI for Player 2, and then press" +
                           " [Enter]: ")
        choice2 = int(choice)

    # Show choices
    print("\nPlayer 1: " + eval(turtle_classes[choice1] + ".class_name()"))
    print("Player 2: " + eval(turtle_classes[choice2] + ".class_name()"))

    # Ask the user to choose an arena
    ###
    arena = 0 # layout ID of arena

    # Create game object with chosen turtles and arena
    print("\nOpening Turtle Combat.")
    game = tc.tcgame.TurtleCombatGame(class1=turtle_classes[choice1],
                                      class2=turtle_classes[choice2],
                                      layout=arena)

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
