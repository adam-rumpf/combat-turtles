### Turtles should also be able to access important global variables like missile speed, lifespan, and radius.
### See about defining them as global variables in a main game object that all classes can see.

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
# method, a bunch of code is automatically run to actually evaluate the
# effects of those changes.

###
# We might want to have the steps be handled by a global object to keep any
# time-dependent game objects in sync.

import turtle
from tc.game.missile import Missile

class CombatTurtle(turtle.Turtle):
    """Parent class for combat turtle AI players.

    Consists mostly of placeholders for methods to be overloaded by the
    subclasses that define the different players, as well as a variety of
    hidden utility methods.

    All attributes and methods are meant to be considered private.
    User-defined subclasses should not attempt to access the attributes or
    methods of any other objects. In addition, user-defined subclasses should
    not attempt to directly alter any built-in attributes (or to use any
    default Turtle methods that would do so, such as goto()), instead relying
    on the included interfacing methods.

    It is encouraged for user-defined subclasses to include their own custom
    attributes and methods, which the user should feel free to modify at
    will.

    Turtle movement is handled using discrete steps, which occur every 50 ms
    (at a rate of 20 steps/sec). The step() method is called once at the end
    of each step, after which the turtle is moved directly to its new
    position according to its current speed and heading. The visible movement-
    related methods (such as forward(), backward(), left(), and right()) do
    not actually move the Turtle, and instead update its internal speed and
    heading attributes, which are then used to perform movement at the end of
    the step.

    The following visible methods are meant for use in user-defined
        subclasses:
        forward(), backward() -- attempts to move forward or backward at a
            given fraction of the turtle's maximum speed (aliases: fd, back,
            bk)
        left(), right() -- turns left or right at a given fraction of the
            turtle's maximum turning speed (aliases: lt, rt)
        fire() -- attempts to fire a missile in the turtle's current facing
            direction
        get_max_speed(), get_max_turn_speed() -- returns the values of the
            turtle's constant attributes, including: maximum speed (px/step)
            and maximum turning speed (deg/step)
        get_position(), get_heading(), get_speed(), get_turn_speed(),
            get_health() -- returns the values of the turtle's variable
            attributes, including: position (px, px), heading (deg), speed
            (px/step), turning speed (deg/step), and health
        other_position(), other_heading(), other_speed(), other_turn_speed(),
            other_speed(), other_health() -- equivalent to the get methods,
            but returns the attributes of the opponent turtle
        distance() -- returns the distance between a given pair of coordinates
        other_distance() -- returns the distance to the opponent turtle (px)
        relative_position() -- returns the position of the opponent turtle
            (px, px) relative to this turtle
        relative_heading() -- returns the relative heading towards the
            opponent turtle (deg, positive for CCW)
        line_of_sight() -- returns whether or not the line to the opponent
            turtle is free of obstacles

    The following methods are meant to be overwritten in user-defined
        subclasses:
        setup() -- code run at the end of the turtle's initialization
        step() -- code run during each step event (which occurs every 50 ms)

    The following static methods can be used to retrieve relevant attributes
    from other classes, including:
        Missile.get_speed() -- missile travel speed (px/step)
        Missile.get_lifespan() -- missile lifespan (steps until explosion)
        Missile.get_proximity() -- missile explosive proximity (px from turtle)
        Missile.get_radius() -- missile explosive radius (px)

    In addition, each Combat Turtle subclass should include a static method
    class_name() that returns the name (as a string) of the class, which is
    used to distinguish between the different player AIs.
    """

    # Static methods declare class constants to be accessed by other classes

    #-------------------------------------------------------------------------

    def class_name():
        """CombatTurtle.class_name() -> str
        Returns the name of the Combat Turtle AI.
        """

        return "CombatTurtle"

    #=========================================================================

    def __init__(self, name=class_name(), col="black", coords=(0.0, 0.0),
                 facing=0.0, other=None):
        """CombatTurtle([name], [col], [coords], [facing], [other]) ->
            CombatTurtle
        Combat Turtle parent constructor.

        User visibility:
            should call -- no
            should overwrite -- no

        Accepts the following optional keyword arguments:
            name (str) ["Combat Turtle"] -- name of turtle
            col (str or color tuple) ["black"] -- color of turtle
            coords (tuple (float, float)) [(0,0, 0.0)] -- initial coordinates
            facing (float) [0.0] -- initial orientation (degrees)
            other (CombatTurtle) [None] -- opponent combat turtle object
        """

        # Initialize turtle
        super().__init__()

        # Set turtle class attributes
        self.speed(0) # movement handled in steps
        self.penup() # don't trace path
        self.shape("turtle") # turtle shape

        # Assign given attributes
        self.name = name
        self.color(col)
        self.goto(coords[0], coords[1])
        self.setheading(facing)
        self.other = other

        # Define constant attributes
        self.max_spd = 5.0 # maximum movement speed (px/step)
        self.max_turn = 5.0 # maximum turning speed (deg/step)
        self.step_time = 50 # time between steps (ms)

        # Define variable attributes
        self.spd = 0.0 # target movement speed (px/step, negative for back)
        self.spd_turn = 0.0 # target CCW turn speed (deg/step, negative for CW)
        self.health = 100.0 # health points (turtle dies when health is zero)

        # Call setup function (contains setup code for specific submodule)
        self.setup()

    #-------------------------------------------------------------------------

    def __str__(self):
        """CombatTurtle.__str__() -> str
        String conversion returns the Combat Turtle's name.

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
        CombatTurtle. It is called each step (every 50 ms), after which any
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

    def get_max_speed(self):
        """CombatTurtle.get_max_speed() -> float
        Returns the maximum speed (px/step) of the turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self.max_spd

    #-------------------------------------------------------------------------

    def get_max_turn_speed(self):
        """CombatTurtle.get_max_turn_speed() -> float
        Returns the maximum turning speed (deg/step) of the turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self.max_turn

    #-------------------------------------------------------------------------

    def get_position(self):
        """CombatTurtle.get_position() -> float
        Returns the current position (px, px) of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self.position()

    #-------------------------------------------------------------------------

    def forward(self, rate=1):
        """CombatTurtle.forward([rate]) -> None
        Tells a turtle to move forward at a given fraction of its max speed.

        Aliases: forward, fd

        User visibility:
            should call -- yes
            should overwrite -- no

        Accepts following optional positional arguments:
            rate (float) [1] -- movement rate, as a float between -1 and 1,
                with 0 meaning no movement, 1 meaning maximum forward speed,
                -1 meaning maximum backward speed, and intermediate values
                meaning a fraction of the maximum speed
        """

        # Determine movement speed (with rate clamped between -1 and 1)
        self.spd = self.max_spd * max(min(rate, 1), -1)

    #-------------------------------------------------------------------------

    def fd(self, rate=1):
        """CombatTurtle.fd([rate]) -> None
        Tells a turtle to move forward at a given fraction of its max speed.

        Aliases: forward, fd

        User visibility:
            should call -- yes
            should overwrite -- no

        Accepts following optional positional arguments:
            rate (float) [1] -- movement rate, as a float between -1 and 1,
                with 0 meaning no movement, 1 meaning maximum forward speed,
                -1 meaning maximum backward speed, and intermediate values
                meaning a fraction of the maximum speed
        """

        self.forward(rate)

    #-------------------------------------------------------------------------

    def backward(self, rate=1):
        """CombatTurtle.backward([rate]) -> None
        Tells a turtle to move backward at a given fraction of its max speed.

        Aliases: backward, back, bk

        User visibility:
            should call -- yes
            should overwrite -- no

        Accepts following optional positional arguments:
            rate (float) [1] -- movement rate, as a float between -1 and 1,
                with 0 meaning no movement, 1 meaning maximum backward speed,
                -1 meaning maximum forward speed, and intermediate values
                meaning a fraction of the maximum speed
        """

        # Equivalent to moving forward at negative rate
        self.forward(-rate)

    #-------------------------------------------------------------------------

    def back(self, rate=1):
        """CombatTurtle.back([rate]) -> None
        Tells a turtle to move backward at a given fraction of its max speed.

        Aliases: backward, back, bk

        User visibility:
            should call -- yes
            should overwrite -- no

        Accepts following optional positional arguments:
            rate (float) [1] -- movement rate, as a float between -1 and 1,
                with 0 meaning no movement, 1 meaning maximum backward speed,
                -1 meaning maximum forward speed, and intermediate values
                meaning a fraction of the maximum speed
        """

        self.backward(rate)

    #-------------------------------------------------------------------------

    def bk(self, rate=1):
        """CombatTurtle.bk([rate]) -> None
        Tells a turtle to move backward at a given fraction of its max speed.

        Aliases: backward, back, bk

        User visibility:
            should call -- yes
            should overwrite -- no

        Accepts following optional positional arguments:
            rate (float) [1] -- movement rate, as a float between -1 and 1,
                with 0 meaning no movement, 1 meaning maximum backward speed,
                -1 meaning maximum forward speed, and intermediate values
                meaning a fraction of the maximum speed
        """

        self.backward(rate)

    #-------------------------------------------------------------------------

    def get_speed(self):
        """CombatTurtle.get_speed() -> float
        Returns the current speed (px/step) of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self.spd

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
        # Another simple alternative could be to use goto and calculate the
        # destination coordinate each step. If this would collide with a wall,
        # cap one coordinate (or both) to equal the border coordinate of the
        # wall.

        # Call standard turtle forward method (pixel version)
        super().forward(int(self.spd))

    #-------------------------------------------------------------------------

    def get_heading(self):
        """CombatTurtle.get_heading() -> float
        Returns the current direction (deg) of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self.heading()

    #-------------------------------------------------------------------------

    def left(self, rate=1):
        """CombatTurtle.left([angle]) -> None
        Tells a turtle to turn left by a given fraction of its turning speed.

        Aliases: left, lt

        User visibility:
            should call -- yes
            should overwrite -- no

        Accepts the following optional keyword arguments:
            rate (float) [1] -- turning rate, as a float between -1 and 1,
                with 0 meaning no turning, 1 meaning maximum counterclockwise
                speed, -1 meaning maximum clockwise speed, and intermediate
                values meaning a fraction of the turning speed
        """

        # Determine turning speed (with rate clamped between -1 and 1)
        self.spd_turn = self.max_turn * max(min(rate, 1), -1)

    #-------------------------------------------------------------------------

    def lt(self, rate=1):
        """CombatTurtle.lt([angle]) -> None
        Tells a turtle to turn left by a given fraction of its turning speed.

        Aliases: left, lt

        User visibility:
            should call -- yes
            should overwrite -- no

        Accepts the following optional keyword arguments:
            rate (float) [1] -- turning rate, as a float between -1 and 1,
                with 0 meaning no turning, 1 meaning maximum counterclockwise
                speed, -1 meaning maximum clockwise speed, and intermediate
                values meaning a fraction of the turning speed
        """

        self.left(rate)

    #-------------------------------------------------------------------------

    def right(self, rate=1):
        """CombatTurtle.right([angle]) -> None
        Tells a turtle to turn right by a given fraction of its turning speed.

        Aliases: right, rt

        User visibility:
            should call -- yes
            should overwrite -- no

        Accepts the following optional keyword arguments:
            rate (float) [1] -- turning rate, as a float between -1 and 1,
                with 0 meaning no turning, 1 meaning maximum clockwise speed,
                -1 meaning maximum counterclockwise speed, and intermediate
                values meaning a fraction of the turning speed
        """

        # Equivalent to turning left at negative rate
        self.left(-rate)

    #-------------------------------------------------------------------------

    def rt(self, rate=1):
        """CombatTurtle.right([angle]) -> None
        Tells a turtle to turn right by a given fraction of its turning speed.

        Aliases: right, rt

        User visibility:
            should call -- yes
            should overwrite -- no

        Accepts the following optional keyword arguments:
            rate (float) [1] -- turning rate, as a float between -1 and 1,
                with 0 meaning no turning, 1 meaning maximum clockwise speed,
                -1 meaning maximum counterclockwise speed, and intermediate
                values meaning a fraction of the turning speed
        """

        self.right(rate)

    #-------------------------------------------------------------------------

    def get_turn_speed(self):
        """CombatTurtle.get_turn_speed() -> float
        Returns the turning speed (CCW deg/step) of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self.spd_turn

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

    #-------------------------------------------------------------------------

    def other_position(self):
        """CombatTurtle.other_position() -> (float, float)
        Returns the coordinates of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if (self.other == None):
            return None

        return self.other.get_position()

    #-------------------------------------------------------------------------

    def distance(self, coords1, coords2):
        """CombatTurtle._distance(coords1, coords2) -> float
        Calculates the distance between a pair of coordinates (px).

        User visibility:
            should call -- no
            should overwrite -- yes

        Requires the following positional arguments:
            coords1 (tuple (float, float)) -- first pair of coordinates
            coords2 (tuple (float, float)) -- second pair of coordinates
        """

        # Calculate Euclidean distance
        return ((coords1[0]-coords2[0])**2 + (coords1[1]-coords2[1])**2)**0.5

    #-------------------------------------------------------------------------

    def other_distance(self):
        """CombatTurtle.other_distance() -> float
        Returns the distance to the opponent turtle (px).

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if (self.other == None):
            return None

        # Calculate distance between pair of coordinates
        return self.distance(self.get_position(), self.other.get_position())

    #-------------------------------------------------------------------------

    def relative_position(self):
        """CombatTurtle.relative_position() -> (float, float)
        Returns coordinates of the opponent Combat Turtle relative to self.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if (self.other == None):
            return None

        # Get both sets of coordinates
        own_coords = self.get_position()
        other_coords = self.other.get_position()

        # Return difference
        return (other_coords[0]-own_coords[0], other_coords[1]-own_coords[1])

    #-------------------------------------------------------------------------

    def other_heading(self):
        """CombatTurtle.other_heading() -> (float, float)
        Returns the heading direction (degrees) of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if (self.other == None):
            return None

        return self.other.get_heading()

    #-------------------------------------------------------------------------

    def relative_heading(self):
        """CombatTurtle.relative_heading() -> float
        Returns the relative heading (deg) to the opponent turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if (self.other == None):
            return None

        ### Calculate heading to other turtle. Find the angle between the
        ### current heading vector and the vector to the other turtle, and
        ### adjust the sign so that left is positive.

        pass

    #-------------------------------------------------------------------------

    def other_speed(self):
        """CombatTurtle.other_speed() -> float
        Returns the current speed (px/step) of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if (self.other == None):
            return None

        return self.other.get_speed()

    #-------------------------------------------------------------------------

    def other_turn_speed(self):
        """CombatTurtle.other_turn_speed() -> float
        Returns the turn speed (CCW deg/step) of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if (self.other == None):
            return None

        return self.other.get_turn_speed()

    #-------------------------------------------------------------------------

    def get_health(self):
        """CombatTurtle.get_health() -> float
        Returns the health of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self.health

    #-------------------------------------------------------------------------

    def other_health(self):
        """CombatTurtle.other_health() -> float
        Returns the health of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if (self.other == None):
            return None

        return self.other.get_health()

    #-------------------------------------------------------------------------

    def line_of_sight(self):
        """CombatTurtle.line_of_sight() -> bool
        Returns whether there is a clear line of sight to the opponent turtle.

        User visibility:
            should call -- yes
            should overwrite -- no

        Returns True if the line between the two turtles is free of obstacles
        and False otherwise.
        """

        if (self.other == None):
            return None

        ### Figure out how to quickly test sight lines. A quick and dirty way
        ### would just be to sample a bunch of points along the sight line to
        ### see whether any collide with a block, but this could be expensive
        ### since it needs to be looped over every block, potentially every
        ### step.

        pass
