"""Defines the block class."""

import tkinter as tk

class Block:
    """Block class.

    Defines rectangular obstacles in the arena. Turtles cannot pass through
    blocks, and missiles explode on contact with blocks.

    The following local read-only attributes can be used to access the
    coordinates of the Block:
        left, right, bottom, top -- returns the left/right/bottom/top
            coordinates of the block

    The following public methods can be used to test for collisions with the
    Block:
        contains(coords[, closed]) -- returns whether a given coordinate lies
            inside this Block's boundaries (either open or closed)
    """

    #=========================================================================

    def __init__(self, game, left, right, bottom, top, col="black"):
        """_Block(left, right, bottom, top) -> _Block
        Block constructor.

        Requires the following positional arguments:
            game (tcgame.TurtleCombatGame) -- game driver object
            left (int) -- smallest x-coordinate (px)
            right (int) -- largest x-coordinate (px)
            bottom (int) -- smallest y-coordinate (px)
            top (int) -- largest y-coordinate (px)

        Accepts the following optional keyword arguments:
            col (str or color tuple) ["black"] -- color of block

        Because screen coordinates begin at the top, "bottom" here actually
        corresponds to the top of the screen, and "top" corresponds to the
        bottom.

        The constructor ensures that left <= right and bottom <= top.
        """

        # Assign given attributes (ensuring order of coordinates)
        self.game = game
        self.canvas = game.canvas # canvas to draw self on
        self._left = min(left, right)
        self._right = max(left, right)
        self._bottom = min(bottom, top)
        self._top = max(bottom, top)
        self.color = col

        # Draw the block
        self._draw()

    #-------------------------------------------------------------------------

    def __del__(self):
        """~Block() -> None
        Block destructor deletes drawing on canvas.
        """

        # Delete sprite (if it has been defined)
        try:
            self.canvas.delete(self.sprite)
        except AttributeError:
            pass
        except tk.TclError:
            pass

    #-------------------------------------------------------------------------

    def contains(self, coords, closed=True):
        """Block.contains(coords[, closed]) -> bool
        Determines whether the block contains a given coordinate.

        Requires the following positional arguments:
            coords (tuple (int, int)) -- coordinate to test

        Accepts the following optional keyword arguments:
            closed (bool [True]) -- whether to include the boundaries

        Returns True if coords is within the block, and False otherwise.
        """

        # Determine output depending on whether boundaries are included
        if closed == True:
            # Closed boundaries
            if (coords[0] >= self.left and coords[0] <= self.right and
                coords[1] >= self.bottom and coords[1] <= self.top):
                return True
        else:
            # Open boundaries
            if (coords[0] > self.left and coords[0] < self.right and
                coords[1] > self.bottom and coords[1] < self.top):
                return True

        # If nothing has been returned yet, the tests failed
        return False

    #-------------------------------------------------------------------------

    def _draw(self):
        """Block._draw() -> None
        Draws a block on the game canvas.
        """

        # Draw a rectangle on the game's canvas
        self.sprite = self.canvas.create_rectangle(self.left, self.bottom,
                          self.right, self.top, fill=self.color)

    #-------------------------------------------------------------------------

    @property
    def left(self):
        """Block.left -> None
        Returns the left coordinate of the block.
        """

        return self._left

    @left.setter
    def left(self, value):
        """Do-nothing boundary setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def right(self):
        """Block.right -> None
        Returns the right coordinate of the block.
        """

        return self._right

    @right.setter
    def right(self, value):
        """Do-nothing boundary setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def bottom(self):
        """Block.bottom -> None
        Returns the bottom coordinate of the block.
        """

        return self._bottom

    @bottom.setter
    def bottom(self, value):
        """Do-nothing boundary setter to prevent overwriting."""

        pass

    #-------------------------------------------------------------------------

    @property
    def top(self):
        """Block.top -> None
        Returns the top coordinate of the block.
        """

        return self._top

    @top.setter
    def top(self, value):
        """Do-nothing boundary setter to prevent overwriting."""

        pass
