"""Defines the modules used throughout the Turtle Combat game."""

###
# Implementation notes:
# Each turtle should maintain an internal timer event that goes off several
# times per second.
# The step() method of the turtle is executed every time this timer goes off,
# and is meant to be overwritten by the AI subclasses to determine what to do
# in every step.
# The subclasses should not overwrite any of the direct movement methods, and
# the normal movement methods are instead overwritten to set internal
# attributes for what the turtle "wants" to do. After running the step()
# method, a bunch of code is automatically run to actuall evaluate the effects
# of those changes.

# Methods to be called:
# forward (and aliases), backward (and aliases), left/right (and aliases)
# fire

# Methods to be overwritten:
# setup
# step

import turtle

#=============================================================================

class CombatTurtle(turtle.Turtle):
    """Parent class for combat turtle AI players.

    Consists mostly of placeholders for methods to be overloaded by the
    subclasses that define the different players, as well as a variety of
    private utility methods.
    """

    #-------------------------------------------------------------------------

    def __init__(self, name, coords, facing, other):
        """CombatTurtle(name, coords, other) -> CombatTurtle
        Combat Turtle parent constructor.

        User visibility:
            should call -- no
            should overwrite -- no

        Requires the following positional arguments:
            name (str) -- name of turtle
            coords (tuple (float, float)) -- initial coordinates
            facing (float) -- initial orientation (degrees)
            other (CombatTurtle) -- opponent combat turtle object
        """

        # Set turtle speed
        self.speed(0) # movement handled in steps

        # Assign given attributes
        self.name = name
        (self.x, self.y) = coords
        self.left(facing)
        self.other = other

        # Define constant attributes
        self.max_spd = 5 # maximum movement speed (px/step)
        self.max_turn = 5 # maximum turning speed (deg/step)

        # Define variable attributes
        self.spd = 0 # target movement speed (px/step, negative for backwards)
        self.spd_turn = 0 # target CCW turn speed (deg/step, negative for CW)
        self.health = 100 # health points (turtle dies when health is zero)

        # Call setup function (contains setup code for specific submodule)
        self.setup()

    #-------------------------------------------------------------------------

    def __str__(self):
        """CombatTurtle.__str__() -> str
        String conversion returns Combat Turtle's name.

        User visibility:
            should call -- no
            should overwrite -- no
        """

        return self.name

    #-------------------------------------------------------------------------

    def setup(self):
        """CombatTurtle.setup() -> None
        Placeholder for Combat Turtle setup procedures.

        User visibility:
            should call -- no
            should overwrite -- yes

        This method is meant to be overwritten in the submodules of
        CombatTurtle. It is called at the end of the constructor. Its purpose
        is to prevent the user from having to overload the constructor in
        their own submodule, in which case they would need to replicate its
        argument list and attribute definitions.
        """

        pass

    #-------------------------------------------------------------------------

    def step(self):
        """CombatTurtle.step() -> None
        The main step event of the Combat Turtle.

        User visibility:
            should call -- no
            should overwrite -- yes

        This method is meant to be overwritten in the submodules of
        CombatTurtle. It is called each step (every 10 ms), after which any
        movement and firing events are actually executed.
        """

        pass

    #-------------------------------------------------------------------------

    def _step(self):
        """CombatTurtle._step() -> None
        The driver for all step events of the Combat Turtle.

        User visibility:
            should call -- no
            should overwrite -- no

        This is a hidden method to act as the driver for everything that the
        Combat Turtle does during a step. It calls the step() method, during
        which the internal movement and firing attributes should be set, and
        then actually evaluates their effects, moving the turtle and firing
        missiles as necessary.
        """

        # Call the user-defined step method
        self.step()

        # Turn turtle
        self._turn()

        # Move turtle
        self._move()

        ###
        # movement, missiles, cooldown, timer

    #-------------------------------------------------------------------------

    def fire(self):
        """CombatTurtle.fire() -> None
        Fires a missile in the turtle's current direction.

        User visibility:
            should call -- yes
            should overwrite -- no

        Creates a Missile object which begins to automatically move in the
        turtle's current direction.
        """

        ###
        # Include a way to account for cooldown.

        ###
        pass

    #-------------------------------------------------------------------------

    def forward(self, rate):
        """CombatTurtle.forward(rate) -> None
        Tells a turtle to move forward at a given fraction of its max speed.

        Aliases: forward, fd

        User visibility:
            should call -- yes
            should overwrite -- no

        Requires the following positional arguments:
            rate (float) -- movement rate, as a float between -1 and 1, with 0
                meaning no movement, 1 meaning maximum forward speed, -1
                meaning maximum backward speed, and intermediate values
                meaning a fraction of the maximum speed
        """

        # Determine movement speed (with rate clamped between 0 and 1)
        self.spd = self.max_spd * max(min(rate, 1), 0)

    #-------------------------------------------------------------------------

    def fd(self, rate):
        """CombatTurtle.fd(rate) -> None
        Tells a turtle to move forward at a given fraction of its max speed.

        Aliases: forward, fd

        User visibility:
            should call -- yes
            should overwrite -- no

        Requires the following positional arguments:
            rate (float) -- movement rate, as a float between -1 and 1, with 0
                meaning no movement, 1 meaning maximum forward speed, -1
                meaning maximum backward speed, and intermediate values
                meaning a fraction of the maximum speed
        """

        self.forward(rate)

    #-------------------------------------------------------------------------

    def backward(self, rate):
        """CombatTurtle.backward(rate) -> None
        Tells a turtle to move backward at a given fraction of its max speed.

        Aliases: backward, back, bk

        User visibility:
            should call -- yes
            should overwrite -- no

        Requires the following positional arguments:
            rate (float) -- movement rate, as a float between -1 and 1, with 0
                meaning no movement, 1 meaning maximum backward speed, -1
                meaning maximum forward speed, and intermediate values
                meaning a fraction of the maximum speed
        """

        # Equivalent to forward of negative rate
        self.forward(-rate)

    #-------------------------------------------------------------------------

    def back(self, rate):
        """CombatTurtle.back(rate) -> None
        Tells a turtle to move backward at a given fraction of its max speed.

        Aliases: backward, back, bk

        User visibility:
            should call -- yes
            should overwrite -- no

        Requires the following positional arguments:
            rate (float) -- movement rate, as a float between -1 and 1, with 0
                meaning no movement, 1 meaning maximum backward speed, -1
                meaning maximum forward speed, and intermediate values
                meaning a fraction of the maximum speed
        """

        self.backward(rate)

    #-------------------------------------------------------------------------

    def bk(self, rate):
        """CombatTurtle.bk(rate) -> None
        Tells a turtle to move backward at a given fraction of its max speed.

        Aliases: backward, back, bk

        User visibility:
            should call -- yes
            should overwrite -- no

        Requires the following positional arguments:
            rate (float) -- movement rate, as a float between -1 and 1, with 0
                meaning no movement, 1 meaning maximum backward speed, -1
                meaning maximum forward speed, and intermediate values
                meaning a fraction of the maximum speed
        """

        self.backward(rate)

    #-------------------------------------------------------------------------

    def _move(self):
        """CombatTurtle._move() -> None
        Moves a turtle according to its spd attribute.

        User visibility:
            should call -- no
            should overwrite -- no

        This is a hidden method called during the step event to handle any
        speed changes that the submodule has enacted using the visible
        forward() and backward() methods (or their aliases).
        """

        ###
        # Add collision checks for walls. We could use the goto method and
        # explicitly calculate the target coordinate, and then call the
        # contains() method for all blocks to see whether it's free; if not,
        # iteratively reduce speed until it is free.

        # Call standard turtle forward method (pixel version)
        super().forward(int(self.spd))

    #-------------------------------------------------------------------------

    def left(self, rate):
        """CombatTurtle.left(angle) -> None
        Tells a turtle to turn left by a given fraction of its turning speed.

        Aliases: left, lt

        User visibility:
            should call -- yes
            should overwrite -- no

        Requires the following positional arguments:
            rate (float) -- turning rate, as a float between -1 and 1, with 0
                meaning no turning, 1 meaning maximum counterclockwise speed,
                -1 meaning maximum clockwise speed, and intermediate values
                meaning a fraction of the turning speed
        """

        # Determine turning speed (with rate clamped between 0 and 1)
        self.spd_turn = self.max_turn * max(min(rate, 1), 0)

    #-------------------------------------------------------------------------

    def lt(self, rate):
        """CombatTurtle.lt(angle) -> None
        Tells a turtle to turn left by a given fraction of its turning speed.

        Aliases: left, lt

        User visibility:
            should call -- yes
            should overwrite -- no

        Requires the following positional arguments:
            rate (float) -- turning rate, as a float between -1 and 1, with 0
                meaning no turning, 1 meaning maximum counterclockwise speed,
                -1 meaning maximum clockwise speed, and intermediate values
                meaning a fraction of the turning speed
        """

        self.left(rate)

    #-------------------------------------------------------------------------

    def right(self, rate):
        """CombatTurtle.right(angle) -> None
        Tells a turtle to turn right by a given fraction of its turning speed.

        Aliases: right, rt

        User visibility:
            should call -- yes
            should overwrite -- no

        Requires the following positional arguments:
            rate (float) -- turning rate, as a float between -1 and 1, with 0
                meaning no turning, 1 meaning maximum clockwise speed, -1
                meaning maximum counterclockwise speed, and intermediate values
                meaning a fraction of the turning speed
        """

        # Equivalent to left of negative rate
        self.left(-rate)

    #-------------------------------------------------------------------------

    def rt(self, rate):
        """CombatTurtle.right(angle) -> None
        Tells a turtle to turn right by a given fraction of its turning speed.

        Aliases: right, rt

        User visibility:
            should call -- yes
            should overwrite -- no

        Requires the following positional arguments:
            rate (float) -- turning rate, as a float between -1 and 1, with 0
                meaning no turning, 1 meaning maximum clockwise speed, -1
                meaning maximum counterclockwise speed, and intermediate values
                meaning a fraction of the turning speed
        """

        self.right(rate)

    #-------------------------------------------------------------------------

    def _turn(self):
        """CombatTurtle._turn() -> None
        Turns a turtle according to its spd_turn attribute.

        User visibility:
            should call -- no
            should overwrite -- no

        This is a hidden method called during the step event to handle any
        turning speed changes that the submodule has enacted using the visible
        left() and right() methods (or their aliases).
        """

        # Call standard turtle left method
        super().left(int(self.spd_turn))

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
