# Turtle Combat

A Python module for programming turtles to play a war game.

See the author's notes for this game [here](https://adam-rumpf.github.io/programs/turtle_combat.html).

Turtle Combat is meant as a learning tool for intermediate-level Python students. It defines a combat game in which programmable [turtle robots](https://en.wikipedia.org/wiki/Turtle_(robot)) move around a battlefield firing missiles to destroy each other. A parent class, `CombatTurtleParent`, defines a variety of basic attributes and methods for these turtle robots, and an `ai/` folder contains a variety of subclasses of this parent class which define different turtle AIs. The main driver script `turtlecombat.py` loads selected AI subclasses to compete against each other in combat.

The player is meant to write their own turtle AI by extending the `CombatTurtleParent` class and overwriting a few key methods. The game is run using discrete step events (at a rate of 1 step every 33 ms), with each turtle defining its actions on a per-step basis. Custom AI scripts (in the form of a standalone `.py` file) can be added to the `ai/` directory to import the player's AI into the game. Several example and template subclasses are included in this directory to get the player started. See also the [documentation below](#player-guide) for a detailed guide to writing custom AIs.

This module is available for free from my [releases page](https://github.com/adam-rumpf/turtle-combat/releases) or as donationware from my [itch.io page](https://adam-rumpf.itch.io/turtle-combat). I encourage you to download it, use it in your own projects, and modify the source code as much as you like.

## Dependencies

This module was developed for Python 3.8.3.

In an effort to maintain portability it uses only modules from the [Python Standard Library](https://docs.python.org/3/library/), including: `glob`, `inspect`, `math`, `os.path`, `random`, `tkinter`

This module also makes use of an `Angle` class, developed as a standalone module available at [github.com/adam-rumpf/python-angles](https://github.com/adam-rumpf/python-angles), and included in its entirety in the `util/` folder.

## Credits

Turtle Combat  
Copyright (c) 2020 Adam Rumpf  
[adam-rumpf.github.io](https://adam-rumpf.github.io/)

Source code released under MIT License  
[github.com/adam-rumpf/turtle-combat](https://github.com/adam-rumpf/turtle-combat)

# Player Guide

This section is meant to provide an overview of how the Turtle Combat game works mechanically, and how a player can create and implement their own custom AI script.

## Running the Game

To begin a game of Turtle Combat, run the main driver `turtlecombat.py` and execute the function `turtle_combat()`. This will take the user through a series of command line entries where the available turtle AIs and arenas will be displayed and selected.

If you already know ahead of time which AIs and arena you wish to load, you can streamline this process by including their indices as arguments of the `turtle_combat()` function. For example, `turtle_combat(0, 1, 2)` would attempt to begin the game with AI `0` playing against AI `1` in arena `2`. Note that the AI indices are based on the alphabetical order of the AI scripts in the `ai/` folder, and thus these indices may change depending on which scripts are included.

## Including a Custom AI Script

AI scripts are located in the `tc/ai/` folder. Any `.py` file in this folder whose name does not begin with an underscore (`_`) is recognized by the game as an AI script, and will be loaded by the main driver when the `turtle_combat()` function is run.

See the included `_template.py` file for a template which includes the basic structure of a valid AI script, as well as documentation of the available attributes and methods. The following features are essential for any AI script:
* `import tc.tcplayer`
* The script must define a `class` named `CombatTurtle` which extends `tc.tcplayer.CombatTurtleParent`.
* The `class_name()`, `class_desc()`, and `class_shape()` static methods should all be overwritten to define the AI's name string, a brief description string, and an integer index for its shape.
* The `setup()` method should be overwritten with any special initialization code required by the AI (this method is called at the end of the object's `__init__()` method).
* The `step()` method should be overwritten with the AI's step event code (this method is called once per step event).

You are free to include any additional methods and attributes as part of your custom AI class, or even additional classes. For safety, it is recommended to restrict the AI to a single file, to import only modules from the Python Standard Library, and to avoid defining methods or attributes that begin with an underscore (`_`) since the `CombatTurtleParent` class contains a large number of private members.

You _should not_ overwrite any other attributes or methods of the `CombatTurtleParent` class. Doing so could break some of the internal workings of the game, or could give the AI an unfair advantage by allowing it to overwrite things such as the built-in movement limitations.

## Game Overview

(mechanics, steps, startup code, geometry of the arena)

## Inherited Features

This section describes the attributes and methods built into the `CombatTurtleParent` class for use in custom AI subclasses.

### Built-In Attributes

The following is a list of attributes available for use in custom turtle AIs. All should be treated as read-only. Most are constant, although some are automatically updated to reflect the current state of the game.

#### Game Constants

#### Own Attributes

#### Opponent Attributes

### Built-In Methods
