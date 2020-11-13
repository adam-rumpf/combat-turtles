# Built-In Example AI

# Title: TurretTurtle
# Author: Adam Rumpf
# Version: 1.0.1
# Date: 11/13/2020

import game.tcturtle

class CombatTurtle(game.tcturtle.TurtleParent):
    """Turret combat turtle.

    Stays completely while turning to face the opponent turtle, shooting when
    within range.
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "TurretTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Stays still and shoots opponent when close enough."

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

        return 3

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

        # Turn towards opponent
        self.turn_towards()

        # Shoot if facing opponent, there is line of sight, and close enough
        if (self.can_shoot and abs(self.relative_heading_towards()) <= 5 and
            self.line_of_sight() and self.distance() <= self.missile_range):
            self.shoot()
