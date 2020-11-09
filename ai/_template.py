# Title: ### AI name ###
# Author: ### Author name ###
# Version: ### major.minor[.build[.revision]] ###
# Date: ### MM/DD/YYYY ###

### Add full instructions, including the game mechanics and what is and is not allowed to be used.
### In particular explain the geometry of the arena, how step events work, and public attributes/methods. In particular mention the negative y-direction, which means that angles work a bit strangely.
### Explain generally what should be included in the methods meant to be overwritten.
### Explain what exactly happens within each step. The speed, turning speed, and shooting status are reset at the beginning of each step (so you need to explicitly tell the turtle to move every step to maintain constant speed). Then the user-defined step() method is called, after which the turtle is turned, then it moves, then it shoots (if instructed to).

import math
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
