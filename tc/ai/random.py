"""Defines a random CombatTurtle object."""

import numpy.random as nprand
import tc.tcplayer

class CombatTurtle(tc.tcplayer.CombatTurtleParent):
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

        # Initialize NumPy RNG
        self.rng = nprand.default_rng()

        # Initialize firing timer
        self.timer = 0 # steps since firing

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for Combat Turtle.

        Randomize direction and move forward at a random speed.
        """

        # Set random direction (uniformly on [-1,1])
        self.left(self.rng.uniform(-1, 1))

        # Move at a random speed (uniform on [0, 1])
        self.forward(self.rng.uniform(0, 1))

        # Make firing decision
        if self.can_fire():
            self.timer += 1 # increment timer

            # Use exponential distribution to decide whether to fire
            if self.rng.exponential(20) < self.timer:
                self.fire()
                self.timer = 0
