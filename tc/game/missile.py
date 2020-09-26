import turtle
from .. import CombatTurtle

class _Missile(turtle.Turtle):
    """Missile class.

    Missile are fired by Combat Turtles. They travel at a fixed speed until
    either colliding with a solid object or player, or until a fixed amount of
    time has passed, and then explode with a fixed radius, dealing damage to
    all nearby players.
    """

    #-------------------------------------------------------------------------

    def __init__(self, shooter, angle):
        """_Missile(shooter, angle) -> _Missile
        Missile constructor.

        Requires the following positional arguments:
            shooter (CombatTurtle) -- turtle object that fired the missile (to
                prevent exploding from collision with owner)
            angle (float) -- direction in which missile was fired
        """

        # Initialize turtle
        super().__init__()

        # Assign given attributes
        self.shooter = shooter
        self.angle = angle

        # Assign constant attributes
        self.speed = 10.0 # constant travel speed (px/step)
        self.step_time = 50 # time between steps (ms)
        self.lifespan = 50 # time until explosion (steps)
        self.proximity = 5.0 # missile explodes when within this distance (px)
                             # of a turtle (except for the shooter)
        self.radius = 20.0 # radius of explosion (px)
