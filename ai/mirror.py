# Built-In Example AI

# Title: MirrorTurtle
# Author: Adam Rumpf
# Version: 1.0.0
# Date: 11/12/2020

import game.tcturtle

class CombatTurtle(game.tcturtle.TurtleParent):
    """Mirror combat turtle.

    Attempts to mirror the location of the opponent turtle (rotated around the
    center of the arena), turning to shoot if it has line of sight.
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "MirrorTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Mirrors opponent's position and shoots when close."

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

        return 1

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for Combat Turtle.
        """

        # Initialize goal coordinate to move towards
        self.goal = self.update_goal()
        
        # Set distance within which to shoot instead of mirror
        self.shoot_dist = 0.5*self.missile_range

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for Combat Turtle.
        """
        
        # Determine behavior based on whether there is line of sight and the
        # opponent is close enough to shoot at
        if (self.line_of_sight() == True and
            self.distance() <= self.shoot_dist):
            # If there is a clear shot, turn towards opponent and shoot
            
            # Turn towards opponent
            self.turn_towards()
            
            # Shoot if able
            if self.can_shoot == True:
                self.shoot()
        else:
            # If there is no clear shot, attempt to move to goal coordinate
            
            # Update target coordinate
            self.goal = self.update_goal()
            
            # Turn towards goal
            self.turn_towards(self.goal)
            
            # Calculate fraction of speed that will take us as close as
            # possible to the goal in one step of movement
            spd = max(1, self.distance(self.goal)/self.max_speed)
            
            # Move towards goal
            self.forward(spd)
    
    #=========================================================================
    
    def update_goal(self):
        """MirrorTurtle.update_goal() -> tuple
        Determines the target coordinate that this turtle should move towards.
        
        During each step this turtle calculates the point within the arena
        opposite the opponent's position (rotated around the central axis).
        """

        return (self.arena_right - self.other_x,
                self.arena_top - self.other_y)
