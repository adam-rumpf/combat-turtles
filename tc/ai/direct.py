"""Defines a direct CombatTurtle object."""

import math
import tc.tkturtle

class CombatTurtle(tc.tkturtle.TkTurtle):
    """Direct combat turtle.

    Its main strategy is to try to move directly towards the opponent, firing
    missiles when it has clear line of sight. It does not pay much attention
    to obstacles.
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "DirectTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Moves directly towards opponent while ignoring obstacles."

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

        return 0

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for direct Combat Turtle.
        """

        pass

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for direct Combat Turtle.
        """

        # Turn towards opponent
        self.turn_towards()

        # Move towards opponent (or away if too close)
        if self.distance() > 4*self.missile_radius:
            self.fd()
        else:
            self.bk()

        # Shoot if facing opponent
        if (self.can_shoot == True and
            abs(self.relative_heading_towards()) <= 10):
            self.shoot()
