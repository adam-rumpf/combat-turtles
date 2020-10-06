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
