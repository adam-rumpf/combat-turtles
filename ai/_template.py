"""This file is meant to be used as a template for writing your own combat
turtle AI submodules. It includes the minimal set of statements required to
define a valid AI submodule. See the other files included in this folder for
full examples of simple AI submodules, as well as the Readme for a full
explanation of how the game works. Online documentation can be found in this
project's GitHub repository at:
    https://github.com/adam-rumpf/combat-turtles

To create a custom combat turtle AI, create a new .py file in the ai/ folder
with a name that does not begin with an underscore (_) (file names beginning
with an underscore are ignored by the main game driver). The minimal program
contents for defining a valid AI are included in this template file, but to
summarize, the submodule must define a class which extends the included
combat turtle parent class and overwrites several of its key methods.

Specifically, all of the following must be included in a valid AI submodule:

 1. The submodule must import the combat turtle parent class by using the
    following import statement:
        import game.tcturtle

 2. The submodule must define a class called "CombatTurtle" which extends the
    parent class by using the following class definition:
        class CombatTurtle(game.tcturtle.TurtleParent):

 3. The submodule must overwrite three of the parent class' static methods,
    including all of the following:
        class_name() -- returns a name string for the AI
        class_desc() -- returns a brief description string for the AI
        class_shape() -- returns either an integer index or a radial
                        coordinate tuple for defining the shape of the turtle
                        to be drawn in-game (see below for details)

 4. The submodule should overwrite the parent class' setup() method. This is
    optional, but should include any special initialization code required by
    your AI, and is run before the first step event of the game.

 5. The submodule should overwrite the parent class' step() method. This method
    is called during each of the game's step events (which occur at a rate of
    approximately 30 steps/second) and is likely where the bulk of your AI's
    code will go, as it defines the turtle's actions during the course of the
    game.

The parent class defines a large number of public attributes and methods for
use in subclass design. Brief descriptions of the available attributes and
methods are included below. See the Readme for more detailed descriptions, or
see the docstrings in the parent class' file in game/tcturtle.py.

DO NOT ATTEMPT TO ACCESS OR OVERWRITE ANY PARENT CLASS MEMBERS NOT ON THIS
LIST! Doing so could break the game, or could give your turtle an unfair
advantage by circumventing the rules.

The following read-only attributes can be used to access game constants:
    max_speed -- maximum linear speed of a turtle (px/step)
    max_turn_speed -- maximum turning speed of a turtle (deg/step)
    shoot_delay -- cooldown period (steps) between missile shots
    missile_speed -- constant linear speed of a missile (px/step)
    missile_range -- maximum range of a missile (px)
    missile_proximity -- trigger proximity of a missile (px)
    missile_radius -- explosive radius of a missile (px)
    missile_damage -- damage dealt by a missile explosion (hp)
    arena_left -- minimum x-coordinate of arena
    arena_right -- maximum x-coordinate of arena
    arena_bottom -- minimum y-coordinate of arena
    arena_top -- maximum y-coordinate of arena

The following read-only attributes can be used to access the turtle's own
status:
    x -- current x-coordinate (px)
    y -- current y-coordinate (px)
    position -- current coordinate tuple (px, px)
    heading -- current heading (deg) normalized to (-180,180]
    speed -- current linear speed (px/step)
    turn_speed -- current turning speed (deg/step)
    health -- current remaining health (hp)
    cooldown -- current cooldown before another missile can be fired (steps)
    can_shoot -- whether or not the turtle is currently able to shoot
    time -- number of steps that have passed since the game began

The following read-only attributes can be used to access the opponent turtle's
status (as of the end of the previous step, except for the cooldown count,
which is current):
    other_x -- opponent's previous x-coordinate (px)
    other_y -- opponent's previous y-coordinate (px)
    other_position -- opponent's previous coordinate tuple (px, px)
    other_heading -- opponent's previous heading (deg) normalized to
        (-180,180]
    other_speed -- opponent's previous linear speed (px/step)
    other_turn_speed -- opponent's previous turning speed (deg/step)
    other_health -- opponent's previous health (hp)
    other_cooldown -- opponent's current cooldown length (steps)
    other_can_shoot -- whether the opponent can currently shoot

The following methods should be used to instruct the turtle to take actions:
    forward([rate]) -- moves forward in current direction at a given fraction
        of its maximum speed (aliases: forward, fd)
    backward([rate]) -- moves backward in current direction at a given
        fraction of its maximum speed (aliases: backward, back, bk)
    left([rate]) -- turns counterclockwise at a given fraction of its maximum
        turning speed (aliases: left, lt)
    right([rate]) -- turns clockwise at a given fraction of its maximum
        turning speed (aliases: right, rt)
    turn_towards([args]) -- turns as far as possible towards a given target
        either at maximum turning speed or exactly enough to face the target
        exactly (aliases: turn_towards, turn_towards, turnto)
    shoot() -- fire missile in current direction and set cooldown to prevent
        shooting again for a set number of steps (aliases: shoot, fire)

The following methods should be used to gather information about the current
state of the game:
    distance([args]) -- returns distance between a given pair of coordinates
        (px) (aliases: distance, dist)
    relative_position([target]) -- returns the relative position of a target
          relative to this turtle (px, px) (aliases: relative_position,
          relpos)
    heading_towards([target]) -- returns the heading from this turtle to a
          target (deg) (aliases: heading_towards, heading_toward, towards,
          toward)
    relative_heading_towards([target]) -- returns the smallest heading change
          required to turn this turtle towards a target (deg) (aliases:
          relative_heading_twards, relative_heading_toward)
    free_space(coord) -- returns whether a given coordinate is free of
          obstacles (aliases: free_space, free)
    line_of_sight([target]) -- returns whether there is a direct line of sight
          between this turtle and a target (aliases: line_of_sight, los)
"""

