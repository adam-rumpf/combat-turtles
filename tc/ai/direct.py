"""Defines a direct CombatTurtle object."""

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

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for direct Combat Turtle.
        """

        # Define constant linear and angular speed factors
        self.speed = 1.0
        self.turn_speed = 1.0

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for direct Combat Turtle.
        """

        # Turn towards opponent
        self.turn_towards()

        # Move towards opponent (unless within blast radius)
        if self.distance() > self.missile_radius():
            self.forward(self.speed)

        ### Shoot if facing opponent
