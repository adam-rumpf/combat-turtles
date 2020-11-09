# Turtle Combat

A Python module for programming turtles to play a war game.

See the author's notes for this game [here](https://adam-rumpf.github.io/programs/turtle_combat.html).

Turtle Combat is meant as a learning tool for intermediate-level Python students. It defines a combat game in which programmable [turtle robots](https://en.wikipedia.org/wiki/Turtle_(robot)) move around a battlefield firing missiles to destroy each other. A parent class, `TurtleParent`, defines a variety of basic attributes and methods for these turtle robots, and an `ai/` folder contains a variety of subclasses of this parent class which define different turtle AIs. The main driver script `turtlecombat.py` loads selected AI subclasses to compete against each other in combat.

The player is meant to write their own turtle AI by extending the `TurtleParent` class and overwriting a few key methods. The game is run using discrete step events (at a rate of approximately 30 steps/second), with each turtle defining its actions on a per-step basis. Custom AI submodules (in the form of a standalone `.py` file) can be added to the `ai/` directory to import the player's AI into the game. Several example and template subclasses are included in this directory to get the player started. See also the [documentation below](#instructions) for a detailed guide to writing custom AIs. Python students might enjoy competing against each other to see whom can come up with the best AI, while Python instructors might consider running a class tournament to encourage students to learn more about object-oriented programming.

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

# Instructions

This section is meant to provide an overview of how the Turtle Combat game works mechanically, and how a player can create and implement their own custom AI submodule.

## Running the Game

To begin a game of Turtle Combat, run the main driver `turtlecombat.py` and execute the function `turtle_combat()`. This will take you through a series of command line entries where the available turtle AIs and arenas will be displayed and selected.

If you already know ahead of time which AIs and arena you wish to load, you can streamline this process by including their indices as arguments of the `turtle_combat()` function. For example, `turtle_combat(0, 1, 2)` would attempt to begin the game with AI `0` playing against AI `1` in arena `2`. Note that the AI indices are based on the alphabetical order of the AI submodules in the `ai/` folder, and thus these indices may change as you add files to this folder.

## Including a Custom AI Submodule

AI submodules are located in the `tc/ai/` folder. Any `.py` file in this folder whose name does not begin with an underscore (`_`) is recognized by the game as an AI submodule, and will be loaded by the main driver when the `turtle_combat()` function is run.

See the included `_template.py` file for a template which includes the basic structure of a valid AI submodule, as well as documentation of the available attributes and methods. The following features are essential for any AI submodule:
* Import `tc.tkturtle`, along with any modules required by your custom AI.
* The submodule must define a `class` named `CombatTurtle` which extends `tc.tkturtle.TurtleParent`.
* The `class_name()`, `class_desc()`, and `class_shape()` static methods should all be overwritten to define the AI's name string, a brief description string, and an integer index for its shape (or a tuple of radii/angles to define a custom shape in polar coordinates).
* The `setup()` method should be overwritten with any special initialization code required by the AI (this method is called at the end of the object's `__init__()` method).
* The `step()` method should be overwritten with the AI's step event code (this method is called once per step event).

You are free to include any additional methods and attributes as part of your custom AI class, or even additional classes. For safety, it is recommended to restrict the AI to a single file, to import only modules from the Python Standard Library, and to avoid defining methods or attributes whose names begin with an underscore (`_`) since the `TurtleParent` class contains a large number of private members.

You __should not__ overwrite any other attributes or methods of the `TurtleParent` class. Doing so could break some of the internal workings of the game, or could give the AI an unfair advantage by allowing it to overwrite things such as the built-in movement limitations.

## Game Overview

...

(mechanics, steps, lack of "momentum", startup code, geometry of the arena [including -y and how headings work], blocks, arenas)

<img src="images/coordinate_system.png" title="Turtle Combat coordinate system." width="400"/>

...

## Inherited Features

This section describes the attributes and methods built into the `TurtleParent` class for use in custom AI subclasses. In defining a subclass you are free to add your own methods and attributes, as long as they do not conflict with any of the built-in members (except for those meant for overwriting as [described above](#including-a-custom-ai-submodule)).

### Built-In Attributes

The following is a list of attributes available for use in custom turtle AIs. All should be treated as read-only. Most are constant, although some are automatically updated to reflect the current state of the game.

#### Game Constants

The following is a list of game-defining constants.

* `self.max_speed` -- Maximum movement speed of a turtle (px/step), and the default speed of the [movement methods](#action-methods).
* `self.max_turn_speed` -- Maximum turning speed of a turtle (deg/step), and the default speed of the [turning methods](#action-methods).
* `self.shoot_delay` -- Length of cooldown between consecutive missile shots (steps).
* `self.missile_speed` -- Constant travel speed of missiles (px/step).
* `self.missile_range` -- Maximum range of missiles (px/step), after which they automatically explode.
* `self.missile_proximity` -- Proximity range of missiles (px). A missile explodes if it passes within this distance of the opponent turtle.
* `self.missile_radius` -- Explosive radius of missiles (px). When a missile explodes it deals damage to all turtles within this range (including the turtle that fired it).
* `self.missile_damage` -- Amount of damage caused by a missile (hp).
* `self.arena_left` -- Left boundary of the arena (px), representing the minimum allowed x-coordinate.
* `self.arena_right` -- Right boundary of the arena (px), representing the maximum allowed x-coordinate.
* `self.arena_bottom` -- Bottom boundary of the arena (px), representing the minimum allowed y-coordinate. Note that, due to the origin's position at the top left of the arena, this actually corresponds to the top of the screen.
* `self.arena_top` -- Top boundary of the arena (px), representing the maximum allowed y-coordinate. Note that, due to the origin's position at the top left of the arena, this actually corresponds to the bottom of the screen.

#### Own Attributes

The following is a list of attributes which describe the turtle's own state.

* `self.x` -- Horizontal coordinate (px).
* `self.y` -- Vertical coordinate (px).
* `self.position` -- Tuple of coordinates (px). Equivalent to `(self.x, self.y)`.
* `self.heading` -- Current heading (deg). Headings are always normalized to the interval `(-180,180]` with `0` indicating east, `90` indicating north, `180` indicating west, and `-90` indicating south.
* `self.speed` -- Current speed (px/step). Note that a turtle's speed is reset to `0` at the beginning of each step and can only become nonzero after the turtle's [movement methods](#action-methods) have been called.
* `self.turn_speed` -- Current turning speed (deg/step). Note that a turtle's turning speed is reset to `0` at the beginning of each step and can only become nonzero after the turtle's [turning methods](#action-methods) have been called.
* `self.health` -- Current health (out of `100`).
* `self.cooldown` -- Length of cooldown until this turtle can shoot again (steps).
* `self.can_shoot` -- Whether this turtle is able to shoot (`True` if so, `False` if not).

#### Opponent Attributes

The following is a list of attributes which describe the opponent turtle's state. Both turtles act simultaneously during the step event, and so these attributes are based on the opponent's attributes as of the end of the previous step.

* `self.other_x` -- Opponent's previous horizontal coordinate (px).
* `self.other_y` -- Opponent's previous vertical coordinate (px).
* `self.other_position` -- Tuple of opponent's previous coordinates (px). Equivalent to `(self.other_x, self.other_y)`.
* `self.other_heading` -- Opponent's previous heading (deg). Headings are always normalized to the interval `(-180,180]` with `0` indicating east, `90` indicating north, `180` indicating west, and `-90` indicating south.
* `self.other_speed` -- Opponent's previous speed (px/step).
* `self.other_turn_speed` -- Opponent's previous turning speed (deg/step).
* `self.other_health` -- Opponent's previous health (out of `100`).

### Built-In Methods

The following is a list of built-in methods available for use in custom turtle AIs, although you are encouraged to write your own as you extend the class.

#### Action Methods

The following is a list of void methods which cause the turtle to perform actions. The main purpose of the `step()` method that defines the turtle's AI is to determine, for each step, which actions to attempt to take.

Note that these methods do not, by themselves, actually cause the turtle to move or shoot: they all set the values of hidden internal variables that specify what the turtle will try to do during the step event. The actual movement is taken care of with hidden internal methods that apply game rules such as enforcing collisions and missile cooldown.

Also note that turtles begin each step with no movement instructions. If you want your turtle to continuously move, it needs to be given movement instructions *every step*.

* `self.forward([rate])` -- Attempts to move the turtle forward in its current direction. Turtles are blocked by the arena's boundaries and block objects. The optional `rate` argument can take any value between `-1` and `1`, and indicates the fraction of the turtle's maximum speed (`self.max_speed`) to travel at, with `1` indicating full speed forward, `0` indicating no movement, `-1` indicating full speed backward, and intermediate values indicating intermediate speeds.  
Aliases: `forward`, `fd`
* `self.backward([rate])` -- Analogous to `self.forward()`, but with positive `rate` indicating backward movement and negative `rate` indicating forward movement.  
Aliases: `backward`, `back`, `bk`
* `self.left([rate])` -- Turns the turtle left. The optional `rate` argument can take any value between `-1` and `1`, and indicates the fraction of the turtle's maximum turning speed (`self.max_turn_speed`) to turn at, with `1` indicating full speed counterclockwise, `0` indicating no turning, `-1` indicating full speed clockwise, and intermediate values indicating intermediate turning speeds.  
Aliases: `left`, `lt`
* `self.right([rate])` -- Analogous to `self.left()`, but with positive `rate` indicating clockwise turning and negative `rate` indicating counterclockwise movement.  
Aliases: `right`, `rt`
* `self.turn_towards([args])` -- Turns the turtle as far as possible to face a given target, either at maximum speed if it cannot be reached in one step, or at a fraction of maximum speed if it is possible to face the target directly within one step. The target depends on the inputs:
  * `self.turn_towards()` -- Turn to face the opponent turtle.
  * `self.turn_towards(int)` -- Turn to get heading to match a given heading (deg).
  * `self.turn_towards(tuple)` -- Turn to face a given coordinate tuple (px, px).
* `self.shoot()` -- Fires a missile in the turtle's current direction. Missiles move at a constant speed until either colliding with a wall or block, getting close enough to the opponent turtle (`self.missile_proximity`), or after traveling a certain distance (`self.missile_range`), and which point they explode, damaging any turtle (including the one that fired it) within its explosive radius (`self.missile_radius`). Does nothing if the turtle is still on cooldown from the last shot.

#### Query Methods

The following is a list of methods which return information about the current state of the game, including the turtle's own position, the other turtle's position, and information about the arena. These are similar to the [own attributes](#own-attributes) and [opponent attributes](#opponent-attributes) above, but implemented as methods rather than attributes since they require (potentially optional) arguments.

* `self.distance([args])` -- Calculates distances between coordinates (px). The distance calculated depends on the inputs:
  * `self.distance()` -- Distance from self to opponent.
  * `self.distance(tuple)` -- Distance from self to a given coordinate tuple (px, px).
  * `self.distance(tuple, tuple)` -- Distance between a pair of given coordinate tuples (px, px).
* `self.relative_position([target])` -- Calculates the relative position from this turtle to a target coordinate (px, px), meaning the change in this turtle's position required to reach the target coordinate.  
If given no argument, the opponent's position is used.
* `self.relative_heading([target])` -- Calculates the heading from this turtle to a target coordinate (deg), meaning the direction required to move from this turtle's position to the target coordinate. Headings are normalized to the interval `(-180,180]` with `0` indicating east, `90` indicating north, `180` indicating west, and `-90` indicating south. Similar to `self.relative_heading_towards()`, but does not take this turtle's current heading into consideration.  
If given no argument, the opponent's position is used.
* `self.relative_heading_towards([target])` -- Calculates the change in heading required to turn this turtle to face a target coordinate (deg), meaning the minimum angle that this turtle would need to turn in order to face the target. Positive headings indicate counterclockwise turning while negative headings indicate clockwise turning. Similar to `self.relative_heading()`, but gives a heading relative to this turtle's current heading.  
If given no argument, the opponent's position is used.
* `self.line_of_sight([target])` -- Determines whether or not there is a line of sight between this turtle and a target coordinate (`True` if so, `False` if not). A line of sight implies that, if this turtle were to immediately fire a missile while facing the specified coordinate, the missile would travel towards the target without obstruction from any block objects.  
If given no argument, the opponent's position is used.
