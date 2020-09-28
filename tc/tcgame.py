import turtle
import tc.tcplayer

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

    #-------------------------------------------------------------------------

    def __init__(self, size=(200, 200), layout=0, class1=None, class2=None):
        """TurtleCombatGame([size], [layout], [p1], [p2]) -> TurtleCombatGame
        Constructor for the Turtle Combat game.

        Sets up window, game variables, step timer, and all in-game objects,
        and then begins the game.

        Accepts the following optional keyword arguments:
            size (tuple (int, int)) [(200, 200)] -- arena width/height (px)
            layout (int) [0] -- arena obstacle layout ID (meanings of IDs
                defined in Arena class)
            class1 (CombatTurtle) [None] -- class of first player object
            class2 (CombatTurtle) [None] -- class of second player object
        """

        ### Also add options for how to set up the arena.

        # Initialize game constants
        self.step_time = 50 # time per step (ms)

        # Set up turtle window
        self.wn = turtle.Screen()
        self.wn.title("Turtle Combat") ### change to state player names

        # Initialize arena
        ###
        self.blocks = [] # list of block objects

        # Initialize players
        self.p1 = None # first player
        self.p2 = None # second player
        if (class1 != None):
            self.p1 = class1()
        if (class2 != None):
            self.p2 = class2()

        # Initialize a missile list
        self.missiles = [] # list of currently-active missile objects

        ### Get arguments to turtle objects

        # Begin game
        self.play_game()
        self.wn.mainloop()

    #-------------------------------------------------------------------------

    def __del__(self):
        """~TurtleCombatGame() -> None
        Turtle Combat game destructor.

        Deletes game objects and closes window.
        """

        # Delete players
        if (self.p1 != None):
            del self.p1
        if (self.p2 != None):
            del self.p2

        # Delete missiles
        del self.missiles[:]

        # Delete blocks
        del self.blocks[:]

        turtle.bye()

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
        if (self.p1 != None):
            self.p1.step()
        if (self.p1 != None):
            self.p1.step()
        for m in self.missiles:
            m.step()

        ### Apply game rules, break out if game hasn't ended yet.

        # Reset timer for next step
        self.wn.ontimer(self.play_game, self.step_time)