# Title: ### AI name ###
# Author: ### Author name ###
# Version: ### major.minor[.build[.revision]] ###
# Date: ### MM/DD/YYYY ###

import game.tcturtle

class CombatTurtle(game.tcturtle.TurtleParent):
    """Template Combat Turtle class.

    You may replace this docstring with any documentation you wish to include
    with this Combat Turtle AI, such as the general strategy it uses.
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.

        The returned name will be used in the AI selection menu by the main
        game driver, and in the game window to label each player.
        """

        ### Replace the returned string with the turtle's name.

        return "TemplateTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.

        This should be a one-line description. The returned string will be
        used in the AI selection menu by the main game driver.
        """

        ### Replace the returned string with a one-line description.

        return "This is a template class that does nothing on its own."

    #-------------------------------------------------------------------------

    def class_shape():
        """CombatTurtle.class_shape() -> (int or tuple)
        Static method to define the Combat Turtle's shape image.

        The return value can be either an integer or a tuple of tuples.

        Returning an integer index selects one of the following preset shapes:
            0 -- arrowhead (also default in case of unrecognized index)
            1 -- turtle
            2 -- plow
            3 -- triangle
            4 -- kite
            5 -- pentagon
            6 -- hexagon
            7 -- star

        A custom shape can be defined by returning a tuple of the form
        (radius, angle), where radius is a tuple of radii and angle is a tuple
        of angles (in radians) describing the polar coordinates of a polygon's
        vertices. The shape coordinates should be given for a turtle facing
        east.
        """

        ### If desired, replace the returned value with a different shape
        ### index (see guide above) or a 2-tuple of n-tuples describing the
        ### radii and angles (respectively) of the turtle's polar shape
        ### coordinates (relative to a turtle facing east).

        ### The following is an example of an acceptable set of custom
        ### coordinates:
        ### return ((16, 14, 12, 14), (0, math.pi/2, math.pi, 3*math.pi/2))

        return 0

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for Combat Turtle.
        """

        ### Place any desired initialization code here.

        pass

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for Combat Turtle.
        """

        ### Place any desired step event code here.

        pass
