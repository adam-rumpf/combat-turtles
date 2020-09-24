"""Defines the modules used throughout the Turtle Combat game."""

import turtle

#=============================================================================

class CombatTurtle(turtle.Turtle):
    """Parent class for combat turtle AI players.

    Consists mostly of placeholders for methods to be overloaded by the
    subclasses that define the different players, as well as a variety of
    private utility methods.
    """

    #-------------------------------------------------------------------------

    def __init__(self, name, coords, other):
        """CombatTurtle(name, coords, other) -> CombatTurtle
        Combat Turtle parent constructor.

        Requires the following positional arguments:
            name (str) -- name of turtle
            coords (tuple (float, float)) -- initial coordinates
            other (CombatTurtle) -- opponent combat turtle object
        """

        # Assign given attributes
        self.name = name
        (self.x, self.y) = coords
        self.other = other

        # Assign automatic attributes
        self.health = 100 # health points (turtle dies when health is zero)
        self.maxspeed = 10 # maximum movement speed (px/sec)
        self.maxturn = 90 # maximum turning speed (deg/sec)

        # Call setup function (contains setup code for specific submodule)
        self.setup()

    #-------------------------------------------------------------------------

    def __str__(self):
        """CombatTurtle.__str__() -> str
        String conversion returns Combat Turtle's name.
        """

        return self.name

    #-------------------------------------------------------------------------

    def setup(self):
        """CombatTurtle.setup() -> None
        Placeholder for Combat Turtle setup procedures.

        This method is meant to be overwritten in the submodules of
        CombatTurtle. It is called at the end of the constructor. Its purpose
        is to prevent the user from having to overload the constructor in
        their own submodule, in which case they would need to replicate its
        argument list and attribute definitions.
        """

        pass

    #-------------------------------------------------------------------------

    def fire(self):
        """CombatTurtle.fire() -> None
        Fires a missile in the turtle's current direction.

        Creates a Missile object which begins to automatically move in the
        turtle's current direction.
        """

        ###
        # Include a way to account for cooldown.

        ###
        pass

    ###
    # Need more methods for movement, turning, and how to handle commands
    # arriving in continuous time. An option could be to have the controlling
    # functions adjust internal state variables, and then have a step event
    # every few milliseconds to take action based on that.

#=============================================================================

class Missile(turtle.Turtle):
    """Missile class.

    Missile are fired by Combat Turtles. They travel at a fixed speed until
    either colliding with a solid object or player, or until a fixed amount of
    time has passed, and then explode with a fixed radius, dealing damage to
    all nearby players.
    """

    #-------------------------------------------------------------------------

    def __init__(self, shooter, angle):
        """Missile(shooter, angle) -> Missile
        Missile constructor.

        Requires the following positional arguments:
            shooter (CombatTurtle) -- turtle object that fired the missile (to
                prevent exploading from collision with owner)
            angle (float) -- direction in which missile was fired
        """

        # Assign given attributes
        self.shooter = shooter
        self.angle = angle

        # Assign automatic attributes
        self.speed = 20 # constant travel speed (px/sec)
        self.lifespan = 2000 # time until explosion (ms)
        self.proximity = 5 # missile explodes when within this distance (px)
                           # of a turtle (except for the shooter)

#=============================================================================

class Block():
    """Block class.

    Defines rectangular obstacles in the arena. Turtles cannot pass through
    blocks, and missile explode on contact with blocks.
    """

    #-------------------------------------------------------------------------

    def __init__(self, left, right, top, bottom):
        """Block(left, right, top, bottom) -> Block
        Block constructor.

        Requires the following positional arguments:
            left (float) -- leftmost x-coordinate (px)
            right (float) -- rightmost x-coordinate (px)
            top (float) -- uppermost y-coordinate (px)
            bottom (float) -- lowermost y-coordinate (px)
        """

        # Assign given attributes
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        ###
        # Use a turtle to draw the block.

    #-------------------------------------------------------------------------

    def contains(self, coords, closed=True):
        """Block.contains(coords[, closed]) -> bool
        Determines whether the block contains a given coordinate.

        Requires the following positional arguments:
            coords (tuple (float, float)) -- coordinate to test

        Accepts the following optional keyword arguments:
            closed (bool [True]) -- whether to include the boundaries

        Returns True if coords is within the block, and False otherwise.
        """

        # Determine output depending on whether boundaries are included
        if (closed == True):
            # Closed boundaries
            if ((coords[0] >= self.left) and (coords[0] <= self.right) and
                (coords[1] >= self.bottom) and (coords[1] <= self.top)):
                return True
        else:
            # Open boundaries
            if ((coords[0] > self.left) and (coords[0] < self.right) and
                (coords[1] > self.bottom) and (coords[1] < self.top)):
                return True

        # If nothing has been returned yet, the tests failed
        return False

#=============================================================================

class Arena():
    """Arena class.

    Acts as a container to store the contents of the arena, including all of
    the blocks.
    """

    #-------------------------------------------------------------------------

    def __init__(self, width, height, walled=True):
        """Arena(width, height[, walled]) -> Arena
        Arena constructor.

        Requires the following positional arguments:
            width (float) -- width of arena (px)
            height (float) -- height of arena (px)

        Accepts the following optional keyword arguments:
            walled (bool [True]) -- whether to generate walls around the arena
        """

        # Assign given attributes
        self.width = width
        self.height = height

        # Initialize block object list
        self.blocks = []

        # Generate walls around arena
        if (walled == True):
            ### Generate blocks.
            pass

        ###
        # Add some methods for automatically generating specific layouts, or
        # possibly random layouts.
