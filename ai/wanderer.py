# Built-In Example AI

# Title: WandererTurtle
# Author: Adam Rumpf
# Version: 1.0.1
# Date: 11/13/2020

import random
import game.tcturtle

class CombatTurtle(game.tcturtle.TurtleParent):
    """Wanderer combat turtle.

    Wanders around randomly until it gets close enough to the opponent, after
    which it directly pursues them.
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "WandererTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Wanders randomly and pursues when close enough."

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

        return 7

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for Combat Turtle.
        """
        
        # Define a random heading and a re-randomization waiting time
        (self.head, self.wait) = self.rerandomize()

        # Define pursuit cutoff distance
        self.pursuit_range = 0.75*self.missile_range

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for Combat Turtle.
        """
        
        # Decrement re-randomization timer
        self.wait -= 1
        
        # If the timer runs out, re-randomize heading and timer
        if self.wait <= 0:
            (self.head, self.wait) = self.rerandomize()
        
        # Determine behavior based on distance from opponent
        if (self.distance() <= self.pursuit_range and
            self.line_of_sight()):
            # Within the pursuit range, move directly towards opponent
            
            # Turn towards opponent
            self.turn_towards()

            # Move towards opponent (or away if too close)
            if self.distance() > 4*self.missile_radius:
                self.forward()
            else:
                self.backward()

            # Shoot if facing opponent and there is line of sight
            if (self.can_shoot and abs(self.relative_heading_towards()) <= 10
                and self.line_of_sight()):
                self.shoot()
        
        else:
            # Outside of pursuit range, randomly wander
            
            # Turn towards randomly-chosen heading and move forward
            self.turn_towards(self.head)
            self.forward()
    
    #=========================================================================
    
    def rerandomize(self):
        """WandererTurtle.rerandomize() -> tuple
        Resets the randomly-chosen heading and timer cutoff.
        
        The Wanderer turtle AI wanders randomly by periodically choosing a
        random direction to move in. This method chooses a new random heading
        and randomizes a timer which determines when to re-randomize the
        heading.
        
        Returns a tuple which includes the new heading (int) and the new
        number of steps to wait (int).
        """
        
        rh = random.randrange(-179, 181) # random heading
        rt = random.randrange(5, 30) # random timer
        
        return (rh, rt)
        
