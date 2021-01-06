# Built-In Example AI

# Title: WallTurtle
# Author: Adam Rumpf
# Version: 1.0.0
# Date: 1/5/2021

import math
import game.tcturtle

class CombatTurtle(game.tcturtle.TurtleParent):
    """Wall-hugging combat turtle.

    A turtle that attempts to navigate around obstacles by "feeling" the walls
    around it.
    
    When it has direct line of sight to the opponent, it moves directly
    towards it. Otherwise it moves towards the opponent until hitting a wall,
    at which point it attempts to turn so that the way ahead is free.
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "WallTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Hugs walls to get around obstacles."

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

        return 2

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for Combat Turtle.
        """

        # Define the relative polar coordinates around the turtle to scan
        self.nose_rel = (8, 0.0) # just ahead of turtle's front
        self.hand_rel = (8, math.pi/2) # to left of turtle

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for Combat Turtle.
        """
        
        # Determine behavior based on whether there is line of sight
        if (self.line_of_sight() == True):
            # If there is line of sight, move directly towards opponent
            
            # Turn towards opponent
            self.turn_towards()
            
            # Move towards opponent (or away if too close)
            if self.distance() > 4*self.missile_radius:
                self.forward()
            else:
                self.backward()

            # Shoot if facing opponent
            if (self.can_shoot == True and
                abs(self.relative_heading_towards()) <= 10):
                self.shoot()

        else:
            # If no line of sight, attempt to navigate around obstacles
            
            # Calculate Cartesian coordinates of nose and hand
            nose = ((self.x + self.nose_rel[0]*
                     math.cos(math.radians(self.heading)+self.nose_rel[1])),
                    (self.y - self.nose_rel[0]*
                     math.sin(math.radians(self.heading)+self.nose_rel[1])))
            hand = ((self.x + self.hand_rel[0]*
                     math.cos(math.radians(self.heading)+self.hand_rel[1])),
                    (self.y - self.hand_rel[0]*
                     math.sin(math.radians(self.heading)+self.hand_rel[1])))
            
            # Determine behavior based on whether nose and hand are clear
            if self.free_space(nose) == True:
                # Move forward when clear ahead
                self.forward()
            else:
                if self.free_space(hand) == True:
                    # If free to left, turn left
                    self.left()
                    self.forward()
                else:
                    # If blocked ahead and to left, turn right
                    self.right()
                    self.forward()
