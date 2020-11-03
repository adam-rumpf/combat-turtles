"""Defines a test CombatTurtle object that simply moves in circles."""

import tc.tkturtle

class CombatTurtle(tc.tkturtle.TkTurtle):
    """Test circular combat turtle.

    This turtle should simply travel in circles and periodically shoot.
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "CircleTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Moves in circles and periodically shoots."
    
    #-------------------------------------------------------------------------

    def class_shape():
        """CombatTurtle.class_shape() -> (int or tuple)
        Static method to define the Combat Turtle's shape image.

        The return value can be either an integer or a tuple of tuples.

        Returning an integer index selects one of the following preset shapes:
            0 -- arrowhead (also default in case of unrecognized index)
            1 -- pentagon
            2 -- plough

        A custom shape can be defined by returning a tuple of the form
        (radius, angle), where radius is a tuple of radii and angle is a tuple
        of angles (in radians) describing the polar coordinates of a polygon's
        vertices.
        """

        return 1

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for Combat Turtle.
        """

        # Define constant linear and angular speed factors
        self.speed = 1.0
        self.turn_speed = 0.5

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for Combat Turtle.

        This turtle's behavior is completely constant and consists of simply
        moving forward while turning, shooting when able.
        """

        self.forward(self.speed)
        self.left(self.turn_speed)
        if self.can_shoot():
            self.shoot()
