"""Defines the main game driver class."""

import tkinter as tk
import tc.tkturtle
from .game.arena import Arena

class TurtleCombatGame:
    """A class to act as the main driver for a game of Turtle Combat.

    This class acts as a container for all game objects (such as the arena and
    turtles), enforces the rules of the game, and implements the automatic
    timer that governs most objects' movement.

    A step occurs every 33 ms (at a rate of approximately 30 steps/sec). At
    the end of each step, this object calls the hidden _step() method of all
    moving objects.
    """

    #=========================================================================

    def __init__(self, size=(800, 800), layout=0, class1=None, class2=None,
                 cutoff=-1):
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
            cutoff (int) [-1] -- game time cutoff (negative for no limit)
        """

        # Initialize game constants
        self.size = size # arena size
        self.step_time = 33 # time per step (ms)
        self.cutoff = cutoff # maximum number of iterations

        # Get turtle names
        self.p1_name = "Player 1" # name of player 1 turtle
        if class1 != None:
            self.p1_name = eval(class1 + ".class_name()")
        self.p2_name = "Player 2" # name of player 2 turtle
        if class2 != None:
            self.p2_name = eval(class2 + ".class_name()")

        # Define window title
        title = ("Turtle Combat: " + self.p1_name + " vs. " + self.p2_name +
                 "(" + Arena.get_names()[layout] + ")")

        # Set up Tkinter window
        self.root = tk.Tk()
        self.root.title(title)

        # Set up arena canvas
        self.canvas = tk.Canvas(self.root, width=size[0], height=size[1],
                                bd=4, relief="sunken")
        self.canvas.grid(column=1, rowspan=2, padx=8, pady=8)

        # Set up name and health displays
        p1_label = tk.Label(self.root, text=self.p1_name,
                            font=("Helvetica", 16), fg="red")
        p1_label.grid(column=0, row=0, padx=8, sticky="S")
        p2_label = tk.Label(self.root, text=self.p2_name,
                            font=("Helvetica", 16), fg="blue")
        p2_label.grid(column=2, row=0, padx=8, sticky="S")

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

        # Get players' health
        ### May replace with a canvas health bar later
        self.p1_health = tk.StringVar(value="") # player 1 health string
        self.p1_health_display = tk.Label(self.root)
        if self.p1 != None:
            self.p1_health.set(str(self.p1.get_health()))
            self.p1_health_display = tk.Label(self.root,
                                              textvariable=self.p1_health,
                                              font=("Helvetica", 12))
        self.p1_health_display.grid(column=0, row=1, padx=8, sticky="N")
        self.p2_health = tk.StringVar(value="") # player 2 health string
        self.p2_health_display = tk.Label(self.root)
        if self.p2 != None:
            self.p2_health.set(str(self.p2.get_health()))
            self.p2_health_display = tk.Label(self.root,
                                              textvariable=self.p2_health,
                                              font=("Helvetica", 12))
        self.p2_health_display.grid(column=2, row=1, padx=8, sticky="N")

        self.root.update()

        # Begin game (after a delay, to allow the arena to initialize)
        self.iteration = 0 # number of steps that the game has gone through
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

    def play_game(self):
        """TurtleCombatGame.play_game() -> None
        Main gameplay loop of Turtle Combat.

        Implemented as a handler for a timer event.

        The main loop mostly consists of iteratively evaluating the step
        events of all in-game objects, creating and destroying objects as
        needed, and evaluating when the game has been won.
        """

        self.iteration += 1

        # Activate the step event of all game objects
        if self.p1 != None:
            self.p1._step()
        if self.p2 != None:
            self.p2._step()

        # Update player health displays
        hp1 = 1 # current player 1 health
        if self.p1 != None:
            hp1 = max(self.p1.get_health(), 0)
            self.p1_health.set(str(hp1))
        hp2 = 1 # current player 2 health
        if self.p2 != None:
            hp2 = max(self.p2.get_health(), 0)
            self.p2_health.set(str(hp2))

        # Decide whether to continue based on player health values
        if hp1 <= 0 and hp2 <= 0:
            # Tie
            self.canvas.create_text(self.size[0]/2 + 2, self.size[1]/2 + 2,
                                    text="Tie!",
                                    font=("Helvetica", 32, "bold"),
                                    fill="gray")
            self.canvas.create_text(self.size[0]/2, self.size[1]/2,
                                    text="Tie!",
                                    font=("Helvetica", 32, "bold"),
                                    fill="yellow")
        elif hp1 <= 0:
            # Player 2 win
            self.canvas.create_text(self.size[0]/2 + 2, self.size[1]/2 + 2,
                                    text=str(self.p2_name)+" wins!",
                                    font=("Helvetica", 32, "bold"),
                                    fill="gray")
            self.canvas.create_text(self.size[0]/2, self.size[1]/2,
                                    text=str(self.p2_name)+" wins!",
                                    font=("Helvetica", 32, "bold"),
                                    fill="blue")
        elif hp2 <= 0:
            # Player 1 win
            self.canvas.create_text(self.size[0]/2 + 2, self.size[1]/2 + 2,
                                    text=str(self.p1_name)+" wins!",
                                    font=("Helvetica", 32, "bold"),
                                    fill="gray")
            self.canvas.create_text(self.size[0]/2, self.size[1]/2,
                                    text=str(self.p1_name)+" wins!",
                                    font=("Helvetica", 32, "bold"),
                                    fill="red")
        elif self.cutoff > 0 and self.iteration >= self.cutoff:
            # Time limit cutoff
            self.canvas.create_text(self.size[0]/2 + 2, self.size[1]/2 + 2,
                                    text="Out of time!",
                                    font=("Helvetica", 32, "bold"),
                                    fill="gray")
            self.canvas.create_text(self.size[0]/2, self.size[1]/2,
                                    text="Out of time!",
                                    font=("Helvetica", 32, "bold"),
                                    fill="yellow")
        else:
            # Continue loop by resetting timer
            self.root.after(self.step_time, self.play_game)
