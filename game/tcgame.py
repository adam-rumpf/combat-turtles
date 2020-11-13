"""Defines the main game driver class."""

import tkinter as tk
import game.tcturtle
import ai
from .obj.arena import Arena
from .obj.missile import Missile

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
        self._size = size # arena size
        self._step_time = 33 # time per step (ms)
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
        self._canvas = tk.Canvas(self.root, width=size[0], height=size[1],
                                 bg="white", bd=4, relief="sunken")
        self._canvas.grid(column=1, rowspan=2, padx=8, pady=8)

        # Set up name and health displays
        p1_label = tk.Label(self.root, text=self.p1_name,
                            font=("Helvetica", 16), fg="red")
        p1_label.grid(column=0, row=0, padx=8, sticky="S")
        p2_label = tk.Label(self.root, text=self.p2_name,
                            font=("Helvetica", 16), fg="blue")
        p2_label.grid(column=2, row=0, padx=8, sticky="S")

        # Initialize arena
        self._arena = Arena(self, size=size, layout=layout)

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
        self.p1_health = tk.StringVar(value="") # player 1 health string
        self.p1_health_display = tk.Label(self.root)
        if self.p1 != None:
            self.p1_health.set(str(self.p1.health))
            self.p1_health_display = tk.Label(self.root,
                                              textvariable=self.p1_health,
                                              font=("Helvetica", 12))
        self.p1_health_display.grid(column=0, row=1, padx=8, sticky="N")
        self.p2_health = tk.StringVar(value="") # player 2 health string
        self.p2_health_display = tk.Label(self.root)
        if self.p2 != None:
            self.p2_health.set(str(self.p2.health))
            self.p2_health_display = tk.Label(self.root,
                                              textvariable=self.p2_health,
                                              font=("Helvetica", 12))
        self.p2_health_display.grid(column=2, row=1, padx=8, sticky="N")
        
        # Set up listeners for keyboard events (for KeyboardTurtle AI)
        if class1 == "ai.keyboard.CombatTurtle":
            self.root.bind("<Up>", lambda e : self.p1._keyboard_move(1))
            self.root.bind("w", lambda e : self.p1._keyboard_move(1))
            self.root.bind("<Down>", lambda e : self.p1._keyboard_move(-1))
            self.root.bind("s", lambda e : self.p1._keyboard_move(-1))
            self.root.bind("<Left>", lambda e : self.p1._keyboard_turn(1))
            self.root.bind("a", lambda e : self.p1._keyboard_turn(1))
            self.root.bind("<Right>", lambda e : self.p1._keyboard_turn(-1))
            self.root.bind("d", lambda e : self.p1._keyboard_turn(-1))
            self.root.bind("<space>", lambda e : self.p1._keyboard_shoot())
        if class2 == "ai.keyboard.CombatTurtle":
            self.root.bind("<Up>", lambda e : self.p2._keyboard_move(1))
            self.root.bind("w", lambda e : self.p2._keyboard_move(1))
            self.root.bind("<Down>", lambda e : self.p2._keyboard_move(-1))
            self.root.bind("s", lambda e : self.p2._keyboard_move(-1))
            self.root.bind("<Left>", lambda e : self.p2._keyboard_turn(1))
            self.root.bind("a", lambda e : self.p2._keyboard_turn(1))
            self.root.bind("<Right>", lambda e : self.p2._keyboard_turn(-1))
            self.root.bind("d", lambda e : self.p2._keyboard_turn(-1))
            self.root.bind("<space>", lambda e : self.p2._keyboard_shoot())

        self.root.update()
        
        # Run AI setup code
        if self.p1 != None:
            self.p1.setup()
        if self.p2 != None:
            self.p2.setup()

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
        del self._arena

    #-------------------------------------------------------------------------

    @property
    def step_time(self):
        """TurtleCombatGame.step_time -> int
        Returns the time between game steps (ms).
        """

        return self._step_time

    @step_time.setter
    def step_time(self, value):
        """Do-nothing step time setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def canvas(self):
        """TurtleCombatGame.canvas -> tkinter.Canvas
        Returns the Canvas object representing the game arena.
        """

        return self._canvas

    @canvas.setter
    def canvas(self, value):
        """Do-nothing canvas setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def arena(self):
        """TurtleCombatGame.arena -> tc.game.Arena
        Returns the game's Arena object.
        """

        return self._arena

    @arena.setter
    def arena(self, value):
        """Do-nothing arena setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def blocks(self):
        """TurtleCombatGame.blocks -> list
        Returns a list of all Block objects in the arena.
        """

        return self._arena.get_blocks()

    @blocks.setter
    def blocks(self, value):
        """Do-nothing block setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def size(self):
        """TurtleCombatGame.size -> tuple
        Returns the dimensions of the arena, as a tuple of integers.
        """

        return self._size

    @size.setter
    def size(self, value):
        """Do-nothing size setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    def intersections(self, coords):
        """TurtleCombatGame.intersections(coords) -> list
        Returns a list of block objects that intersect a given coordinate.

        Requires the following positional arguments:
            coords (tuple (int, int)) -- coordinate to test

        If the coordinate intersects no blocks, an empty list will be
        returned.
        """

        return self._arena.intersections(coords)
    
    #-------------------------------------------------------------------------

    def blocked(self, coords):
        """TurtleCombatGame.blocked(coords) -> bool
        Returns whether a given coordinate intersects any block objects.

        Requires the following positional arguments:
            coords (tuple (int, int)) -- coordinate to test

        Returns True if the coordinate intersects some block object and False
        otherwise.
        """

        return self._arena.blocked(coords)

    #-------------------------------------------------------------------------

    def _message_position(self):
        """TurtleCombatGame._message_position() -> tuple
        Determines the coordinates of messages to display on the arena canvas.

        When the game ends, a message is displayed somewhere in the arena to
        announce the result. In order to avoid covering up the turtles, we
        choose one of five positions: the center or one of the corners.

        If the center is free of turtles, the message is displayed there.
        Otherwise we choose the corner for which the sum of distances to each
        turtle is the greatest.
        """

        # Get turtle coordinates and center coordinates
        (x1, y1) = self.p1.position
        (x2, y2) = self.p2.position
        (xc, yc) = (self.size[0]/2, self.size[1]/2)

        # Define safety margin for text box size
        (xr, yr) = (300, 80)

        # If the center is free, display there
        if ((x1 < xc-xr or x1 > xc+xr) and (x2 < xc-xr or x2 > xc+xr)
            and (y1 < yc-yr or y1 > yc+yr) and (y2 < yc-yr or y2 > yc+yr)):
            return (xc, yc)

        # Otherwise find the corner furthest from both turtles
        corners = [(xr, yr), (self.size[0]-xr, yr), (xr, self.size[1]-yr),
                   (self.size[0]-xr, self.size[1]-yr)] # corner coordinates
        dist = [self.p1.distance(corners[i]) + self.p2.distance(corners[i])
                for i in range(len(corners))] # distances to all corners
        mi = dist.index(max(dist)) # index of maximum distance
        return corners[mi]

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
        
        # Activate the step event of all missiles
        if self.p1 != None:
            for m in self.p1._missiles:
                m._step()
        if self.p2 != None:
            for m in self.p2._missiles:
                m._step()

        # Activate the step event of all turtles
        if self.p1 != None:
            self.p1._step()
        if self.p2 != None:
            self.p2._step()

        # Update other attributes
        if self.p1 != None:
            self.p1._get_other_attributes()
        if self.p2 != None:
            self.p2._get_other_attributes()

        # Update player health displays
        hp1 = 1 # current player 1 health
        if self.p1 != None:
            hp1 = max(self.p1.health, 0)
            self.p1_health.set(str(hp1))
        hp2 = 1 # current player 2 health
        if self.p2 != None:
            hp2 = max(self.p2.health, 0)
            self.p2_health.set(str(hp2))

        # Decide whether to continue based on player health values
        if hp1 <= 0 and hp2 <= 0:
            # Tie
            pos = self._message_position()
            self._canvas.create_text(pos[0] + 2, pos[1] + 2,
                                     text="Tie!",
                                     font=("Helvetica", 32, "bold"),
                                     fill="gray")
            self._canvas.create_text(pos[0], pos[1],
                                     text="Tie!",
                                     font=("Helvetica", 32, "bold"),
                                     fill="yellow")
        elif hp1 <= 0:
            # Player 2 win
            pos = self._message_position()
            self._canvas.create_text(pos[0] + 2, pos[1] + 2,
                                     text=str(self.p2_name)+" wins!",
                                     font=("Helvetica", 32, "bold"),
                                     fill="gray")
            self._canvas.create_text(pos[0], pos[1],
                                     text=str(self.p2_name)+" wins!",
                                     font=("Helvetica", 32, "bold"),
                                     fill="blue")
        elif hp2 <= 0:
            # Player 1 win
            pos = self._message_position()
            self._canvas.create_text(pos[0] + 2, pos[1] + 2,
                                     text=str(self.p1_name)+" wins!",
                                     font=("Helvetica", 32, "bold"),
                                     fill="gray")
            self._canvas.create_text(pos[0], pos[1],
                                     text=str(self.p1_name)+" wins!",
                                     font=("Helvetica", 32, "bold"),
                                     fill="red")
        elif self.cutoff > 0 and self.iteration >= self.cutoff:
            # Time limit cutoff
            if hp1 < hp2:
                # Player 1 win
                pos = self._message_position()
                self._canvas.create_text(pos[0] + 2, pos[1] + 2,
                                         text=("Out of time!\n"+
                                               str(self.p1_name)+" wins!"),
                                         font=("Helvetica", 32, "bold"),
                                         fill="gray")
                self._canvas.create_text(pos[0], pos[1],
                                         text=("Out of time!\n"+
                                               str(self.p1_name)+" wins!"),
                                         font=("Helvetica", 32, "bold"),
                                         fill="red")
            elif hp2 < hp1:
                # Player 2 win
                pos = self._message_position()
                self._canvas.create_text(pos[0] + 2, pos[1] + 2,
                                         text=("Out of time!\n"+
                                               str(self.p2_name)+" wins!"),
                                         font=("Helvetica", 32, "bold"),
                                         fill="gray")
                self._canvas.create_text(pos[0], pos[1],
                                         text=("Out of time!\n"+
                                               str(self.p2_name)+" wins!"),
                                         font=("Helvetica", 32, "bold"),
                                         fill="blue")
            else:
                # Tie
                pos = self._message_position()
                self._canvas.create_text(pos[0] + 2, pos[1] + 2,
                                         text="Out of time!",
                                         font=("Helvetica", 32, "bold"),
                                         fill="gray")
                self._canvas.create_text(pos[0], pos[1],
                                         text="Out of time!",
                                         font=("Helvetica", 32, "bold"),
                                         fill="yellow")
        else:
            # Continue loop by resetting timer
            self.root.after(self.step_time, self.play_game)
