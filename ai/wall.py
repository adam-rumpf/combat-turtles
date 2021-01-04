# Built-In Example AI

# Title: WallTurtle
# Author: Adam Rumpf
# Version: 1.0.0
# Date: 11/26/2020

import game.tcturtle

class CombatTurtle(game.tcturtle.TurtleParent):
    """Wall-hugging combat turtle.

    A turtle that attempts to navigate around obstacles by hugging walls using
    a left-hand rule.
    
    When it has direct line of sight to the opponent, it moves directly
    towards it. Otherwise it moves towards the opponent until hitting a wall,
    at which point it wraps around the wall by keeping its left side against
    it.
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "WallTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Hugs walls to get around obstacles."

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

        return 2

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for Combat Turtle.
        """

        pass

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for Combat Turtle.
        """
        
        # Outline:
        # Turn and move towards the opponent as long as there's line of sight.
        # Otherwise, attempt to move towards opponent while scanning ahead of self.
        # If there's an obstacle, begin wall hugging behavior, which is based on scanning a point to left of self.
        # As long as that point is free, turn right while moving forward until it becomes blocked for the first time.
        # As long as that point is blocked, move forward.
        # After sticking to a wall, turn left whenever the point to the turtle's left is unblocked.

        pass
