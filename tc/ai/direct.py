"""Defines a direct CombatTurtle object."""

import tc.tcplayer

class CombatTurtle(tc.tcplayer.CombatTurtleParent):
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

        pass
