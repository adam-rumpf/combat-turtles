"""Defines a drunken CombatTurtle object."""

### Add full instructions, including the game mechanics and what is and is not allowed to be used.

import tc.tcplayer

class CombatTurtle(tc.tcplayer.CombatTurtleParent):
    """Template Combat Turtle class."""

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "TemplateTurtle"

    #-------------------------------------------------------------------------

    def class_desc():
        """CombatTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "This is a template class that does nothing on its own."
    
    #-------------------------------------------------------------------------

    def class_shape():
        """CombatTurtle.class_shape() -> (int or tuple)
        Static method to define the Combat Turtle's shape image.

        The return value can be either an integer or a tuple of tuples.

        Returning an integer index selects one of the following preset shapes:
            0 -- arrowhead (also default in case of unrecognized index)
            1 -- pentagon
            2 -- plough

        A custom shape can be defined by returning a tuple of the form
        (radius, angle), where radius is a tuple of radii and angle is a tuple
        of angles (in radians) describing the polar coordinates of a polygon's
        vertices.
        """

        return 0

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
