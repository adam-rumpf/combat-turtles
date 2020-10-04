"""Defines the missile class."""

### Need to add more methods to work from scratch.
### For simplicity, just make missiles a circle.

class Missile:
    """Missile class.

    Missiles are fired by Combat Turtles. They travel at a fixed speed until
    either colliding with a solid object or player, or until a fixed amount of
    time has passed, and then explode with a fixed radius, dealing damage to
    all nearby turtles.

    Each Combat Turtle maintains a list of all currently-active missiles it
    has fired. The missile's step() method is called during its owner's
    _step() method. Its owner also handles the deletion of the missile object
    after it explodes.
    """

    # Static methods declare class constants to be accessed by other classes

    #-------------------------------------------------------------------------

    def get_speed():
        """Missile.get_speed() -> int
        Returns missile travel speed (px/step).

        Missiles travel at a constant speed in the direction of their initial
        heading.
        """

        return 10

    #-------------------------------------------------------------------------

    def get_lifespan():
        """Missile.get_lifespan() -> int
        Returns missile lifespan (steps).

        If a missile has not collided with anything, it automatically explodes
        after this number of steps.
        """

        return 25

    #-------------------------------------------------------------------------

    def get_proximity():
        """Missile.get_proximity() -> int
        Returns missile proximity distance (px).

        Missiles explode when they get within this distance of an opponent
        Combat Turtle.
        """

        return 5

    #-------------------------------------------------------------------------

    def get_radius():
        """Missile.get_radius() -> int
        Returns missile explosive radius.

        When a missile explodes, any turtle within this radius is damaged
        (including the missile's shooter).
        """

        return 20

    #=========================================================================

    def __init__(self, shooter, angle):
        """Missile(shooter, angle) -> Missile
        Missile constructor.

        Requires the following positional arguments:
            shooter (CombatTurtle) -- turtle object that fired the missile
            angle (int) -- direction in which missile was fired
        """

        ### Set appearance and colors, and handle trail option.
        ### If needed, delete drawings on death.

        # Set turtle class attributes
        self.hideturtle() # hide before moving into position
        self.speed(0) # movement handled in steps
        self.shape("arrow")
        self.resizemode("user")
        self.shapesize(0.5, 0.5)
        self.color("gray")
        self.penup()
        self.goto(shooter.get_position()) # go to parent turtle's position
        self.setheading(angle)
        if trail:
            self.pendown()
        self.showturtle()

        # Define associated shooter Combat Turtle
        self.shooter = shooter

        # Assign constant attributes
        self.spd = Missile.get_speed() # constant travel speed (px/step)
        self.step_time = 40 # time between steps (ms)
        self.proximity = Missile.get_proximity() # missile explodes when
            # within this distance (px) of a turtle (except for the shooter)
        self.radius = Missile.get_lifespan() # radius of explosion (px)

        # Initialize countdown timer
        self.countdown = Missile.get_lifespan() # time until explosion (steps)

    #-------------------------------------------------------------------------

    def step(self):
        """Missile.step() -> None
        The step event of missile objects.

        This method is called during each step event of the game. This handles
        the missile's movement, collision detection, and expiration.
        """

        # Decrement timer
        self.countdown -= 1

        # If timer has expired, explode
        if self.countdown <= 0:
            self._explode()

        # Move forward
        self.forward(self.spd)

        # Test for block collisions
        ###

        # Test for proximity to opponent turtle
        ###

    #-------------------------------------------------------------------------

    def _explode(self):
        """Missile._explode() -> None
        Causes an explosion at the missile's location.

        Missiles explode on contact with the enemy turtle or an obstacle, or
        when their timer expires.

        The explosion affects all turtles within a set radius of the missile,
        after which the missile object is deleted.
        """

        ###

        # Notify shooter to delete this missile
        self._notify()

    #-------------------------------------------------------------------------

    def _notify(self):
        """Missile.notify() -> None
        Notifies the missile's Combat Turtle to delete the missile object.

        Each Combat Turtle should maintain a list of all currently-active
        missiles it has fired. This method is called when the missile
        explodes, and notifies its parent Combat Turtle to delete it from the
        list, as well as to delete the object.
        """

        pass
