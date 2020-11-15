# Built-In AI

# Title: KeyboardTurtle
# Author: Adam Rumpf
# Version: 1.0.1
# Date: 11/14/2020

# Note: This included AI should not be looked to as an example for your own AI
# module design. In order to implement keyboard control it is necessary for
# this class to override some of the hidden TurtleParent class methods, which
# you SHOULD NOT do in your own custom AI modules.

import math
import game.tcturtle
from game.obj.missile import Missile

class CombatTurtle(game.tcturtle.TurtleParent):
    """Keyboard combat turtle.

    This is a unique combat turtle that is driven by keyboard input rather
    than running itself.
    
    The keyboard controls are as follows:
        [Up]/[W] -- move forward at full speed
        [Down]/[S] -- move backward at full speed
        [Left]/[A] -- turn counterclockwise at full speed
        [Right]/[D] -- turn clockwise at full speed
        [Space] -- shoot a missile
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "KeyboardTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Controlled by keyboard input (WASD/Arrows + Space)."

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

        return 0

    #=========================================================================
    
    def _keyboard_move(self, dir):
        """KeyboardTurtle._keyboard_move(dir) -> None
        Keyboard Turtle AI override for movement method.
        
        Requires the following positional arguments:
            dir (int) -- 1 for forward, -1 for backward
        """
        
        # Set new coordinates
        self._x += int(dir*self.max_speed*
                       math.cos(math.radians(self.heading)))
        self._y -= int(dir*self.max_speed*
                       math.sin(math.radians(self.heading)))

        # Check whether the destination intersects any blocks
        blocks = self._game.intersections((self.x, self.y))
        if len(blocks) > 0:
            # If so, check all intersecting blocks and move to outside
            for b in blocks:
                # Determine overlap on each side
                overlap = [1000000 for i in range(4)] # ordered overlaps
                if self.x >= b.left:
                    overlap[0] = self.x - b.left
                if self.x <= b.right:
                    overlap[1] = b.right - self.x
                if self.y >= b.bottom:
                    overlap[2] = self.y - b.bottom
                if self.y <= b.top:
                    overlap[3] = b.top - self.y

                # Find minimum nonzero overlap
                mo = overlap.index(min(overlap))

                # Reset coordinates based on minimum overlap
                if mo == 0:
                    self._x -= overlap[0] - 1
                elif mo == 1:
                    self._x += overlap[1] + 1
                elif mo == 2:
                    self._y -= overlap[2] - 1
                else:
                    self._y += overlap[3] + 1
    
    #-------------------------------------------------------------------------
    
    def _keyboard_turn(self, dir):
        """KeyboardTurtle._keyboard_turn(dir) -> None
        Keyboard Turtle AI override for turning method.
        
        Requires the following positional arguments:
            dir (int) -- 1 for CCW, -1 for CW
        """
        
        # Change heading
        self._heading += int(dir*self.max_turn_speed)
    
    #-------------------------------------------------------------------------
    
    def _keyboard_shoot(self):
        """KeyboardTurtle._keyboard_shoot() -> None
        Keyboard Turtle AI override for shooting method.
        """
        
        # If on cooldown, do nothing
        if self.cooldown > 0:
            return None

        # Otherwise create a missile object and add to the list
        self._cooldown = self.shoot_delay # reset cooldown duration
        self._missiles.append(Missile(self._game, self, self._other,
                                      self.position, self.heading))
