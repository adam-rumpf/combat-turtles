"""Defines a drunken CombatTurtle object."""

import tc.tcplayer

class CombatTurtle(tc.tcplayer.CombatTurtleParent):
    """Drunken combat turtle.

    This is a slightly less randomized version of the random turtle. Its
    movement is mostly randomized, but biased towards moving in the opponent's
    direction, and it fires only when pointing towards the opponent.
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "DrunkenTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Wanders semi-randomly towards the opponent."

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

        pass
