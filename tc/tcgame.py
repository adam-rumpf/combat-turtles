"""Defines the main game driver class."""

import tkinter as tk
import tc.tkturtle
from .game.arena import Arena

class TurtleCombatGame:
    """A class to act as the main driver for a game of Turtle Combat.

    This class acts as a container for all game objects (such as the arena and
    turtles), enforces the rules of the game, and implements the automatic
    timer that governs most objects' movement.

    A step occurs every 40 ms (at a rate of 25 steps/sec). At the end of each
    step, this object calls the hidden _step() method of all moving objects.
    """

    #=========================================================================

    def __init__(self, size=(800, 800), layout=0, class1=None, class2=None):
        """TurtleCombatGame([size], [layout], [p1], [p2]) -> TurtleCombatGame
        Constructor for the Turtle Combat game.

        Sets up window, game variables, step timer, and all in-game objects,
        and then begins the game.

        The turtle classes must be given as strings which give the full
        submodule path, for example "tc.ai.direct.CombatTurtle".

        Accepts the following optional keyword arguments:
            size (tuple (int, int)) [(800, 800)] -- arena width/height (px)
            layout (int) [0] -- arena obstacle layout ID (meanings of IDs
                defined in Arena class)
            class1 (str) [None] -- full class name of first player object
            class2 (str) [None] -- full class name of second player object
        """

        # Initialize game constants
        self.step_time = 40 # time per step (ms)

        # Define game title string
        title = "Turtle Combat: "
        if class1 != None and class2 != None:
            title += (eval(class1 + ".class_name()") + " vs. " +
                      eval(class2 + ".class_name()") + " ")
        title += "(" + Arena.get_names()[layout] + ")"

        # Set up Tkinter window
        self.root = tk.Tk()
        self.root.title(title)
        self.canvas = tk.Canvas(self.root, width=size[0], height=size[1],
                                relief="sunken")
        self.canvas.grid(column=1)
        self.root.update()
        ### Change this to grid to place turtle health outside arena.

        # Initialize arena
        self.arena = Arena(self, size=size, layout=layout)

        # Initialize players
        self.p1 = None # first player
        self.p2 = None # second player
        if class1 != None:
            coords = Arena.get_p1_coords(layout)
            heading = Arena.get_p1_heading(layout)
            argstring = ("(self, col=\"red\", coords=" + str(coords) +
                         ", heading=" + str(heading) + ", name=\"Player 1\")")
            self.p1 = eval(class1 + argstring)
        if class2 != None:
            coords = Arena.get_p2_coords(layout)
            heading = Arena.get_p2_heading(layout)
            argstring = ("(self, col=\"blue\", coords=" + str(coords) +
                         ", heading=" + str(heading) + ", name=\"Player 2\")")
            self.p2 = eval(class2 + argstring)

        # Give players each others' pointers
        if self.p1 != None and self.p2 != None:
            self.p1._set_other(self.p2)
            self.p2._set_other(self.p1)

        # Begin game (after a delay, to allow the arena to initialize)
        self.root.after(500, self.play_game)
        self.root.mainloop()

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

        # Delete arena
        del self.arena

    #-------------------------------------------------------------------------

    def get_step_time(self):
        """TurtleCombatGame.get_step_time() -> int
        Returns the time between game steps (ms).
        """

        return self.step_time

    #-------------------------------------------------------------------------

    def get_canvas(self):
        """TurtleCombatGame.get_canvas() -> tkinter.Canvas
        Returns the Canvas object representing the game arena.
        """

        return self.canvas

    #-------------------------------------------------------------------------

    def get_arena(self):
        """TurtleCombatGame.get_arena() -> tc.game.Arena
        Returns the game's Arena object.
        """

        return self.arena

    #-------------------------------------------------------------------------

    def get_blocks(self):
        """TurtleCombatGame.get_blocks() -> list
        Returns a list of all Block objects in the arena.
        """

        return self.arena.get_blocks()

    #-------------------------------------------------------------------------

    def intersections(self, coords):
        """TurtleCombatGame.intersections(coords) -> list
        Returns a list of block objects that intersect a given coordinate.

        Requires the following positional arguments:
            coords (tuple (int, int)) -- coordinate to test

        If the coordinate intersects no blocks, an empty list will be
        returned.
        """

        return self.arena.intersections(coords)

    #-------------------------------------------------------------------------

    ###
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
            self.p1._step()
        if self.p2 != None:
            self.p2._step()

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
            self.root.after(self.step_time, self.play_game)
