"""Main Combat Turtles script.

Running this script automatically loads all necessary modules to play a game
of Turtle Combat and then starts the game.
"""

import argparse
import inspect
import game
import ai

#=============================================================================

def combat_turtles(tid1=-1, tid2=-1, aid=-1, cutoff=-1):
    """combat_turtles() -> None
    Combat Turtles game driver.

    By default this function will present the user with options for the game
    setup, including which turtle AI modules to use and which arena layout to
    use. Optional keyword arguments can be used to automatically fill these
    fields. Note, however, that these indices depend on the order in which the
    submodules are loaded from the ai/ directory, which could change as
    modules are added or removed.

    Accepts the following optional keyword arguments:
        tid1 (int) [-1] -- index of player 1 turtle class (in the list of all
            available combat turtle AI submodules)
        tid2 (int) [-1] -- index of player 2 turtle class (in the list of all
            available combat turtle AI submodules)
        aid (int) [-1] -- index of arena layout (in the list of all available
            arena layouts)
        cutoff (int) [-1] -- iteration cutoff for game (negative for no limit)
    """

    # In order to allow the user to place additional AI modules inside the ai/
    # directory, we generate a list of strings which include the full
    # addresses of the AI objects (for example, ai.direct.CombatTurtle). These
    # can then be used with the exec() or eval() function to instantiate the
    # necessary turtle objects.
    # All Combat Turtle AIs are required to use the class name "CombatTurtle",
    # so this only requires us to find the name of the module.

    # Build list of class names for each module that includes CombatTurtle
    print("Finding Combat Turtle AI modules...", end="")
    turtle_classes = []
    for f in ai.__all__:
        # Use static method to test whether the module includes the class
        try:
            eval("ai." + f + ".CombatTurtle.class_name()")
            turtle_classes.append("ai." + f + ".CombatTurtle")
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
        choice = str(tid1)
        while choice not in indices:
            choice = input("Input an Index [0-" + str(len(turtle_classes)-1) +
                           "] to choose the AI for Player 1, and then press" +
                           " [Enter]: ")
        choice1 = int(choice)

        # Ask for Player 2 choice until getting a valid response
        choice = str(tid2)
        while choice not in indices:
            choice = input("Input an Index [0-" + str(len(turtle_classes)-1) +
                           "] to choose the AI for Player 2, and then press" +
                           " [Enter]: ")
        choice2 = int(choice)

    # Show players
    print("\nPlayer 1: " + eval(turtle_classes[choice1] + ".class_name()"))
    print("Player 2: " + eval(turtle_classes[choice2] + ".class_name()"))

    # Display arena choices
    print()
    arena_names = game.obj.arena.Arena.get_names() # list of all arena layouts
    _arena_table(arena_names)

    # Ask the user to choose an arena
    arena = 0 # index of arena layout
    if len(arena_names) > 1:
        indices = {str(i) for i in range(len(arena_names))} # valid indices

        # Ask for layout choice until getting a valid response
        choice = str(aid)
        while choice not in indices:
            choice = input("Input an Index [0-" + str(len(arena_names)-1) +
                           "] to choose the arena layout, and then press" +
                           " [Enter]: ")
        arena = int(choice)

    # Show arena
    print("\nArena: " + arena_names[arena])

    # Create game object with chosen turtles and arena
    print("\nOpening Combat Turtles.")
    print("Game in progress...")
    gm = game.tcgame.TurtleCombatGame(class1=turtle_classes[choice1],
                                      class2=turtle_classes[choice2],
                                      layout=arena, cutoff=cutoff)

    # Delete game object when done
    print("Closing Combat Turtles.")
    del gm

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

#-----------------------------------------------------------------------------

def _arena_table(arenas):
    """_arena_table(arenas) -> None
    Prints a table of listed arena layouts.

    Requires the following positional arguments:
        arenas (list (str)) -- list of arena layout names
    """

    # Print header
    print("Index\tName")
    print("-"*60)

    # Print names
    for i in range(len(arenas)):
        print(str(i) + "\t" + arenas[i])

#=============================================================================

# Define docstrings for command line usage
_vers = """Combat Turtles v1.1.0
Copyright (c) 2021 Adam Rumpf <adam-rumpf.github.io>
Released under MIT License <github.com/adam-rumpf/combat-turtles>
"""
_desc = """Initializes a game of Combat Turtles. Command line arguments can be
supplied to specify player AIs and the arena (see below for details). Excluding
any of these arguments will prompt the user to specify them on startup.

Note that the player AIs are indexed alphabetically, which may cause indices to
change as new modules are added to the ai/ directory.
"""
_epil = """See full documentation online at
<adam-rumpf.github.io/combat-turtles>
"""

# Initialize game (options can be set from command line)
if __name__ == "__main__":

    # Initialize argument parser
    parser = argparse.ArgumentParser(description=_desc, epilog=_epil)

    # Execute function (add optional arguments to streamline process)
    # tid1 -- player 1 ID
    # tid2 -- player 2 ID
    # aid -- arena ID
    # cutoff -- game time limit (steps)
    combat_turtles()
