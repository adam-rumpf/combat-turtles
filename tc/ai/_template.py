# Title: ### AI name ###
# Author: ### Author name ###
# Version: ### major.minor[.build[.revision]] ###
# Date: ### MM/DD/YYYY ###

### Add full instructions, including the game mechanics and what is and is not allowed to be used.
### In particular explain the geometry of the arena, how step events work, and public attributes/methods.
### Explain generally what should be included in the methods meant to be overwritten.

import tc.tcplayer

class CombatTurtle(tc.tcplayer.CombatTurtleParent):
    """Template Combat Turtle class.
    
    You may replace this docstring with any documentation you wish to include
    with this Combat Turtle AI, such as the general strategy it uses.
    """

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        
        The returned name will be used in the AI selection menu by the main
        game driver, and in the game window to label each player.
        """

        ### Replace the returned string with the turtle's name.
        return "TemplateTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        
        This should be a one-line description. The returned string will be
        used in the AI selection menu by the main game driver.
        """

        ### Replace the returned string with a one-line description.
        return "This is a template class that does nothing on its own."
    
    #-------------------------------------------------------------------------

    def class_shape():
        """CombatTurtle.class_shape() -> (int or tuple)
        Static method to define the Combat Turtle's shape image.

        The return value can be either an integer or a tuple of tuples.

        Returning an integer index selects one of the following preset shapes:
            0 -- arrowhead (also default in case of unrecognized index)
            1 -- pentagon
            2 -- plow

        A custom shape can be defined by returning a tuple of the form
        (radius, angle), where radius is a tuple of radii and angle is a tuple
        of angles (in radians) describing the polar coordinates of a polygon's
        vertices. The shape coordinates should be given for a turtle facing
        east.
        """

        ### If desired, replace the returned value with a different shape
        ### index (see guide above) or a 2-tuple of n-tuples describing the
        ### radii and angles (respectively) of the turtle's polar shape
        ### coordinates (relative to a turtle facing east).
        return 0

    #=========================================================================

    def setup(self):
        """CombatTurtle.setup() -> None
        Initialization code for Combat Turtle.
        """

        ### Place any desired initialization code here.
        pass

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.setup() -> None
        Step event code for Combat Turtle.
        """

        ### Place any desired step event code here.
        pass
