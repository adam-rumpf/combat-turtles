"""Defines a parent turtle class using Tkinter."""

import tkinter as tk
import math
from .obj.arena import Arena
from .obj.block import Block
from .obj.missile import Missile
from .util.angles import Angle

class TurtleParent:
    """Class to use as the parent of Combat Turtle classes.

    This class is meant to reproduce much of the functionality of the standard
    'turtle' class, but with less overhead due to the step-based gameplay. It
    consists mostly of placeholders for methods to be overloaded by the
    subclasses that define the different players, visible frontend methods for
    use in defining AI subclasses, and a variety of hidden utility methods.

    All attributes and methods are meant to be private. User-defined
    subclasses should not attempt to access the attributes or methods of any
    other objects. It is encouraged for user-defined subclasses to include
    their own custom attributes and methods, which the user should feel free
    to modify at will.

    Turtle movement is handled using discrete steps, which occur every 33 ms
    (at a rate of approximately 30 steps/sec). The step() method is called
    once at the end of each step, after which the turtle is moved directly to
    its new position according to its current speed and heading. The visible
    movement-related methods (such as forward(), backward(), left(), and
    right()) do not actually move the turtle, and instead update its internal
    speed and heading attributes, which are then used to perform movement at
    the end of the step.
    
    The following methods are meant to be overwritten in user-defined
    subclasses:
        class_name() -- (static method) returns the name of the class for use
            in distinguishing between different turtle AIs
        class_desc() -- (static method) returns a one-line description of the
            turtle AI
        class_shape() -- (static method) returns either an integer index or a
            radius tuple and an angle tuple to define the turtle's shape image
        setup() -- code run at the end of the turtle's initialization
        step() -- code run during each step event
    
    This class also defines a large number of public attributes and methods
    for use in subclasses, summarized below.
    
    The following read-only attributes can be used to access game constants:
        max_speed -- maximum linear speed of a turtle (px/step)
        max_turn_speed -- maximum turning speed of a turtle (deg/step)
        shoot_delay -- cooldown period (steps) between missile shots
        missile_speed -- constant linear speed of a missile (px/step)
        missile_range -- maximum range of a missile (px)
        missile_proximity -- trigger proximity of a missile (px)
        missile_radius -- explosive radius of a missile (px)
        missile_damage -- damage dealt by a missile explosion (hp)
        arena_left -- minimum x-coordinate of arena
        arena_right -- maximum x-coordinate of arena
        arena_bottom -- minimum y-coordinate of arena
        arena_top -- maximum y-coordinate of arena
    
    The following read-only attributes can be used to access the turtle's own
    status:
        x -- current x-coordinate (px)
        y -- current y-coordinate (px)
        position -- current coordinate tuple (px, px)
        heading -- current heading (deg) normalized to (-180,180]
        speed -- current linear speed (px/step)
        turn_speed -- current turning speed (deg/step)
        health -- current remaining health (hp)
        cooldown -- current cooldown before another missile can be fired
            (steps)
        can_shoot -- whether or not the turtle is currently able to shoot
        time -- number of steps that have passed since the game began
    
    The following read-only attributes can be used to access the opponent
    turtle's status (as of the end of the previous step, except for the
    cooldown count, which is current):
        other_x -- opponent's previous x-coordinate (px)
        other_y -- opponent's previous y-coordinate (px)
        other_position -- opponent's previous coordinate tuple (px, px)
        other_heading -- opponent's previous heading (deg) normalized to
            (-180,180]
        other_speed -- opponent's previous linear speed (px/step)
        other_turn_speed -- opponent's previous turning speed (deg/step)
        other_health -- opponent's previous health (hp)
        other_cooldown -- opponent's current cooldown length (steps)
        other_can_shoot -- whether the opponent can currently shoot
    
    The following methods should be used to instruct the turtle to take
    actions:
        forward([rate]) -- moves forward in current direction at a given
            fraction of its maximum speed (aliases: forward, fd)
        backward([rate]) -- moves backward in current direction at a given
            fraction of its maximum speed (aliases: backward, back, bk)
        left([rate]) -- turns counterclockwise at a given fraction of its
            maximum turning speed (aliases: left, lt)
        right([rate]) -- turns clockwise at a given fraction of its maximum
            turning speed (aliases: right, rt)
        turn_towards([args]) -- turns as far as possible towards a given
            target, either at maximum turning speed or exactly enough to face
            the target exactly (aliases: turn_towards, turn_towards, turnto)
        shoot() -- fire missile in current direction and set cooldown to
            prevent shooting again for a set number of steps (aliases: shoot,
            fire)
    
    The following methods should be used to gather information about the
    current state of the game:
        distance([args]) -- returns distance between a given pair of
            coordinates (px) (aliases: distance, dist)
        relative_position([target]) -- returns the relative position of a
            target relative to this turtle (px, px) (aliases:
            relative_position, relpos)
        heading_towards([target]) -- returns the heading from this turtle to
            a target (deg) (aliases: heading_towards, heading_toward, towards,
            toward)
        relative_heading_towards([target]) -- returns the smallest heading
            change required to turn this turtle towards a target (deg)
            (aliases: relative_heading_twards, relative_heading_toward)
        free_space(coord) -- returns whether a given coordinate is free of
            obstacles (aliases: free_space, free)
        line_of_sight([target]) -- returns whether there is a direct line of
            sight between this turtle and a target (aliases: line_of_sight,
            los)
    """
    
    #=========================================================================
    # Static methods
    #=========================================================================

    def class_name():
        """TurtleParent.class_name() -> str
        Static method to return the name of the Combat Turtle AI.
        """

        return "TurtleParent"

    #-------------------------------------------------------------------------

    def class_desc():
        """TurtleParent.class_desc() -> str
        Static method to return a description of the Combat Turtle AI.
        """

        return "Parent class of all Combat Turtle classes."

    #-------------------------------------------------------------------------

    def class_shape():
        """TurtleParent.class_shape() -> (int or tuple)
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
    # Special methods
    #=========================================================================

    def __init__(self, game, name=class_name(), col="black",
                 coords=(0, 0), heading=0):
        """TurtleParent(game, [name], [col], [coords], [facing]) ->
        TurtleParent
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
            (self._shape_radius, self._shape_angle) = self._shape(cs)
        elif type(cs) == tuple and len(cs) == 2:
            # Custom coordinates
            (self._shape_radius, self._shape_angle) = cs
        else:
            # Default to arrowhead
            (self._shape_radius, self._shape_angle) = self._shape(0)

        # Define variable attributes
        self._other = None # opponent turtle object
        self._speed = 0 # target movement speed (px/step, negative for back)
        self._speed_turn = 0 # target CCW turn speed (deg/step, < 0 for CW)
        self._health = 100 # health points (turtle dies when health is zero)
        self._cooldown = 0 # delay until able to shoot next (steps)
        self._shooting = False # whether the turtle is attempting to shoot
        self._time = 0 # current step number

        # Draw self
        self._redraw()

        # Initialize list of currently-active missiles shot by this turtle
        self._missiles = []

    #-------------------------------------------------------------------------

    def __str__(self):
        """TurtleParent.__str__() -> str
        String conversion returns the Combat Turtle's name.

        User visibility:
            should call -- no
            should overwrite -- no
        """

        return self._name

    #-------------------------------------------------------------------------

    def __del__(self):
        """~TurtleParent.() -> None
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
    
    #=========================================================================
    # Game constant attributes
    #=========================================================================
    
    @property
    def max_speed(self):
        """TurtleParent.max_speed -> int
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
        """TurtleParent.max_turn_speed -> int
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
    def shoot_delay(self):
        """TurtleParent.shoot_delay -> int
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
    def missile_speed(self):
        """TurtleParent.missile_speed -> int
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
        """TurtleParent.missile_range -> int
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
        """TurtleParent.missile_proximity -> int
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
        """TurtleParent.missile_radius -> int
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
        """TurtleParent.missile_damage -> int
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

    @property
    def arena_left(self):
        """TurtleParent.arena_left -> int
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
        """TurtleParent.arena_right -> int
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
        """TurtleParent.arena_bottom -> int
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
        """TurtleParent.arena_top -> int
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
    
    #=========================================================================
    # Turtle attributes
    #=========================================================================
    
    @property
    def x(self):
        """TurtleParent.x -> int
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
        """TurtleParent.y -> int
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
        """TurtleParent.position -> tuple
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
    def heading(self):
        """TurtleParent.heading -> int
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

    @property
    def speed(self):
        """TurtleParent.speed -> int
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

    @property
    def turn_speed(self):
        """TurtleParent.turn_speed -> int
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

    @property
    def cooldown(self):
        """TurtleParent.cooldown -> int
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
        """TurtleParent.can_shoot -> bool
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

    @property
    def health(self):
        """TurtleParent.health -> int
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
    def time(self):
        """TurtleParent.time -> int
        Keeps track of the step number of the current game.

        User visibility:
            should call -- yes
            should overwrite -- no
        
        The time attribute is initialized as 0 when the game begins and
        increments by 1 at the end of each step.
        """

        return self._time

    @time.setter
    def time(self, value):
        """Do-nothing time setter to prevent overwriting."""

        pass
    
    #=========================================================================
    # Opponent attributes
    #=========================================================================
    
    @property
    def other_x(self):
        """TurtleParent.other_x -> int
        Returns the current x-coordinate (px) of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if self._other == None:
            return None

        return self._other_prev_position[0]

    @other_x.setter
    def other_x(self, value):
        """Do-nothing position setter to prevent overwriting."""

        pass
    
    #-------------------------------------------------------------------------

    @property
    def other_y(self):
        """TurtleParent.other_y -> int
        Returns the current y-coordinate (px) of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if self._other == None:
            return None

        return self._other_prev_position[1]

    @other_y.setter
    def other_y(self, value):
        """Do-nothing position setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def other_position(self):
        """TurtleParent.other_position -> tuple
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

    @property
    def other_heading(self):
        """TurtleParent.other_heading -> int
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

    @property
    def other_speed(self):
        """TurtleParent.other_speed -> int
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
        """TurtleParent.other_turn_speed -> int
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
    def other_health(self):
        """TurtleParent.other_health -> int
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
    def other_cooldown(self):
        """TurtleParent.other_cooldown -> int
        Returns the (current) cooldown of the opponent Combat Turtle.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if self._other == None:
            return None

        return self._other_cooldown

    @other_cooldown.setter
    def other_cooldown(self, value):
        """Do-nothing other cooldown setter to prevent overwriting."""

        pass
    
    #-------------------------------------------------------------------------

    @property
    def other_can_shoot(self):
        """TurtleParent.other_can_shoot -> int
        Returns whether the opponent Combat Turtle can currently shoot.

        User visibility:
            should call -- yes
            should overwrite -- no
        """

        if self._other == None:
            return None

        return self.other_cooldown <= 0

    @other_can_shoot.setter
    def other_can_shoot(self, value):
        """Do-nothing other shoot status setter to prevent overwriting."""

        pass
    
    #=========================================================================
    # Placeholder methods (for overwriting in subclasses)
    #=========================================================================
    
    def setup(self):
        """TurtleParent.setup() -> None
        Placeholder for Combat Turtle setup procedures.

        User visibility:
            should call -- no
            should overwrite -- yes

        This method is meant to be overwritten in the submodules of
        TurtleParent. It is called at the end of the constructor. Its purpose
        is to prevent the user from having to overload the constructor in
        their own submodule, in which case they would need to replicate its
        argument list and attribute definitions.
        
        Note that, for technical reasons, this is actually called by the main
        game driver before the first step event rather than being called
        within this object's __init__ method.
        """

        pass

    #-------------------------------------------------------------------------

    def step(self):
        """TurtleParent.step() -> None
        The main step event of the Combat Turtle.

        User visibility:
            should call -- no
            should overwrite -- yes

        This method is meant to be overwritten in the submodules of
        TurtleParent. It is called each step (every 33 ms), after which any
        movement and firing events are actually executed.
        """

        pass
    
    #=========================================================================
    # Initialization methods
    #=========================================================================
    
    def _set_other(self, other):
        """TurtleParent._set_other(other) -> None
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
    
    def _shape(self, index):
        """TurtleParent._shape(index) -> tuple
        Returns the polar coordinates of the turtle's shape polygon.

        User visibility:
            should call -- no
            should overwrite -- no

        Requires the following positional arguments:
            index -- integer index of shape profile

        User-defined Combat Turtles can define their own sets of coordinates
        for drawing the turtle's shape. This function returns one of the
        preset shapes based on an integer index.
        """

        # Output coordinates based on integer index
        if index == 1:
            # Turtle
            radius = (18, 16, 10, 10, 14, 16, 14, 10, 10, 14, 16, 14, 10, 12,
                      18, 12, 10, 14, 16, 14, 10, 10, 14, 16, 14, 10, 10, 16)
            angle = (0, math.pi/12, math.pi/10, 11*math.pi/42, 13*math.pi/48,
                     math.pi/3, 19*math.pi/48, 17*math.pi/42, 73*math.pi/105,
                     169*math.pi/240, 23*math.pi/30, 199*math.pi/240,
                     88*math.pi/105, 29*math.pi/30, math.pi, -29*math.pi/30,
                     -88*math.pi/105, -199*math.pi/240, -23*math.pi/30,
                     -169*math.pi/240, -73*math.pi/105, -17*math.pi/42,
                     -19*math.pi/48, -math.pi/3, -13*math.pi/48,
                     -11*math.pi/42, -math.pi/10, -math.pi/12)
        elif index == 2:
            # Plow
            r1 = 14
            r2 = 8
            radius = (2*r1/3, r2, math.sqrt(r1**2 + r2**2),
                      math.sqrt(r1**2 + r2**2), r2)
            angle = (0, math.pi/2, math.atan2(r2, -r1), math.atan2(-r2, -r1),
                     -math.pi/2)
        elif index == 3:
            # Triangle
            r1 = 16
            r2 = 12
            radius = (r1, r2, r2)
            angle = (0, 2*math.pi/3, -2*math.pi/3)
        elif index == 4:
            # Kite
            r1 = 16
            r2 = 12
            radius = (r1, r2, 3*r1/4, r2)
            angle = (0, 2*math.pi/3, math.pi, 4*math.pi/3)
        elif index == 5:
            # Pentagon
            r1 = 16
            r2 = 10
            radius = (r1, r2, r2, r2, r2)
            angle = (0, 2*math.pi/5, 4*math.pi/5, 6*math.pi/5, 8*math.pi/5)
        elif index == 6:
            # Hexagon
            r1 = 16
            r2 = 14
            radius = (r1, r2, r2, r1, r2, r2)
            angle = (0, math.pi/5, 2*math.pi/3, math.pi, 4*math.pi/3,
                     9*math.pi/5)
        elif index == 7:
            # Star
            r1 = 16
            r2 = 8
            t = math.pi/5
            radius = (r1, r2, 3*r1/4, 3*r2/4, 3*r1/4, r2/2, 3*r1/4, 3*r2/4,
                      3*r1/4, r2)
            angle = (0, t, 2*t, 3*t, 4*t, 5*t, 6*t, 7*t, 8*t, 9*t)
        else:
            # Default to arrowhead
            r1 = 16
            r2 = 10
            radius = (r1, 2*r2/math.sqrt(3), 0, 2*r2/math.sqrt(3))
            angle = (0, 2*math.pi/3, math.pi, 4*math.pi/3)

        return (radius, angle)
    
    #=========================================================================
    # Drawing methods
    #=========================================================================

    def _poly(self):
        """TurtleParent._poly() -> list
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
            coords[2*i+1] = int(self._y - (self._shape_radius[i]*
                                math.sin(self._shape_angle[i]+angle)))
        coords[-2] = coords[0]
        coords[-1] = coords[1]

        return coords
    
    #-------------------------------------------------------------------------

    def _redraw(self):
        """TurtleParent._redraw() -> None
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
    
    #=========================================================================
    # Hidden step event methods
    #=========================================================================
    
    def _step(self):
        """TurtleParent._step() -> None
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

        # Attempt to shoot
        self._shoot()

        # Update sprite
        self._redraw()
        
        # Increment timer
        self._time += 1
    
    #-------------------------------------------------------------------------
    
    def _get_other_attributes(self):
        """TurtleParent._get_other_attributes() -> None
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
        self._other_cooldown = max(0, self._other.cooldown - 1)
    
    #=========================================================================
    # Linear movement methods
    #=========================================================================
    
    def forward(self, rate=1):
        """TurtleParent.forward([rate]) -> None
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
        """TurtleParent.backward([rate]) -> None
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

    def _move(self):
        """TurtleParent._move() -> None
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
        self._y -= int(self.speed*math.sin(math.radians(self.heading)))
        
        # Bound coordinates to arena size
        self._x = min(self.arena_right, max(self.arena_left, self._x))
        self._y = min(self.arena_top, max(self.arena_bottom, self._y))

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
    
    #=========================================================================
    # Turning methods
    #=========================================================================
    
    def left(self, rate=1):
        """TurtleParent.left([angle]) -> None
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
        """TurtleParent.right([angle]) -> None
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

    def turn_towards(self, target=None):
        """TurtleParent.turn_towards([target]) -> None
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

        # If no target, use opponent turtle's position
        if target == None:
            target = self.other_position

        # If given a specific heading, generate a coordinate to turn towards
        if type(target) == int or type(target) == float:
            target = (int(self.x + 10000*math.cos(math.radians(target))),
                      int(self.y - 10000*math.sin(math.radians(target))))

        # Turn towards coordinates
        if type(target) == tuple:
            # Find relative heading to target
            turn = self.relative_heading_towards(target)
            turn = min(max(turn, -self.max_turn_speed), self.max_turn_speed)
            turn /= self.max_turn_speed

            # Turn in the needed direction
            self.left(turn)
    
    # Set aliases
    turn_toward = turn_towards
    turnto = turn_towards
    
    #-------------------------------------------------------------------------

    def _turn(self):
        """TurtleParent._turn() -> None
        Turns a turtle according to its speed_turn attribute.

        User visibility:
            should call -- no
            should overwrite -- no

        This is a hidden method called during the step event to handle any
        turning speed changes that the submodule has enacted using the visible
        left() and right() methods (or their aliases).
        """

        # Change heading
        self._heading += int(self._speed_turn)
    
    #=========================================================================
    # Missile methods
    #=========================================================================
    
    def shoot(self):
        """TurtleParent.shoot() -> None
        Tells a turtle to shoot a missile.

        User visibility:
            should call -- yes
            should overwrite -- no

        Attempts to shoot a missile in the turtle's current direction. If the
        turtle is still on cooldown from the previous shot, this does nothing.
        """

        # Set shooting status
        self._shooting = True
    
    # Set aliases
    fire = shoot
    
    #-------------------------------------------------------------------------

    def _shoot(self):
        """TurtleParent._shoot() -> None
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

    def _delete_missile(self, missile):
        """TurtleParent._delete_missile(missile) -> None
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
    
    #=========================================================================
    # Health methods
    #=========================================================================
    
    def _heal(self, hp):
        """TurtleParent.heal(hp) -> None
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
        """TurtleParent.damage(dmg) -> None
        Reduces the Combat Turtle's health.

        User visibility:
            should call -- no
            should overwrite -- no

        Requires the following positional arguments:
            hp (int) -- amount of health to remove
        """

        self._health -= hp
    
    #=========================================================================
    # Query methods
    #=========================================================================
    
    def distance(self, *args):
        """TurtleParent.distance([coords1[, coords2]]) -> float
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
    
    # Set aliases
    dist = distance

    #-------------------------------------------------------------------------

    def relative_position(self, target=None):
        """TurtleParent.relative_position -> tuple
        Returns position of a target coordinate relative to self.

        User visibility:
            should call -- yes
            should overwrite -- no

        This method can be called in several different formats depending on
        whether a target is specified:
            None -- returns relative position of opponent turtle
            tuple (int, int) -- returns relative position of the given
                coordinate

        The coordinates returned by this method represent the movement
        required to get from this Combat Turtle's position to the specified
        target position.
        """

        # If no target, use opponent turtle's position
        if target == None:
            target = self.other_position

        # Return difference
        return (target[0] - self.x, target[1] - self.y)
    
    # Set aliases
    relpos = relative_position
    
    #-------------------------------------------------------------------------

    def heading_towards(self, target=None):
        """TurtleParent.heading_towards([target]) -> int
        Returns the heading (deg) towards a target coordinate.

        User visibility:
            should call -- yes
            should overwrite -- no

        This method can be called in several different formats depending on
        whether a target is specified:
            None -- returns relative heading towards opponent turtle
            tuple (int, int) -- returns relative heading towards the given
                coordinate

        The returned heading is a value between -180 degrees and 180 degrees,
        representing the direction of travel from this Combat Turtle's
        position to the specified target (with 0 degrees meaning due east).
        This is based entirely on the coordinates of this Combat Turtle and
        the target, and has nothing to do with this Turtle's current heading.

        To find the change in heading required for this Combat Turtle to turn
        towards the target based on its current direction, use
        relative_heading_towards().
        """

        # If no target, use opponent turtle's position
        if target == None:
            target = self.other_position

        # Get position relative to target
        (dx, dy) = self.relative_position(target)

        # Calculate relative heading using arctan (Angle class mods result)
        return int(math.degrees(Angle(math.atan2(-dy, dx))))
    
    # Set aliases
    heading_toward = heading_towards
    towards = heading_towards
    toward = heading_towards

    #-------------------------------------------------------------------------

    def relative_heading_towards(self, target=None):
        """TurtleParent.relative_heading_towards([target]) -> int
        Returns the change in heading (deg) needed to turn towards a target.

        User visibility:
            should call -- yes
            should overwrite -- no

        This method can be called in several different formats depending on
        whether a target is specified:
            None -- returns relative heading towards opponent turtle
            tuple (int, int) -- returns relative heading towards the given
                coordinate

        The returned heading is a value between -180 degrees and 180 degrees,
        representing the smallest change in heading required for this Combat
        Turtle to turn towards the given target coordinate (positive for
        counterclockwise, negative for clockwise).

        To simply find the direction from this Combat Turtle to the target
        (without regard for this Turtle's current direction), use
        relative_heading().
        """

        # Calculate absolute heading towards target
        ah = Angle(self.heading_towards(target), "degrees")

        # Return difference in headings
        return int(ah - self.heading)
    
    # Set aliases
    relative_heading_toward = relative_heading_towards
    
    #-------------------------------------------------------------------------
    
    def free_space(self, coord):
        """TurtleParent.free_space(coord) -> bool
        Determines whether a given coordinate is free of obstacles.
        
        User visibility:
            should call -- yes
            should overwrite -- no
        
        Requires the following positional arguments:
            coord (tuple (int, int)) -- position coordinates (px, px)
        
        Returns True if the given coordinate is within the arena and does not
        intersect with a Block object, and False otherwise.
        """
        
        # Verify that the coordinates are within bounds
        if (coord[0] < self.arena_left or coord[0] > self.arena_right or
            coord[1] < self.arena_bottom or coord[1] > self.arena_top):
            return False
        
        # Check whether the destination intersects any blocks
        if self._game.blocked(coord) == True:
            return False
        
        # If we made it past both tests, then the position must be free
        return True
    
    # Set aliases
    free = free_space
    
    #-------------------------------------------------------------------------

    def line_of_sight(self, target=None):
        """TurtleParent.line_of_sight([target]) -> bool
        Returns whether there is a clear line of sight to a target.

        User visibility:
            should call -- yes
            should overwrite -- no
        
        This method can be called in several different formats depending on
        whether a target is specified:
            None -- target becomes opponent turtle's coordinates
            tuple (int, int) -- line of sight to specified coordinate

        Returns True if the line between this turtle and the target coordinate
        is free of obstacles and False otherwise. In particular, "free of
        obstacles" means that, if this turtle were to fire a missile while
        facing the target coordinate, the missile would reach the target
        before colliding with any blocks.
        """

        # If no target, use opponent turtle's position
        if target == None:
            target = self.other_position
        
        # Get heading towards target
        rh = math.radians(self.heading_towards(target))
        
        # Get initial signs of x- and y-direction differences
        sx = self._sign(target[0] - self.x) # x-direction sign
        sy = self._sign(target[1] - self.y) # y-direction sign
        
        # Handle the trivial case of the turtle's own coordinate
        if sx == 0 and sy == 0:
            return True
        
        # Test sample points on path to target
        pt = list(self.position) # sample point
        spd = self.missile_speed # move sample point at missile speed
        iter = 0 # number of samples tested (for iteration cutoff)
        while True:
            # Loop repeats until either reaching an iteration cutoff, finding
            # a block collision, or moving past the target coordinate
            
            # Move sample point
            pt[0] += spd*math.cos(rh)
            pt[1] -= spd*math.sin(rh)
            
            # If the point collides with a block, there is no clear path
            if self.free_space(pt) == False:
                return False
            
            # If the point has moved past the target, there must be clear path
            if (self._sign(target[0] - pt[0]) != sx or
                self._sign(target[1] - pt[1]) != sy):
                return True
            
            # If past iteration cutoff, return False
            iter += 1
            if iter >= 100:
                return False
    
    # Set aliases
    los = line_of_sight
    
    #-------------------------------------------------------------------------
    
    def _sign(self, num):
        """TurtleParent._sign(num) -> int
        Returns the sign of a number.
        
        User visibility:
            should call -- no
            should overwrite -- no
        
        The sign of a number is 1 for positive, -1 for negative, and 0 for
        zero.
        """
        
        if num > 0:
            return 1
        elif num < 0:
            return -1
        else:
            return 0
