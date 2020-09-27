import turtle

class Missile(turtle.Turtle):
    """Missile class.

    Missiles are fired by Combat Turtles. They travel at a fixed speed until
    either colliding with a solid object or player, or until a fixed amount of
    time has passed, and then explode with a fixed radius, dealing damage to
    all nearby turtles.
    """

    # Static methods declare class constants to be accessed by other classes

    #-------------------------------------------------------------------------

    def get_speed():
        """Missile.get_speed() -> float
        Returns missile travel speed (px/step).

        Missiles travel at a constant speed in the direction of their initial
        heading.
        """

        return 10.0

    #-------------------------------------------------------------------------

    def get_lifespan():
        """Missile.get_lifespan() -> int
        Returns missile lifespan (steps).

        If a missile has not collided with anything, it automatically explodes
        after this number of steps.
        """

        return 50

    #-------------------------------------------------------------------------

    def get_proximity():
        """Missile.get_proximity() -> float
        Returns missile proximity distance (px).

        Missiles explode when they get within this distance of an opponent
        Combat Turtle.
        """

        return 5.0

    #-------------------------------------------------------------------------

    def get_radius():
        """Missile.get_radius() -> float
        Returns missile explosive radius.

        When a missile explodes, any turtle within this radius is damaged
        (including the missile's shooter).
        """

        return 20.0

    #=========================================================================

    def __init__(self, shooter, angle, trail=True):
        """Missile(shooter, angle[, trail]) -> Missile
        Missile constructor.

        Requires the following positional arguments:
            shooter (CombatTurtle) -- turtle object that fired the missile (to
                prevent exploding from collision with owner)
            angle (float) -- direction in which missile was fired

        Accepts the following optional keyword argument:
            trail (bool) [True] -- whether or not to draw a trail for the
                missile's path
        """

        # Initialize turtle
        super().__init__()

        ### Set appearance and colors, and handle trail option.
        ### If needed, delete drawings on death.

        # Set turtle class attributes
        self.speed(0) # movement handled in steps
        self.shape("arrow") # turtle shape

        # Assign given attributes
        self.shooter = shooter
        self.angle = angle

        # Assign constant attributes
        self.spd = Missile.get_speed() # constant travel speed (px/step)
        self.step_time = 50 # time between steps (ms)
        self.lifespan = Missile.get_lifespan() # time until explosion (steps)
        self.proximity = Missile.get_proximity() # missile explodes when
            # within this distance (px) of a turtle (except for the shooter)
        self.radius = Missile.get_lifespan() # radius of explosion (px)
