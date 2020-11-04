"""Defines a turtle class using Tkinter."""

### Note: May need to update the 33 ms (30 steps/sec) step timing description.

### In the template, list the public methods and sort by general purpose (action, opponent info, constant info, self info).
### Also reorder these methods by category.

### We may have to change the way that headings are handled, since turtles might spin around from handling absolute headings that are equivalent.
### Look at all of the functions where headings are significant and see how they are handled.
### Whenever comparing two headings, we generally want the smallest angle between them, with a sign indicating which is CCW and which is CW.

import tkinter as tk
import math
from .game.arena import Arena
from .game.block import Block
from .game.missile import Missile
from .util.angles import Angle

class TkTurtle:
    """Tkinter turtle class to use as the parent of Combat Turtle classes.

    This class is meant to reproduce much of the functionality of the standard
    'turtle' class, but with less overhead due to the step-based gameplay. It
    consists mostly of placeholders for methods to be overloaded by the
    subclasses that define the different players, visible frontend methods for
    use in defining AI subclasses, and a variety of hidden utility methods.

    All attributes and methods are meant to be considered private.
    User-defined subclasses should not attempt to access the attributes or
    methods of any other objects. It is encouraged for user-defined subclasses
    to include their own custom attributes and methods, which the user should
    feel free to modify at will.

    Turtle movement is handled using discrete steps, which occur every 33 ms
    (at a rate of approximately 30 steps/sec). The step() method is called
    once at the end of each step, after which the turtle is moved directly to
    its new position according to its current speed and heading. The visible
    movement-related methods (such as forward(), backward(), left(), and
    right()) do not actually move the Turtle, and instead update its internal
    speed and heading attributes, which are then used to perform movement at
    the end of the step.

    The following local read-only attributes are meant for use in user-defined
    subclasses:
        max_speed, max_turn_speed -- returns the values of the turtle's
            constant attributes, including: maximum speed (px/step) and
            maximum turning speed (deg/step)
        position, heading, speed, turn_speed, health -- returns the values of
            the turtle's variable attributes, including: position (px, px),
            heading (deg), speed (px/step), turning speed (deg/step), and
            health
        shoot_delay -- returns delay between shooting missiles (steps)
        cooldown -- returns number of steps between shooting missiles
        can_shoot -- returns whether the turtle is currently able to shoot
        other_position, other_heading, other_speed, other_turn_speed,
            other_health -- equivalent to the local attributes, but returns
            the attributes of the opponent turtle as of the end of the
            previous step
        missile_speed -- returns the travel speed of missiles (px/step)
        missile_range -- returns the maximum range of missiles (px)
        missile_proximity -- returns the proximity radius of missiles (px)
        missile_radius -- returns the explosion radius of missiles (px)
        missile_damage -- returns the damage dealt by a missile
        arena_left, arena_right, arena_top, arena_bottom -- returns the
            coordinates of the arena boundaries

    The following visible methods are meant for use in user-defined
    subclasses:
        forward(), backward() -- attempts to move forward or backward at a
            given fraction of the turtle's maximum speed (aliases: fd, back,
            bk)
        left(), right() -- turns left or right at a given fraction of the
            turtle's maximum turning speed (aliases: lt, rt)
        turn_towards() -- turns as far as possible to face a given coordinate
        shoot() -- attempts to shoot a missile in the turtle's current facing
            direction
        distance() -- returns the distance between a pair of coordinates (px),
            including distance to opponent turtle
        relative_position() -- returns the position of the opponent turtle
            (px, px) relative to this turtle
        relative_heading() -- returns the relative heading towards the
            opponent turtle (deg, positive for CCW)
        line_of_sight() -- returns whether or not the line to the opponent
            turtle is free of obstacles

    The following methods are meant to be overwritten in user-defined
    subclasses:
        class_name() -- (static method) returns the name of the class for use
            in distinguishing between different Combat Turtle AIs
        class_desc() -- (static method) returns a one-line description of the
            Combat Turtle AI
        class_shape() -- (static method) returns either an integer index or a
            radius tuple and an angle tuple to define the turtle's shape image
        setup() -- code run at the end of the turtle's initialization
        step() -- code run during each step event (which occurs every 33 ms)
    """

    # Static methods declare class constants to be accessed by other classes

    #-------------------------------------------------------------------------

    def class_name():
        """TkTurtle.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "CombatTurtleParent"

    #-------------------------------------------------------------------------

    def class_desc():
        """TkTurtle.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Parent class of all Combat Turtle classes."

    #-------------------------------------------------------------------------

    def class_shape():
        """TkTurtle.class_shape() -> (int or tuple)
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

        return 0

    #=========================================================================

    def __init__(self, game, name=class_name(), col="black",
                 coords=(0, 0), heading=0, dim=(30, 20)):
        """TkTurtle(game, [name], [col], [coords], [facing], [dim]) ->
        TkTurtle
        Combat Turtle parent constructor.

        User visibility:
            should call -- no
            should overwrite -- no

        Requires the following positional arguments:
            game (tcgame.TurtleCombatGame) -- game driver object

        Accepts the following optional keyword arguments:
            name (str) ["Combat Turtle"] -- name of turtle
            col (str or color tuple) ["black"] -- color of turtle
            coords (tuple (int, int)) [(0,0, 0.0)] -- initial coordinates
            heading (int) [0] -- initial orientation (degrees north of east)
            dim (tuple (int, int)) [(30, 20)] -- length and width (px) of
                turtle's sprite
        """

        # Assign given attributes
        self._name = name
        (self._x, self._y) = coords
        self._heading = Angle(heading, "degrees")
        self._game = game
        self._canvas = game.canvas
        self._color = col

        # Define constant attributes
        self._max_speed = 4 # maximum movement speed (px/step)
        self._max_turn_speed = 15 # maximum turning speed (deg/step)
        self._shoot_delay = 60 # delay between missile shots (steps)

        # Define shape coordinates
        cs = self.__class__.class_shape()
        if type(cs) == int:
            # Preset integer index
            (self._shape_radius, self._shape_angle) = self._shape(dim, cs)
        elif type(cs) == tuple and len(cs) == 2:
            # Custom coordinates
            (self._shape_radius, self._shape_angle) = cs
        else:
            # Default to arrowhead
            (self._shape_radius, self._shape_angle) = self._shape(dim, 0)

        # Define variable attributes
        self._other = None # opponent turtle object
        self._speed = 0 # target movement speed (px/step, negative for back)
        self._speed_turn = 0 # target CCW turn speed (deg/step, < 0 for CW)
        self._health = 100 # health points (turtle dies when health is zero)
        self._cooldown = 0 # delay until able to shoot next (steps)
        self._shooting = False # whether the turtle is attempting to shoot

        # Draw self
        self._redraw()

        # Initialize list of currently-active missiles shot by this turtle
        self._missiles = []

        # Call setup function (contains setup code for specific submodule)
        self.setup()

    #-------------------------------------------------------------------------

    def __str__(self):
        """TkTurtle.__str__() -> str
        String conversion returns the Combat Turtle's name.

        User visibility:
            should call -- no
            should overwrite -- no
        """

        return self._name

    #-------------------------------------------------------------------------

    def __del__(self):
        """~TkTurtle.() -> None
        Combat Turtle destructor.

        Deletes drawing on canvas and all associated Missile objects.
        """

        # Delete sprite (if it has been defined)
        try:
            self._canvas.delete(self._sprite)
        except AttributeError:
            pass
        except tk.TclError:
            pass

        # Delete all missile objects
        del self._missiles[:]

    #-------------------------------------------------------------------------

    def setup(self):
        """TkTurtle.setup() -> None
        Placeholder for Combat Turtle setup procedures.

        User visibility:
            should call -- no
            should overwrite -- yes

        This method is meant to be overwritten in the submodules of TkTurtle.
        It is called at the end of the constructor. Its purpose is to prevent
        the user from having to overload the constructor in their own
        submodule, in which case they would need to replicate its argument
        list and attribute definitions.
        """

        pass

    #-------------------------------------------------------------------------

    def step(self):
        """TkTurtle.step() -> None
        The main step event of the Combat Turtle.

        User visibility:
            should call -- no
            should overwrite -- yes

        This method is meant to be overwritten in the submodules of TkTurtle.
        It is called each step (every 33 ms), after which any movement and
        firing events are actually executed.
        """

        pass

    #-------------------------------------------------------------------------

    def _shape(self, dim, index):
        """TkTurtle._shape(dim, index) -> tuple
        Returns the polar coordinates of the turtle's shape polygon.

        User visibility:
            should call -- no
            should overwrite -- no

        User-defined Combat Turtles can define their own sets of coordinates
        for drawing the turtle's shape. This function returns one of the
        preset shapes based on an integer index.
        """

        # Output coordinates based on integer index
        if index == 1:
            # Pentagon
            r1 = dim[0]/2
            r2 = dim[1]/2
            radius = (r1, r2, r2, r2, r2, r1)
            angle = (0, 2*math.pi/5, 4*math.pi/5, 6*math.pi/5, 8*math.pi/5, 0)
        elif index == 2:
            # Plow
            r1 = dim[0]/2
            r2 = dim[1]/2
            radius = (r1, r2, math.sqrt(r1**2 + r2**2),
                      math.sqrt(r1**2 + r2**2), r2)
            angle = (0, math.pi/2, math.atan2(r2, -r1), math.atan2(-r2, -r1),
                     -math.pi/2)
        else:
            # Default to arrowhead
            r1 = dim[0]/2
            r2 = dim[1]/2
            radius = (r1, 2*r2/math.sqrt(3), 0, 2*r2/math.sqrt(3), r1)
            angle = (0, 2*math.pi/3, math.pi, 4*math.pi/3, 0)

        return (radius, angle)

    #-------------------------------------------------------------------------

    def _redraw(self):
        """TkTurtle._redraw() -> None
        Redraws sprite on canvas to update appearance after moving.

        User visibility:
            should call -- no
            should overwrite -- no

        This method is called at the end of each step to update the turtle
        sprite's position on the screen. The existing sprite is deleted and a
        new polygon is drawn at the new position and orientation.
        """

        # Delete existing sprite (undefined during initial draw)
        try:
            self._canvas.delete(self._sprite)
        except AttributeError:
            pass

        # Draw new sprite
        self._sprite = self._canvas.create_polygon(self._poly(),
                                                   fill=self._color)

    #-------------------------------------------------------------------------

    def _set_other(self, other):
        """TkTurtle._set_other(other) -> None
        Sets a pointer to the opponent Combat Turtle.

        User visibility:
            should call -- no
            should overwrite -- no

        Both Combat Turtles involved in the game must be instantiated before
        the 'other' attribute can be set. This method is meant to be called by
        the game driver after defining both players.
        """

        self._other = other
        self._get_other_attributes()

    #-------------------------------------------------------------------------

    def _get_other_attributes(self):
        """TkTurtle._get_other_attributes() -> None
        Gets the public attributes of the opponent Combat Turtle.

        User visibility:
            should call -- no
            should overwrite -- no

        This method is called by the game driver after all Combat Turtles have
        completed their moves for the current step. This object's methods that
        measure the position of the other turtle are based on these end-of-
        step updates from the previous step, in order to prevent asymmetry
        from one turtle completing all of its step actions before the other.
        """

        if self._other == None:
            return None

        # Access other Combat Turtle's public properties
        self._other_prev_position = self._other.position
        self._other_prev_heading = self._other.heading
        self._other_prev_speed = self._other.speed
        self._other_prev_turn_speed = self._other.turn_speed
        self._other_prev_health = self._other.health

    #-------------------------------------------------------------------------

    def _poly(self):
        """TkTurtle._poly() -> list
        Creates a list of coordinates to define the turtle's shape polygon.

        User visibility:
            should call -- no
            should overwrite -- no

        Turtles are drawn as polygons, centered at the object's coordinates
        and rotated according to its heading.
        """

        # Calculate new coordinates by rotating shape template and offsetting
        coords = [0 for i in range(2*(len(self._shape_radius)+1))]
        angle = math.radians(self.heading) # convert heading to rad
        for i in range(len(self._shape_angle)):
            coords[2*i] = int(self._x + (self._shape_radius[i]*
                              math.cos(self._shape_angle[i]+angle)))
            coords[2*i+1] = int(self._y + (self._shape_radius[i]*
                                math.sin(self._shape_angle[i]+angle)))
        coords[-2] = coords[0]
        coords[-1] = coords[1]

        return coords

    #-------------------------------------------------------------------------

    def _step(self):
        """TkTurtle._step() -> None
        The driver for all step events of the Combat Turtle.

        User visibility:
            should call -- no
            should overwrite -- no

        This is a hidden method to act as the driver for everything that the
        Combat Turtle does during a step. It calls the step() method, during
        which the internal movement and firing attributes should be set, and
        then actually evaluates their effects, moving the turtle and firing
        missiles as necessary.

        Any missiles shot by this Combat Turtle are also updated here using
        the missile's step() method.
        """

        # Reset speed and shooting status
        self._speed = 0
        self._speed_turn = 0
        self._shooting = False

        # Reduce cooldown
        if self.cooldown > 0:
            self._cooldown -= 1

        # Call the user-defined step method
        self.step()

        # Turn turtle
        self._turn()

        # Move turtle
        self._move()

        # Update all missiles
        for m in self._missiles:
            m._step()

        # Attempt to shoot
        self._shoot()

        # Update sprite
        self._redraw()

    #-------------------------------------------------------------------------

    def _shoot(self):
        """TkTurtle._shoot() -> None
        Shoots a missile in the turtle's current direction.

        User visibility:
            should call -- no
            should overwrite -- no

        Creates a Missile object which begins to automatically move in the
        turtle's current direction.
        """

        # If on cooldown or if not shooting, do nothing
        if self._shooting == False or self.cooldown > 0:
            return None

        # Otherwise create a missile object and add to the list
        self._cooldown = self.shoot_delay # reset cooldown duration
        self._missiles.append(Missile(self._game, self, self._other,
                                      self.position, self.heading))

    #-------------------------------------------------------------------------

    @property
    def max_speed(self):
        """TkTurtle.max_speed -> int
        Returns the maximum speed (px/step) of the turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self._max_speed

    @max_speed.setter
    def max_speed(self, value):
        """Do-nothing max speed setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def max_turn_speed(self):
        """TkTurtle.max_turn_speed -> int
        Returns the maximum turning speed (deg/step) of the turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self._max_turn_speed

    @max_turn_speed.setter
    def max_turn_speed(self, value):
        """Do-nothing max turn speed setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def x(self):
        """TkTurtle.x -> int
        Returns the current x-coordinate (px) of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self._x

    @x.setter
    def x(self, value):
        """Do-nothing position setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def y(self):
        """TkTurtle.y -> int
        Returns the current y-coordinate (px) of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self._y

    @y.setter
    def y(self, value):
        """Do-nothing position setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def position(self):
        """TkTurtle.position -> tuple
        Returns the current position (px, px) of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return (self.x, self.y)

    @position.setter
    def position(self, value):
        """Do-nothing position setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def shoot_delay(self):
        """TkTurtle.shoot_delay -> int
        Returns the minimum delay between shooting missiles (steps).

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self._shoot_delay

    @shoot_delay.setter
    def shoot_delay(self, value):
        """Do-nothing shooting delay setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def cooldown(self):
        """TkTurtle.cooldown -> int
        Returns delay until the Combat Turtle is next able to shoot (steps).

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self._cooldown

    @cooldown.setter
    def cooldown(self, value):
        """Do-nothing cooldown setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def can_shoot(self):
        """TkTurtle.can_shoot -> bool
        Returns whether or not the Combat Turtle is able to shoot.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return (self._cooldown <= 0)

    @can_shoot.setter
    def can_shoot(self, value):
        """Do-nothing shoot indicator setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    def shoot(self):
        """TkTurtle.shoot() -> None
        Tells a turtle to shoot a missile.

        User visibility:
            should call -- yes
            should overwrite -- no

        Attempts to shoot a missile in the turtle's current direction. If the
        turtle is still on cooldown from the previous shot, this does nothing.
        """

        # Set shooting status
        self._shooting = True

    #-------------------------------------------------------------------------

    def forward(self, rate=1):
        """TkTurtle.forward([rate]) -> None
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
        self._speed = int(self.max_speed * max(min(rate, 1), -1))

    # Set aliases
    fd = forward

    #-------------------------------------------------------------------------

    def backward(self, rate=1):
        """TkTurtle.backward([rate]) -> None
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

    # Set aliases
    back = backward
    bk = backward

    #-------------------------------------------------------------------------

    @property
    def speed(self):
        """TkTurtle.speed -> int
        Returns the current speed (px/step) of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self._speed

    @speed.setter
    def speed(self, value):
        """Do-nothing speed setter to prevent overwriting. """

        pass

    #-------------------------------------------------------------------------

    def _move(self):
        """TkTurtle._move() -> None
        Moves a turtle according to its speed attribute.

        User visibility:
            should call -- no
            should overwrite -- no

        This is a hidden method called during the step event to handle any
        speed changes that the submodule has enacted using the visible
        forward() and backward() methods (or their aliases).
        """

        # Set new coordinates
        self._x += int(self.speed*math.cos(math.radians(self.heading)))
        self._y += int(self.speed*math.sin(math.radians(self.heading)))

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

    @property
    def heading(self):
        """TkTurtle.heading -> int
        Returns the current direction (deg) of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no

        For the purposes of internal calculations, headings are stored as a
        private Angle variable which automatically handles revolutions.
        Accessing the variable returns the integer version of the heading,
        which is always normalized to lie between (-180,180] degrees.
        """

        return int(self._heading)

    @heading.setter
    def heading(self, value):
        """Do-nothing heading setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    def left(self, rate=1):
        """TkTurtle.left([angle]) -> None
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
        self._speed_turn = int(self.max_turn_speed * max(min(rate, 1), -1))

    # Set aliases
    lt = left

    #-------------------------------------------------------------------------

    def right(self, rate=1):
        """TkTurtle.right([angle]) -> None
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

    # Set aliases
    rt = right

    #-------------------------------------------------------------------------

    @property
    def turn_speed(self):
        """TkTurtle.turn_speed -> int
        Returns the turning speed (CCW deg/step) of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self._speed_turn

    @turn_speed.setter
    def turn_speed(self, value):
        """Do-nothing turning speed setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    def _turn(self):
        """TkTurtle._turn() -> None
        Turns a turtle according to its speed_turn attribute.

        User visibility:
            should call -- no
            should overwrite -- no

        This is a hidden method called during the step event to handle any
        turning speed changes that the submodule has enacted using the visible
        left() and right() methods (or their aliases).
        """

        # Change heading (negate angle due to origin at top of screen)
        self._heading -= int(self._speed_turn)

    #-------------------------------------------------------------------------

    @property
    def other_position(self):
        """TkTurtle.other_position -> tuple
        Returns the coordinates of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if self._other == None:
            return None

        return self._other_prev_position

    @other_position.setter
    def other_position(self, value):
        """Do-nothing other position setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    def distance(self, *args):
        """TkTurtle.distance([coords1[, coords2]]) -> float
        Calculates the distance between a pair of coordinates (px).

        User visibility:
            should call -- yes
            should overwrite -- no

        This method can be called in several different formats depending on
        the number of arguments:
            0 arguments -- returns distance between self and opponent
            1 argument -- returns distance between self and given coordinate
                (int, int)
            2 arguments -- returns distance between given pair of coordinates,
                both (int, int)
        """

        # Default arguments
        coords1 = self.position
        coords2 = self.position
        if self._other != None:
            coords2 = self._other.position

        # Modify depending on given inputs
        if len(args) >= 1:
            coords2 = args[0]
        if len(args) >= 2:
            coords1 = args[1]

        # Calculate Euclidean distance
        return math.sqrt((coords1[0]-coords2[0])**2 +
                         (coords1[1]-coords2[1])**2)

    #-------------------------------------------------------------------------

    def relative_position(self):
        """TkTurtle.relative_position -> tuple
        Returns coordinates of the opponent Combat Turtle relative to self.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if self._other == None:
            return None

        # Get both sets of coordinates
        own_coords = self.position
        other_coords = self._other.position

        # Return difference
        return (other_coords[0]-own_coords[0], other_coords[1]-own_coords[1])

    #-------------------------------------------------------------------------

    @property
    def other_heading(self):
        """TkTurtle.other_heading -> int
        Returns the heading direction (deg) of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if self._other == None:
            return None

        return int(self._other_prev_heading)

    @other_heading.setter
    def other_heading(self, value):
        """Do-nothing other heading setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    def relative_heading(self):
        """TkTurtle.relative_heading() -> int
        Returns the relative heading (deg) to the opponent turtle.

        User visibility:
            should call -- yes
            should overwrite -- no

        The returned heading is a value between -180 degrees and 180 degrees,
        representing the smallest heading change that would turn this Combat
        Turtle to face its opponent (positive represents counterclockwise,
        negative represents clockwise).
        """

        if self._other == None:
            return None

        ### Calculate heading to other turtle. Find the angle between the
        ### current heading vector and the vector to the other turtle, and
        ### adjust the sign so that left is positive.

    #-------------------------------------------------------------------------

    def turn_towards(self, target=None):
        """TkTurtle.turn_towards([target]) -> None
        Turns the Combat Turtle as far as possible towards a target.

        User visibility:
            should call -- yes
            should overwrite -- no

        This method can be called in several different formats depending on
        whether a target is specified, and what type it is:
            None -- target becomes opponent turtle's coordinates
            int -- turtle will attempt to turn towards the given heading
            tuple (int, int) -- turtle will attempt to turn to face a given
                coordinate

        This method automatically attempts to turn the Combat Turtle towards a
        given heading or set of coordinates. If possible, it will turn
        directly to the target, but if this would require turning more than
        the maximum turning speed will allow, it will instead turn as far as
        possible towards the specified target.
        """

        # Default to opponent coordinates
        if target == None:
            self.turn_towards(target=self.other_position)

        # Turn towards coordinates if given a tuple
        if type(target) == type((0, 0)):
            pass
            ###
            ### Turn left equal to the relative heading,
            ### clamped at +/- maximum turn speed.

        # Turn towards heading if given an int or float
        else:
            # Calculate a point to turn towards to use min angle calculations
            point = (int(self._x + 1000*math.cos(math.radians(target))),
                     int(self._y + 1000*math.sin(math.radians(target))))
            print(point)###
            self.turn_towards(target=point)

    #-------------------------------------------------------------------------

    @property
    def other_speed(self):
        """TkTurtle.other_speed -> int
        Returns the current speed (px/step) of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if self._other == None:
            return None

        return self._other_prev_speed

    @other_speed.setter
    def other_speed(self, value):
        """Do-nothing other speed setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def other_turn_speed(self):
        """TkTurtle.other_turn_speed -> int
        Returns the turn speed (CCW deg/step) of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if self._other == None:
            return None

        return self._other_prev_turn_speed

    @other_turn_speed.setter
    def othspeed(self, value):
        """Do-nothing speed setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def health(self):
        """TkTurtle.health -> int
        Returns the health of the Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return self._health

    @health.setter
    def health(self, value):
        """Do-nothing health setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def other_health(self):
        """TkTurtle.other_health -> int
        Returns the health of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if self._other == None:
            return None

        return self._other_prev_health

    @other_health.setter
    def other_health(self, value):
        """Do-nothing other health setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def missile_speed(self):
        """TkTurtle.missile_speed -> int
        Returns the constant travel speed of missiles (px/step).

        User visibility:
            should call -- yes
            should overwrite -- no

        Missile objects shot by a Combat Turtle travel at this constant speed
        in a straight line in the direction of fire.
        """

        return Missile.get_speed()

    @missile_speed.setter
    def missile_speed(self, value):
        """Do-nothing missile speed setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def missile_range(self):
        """TkTurtle.missile_range -> int
        Returns the maximum range of missiles (px).

        User visibility:
            should call -- yes
            should overwrite -- no

        Missile objects explode after a set delay (unless making contact with
        a solid object or opponent turtle first). This method uses the missile
        speed and delay to calculate the resulting range.
        """

        return Missile.get_speed() * Missile.get_lifespan()

    @missile_range.setter
    def missile_range(self, value):
        """Do-nothing missile range setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def missile_proximity(self):
        """TkTurtle.missile_proximity -> int
        Returns the proximity distance of missiles (px).

        User visibility:
            should call -- yes
            should overwrite -- no

        Missiles explode if they are within this distance of the opponent
        turtle.
        """

        return Missile.get_proximity()

    @missile_proximity.setter
    def missile_proximity(self, value):
        """Do-nothing missile proximity setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def missile_radius(self):
        """TkTurtle.missile_radius -> int
        Returns the explosive radius of missiles (px).

        User visibility:
            should call -- yes
            should overwrite -- no

        When a missile explodes (either due to colliding with an object or
        after reaching its maximum range), it creates an explosion with this
        radius, damaging any turtle within the radius (including the turtle
        that shot it).
        """

        return Missile.get_radius()

    @missile_radius.setter
    def missile_radius(self, value):
        """Do-nothing missile radius setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def missile_damage(self):
        """TkTurtle.missile_damage -> int
        Returns the damage caused by a missile explosion.

        User visibility:
            should call -- yes
            should overwrite -- no

        Missiles deal a constant amount of damage to all turtles within their
        explosive radius.
        """

        return Missile.get_damage()

    @missile_damage.setter
    def missile_damage(self, value):
        """Do-nothing missile damage setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    def _delete_missile(self, missile):
        """TkTurtle._delete_missile(missile) -> None
        Deletes a missile object from the turtle's missile list.

        User visibility:
            should call -- no
            should overwrite -- no

        Requires the following positional arguments:
            missile (Missile) -- missile object to delete from the list
        """

        # Attempt to remove the missile from the list
        try:
            self._missiles.remove(missile)
        except ValueError:
            pass

        # Delete the missile
        del missile

    #-------------------------------------------------------------------------

    def _heal(self, hp):
        """TkTurtle.heal(hp) -> None
        Adds to the Combat Turtle's health.

        User visibility:
            should call -- no
            should overwrite -- no

        Requires the following positional arguments:
            hp (int) -- amount of health to add
        """

        self._health += hp

    #-------------------------------------------------------------------------

    def _damage(self, hp):
        """TkTurtle.damage(dmg) -> None
        Reduces the Combat Turtle's health.

        User visibility:
            should call -- no
            should overwrite -- no

        Requires the following positional arguments:
            hp (int) -- amount of health to remove
        """

        self._health -= hp

    #-------------------------------------------------------------------------

    def line_of_sight(self):
        """TkTurtle.line_of_sight() -> bool
        Returns whether there is a clear line of sight to the opponent turtle.

        User visibility:
            should call -- yes
            should overwrite -- no

        Returns True if the line between the two turtles is free of obstacles
        and False otherwise.
        """

        if self._other == None:
            return None

        ### Figure out how to quickly test sight lines. A quick and dirty way
        ### would just be to sample a bunch of points along the sight line to
        ### see whether any collide with a block, but this could be expensive
        ### since it needs to be looped over every block, potentially every
        ### step. However, most arenas should include less than 8 or so
        ### blocks, and we don't really need to check the walls.
        ### Specifically, we could immediately calculate all of the points
        ### that a missile would pass through (given its speed and direction)
        ### and test whether each point collides with a block.

    #-------------------------------------------------------------------------

    @property
    def arena_left(self):
        """TkTurtle.arena_left -> int
        Returns the minimum x-coordinate of the arena boundary.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return 0

    @arena_left.setter
    def arena_left(self, value):
        """Do-nothing arena boundary setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def arena_right(self):
        """TkTurtle.arena_right -> int
        Returns the maximum x-coordinate of the arena boundary.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return int(self._canvas["width"])

    @arena_right.setter
    def arena_right(self, value):
        """Do-nothing arena boundary setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def arena_bottom(self):
        """TkTurtle.arena_bottom -> int
        Returns the minimum y-coordinate of the arena boundary.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return 0

    @arena_bottom.setter
    def arena_bottom(self, value):
        """Do-nothing arena boundary setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def arena_top(self):
        """TkTurtle.arena_top -> int
        Returns the maximum y-coordinate of the arena boundary.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        return int(self._canvas["height"])

    @arena_top.setter
    def arena_top(self, value):
        """Do-nothing arena boundary setter to prevent overwriting."""

        pass
