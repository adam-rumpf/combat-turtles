"""Defines the missile class."""

import math
import tkinter as tk

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

        return 40

    #-------------------------------------------------------------------------

    def get_proximity():
        """Missile.get_proximity() -> int
        Returns missile proximity distance (px).

        Missiles explode when they get within this distance of an opponent
        Combat Turtle.
        """

        return 20

    #-------------------------------------------------------------------------

    def get_radius():
        """Missile.get_radius() -> int
        Returns missile explosive radius.

        When a missile explodes, any turtle within this radius is damaged
        (including the missile's shooter).
        """

        return 20

    #-------------------------------------------------------------------------

    def get_damage():
        """Missile.get_damage() -> int
        Returns missile damage.

        Missiles deal a constant amount of damage to any turtle within their
        explosive radius.
        """

        return 20

    #=========================================================================

    def __init__(self, game, shooter, target, coords, heading):
        """Missile(game, target, heading) -> Missile
        Missile constructor.

        Requires the following positional arguments:
            game (tcgame.TurtleCombatGame) -- game driver object
            shooter (tkturtle.CombatTurtle) -- combat turtle that shot this
                missile (missile maintained in its shooter's list)
            target (tkturtle.CombatTurtle) -- combat turtle to treat as the
                target (missile explodes when close enough to target)
            coords (tuple (int, int)) -- initial coordinates of missile
            heading (int) -- constant heading for missile
        """

        # Assign given attributes
        self.game = game
        self.canvas = game.canvas # canvas to draw self on
        self.shooter = shooter
        self.target = target
        self.x = coords[0]
        self.y = coords[1]
        self.heading = heading

        # Assign constant attributes
        self.sprite_radius = 4 # radius of circular missile sprite
        self.speed = Missile.get_speed() # constant travel speed (px/step)
        self.proximity = Missile.get_proximity() # missile explodes when
            # within this distance (px) of the target turtle
        self.radius = Missile.get_lifespan() # radius of explosion (px)
        self.damage = Missile.get_damage() # damage on hit
        self.exploding_frames = 4 # number of steps for explosion animation

        # Initialize countdown timer
        self.countdown = Missile.get_lifespan() # time until explosion (steps)
        self.exploding = 0 # time since explosion began (steps)
        
        # Initialize list of points to define smoke trail line
        self.path = [self.x, self.y]

        # Draw self
        self._redraw()

    #-------------------------------------------------------------------------

    def __del__(self):
        """~Missile.__del__() -> None
        Missile destructor deletes drawing on canvas.
        """

        # Delete sprite (if it has been defined)
        try:
            self.canvas.delete(self.sprite)
        except AttributeError:
            pass
        except tk.TclError:
            pass
        
        # Delete smoke trail (if it has been defined)
        try:
            self.canvas.delete(self.trail)
        except AttributeError:
            pass
        except tk.TclError:
            pass

    #-------------------------------------------------------------------------

    def _step(self):
        """Missile._step() -> None
        The step event of missile objects.

        This method is called during each step event of the game. This handles
        the missile's movement, collision detection, and expiration.
        """

        # Decrement timer
        self.countdown -= 1

        # Determine behavior depending on explosion status
        if self.exploding <= 0:

            # If not already exploding, move and test for collisions/timers

            # Move forward
            self.x += self.speed*math.cos(math.radians(self.heading))
            self.y -= self.speed*math.sin(math.radians(self.heading))
            
            # Add point to smoke trail
            self.path += [self.x, self.y]

            # Determine whether to explode
            explode = False

            # If timer has expired, explode
            if self.countdown == 0:
                explode = True

            # Test for wall collisions
            elif (self.x < 0 or self.x > int(self.game.canvas["width"]) or
                  self.y < 0 or self.y > int(self.game.canvas["height"])):
                explode = True

            # Test for proximity to target turtle
            elif self.target.distance((self.x, self.y)) < self.proximity:
                explode = True

            # Test for block collisions
            elif len(self.game.intersections((self.x, self.y))) > 0:
                explode = True

            # If any explosion trigger is activated, explode
            if explode == True:
                self._explode()

        else:
            # If already exploding, increment counter
            self.exploding += 1

        # Delete self after explosion animation is complete
        if self.exploding >= self.exploding_frames:
            self._remove()

        # Update sprite
        self._redraw()

    #-------------------------------------------------------------------------

    def _redraw(self):
        """Missile.redraw() -> None
        Redraws sprite on canvas to update appearance after moving.

        User visibility:
            should call -- no
            should overwrite -- no

        This method is called at the end of each step to update the missile's
        appearance on the screen.
        """

        # Delete sprite (if it has been defined)
        try:
            self.canvas.delete(self.sprite)
        except AttributeError:
            pass
        except tk.TclError:
            pass
        
        # Delete smoke trail (if it has been defined)
        try:
            self.canvas.delete(self.trail)
        except AttributeError:
            pass
        except tk.TclError:
            pass
        
        # Draw smoke trail
        if len(self.path) >= 4:
            self.trail = self.canvas.create_line(self.path, width=2,
                                                 dash=(1,2),
                                                 fill="light gray")

        # Draw sprite depending on whether the missile has exploded
        if self.exploding <= 0:
            # During travel, draw self as a gray circle
            self.sprite = self.canvas.create_oval(self.x-self.sprite_radius,
                                                  self.y-self.sprite_radius,
                                                  self.x+self.sprite_radius,
                                                  self.y+self.sprite_radius,
                                                  fill="gray", outline="gray")
        else:
            # During explosion, draw a growing explosive radius
            r = int((self.exploding/self.exploding_frames)*self.radius)
            self.sprite = self.canvas.create_oval(self.x-r, self.y-r,
                                                  self.x+r, self.y+r,
                                                  fill="yellow",
                                                  outline="red")

    #-------------------------------------------------------------------------

    def _explode(self):
        """Missile._explode() -> None
        Causes an explosion at the missile's location.

        Missiles explode on contact with the enemy turtle or an obstacle, or
        when their timer expires.

        The explosion affects all turtles within a set radius of the missile,
        after which the missile object is deleted from its shooter's missile
        list.
        """

        # Damage shooter if close enough
        if self.shooter.distance((self.x, self.y)) < self.radius:
            self.shooter._damage(self.damage)

        # Damage target if close
        if self.target.distance((self.x, self.y)) < self.radius:
            self.target._damage(self.damage)

        # Increment exploding timer
        self.exploding += 1

    #-------------------------------------------------------------------------

    def _remove(self):
        """Missile._remove() -> None
        Removes a missile after its explosion animation has completed.

        The actual deletion of this object is handled by the combat turtle
        that shot the missile, which maintains a list of all currently-active
        missiles it has shot. This method prompts the turtle to remove the
        missile from its list and delete the object.
        """

        # Notify shooter to delete this missile
        self.shooter._delete_missile(self)
