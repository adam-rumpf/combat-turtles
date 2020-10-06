"""Defines the block class."""

import tkinter as tk

class Block:
    """Block class.

    Defines rectangular obstacles in the arena. Turtles cannot pass through
    blocks, and missiles explode on contact with blocks.
    """

    #=========================================================================

    def __init__(self, game, left, right, bottom, top, col="black"):
        """_Block(left, right, bottom, top) -> _Block
        Block constructor.

        Requires the following positional arguments:
            game (tcgame.TurtleCombatGame) -- game driver object
            left (int) -- leftmost x-coordinate (px)
            right (int) -- rightmost x-coordinate (px)
            bottom (int) -- lowermost y-coordinate (px)
            top (int) -- uppermost y-coordinate (px)

        Accepts the following optional keyword arguments:
            col (str or color tuple) ["black"] -- color of block
        """

        # Assign given attributes
        self.game = game
        self.canvas = game.get_canvas() # canvas to draw self on
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
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
