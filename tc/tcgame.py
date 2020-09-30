"""Defines the main game driver class."""

import turtle
import tc.tcplayer
from tc.game.arena import Arena
from tc.game.missile import Missile

class TurtleCombatGame:
    """A class to act as the main driver for a game of Turtle Combat.

    This class acts as a container for all game objects (such as the arena and
    turtles), enforces the rules of the game, and implements the automatic
    timer that governs most objects' movement.

    A step occurs every 50 ms (at a rate of 20 steps/sec). At the end of each
    step, this object calls the hidden _step() method of all moving objects.
    Moving objects are all turtle subclasses, but they move instantly during
    their step events rather than moving smoothly with the built-in turtle
    methods.
    """

    #=========================================================================

    def __init__(self, size=(600, 400), layout=0, class1=None, class2=None):
        """TurtleCombatGame([size], [layout], [p1], [p2]) -> TurtleCombatGame
        Constructor for the Turtle Combat game.

        Sets up window, game variables, step timer, and all in-game objects,
        and then begins the game.

        The turtle classes must be given as strings which give the full
        submodule path, for example "tc.ai.keyboard.CombatTurtle".

        Accepts the following optional keyword arguments:
            size (tuple (int, int)) [(600, 400)] -- arena width/height (px)
            layout (int) [0] -- arena obstacle layout ID (meanings of IDs
                defined in Arena class)
            class1 (str) [None] -- full class name of first player object
            class2 (str) [None] -- full class name of second player object
        """

        # Initialize game constants
        self.step_time = 50 # time per step (ms)

        # Define game title string
        title = "Turtle Combat: "
        if class1 != None and class2 != None:
            title += (eval(class1 + ".class_name()") + " vs. " +
                      eval(class2 + ".class_name()") + " ")
        title += "(" + Arena.get_names()[layout] + ")"

        # Set up turtle window
        self.wn = turtle.Screen()
        self.wn.screensize(size[0], size[1])
        self.wn.setup(size[0]+50, size[1]+50) # screen size with small margin
        self.wn.title(title)

        # Initialize arena
        self.arena = Arena(size=size, layout=layout, walls=5)

        # Initialize players
        self.p1 = None # first player
        self.p2 = None # second player
        if class1 != None:
            coords = Arena.get_p1_coords(layout)
            heading = Arena.get_p1_heading(layout)
            argstring = ("(col=\"red\", coords=" + str(coords) +
                         ", facing=" + str(heading) + ")")
            self.p1 = eval(class1 + argstring)
        if class2 != None:
            coords = Arena.get_p2_coords(layout)
            heading = Arena.get_p2_heading(layout)
            argstring = ("(col=\"blue\", coords=" + str(coords) +
                         ", facing=" + str(heading) + ")")
            self.p2 = eval(class2 + argstring)

        # Give players each others' pointers
        if self.p1 != None and self.p2 != None:
            self.p1._set_other(self.p2)
            self.p2._set_other(self.p1)

        # Initialize a missile list
        self.missiles = [] # list of currently-active missile objects

        # Begin game (after a delay, to allow the arena to initialize)
        self.wn.ontimer(self.play_game, 1000)
        self.wn.mainloop()

    #-------------------------------------------------------------------------

    def __del__(self):
        """~TurtleCombatGame() -> None
        Turtle Combat game destructor.

        Deletes game objects and closes window.
        """

        # Delete players
        if self.p1 != None:
            del self.p1
        if self.p2 != None:
            del self.p2

        # Delete missiles
        del self.missiles[:]

        # Delete arena
        del self.arena

        # Attempt to close window (needed in certain Python IDEs)
        try:
            turtle.bye()
        except turtle.Terminator:
            pass

    #-------------------------------------------------------------------------

    def play_game(self):
        """TurtleCombatGame.play_game() -> None
        Main gameplay loop of Turtle Combat.

        Implemented as a handler for a timer event.

        The main loop mostly consists of iteratively evaluating the step
        events of all in-game objects, creating and destroying objects as
        needed, and evaluating when the game has been won.
        """

        # Activate the step event of all game objects
        if self.p1 != None:
            self.p1.step()
        if self.p1 != None:
            self.p1.step()
        for m in self.missiles:
            m.step()

        # Check whether a player's health has reached zero
        game_over = False # whether to end the game
        if self.p1 != None:
            if self.p1.get_health() <= 0:
                game_over = True
        if self.p2 != None:
            if self.p2.get_health() <= 0:
                game_over = True

        # Either end the game or go to the next loop
        if game_over == True:
            # Game over (break loop)
            ### Determine how to display a winner.
            pass
        else:
            # Continue loop by resetting timer
            self.wn.ontimer(self.play_game, self.step_time)
