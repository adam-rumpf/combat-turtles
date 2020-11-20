# Built-In Example AI

# Title: DrunkenTurtle
# Author: Adam Rumpf
# Version: 1.1.0
# Date: 11/20/2020

import math
import random
import game.tcturtle

class CombatTurtle(game.tcturtle.TurtleParent):
    """Drunken combat turtle.
    
    This is a variant of DirectTurtle whose behavior is slightly
    unpredictable. It generally moves towards its opponent, but its target
    heading and approach distance vary sinusoidally over time, and its
    decisions about whether to shoot are slightly randomized.
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

        return 5

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for Combat Turtle.
        """

        # Define parameters for variations
        self.wander_amp = 15 # amplitude of sinusoidal wandering noise (deg)
        self.wander_wl = 43 # wavelength of sinusoidal wandering noise (steps)
        self.approach_amp = 1.5*self.missile_radius # amplitude of sinusoidal
                                                    # approach radius
        self.approach_wl = 81 # wavelength of sinusoidal approach radius
        self.shoot_prob = 0.1 # probability to shoot when the option exists

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for Combat Turtle.
        """

        # Get direction towards opponent and add sinusoidal noise
        dir = self.heading_towards()
        dir += self.wander_amp*math.sin((2*math.pi*self.time)/self.wander_wl)
        
        # Turn towards the specified heading
        self.turn_towards(dir)
        
        # Determine minimum approach distance by adding noise
        dist = 4*self.missile_radius
        dist += self.approach_amp*math.sin((2*math.pi*self.time)
                                           /self.approach_wl)

        # Move towards opponent (or away if too close)
        if self.distance() > dist:
            self.forward()
        else:
            self.backward()

        # Shoot if facing opponent and there is line of sight
        if (self.can_shoot and abs(self.relative_heading_towards()) <= 10 and
            self.line_of_sight()):
            # Roll for random chance to shoot
            if random.random() < self.shoot_prob:
                self.shoot()
