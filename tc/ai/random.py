"""Defines a random CombatTurtle object."""

import random
import tc.tkturtle

class CombatTurtle(tc.tkturtle.TkTurtle):
    """Random combat turtle.

    This turtle's behavior in each step is completely randomized, and has
    nothing to do with it or its opponent's position.
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "RandomTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Completely randomized behavior."

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for Combat Turtle.

        Sets up a timer variable to measure how long the turtle has gone
        between firing, so that it can fire according to an exponential
        distribution.
        """

        pass

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for Combat Turtle.

        Randomize direction and move forward at a random speed.
        """

        pass
